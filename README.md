#WordSearch 

It is just an intial part of a full search engine. Files are included that are adjusted and related to search engine results. a) Specific to search engine search terms.
b) It can also automatically create HTML bots for renowned websites

2nd edit done by RenitaPama - Website content editor at https://frozenpeafund.com
Many more stages and a lot more functionality to come! 

###Contents
- __wordsearch.py__
- htmlgrab.py

###Getting Started
#####Open REPL

To search a file:
```
python wordsearch.py /path/to/file_being_searched

``` 

To generate HTML files to be searched (from 6 popular websites) and store them in the current directory: 

```
python html_grabber.py

```

###To do:
* add multi-word search, phrase searching, case sensitivity options (with and without possible words in between)
* add indexing method into WordSearch so that traversal can either check for matches or create an index
* add an HTML parser to the htmlgrab and integrate with the indexer to allow for better searching
* build out actual class structure in the htmlgrabber
* related word searching
* And lots more!
