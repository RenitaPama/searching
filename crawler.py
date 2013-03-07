import sys
import Queue
import indexer
import urlparse
from pymongo import MongoClient,errors,DESCENDING,ASCENDING
import pprint
from threading import Thread
from robotparser import RobotFileParser # used to check robot files
from urlparse import urlparse,urljoin

DEFAULT_URLS = ['http://www.google.com','http://www.amazon.com','http://www.nytimes.com','http://www.racialicious.com','http://www.groupon.com','http://www.yelp.com']
DEFAULT_DEPTH = 2
# SIMPLE_INDEX = MongoClient().index_db.simple_index # mongo collection


class BFS_Crawler:
	"""Create an instance of Crawler with a root and its tree"""
	def __init__(self,start = ['http://www.smittenkitchen.com'],depth = DEFAULT_DEPTH):#add index = SIMPLE_INDEX as a param
		"""Initialize the crawler with the starting urls"""
		self.rp = RobotFileParser()
		self.root = start
		self.depth = depth
		try:
			self.simple_index = MongoClient().index_db.simple_index # mongo collection
		except errors.ConnectionFailure:
			print "Your attempt to connect failed"

	def make_mongo_index(self):
		self.simple_index.create_index(('pages.url',ASCENDING),('_id',DESCENDING)) # creates an index on _id and pages.url (also allows queries for 'urls')

	def process_page(self,url): 
		"""Retrieve all html data from a webpage,index it and return a list of links"""
		links = []
		try:
			page_object = indexer.Page(url)
		except indexer.IndexerError:
			print indexer.IndexerError
		else:
			return page_object

	def robot_check(self,url):
		"""Return true if the url is okay to visit"""
		parsed_url = urlparse(url)
		root = parsed_url[0] + '://' + page_url[1]
		robots_url = urljoin(root,'/robots.txt')
		self.rp.set_url(robot_url)
		self.rp.read()
		return self.rp.can_fetch("*",url)

	def update_index(self,page):
		new_entries = page.make_rlink_index() # all new entries to be added to the db

		for entry in new_entries:
			term,rlink = entry
			url = page.url

			self.simple_index.update({'_id':term,'url':url},{'$push':{'pages':{'url':url,'relevance':rlink,'crawl_time':page.crawl_time}}},upsert=True) # upsert will update or insert

		print "There are %s entries in the database"%str(self.simple_index.count())
		return True # returns only if no error is thrown

	def BFS_crawl(self):
		"""Return a sorted list of all links self.depth away from the original"""
		nodes = Queue.Queue()
		self.ever_seen = set() #keeps track of which links have been crawled on this go (note: will re-crawl links already crawled in a new crawl)
		
		for link in self.root:
			nodes.put((link,0))#enqueues (start,layer)
			self.ever_seen.add(link)
		self.make_mongo_index()#creates new index so that it's available for all subsequent queries (on '_id','url')

		for _ in xrange(5):
			t = Thread(target=self.crawler_process,args=(nodes,))
			t.daemon = True
			t.start()
		print "Waiting on the queue to be flushed"
		nodes.join() #blocking
		print "You've done it"
						
	def crawler_process(self,queue):
		print "New process started"

		current_depth = 0
		while True:
			current_url, current_depth = queue.get()

			print "Crawling: {0}\nCurrent Depth: {1}".format(current_url,current_depth)
			
			page = self.process_page(current_url) # # index the page, (maybe in try-catch)
			if page:
				self.update_index(page)
				for link in filter(self.robot_check,page.links):
					if link not in self.ever_seen and current_depth <= self.depth:
						queue.put((link,current_depth+1)) # put it in the queue to be crawled
						self.ever_seen.add(link)
			else:
				self.ever_seen.remove(current_url)
			queue.task_done()
		print "Process finished"


if __name__ == '__main__':
	c = BFS_Crawler()
	c.BFS_crawl()
	



