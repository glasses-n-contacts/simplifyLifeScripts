import subprocess
import sys
from bs4 import BeautifulSoup
import requests

aniChartUrl="https://www.livechart.me/"
great_studios = ["MAPPA","A-1 Pictures","Bones","Madhouse"]
good_studios = ["ufotable","Production I.G","Brains Base", "Shaft"]
ok_studios = ["Lerche"]

bad_tags = ["School", "Harem"]
sort_of_bad_tags = ["Slice of Life"]
good_tags = ["Psychological","Seinen","Horror","Mystery"]


def findSeasonRecs():
	season_anime = {}
	scores = {}
	print "Anime season (summer, spring, winter, or fall)"
	season = sys.stdin.readline().strip()
	print "year?"
	year = sys.stdin.readline().strip()
	url = aniChartUrl + season+"-"+year+"/tv"
	print(url)
	r = requests.get(url)
	data = r.text
	#print(data)
	soup = BeautifulSoup(data,  "html.parser")
	animez = soup.find_all("div", {"class": "anime-card"})
	for anime in animez:
		titlez = anime.find_all("h3",{"class":"main-title"})[0]
		title = titlez.text
		scores[title] = 0 #each show starts off with 0

		#check title
		if "death" in title:
			scores[title]+=2

		#check the tag
		tags = [tag.text for tag in anime.find_all("ol",{"class":"anime-tags"})[0].find_all("li")]
		for tag in tags:
			if tag in good_tags:
				scores[title] += 6
			elif tag in sort_of_bad_tags:
				scores[title] -= 1
			elif tag in bad_tags:
				scores[title] -= 6
		season_anime[title] = {"tags":tags}
		studios = anime.find_all("ul",{"class":"anime-studios"})

		#check the studios
		parsed_studios = []
		for studio in studios:
			if studio.find_all("a"):
				stud = studio.find_all("a")[0].text
				if stud in great_studios:
					scores[title] += 6
				elif stud in good_studios:
					scores[title] += 3
				elif stud in ok_studios:
					scores[title] += 1
				parsed_studios.append(stud)
			else:
				parsed_studios.append(studio.find_all("li")[0].text)
		season_anime[title]["studios"]=parsed_studios

		#check description
		descriptionz = anime.find_all
	print season_anime



if __name__ == "__main__":
    findSeasonRecs()
