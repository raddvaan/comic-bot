#Comic Bot
import requests
from bs4 import BeautifulSoup
import re
import os
#import pdb
marvelSort = "E:\Comics\Marvel"
dcSort = "E:\Comics\DC"
ultSort = "E:\Comics\\Ultimate Marvel"
newmarvel = "E:\Comics New\Marvel"
newdc = "E:\Comics New\DC"
newult = "E:\Comics New\\Ultimate Marvel"
testdir = "E:\TEST"
newtest = "E:\TESTNEW"
comtitles = []

comdic = {}
def comic_finder(comicTitle, comicYear): #searches known databeses
	if comicYear == "0000":
		year = year_prompt(comicTitle)
	else:
		year = comicYear
	cdburl = "http://www.comicbookdb.com/search.php?form_search=" + str(comicTitle) + " " + year + "&form_searchtype=Title"
	cdburl2 = "http://www.comicbookdb.com/title.php?ID=348"
	source_code = requests.get(cdburl)
	plain_text = source_code.text
	soup = BeautifulSoup(plain_text, "html.parser")
	for link in soup.find_all('a',href=re.compile('title.php?')):
		print(link.string)

#comic_finder("The Amazing Spider-Man")

def name_scrub(dname,filetype): #function scrubs dirty name to a standard
	#pdb.set_trace()
	print(dname)
	dname = dname.replace("#","")
	namenotype = dname[0:len(dname) - len(filetype)]+ " "
	#print(namenotype)
	issuearr = issue_cracker(namenotype)
	#0-pure issue, 1-leading zero no dot, 2-nodot pure issue
	issue = issuearr[0]
	
	lzissue = issuearr[1]
	#print(issuearr)
		
	#print(issue)

	issyr = year_cracker(dname)
	#print(issyr)
			#Attempts to find a year, if fails, sets year to 0000, perhaps set a reasonable range limit (eg 1900 to 2999, to filter yaers in names)
	
	#comic_finder(title,issyr)
	#print("TITLE : " + title)
	#issin = re.search(" " + issue + "[ ,(]", dname).span()[0]
	#title = dname[0:issin]
	
		#regex to search for exact match of issue 
	volume,voli1,voli2 = volume_finder(dname)
	
	if volume == "none":
		title = title_cracker(dname,issue)
		cleanname = str(title)+ " - "+ str(lzissue) + filetype 
	else:
		title = title_cracker(dname,issue)
		title = title[0:voli1 - 1]
		cleanname = str(title  +" - " + str(volume) + " " + str(lzissue) + filetype)	
	
		#combines elements of scrubbed name
	print(cleanname + "\n")
	print(subtitle_scraper(dname,issue))

	subsresults,substatus = subtitle_scraper(dname,issue)
	if substatus == "false":
		basetitle = title
	else:
		basetitle = subsresults

	print(basetitle)
	#comic_finder(title)
		#calls to search the ComicDB
	return cleanname, basetitle


def scan_folder(location): #Temp Functionto scan folder
	
	for root, dirs, files in os.walk(location):
		sub = root
		print(sub)
		for file in os.listdir(sub):
			try:
				
				#pdb.set_trace()
				filestatus,filetype = type_check(file)
				#print(type_check(filetype))
				print(filetype)
				if filestatus == "clear":
					orifile = file
				#s	print("namescrub =" + name_scrub(file,filetype))
					scrubname = name_scrub(file,filetype)
					print('sname')
					print(scrubname)
					if scrubname == "false":
						newname,namescrap = name_scrub(file,filetype)
						

					else:
						print("else")
						foldertitle,newname = name_scrub(file,filetype)
					
					
					#print("NEW NAME + " + str(newname))
					
					if location == marvelSort:
						newloc = newmarvel
					elif location == dcSort:
						newloc = newdc
					elif location == ultSort:
						newloc = newult
					
					#comtitles.append(title)

					move_file(file,newname,foldertitle,sub,newloc)
			except:
				print("EXCEPT")
				if location == marvelSort:
					newloc = newmarvel
				elif location == dcSort:
					newloc = newdc
				elif location == ultSort:
					newloc = newult
				elif location == testdir:
					newloc = newtest
				#print(newloc)
				pass
		#name_scrub(file,filetype)
	return



def move_file(oldfilename,newfilename,title,oldlocation,newlocation):
	print(oldfilename,newfilename,title,oldlocation,newlocation)
	return


def issue_cracker(dname):	
	
	try:
		
		issue = str(re.search('[ ,#][0-9]{1,3}(.\d?)[\(, ]'  , dname).group(0).replace(" ", "").replace("(","")).replace("#","")
		#print(issue)
		lzissue = issue
		print(lzissue)
	except:
		#try:
		#	issue = re.search(' [0-9]{1,2}.\d?[ ,(,.]?'  , dname).group(0).replace(" ", "").replace("(","")
			
			
			#lzissue = "0" + issue
		#except:

		issue = "(One Shot)"	
	if len(issue) == 2:
		lzissue = "0" + issue
	else:

		lzissue = issue
	#print(issue + " " + lzissue)
	return issue, lzissue


def title_cracker(dname, issue):
	if issue == "(One Shot)":
		try:
			titcrapin = re.search(' \(\D{1,50}\)',dname).span()[0]
			title = dname[0:titcrapin]
		except:
			title = dname
	else:
		title = dname[0:(re.search(" " + issue + "[ ,(]?", dname).span()[0])]
		#print(title)
	
	#print(title)
	return title

def year_cracker(dname):
	try:

		issyr = re.search('\(\d\d\d\d\)', dname).group(0).replace("(","").replace(")","")
		
	except:
		issyr = "0000"

	return issyr

def type_check(file):
	filetype = re.search("\.[a-zA-Z]{2,4}",file)
	#print(filetype)
	notcomics = [".txt",".db",".rar",".doc",".docx",".jpg",".png"]
	if filetype.group(0) in notcomics:
		status = "skip"
		
	else:
		status = "clear"
	return status, filetype.group(0)

def year_prompt(comtitle):
	year = "1963"
	return year


def volume_finder(dname):
	
	try:
		volobj = re.search("v(ol)?\s?\d{1,2}",dname,re.IGNORECASE)
		volume = volobj.group(0)
		voli1 = volobj.span()[0]
		voli2 = volobj.span()[1]
		#print(volume)
		volumeno = re.search("\d{1,2}",volume).group(0)
		#print(volumeno)
		if len(volumeno) == 2:
			volume = "V" + volumeno
		else:
			volume = "V0" + volumeno
		return volume, voli1, voli2
	except:
		voli1,voli2,volume = "none","none","none"

		#print(volume)
		return volume, voli1, voli2

def subtitle_scraper(dname, issue):
	try:
		dashfind = re.search(" - ", dname).span()[0]
		issuein = re.search(issue, dname).span()[0]
		subtitle = dname[dashfind:issuein]
		title = dname[0:dashfind]
	except:
		title = dname
		subtitle = "false"
	#print("TITLE " + title)
	#print("SUB " + subtitle)
	return title, subtitle




	 



#RUN#
title_cracker("Before Watchmen Dollar Bill.cbr","(One Shot)")
#volume_finder("x-men Vol2 ")
#type_check("The Unbeatable Squirrel Girl 006 (2016) (4 covers) (digital) (Minutemen-Midas).cbr")
#type_check("marvcel.txt")	
