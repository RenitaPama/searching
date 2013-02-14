import urllib2
import os
# import pdb

default_urls = ['http://www.google.com','http://www.amazon.com','http://www.nytimes.com','http://www.racialicious.com','http://www.groupon.com','http://www.yelp.com']
current_directory = os.path.abspath(os.curdir)

def html_grabber(urls = None,directory = None):
	"""Grab all HTML from a page, write it to a new file in the specified directory (defaults to current directory)"""
	if urls is None:
		urls = default_urls
	if directory is None:
		directory = current_directory

	for url in urls:
		site_name = url.split('www.')[1].rstrip('.com')
		file_name = '{}/{}.html'.format(directory,site_name)

		new_file = open(file_name,'a') 
		filish_object = urllib2.urlopen(url)

		data = filish_object.read()
		new_file.write(data)
		print "Site name: {} \n File: {}".format(site_name,file_name)
		new_file.close()

if __name__ == '__main__':
	html_grabber()


# from HTMLParser import HTMLParser

# # create a subclass and override the handler methods
# class MyHTMLParser(HTMLParser):
#     def handle_starttag(self, tag, attrs):
#         print "Encountered a start tag:", tag
#     def handle_endtag(self, tag):
#         print "Encountered an end tag :", tag
#     def handle_data(self, data):
#         print "Encountered some data  :", data

# # instantiate the parser and fed it some HTML
# parser = MyHTMLParser()
# parser.feed('<html><head><title>Test</title></head>'
#             '<body><h1>Parse me!</h1></body></html>')