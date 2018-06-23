# -*- coding utf-u -*-
"""

@author: Sam
"""

import os 
import pandas as pd
from collections import defaultdict, Counter
import re
import json
from subprocess import call
import zipfile as zf
from extract_all_tags import * 

repo_dir = os.path.expanduser(r"~/LexisNexisCorpus")
zip_dir = os.path.expanduser(r"~/data/content-zip/content")
states_summ_fn = "states_counts.csv" 

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


