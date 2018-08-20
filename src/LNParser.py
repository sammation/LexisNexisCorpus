# -*- coding utf-u -*-
"""

@author: Sam
"""

import os 
import pandas as pd
from collections import defaultdict, Counter, OrderedDict
import re
import string
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
parse_errors = dest_path / "parse_errors.txt" 

parsed_tags = 	["fullCaseName", "docketNumber", "courtName", "jurisSystem", "citeForThisResource",
				 "opinion", "caseOpinionBy", "judges", "citations", "counselors", "paginationSchemes"]

metadata_headers = ["path_jurisSystem", "path_courtName", "path_Year", "path_caseID"] + parsed_tags

punc_re = re.compile('[%s]' % re.escape(string.punctuation))

def parseDir(pathToSourceDir):
	sourceDir = Path(pathToSourceDir)
	files = [f for f in sourceDir.iterdir() if f.is_file()] 
	currProgress = set([floor(i * len(files)) for i in progress])
	for i, f in enumerate(files): 
		for parsedCase in parseFile(f):
			try: 
				case_id = parsedCase["citeForThisResource"][0]["citeDefinition"]
				print(parsedCase["citeForThisResource"][0])
				jurisSystem = parsedCase["jurisSystem"]["normalizedShortName"].lower() 
				courtName = '_'.join(punc_re.sub('', parsedCase["courtName"].lower()).split())
				if "filedDate" in parsedCase: 
					year = parsedCase["filedDate"]["year"]
				elif "decisionDate" in parsedCase: 
					year = parsedCase["decisionDate"]["year"]
				else: 
					raise KeyError
			except Exception as e: 
				s = '\t'.join((str(f),repr(e))) + '\n'
				print(s)
				with parse_errors.open('a') as errorFile: 
					errorFile.write(s)
				continue

			# save parsed data to tsv in jurisSystem folder
			parsed_data =   [jurisSystem, courtName, year, case_id] + \
							[str(parsedCase.get(tag, "None")) for tag in parsed_tags]
			metadata_path = dest_path / jurisSystem 
			metadata_path.mkdir(parents = True, exist_ok = True) 
			metadata_filepath = metadata_path / "metadata.tsv" 
			if not metadata_filepath.is_file(): 
				with metadata_filepath.open('a') as outfile: 
					outfile.write('\t'.join(metadata_headers) + '\n') 
			with metadata_filepath.open('a') as outfile: 
				outfile.write('\t'.join(parsed_data))

			# save case text to file
			caseFilePath = dest_path / jurisSystem / courtName / year 
			caseFilePath.mkdir(parents = True, exist_ok = True) 
			caseFile = caseFilePath / case_id	
			with caseFile.open('w') as outfile: 
				outfile.write(parsedCase["caseText"])


			

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
			parseDir(os.path.join(repo_dir, 'content', num))
			print("Deleting", zf)
			delete_zip_file(zf)
			print("Deleting zip dir "+ zf)
			delete_unzipped_folder(os.path.join(repo_dir,'content',num))
		except Exception as e: 
			print("Error in copying, unzipping, or deleting")
			print(repr(e))
			with open(errorfn, 'a') as eFile: 
				eFile.write(str(zf) + " " + repr(e) + "\n")
