from __future__ import unicode_literals
import urllib
import urllib.parse
import urllib.request

# pip3 install BeautifulSoup4
from bs4 import BeautifulSoup

# pip3 install youtube_dl
import youtube_dl

def generate_yt_url(user_input: 'str: search in YT search bar') -> ['YT URLS']:
	'''
	generates a list of all of the urls in the first page of the YT search
	'''

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

def download_mp3(url: str):
	'''
	given a youtube URL, this
	function downloads the video
	as an mp3
	'''

	ydl_opts = {
	    'format': 'bestaudio/best',
	    'postprocessors': [{
	        'key': 'FFmpegExtractAudio',
	        'preferredcodec': 'mp3',
	        'preferredquality': '192',
	    }],
	}

	downloader = youtube_dl.YoutubeDL(ydl_opts)

	# this makes sure it is a URL and not a playlist
	url = url.split('&')[0]

	# takes in a list of urls, but we're just doing 1 url
	downloader.download([url])
