import requests, re, os, sys, subprocess, short_url
from bs4 import BeautifulSoup
from tabulate import tabulate
from urllib.request import urlopen

def open_webpage(url):
	if sys.platform == "win32":
		os.startfile(url)
	else:
		opener ="open" if sys.platform == "darwin" else "xdg-open"
		subprocess.call([opener, url])

def get_response_from_server():
	response = urlopen('http://www.espncricinfo.com/ci/engine/match/index.html?view=live')
	if(response == None):
		print ("No Internet Connection !!")
	else:
		return extract_results(response)

def get_html_response(response):
	page_source = response.read()
	soup = BeautifulSoup(page_source, "html.parser")
	return soup

def extract_results(response):
	soup = get_html_response(response)
	matches = soup.find('section',{'id':'live-match-data'})

	match_scorecard = []
	first_innings = []
	second_innings = []
	match_status = []

	for match in matches.find_all('section',{'class':'default-match-block'}):
		match_info = match.find('a')
		if match_info.parent.name == 'span':
			scorecard = str(match_info['href'])		
			match_scorecard.append(scorecard)

		first_score = match.find('div',{'class':'innings-info-1'}).get_text()
		first_innings.append(first_score)
		second_score = match.find('div',{'class':'innings-info-2'}).get_text()
		second_innings.append(second_score)

		status = match.find('div',{'class':'match-status'})
		status_info = status.find('span').get_text()
		match_status.append(status_info[0:75])

	return first_innings, second_innings, match_status, match_scorecard

def tabulate_results(first_innings,second_innings,match_status,match_scorecard):
	t = []
	for i in range(len(first_innings)):
		element = []
		element.append(i)
		element.append(first_innings[i])
		element.append(second_innings[i])
		element.append(match_status[i])
		t.append(element)

	print (tabulate(t,headers=["Index","First Innings","Second Innings","Match Status"]))

def main():
	first_innings, second_innings, match_status, match_scorecard = get_response_from_server()
	
	tabulate_results(first_innings,second_innings,match_status,match_scorecard)

	length = len(first_innings)
	input_index = int(input("Choose option: 0-"+str(length-1) + " to view scorecard OR press " + str(length) + " to exit : "))

	if(input_index == length):
		sys.exit(1)
	else:
		open_webpage(match_scorecard[input_index])

if __name__ == "__main__":
	main()
