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

repo_dir = os.path.expanduser(r"~/LexisNexisCorpus")
zip_dir = os.path.expanduser(r"~/data/content-zip/content")
states_summ_fn = "states_counts.csv" 

courtCaseRE = r"<courtCaseDoc.*?/courtCaseDoc>"

xmlConverter = Yahoo()
progress = [i/10 for i in range(11)]
errors = []

def parseDir(mongoCollection, pathToSourceDir):
	sourceDir = Path(pathToSourceDir)
	files = [f for f in sourceDir.iterdir() if f.is_file()] 
	currProgress = set([floor(i * len(files)) for i in progress])
	for i, f in enumerate(files): 
		for parsedCase in parseFile(f):
			mongoCollection.insert_one(parsedCase)
		if i in currProgress: 
			print("{0}/{1} files done in {2}".format(i, len(files), pathToSourceDir))

def parseFile(pathFile):
	parsedCases = [] 
	with pathFile.open() as infile: 
		for m in re.findall(courtCaseRE, infile.read()): 
			try: 
				caseXml = ElementTree.fromstring(m)  
				caseDict = xmlConverter.data(caseXml)
				caseDict = json.loads(json.dumps(caseDict).replace('.','_'))
				parsedCases.append(caseDict)
			except Exception as e: 
				print("Error occurred on {0} - {1}".format(pathFile.resolve(), e.message))
				errors.append((pathFile.resolve(), e.message))
	return parsedCases
	

def uploadDir(mongoCollection, pathToSourceDir): 
	parseDir(mongoCollection, pathToSourceDir)	

if __name__ == "__main__": 
	zipfiles = [z for z in get_all_state_zips() if z.endswith(".zip")]
	
	client = pymongo.MongoClient()
	db = client.LexisNexis
	mongoCollection = db["cases"]
	for zf in zipfiles[:len(zipfiles)//10]:
		print("Copying", zf)
		copy_zip_file(zf)
		print("Unzipping", zf)
		unzip_file(zf)
		num = zf[:-4] 
		print("Parsing cases")
		uploadDir(mongoCollection, os.path.join(repo_dir, 'content', num))
		print("Deleting", zf)
		delete_zip_file(zf)
		print("Deleting zip dir")
		delete_unzipped_folder(os.path.join(repo_dir,'content',num))
	with open("errors.json",'w') as outfile: 
		json.dump(outfile, errors)


'''
class LNParser(object):
    
    def __init__(self, zip_dir, zip_files, repo_dir):
        self.repo_dir = repo_dir
        self.zip_dir = zip_dir
        self.zip_files = zip_files
        

    def copy_and_unzip(zipfn):
        print("copying", zipfn)
        copy_zip_file(zipfile)
        print("unzipping", zipfn)
        unzip_file(zipfile)

    def delete_zip(zipfn):
        print("deleting", zipfn)
        delete_zip_file(zipfn)
        unzip_dir = os.path.join(repo_dir,'content',zipfn[:-4])
        print("deleting",unzip_dir)
        delete_unzipped_folder(unzip_dir)

    def demo_extract_tag(self, tagName, save = False):
        return self._extract_tag_from_files(tagName, list(self.zip_files[0]), save)

    def extract_tag_from_all_files(self,tagName, save=False):
        return self._extract_tag_from_files(tagName, self.zip_files, save)

    def _extract_tag_from_files(self, tagName, zip_files, save = False):
        tag_re = "<{}.*?</{}>"
        tag = defaultdict(lambda: defaultdict(list))
        content_dir = os.path.join(self.repo_dir, 'content')
        errors = []  
        for zipfn in zip_files:
            try:
                LNParser.copy_and_unzip(zipfn)
                
                num = zipfn[:-4]
                unzipped_content_dir = os.path.join(content_dir, num)
                all_fns = os.listdir(unzipped_content_dir)
                num_all_fns = len(all_fns)
                for fn in all_fns:
                    fn_fullPath = os.path.join(unzipped_content_dir, fn)
                    if os.path.isfile(fn_fullPath): 
                        with open(fn_fullPath) as in_fp: 
                            # TODO: avoid full file read()
                            for match in re.findall(tag_re, infile.read())
                                tag[zipfn][fn].append(str(match))
            except Exception as e:
                errors.append((zipfn, e.message))
            
            delete_zip(zipfn)

        if save: 
            json.dumps(tag, os.path.join(self.repo_dir,'tags',f"{tagName}.json"))
            json.dumps(errors, os.path.join(self.repo_dir,'errors.json'))

        return tag, errors
'''

