#!usr/bin/python
# This script parses the search result of several iMDB advanced search URLs
# and saves all the movie titles in each page.

from urllib2 import urlopen
from bs4 import BeautifulSoup
import codecs
import urllib2
import os
import glob

URLs = [
			"http://www.imdb.com/search/title?count=100&countries=us&num_votes=12000,&sort=user_rating,desc&title_type=feature&user_rating=8.0,",
			"http://www.imdb.com/search/title?at=0&count=100&countries=us&num_votes=12000,&sort=user_rating,desc&start=101&title_type=feature&user_rating=8.0,10",
			"http://www.imdb.com/search/title?at=0&count=100&countries=us&num_votes=12000,&sort=user_rating,desc&start=201&title_type=feature&user_rating=8.0,10"
		]

USStates = {
			   "Alabama" : "AL",
			   "Alaska" : "AK",
			   "Arizona" : "AZ",
			   "Arkansas" : "AR",
			   "California" : "CA",
			   "Colorado" : "CO",
			   "Connecticut" : "CT",
			   "Delaware" : "DE",
			   "Florida" : "FL",
			   "Georgia" : "GA",
			   "Hawaii" : "HI",
			   "Idaho" : "ID",
			   "Illinois" : "IL",
			   "Indiana" : "IN",
			   "Iowa" : "IA",
			   "Kansas" : "KS",
			   "Kentucky" : "KY",
			   "Louisiana" : "LA",
			   "Maine" : "ME",
			   "Maryland" : "MD",
			   "Massachusetts" : "MA",
			   "Michigan" : "MI",
			   "Minnesota" : "MN",
			   "Mississippi" : "MS",
			   "Missouri" : "MO",
			   "Montana" : "MT",
			   "Nebraska" : "NE",
			   "Nevada" : "NV",
			   "New Hampshire" : "NH",
			   "New Jersey" : "NJ",
			   "New Mexico" : "NM",
			   "New York" : "NY",
			   "North Carolina" : "NC",
			   "North Dakota" : "ND",
			   "Ohio" : "OH",
			   "Oklahoma" : "OK",
			   "Oregon" : "OR",
			   "Pennsylvania" : "PA",
			   "Rhode Island" : "RI",
			   "South Carolina" : "SC",
			   "South Dakota" : "SD",
			   "Tennessee" : "TN",
			   "Texas" : "TX",
			   "Utah" : "UT",
			   "Vermont" : "VT",
			   "Virginia" : "VA",
			   "Washington" : "WA",
			   "West Virginia" : "WV",
			   "Wisconsin" : "WI",
			   "Wyoming" : "WY"
			}

movies = []
links = []
dictionary = {}
years = []
ratings = []
budget = []
locations = []

class Parser:

	# Construct lists with title, rating, and year
	def get_movies (self, url):
		html = urlopen(url).read()
		soup = BeautifulSoup(html, "lxml")
		tableItems = soup.findAll("td", {"class":"title"})
		self.get_movie_rating(soup)
		for b in tableItems:
			movies.append(b.find("a").contents[0])
			movie_link = b.find("a")['href']
			links.append(movie_link)
			budget.append(self.get_movie_budget(movie_link))
			locations.append(self.get_movie_location(movie_link))

	def get_movie_budget (self, title_url):
		b_url = "http://www.imdb.com" + title_url + "business?ref_=tt_dt_bus"
		b_html = urlopen(b_url).read()
		b_soup = BeautifulSoup(b_html, "lxml")
		items = b_soup.find("div", {"id":"tn15content"})
		movie_budget = items.h5.nextSibling[2:-12]
		if ( len(movie_budget) >= 7):
			return movie_budget
		else:
			return "None"
		#budget.append(movie_budget)

	def get_movie_location (self, title_url):
		l_url = "http://www.imdb.com" + title_url + "locations?ref_=tt_dt_dt"
		l_html = urlopen(l_url).read()
		l_soup = BeautifulSoup(l_html, "lxml")
		try:
			full_loc = l_soup.find("div",{"class":"soda odd"}).a.contents[0][:-1].split(',')
		except AttributeError:
			return "None"
		if (full_loc[-1][1:] != "USA"):
			return "None"
		else:
			return full_loc[-2][1:]

	def get_movie_year (self, soup):
		mov_years = soup.findAll("span",{"class":"year_type"})
		for year in mov_years:
			years.append(year.contents[0].strip("(").strip(")"))

	def get_movie_rating (self, soup):
		mov_ratings = soup.findAll("span", {"class":"rating-rating"})
		for rating in mov_ratings:
			num_rating = rating.find("span",{"class":"value"}).contents[0]
			ratings.append(num_rating)

	def write_list_to_file (self, filename):
		with codecs.open("movies.txt", "wb", encoding="utf-8") as f:
			#f.write("\n".join(map(lambda x: x, movies)))
			u_movies = []
			u_budget = []
			u_locations = []
			for index in range(len(movies)):
				u_movies.append(movies[index].encode('utf-8'))
				u_budget.append(budget[index].encode('utf-8'))
				u_locations.append(locations[index].encode('utf-8'))
			for index in range(len(movies)):
				f.write(`u_movies[index]`+'\t\t\t'+`u_budget[index]`+'\t\t\t'+`u_locations[index]`+'\n')
		f.close()

	def get_search_link (self, state):
		q_state = urllib2.quote(state)
		search_url = "http://www.imdb.com/search/title?count=100&locations=%s&num_votes=12000,&sort=user_rating,desc&title_type=feature&user_rating=7.3," % q_state
		return search_url

	def get_results_no (self, state):
		search_url = self.get_search_link(state)
		html = urlopen(search_url).read()
		soup = BeautifulSoup(html, "lxml")
		rdiv = soup.find("div",{"class":"leftright"})
		try:
			num = int(rdiv.div.contents[0].replace('\n',' ').split(' ')[1])
			result = num
		except ValueError:
			try:
				num = rdiv.div.contents[0].replace('\n',' ').split(' ')[3]
				result = num
			except AttributeError:
				result = 0
		except AttributeError:
			result = 0

		self.get_thumbnails_by_state(soup, result, state)
		return result

	def get_thumbnails_by_state(self, soup_, result_, state_):
		# Limit img results to 5
		if (result_ > 5):
			result_ = 5
		try:
			img_links = soup_.findAll("td", {"class" : "image"})
			for it in range(result_):
				img_link = img_links[it].img["src"]
				# Get higher quality thumbnails
				img_link = img_link.replace("SX54_CR0,0,54,74", "SY317_CR4,0,214,317")
				img_file = open("./Visualization/data/"+USStates[state_]+str(it)+".png", "w")
				img_file.write(urllib2.urlopen(img_link).read())
				img_file.close()
		except AttributeError:
			return

	def write_results_no_to_file (self, filename):
		with codecs.open(filename, "wb", encoding="utf-8") as f:
			for state in USStates:
				f.write(`USStates[state]`+'\t'+`str(self.get_results_no(state))`+'\n')
		f.close()


def main():
	parser = Parser()
	parser.write_results_no_to_file("NoFilmsByAbbrv.txt")


if __name__ == '__main__':
	main()
