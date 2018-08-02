# -*- coding utf-u -*-
"""

@author: Sam
"""

import os 
import pandas as pd
from collections import defaultdict, Counter, OrderedDict
import re
import json
from subprocess import call
import zipfile as zf
from extract_all_tags import * 
import pymongo
from xmljson import Yahoo 
from pathlib import Path
from xml.etree import ElementTree
from math import floor
from parse_cases import parse_case

repo_dir = os.path.expanduser(r"~/LexisNexisCorpus")
zip_dir = os.path.expanduser(r"~/data/content-zip/content")
states_summ_fn = "states_counts.csv" 

courtCaseRE = r"<courtCaseDoc.*?/courtCaseDoc>"

xmlConverter = Yahoo()
progress = [i/10 for i in range(11)]
errorfn = "errors.txt" 

def parseDir(mongoCollection, pathToSourceDir):
	sourceDir = Path(pathToSourceDir)
	files = [f for f in sourceDir.iterdir() if f.is_file()] 
	currProgress = set([floor(i * len(files)) for i in progress])
	for i, f in enumerate(files): 
		for parsedCase in parseFile(f):
			try: 
				#print(parsedCase)
				mongoCollection.insert_one(parsedCase)
			except Exception as e: 
				with open(errorfn, 'a') as eFile:
					print("upload error: " + str(f))
					eFile.write(','.join((str(f.absolute()), "upload error")))
		if i in currProgress: 
			print("{0}/{1} files done in {2}".format(i, len(files), pathToSourceDir))

def parseFile(pathFile):
	parsedCases = [] 
	with pathFile.open() as infile: 
		for m in re.findall(courtCaseRE, infile.read()): 
			try: 
				parsedCase = parse_case(m) 
				parsedCases.append(parsedCase) 
			except Exception as e:
				with open(errorfn,'a') as eFile: 
					print("parse error: " + str(pathFile))
					print(repr(e))
					eFile.write(','.join((str(pathFile.absolute()), "parse error")))
	return parsedCases

def uploadDir(mongoCollection, pathToSourceDir): 
	parseDir(mongoCollection, pathToSourceDir)	

if __name__ == "__main__": 
	zipfiles = [z for z in get_all_state_zips() if z.endswith(".zip")]
	client = pymongo.MongoClient()
	db = client.LexisNexis
	mongoCollection = db["cases"]
	for i, zf in enumerate(zipfiles):
		print("--------------------------")
		print("Starting zip file {0}/{1}".format(i, len(zipfiles)))
		print("Copying", zf)
		copy_zip_file(zf)
		print("Unzipping", zf)
		unzip_file(zf)
		num = zf[:-4] 
		print("Parsing cases")
		uploadDir(mongoCollection, os.path.join(repo_dir, 'content', num))
		print("Deleting", zf)
		delete_zip_file(zf)
		print("Deleting zip dir "+ zf)
		delete_unzipped_folder(os.path.join(repo_dir,'content',num))

