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

dest_path = Path("/mnt/usb-10T-1/Data-eta2103/export/") 
metadata = dest_path / "metadata.tsv" 

def parseDir(mongoCollection, pathToSourceDir):
	sourceDir = Path(pathToSourceDir)
	files = [f for f in sourceDir.iterdir() if f.is_file()] 
	currProgress = set([floor(i * len(files)) for i in progress])
	for i, f in enumerate(files): 
		for parsedCase in parseFile(f):
			try:
				if "filedDate" in parsedCase: 
					year = parsedCase["filedDate"]["year"]
				elif "decisionDate" in parsedCase: 
					year = parsedCase["decisionDate"]["year"]
				else: 
					raise KeyError

				case_id = parsedCase["citeForThisResource"]["citeDefinition"] 
				jurisSystem = parsedCase["jurisSystem"]["normalizedShortName"] 
				courtName = parsedCase["courtName"] 
				fullCaseName = parsedCase["fullCaseName"]
				docketNumber = parsedCase["docketNumber"] 
				caseText = parsedCase["caseText"] 

				save_path = dest_path / jurisSystem / courtName / year 
				save_path.mkdir(parents=True, exist_ok=True)
				save_path = save_path / case_id
				with save_path.open('w') as outfile: 
					outfile.write(caseText) 
				with metadata.open('a') as outfile: 
					outfile.write('\t'.join([str(t) for t in (case_id, jurisSystem, courtName, fullCaseName, docketNumber)]) + '\n')

			except Exception as e: 
				with open(errorfn, 'a') as eFile:
					print("extract error: " +  repr(e))
					eFile.write(','.join((str(f.absolute()), "extract error")))
					eFile.write("\n")
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
					eFile.write("\n")
	return parsedCases

def uploadDir(mongoCollection, pathToSourceDir): 
	parseDir(mongoCollection, pathToSourceDir)	

if __name__ == "__main__": 
	zipfiles = [z for z in get_all_state_zips() if z.endswith(".zip")]
	client = pymongo.MongoClient()
	db = client.LexisNexis
	mongoCollection = db["cases"]
	start = 0
	end = 10
	for i, zf in enumerate(zipfiles[start:end]):
		print("--------------------------")
		print("Starting zip file {0}/{1}".format(i + start, len(zipfiles)))
		try:
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
		except Exception as e: 
			print("Error in copying, unzipping, or deleting")
			print(repr(e))
			with open(errorfn, 'a') as eFile: 
				eFile.write(str(zf) + " " + repr(e) + "\n")
