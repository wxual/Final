#!/usr/bin/python
#
#  The program was written by Raymond WONG.
#  The program is used for illustrating how to perform data crawling on one single webpage,
#  to save this webpage to the working directory of our computer, 
#  to obtain a list of all links found in "href" of the "a" HTML tags
#  and save the list in a file called "listOfLink.txt"
#
import scrapy

class OneWebpageSpider(scrapy.Spider):
	name = "OneWebpage"
	start_urls = [ "https://oceans11.lanl.gov/deepwaterimpact/yC31_300x300x300-FourScalars_resolution.html" ]
	
	# Constructor (which is called at the beginning)
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		print("This is called at the beginning.")
		
	# Closed (which is called at the end)
	def closed(self, reason):
		print("This is called at the end.")
			
	def parse(self, response):
		# We perform the following operations

		# Operation 1: Save the HTML file to the working directory of our computer
		crawlFilename = response.url.split("/")[-1]
		with open(crawlFilename, "wb") as f:
			f.write(response.body)
		self.log("Saved File {} ".format(crawlFilename))
		
		# Operation 2: Obtain a list of all links found in "href" of the "a" HTML tags
		#              and save the list in a file called "listOfLink.txt"
		# Step (a): Find a list of all links found in "href" of the "a" HTML tags
		listOfLink = response.xpath("//a[@href]/@href").extract()

		# Step (b): Save the list in a file called "listOfLink.txt"
		linkFilename = "yC31.txt"
		with open(linkFilename, "w") as f:
			for link in listOfLink:
				f.write(link)
				f.write("\n")			
			
		self.log("Saved File {} ".format(linkFilename))


