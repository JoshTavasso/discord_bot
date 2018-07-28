import urllib
import urllib.parse
import urllib.request

# pip3 install BeautifulSoup4
from bs4 import BeautifulSoup


def generate_yt_url(user_input: 'str: search in YT search bar') -> ['YT URLS']:

	# turn user input into a query
	search_query = urllib.parse.quote(user_input)

	# add query to youtube URL
	url = "https://www.youtube.com/results?search_query=" + search_query

	# get webpage
	response = urllib.request.urlopen(url)

	# read the webpage
	html = response.read()

	# parse the webpage, get list of videos from front page of search
	videos = []
	parsed_html = BeautifulSoup(html, "html.parser")
	for video in parsed_html.findAll(attrs={'class':'yt-uix-tile-link'}):
	    videos.append(('https://www.youtube.com' + video['href']))
	    
	return videos