'''
youtube.py
module for youtube related features
'''

#### IMPORTS ####

# First Party (python3 native)

from __future__ import unicode_literals
import urllib
import urllib.parse
import urllib.request

# Third Party:

# pip3 install BeautifulSoup4
# pip3 install bs4
from bs4 import BeautifulSoup

# pip3 install youtube_dl
import youtube_dl

#### CONSTANTS ####

# youtube options when downloading a video
opts = dict(
    format="bestaudio/best",
    extractaudio=True,
    audioformat="mp3",
    noplaylist=True,
    default_search="auto",
    quiet=True,
    nocheckcertificate=True)

yt_url = 'https://www.youtube.com'

#### FUNCTIONS ####

def _check_url(url) -> bool:
	'''
	checks if the url contains a youtube video
	and returns boolean based on that
	
	Covers cases in which URL leads to a youtube 
	channel or playlist

	will edit this later
	'''

	return True

def front_page_info(user_input: 'str: search in YT search bar') -> {'Title: URL'}:
	'''
	generates a dictionary containing data based on the user input.
	dictionary consists of video title as key, video URL as value.
	'''

	# turn user input into a query
	search_query = urllib.parse.quote(user_input)

	# add query to youtube URL
	url = "https://www.youtube.com/results?search_query=" + search_query

	# get webpage
	response = urllib.request.urlopen(url)

	# read the webpage
	html = response.read()

	# parse the webpage, get dictionary of video info where key is video
	# title is value is URL

	videos = dict()
	parsed_html = BeautifulSoup(html, "html.parser")
	for video in parsed_html.findAll(attrs={'class':'yt-uix-tile-link'}):
		title = video['title']
		url = 'https://www.youtube.com' + video['href']

		# make sure url is *just* a video, not a 
		# playlist or channel
		url = url.split('&')[0]
		if _check_url(url):
			videos[title] = url
	    
	return videos

def is_youtube_url(url) -> bool:
	'''
	returns True if the URL given is a 
	youtube URL
	'''

	return True if (yt_url in url and _check_url(url) == True) else False

def download_mp3(url: str) -> None:
	'''
	given a youtube URL,
	this function downloads the video
	as an mp3 into the directory that 
	this file is in
	'''
	ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{'key': 'FFmpegExtractAudio',
    					'preferredcodec': 'mp3', 
    					'preferredquality': '192'}],
    'nocheckcertificate': True}

	downloader = youtube_dl.YoutubeDL(ydl_opts)

	# this makes sure it is a URL and not a playlist
	url = url.split('&')[0]

	# takes in a list of urls, but we're just doing 1 url
	downloader.download([url])