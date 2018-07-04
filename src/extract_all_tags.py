# -*- coding: utf-8 -*-
"""
Created on Sun Jun 17 16:02:55 2018

@author: Sam
"""
import os
import pandas as pd
from collections import defaultdict
import re
import json
from shutil import copy2, rmtree
from subprocess import call
import zipfile as zf

repo_dir = os.path.expanduser(r"~/LexisNexisCorpus")
content_fn = r"content-zip-titles-2018-04-25.csv" 
zip_dir = os.path.expanduser(r"~/data/content-zip/content/")
errorzips = []



def get_all_state_zips(): 
    names = pd.read_csv(os.path.join(repo_dir, content_fn))
    return names.loc[names["type"] == "states"]["zip"].tolist()

def copy_zip_file(zip_fn): 
    copy2(os.path.join(zip_dir, zip_fn), repo_dir)
    
def delete_zip_file(zip_fn):
    os.remove(os.path.join(repo_dir, zip_fn))
    
def delete_unzipped_folder(directory): 
    rmtree(directory)
    
def unzip_file(zip_fn): 
    zip_ref = zf.ZipFile(os.path.join(repo_dir, zip_fn), 'r')
    zip_ref.extractall(repo_dir)
    zip_ref.close()

if __name__ == "__main__":
    for zipfile in get_all_state_zips(): 
        if zipfile.endswith(".zip"):
            num = zipfile[:-4]
            try:
                tags = dict() 
                print("copying",zipfile)
                copy_zip_file(zipfile)
                print("unzipping",zipfile)
                unzip_file(zipfile)
                print("extracting tags")
                for filename in os.listdir(os.path.join(repo_dir, 'content',num)):
                    if os.path.isfile(os.path.join(repo_dir, 'content',num,filename)):
                        with open(os.path.join(repo_dir, 'content', num, filename)) as infile: 
                            tags[filename] = defaultdict(int)
                            for match in re.findall(r"</.*?>", infile.read()):
                                tags[filename][match[2:-1]] += 1
                print("deleting",zipfile)
                delete_zip_file(zipfile)
                print("deleting", os.path.join(repo_dir, 'content',num))
                delete_unzipped_folder(os.path.join(repo_dir, 'content',num))
                print("writing tags to", os.path.join(repo_dir, "tags", num+"_tags.json"))
                with open(os.path.join(repo_dir, "tags", num+"_tags.json"), 'w') as outfile:
                    json.dump(tags, outfile, indent = 1)
            except KeyboardInterrupt: 
                exit()
            except:
                errorzips.append(zipfile)

    with open(os.path.join(repo_dir, "error_zips.txt"), 'w') as outfile: 
        outfile.write('\n'.join(errorzips))

=======
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 17 16:02:55 2018

@author: Sam
"""
import os
import pandas as pd
from collections import defaultdict
import re
import json
from shutil import copy2, rmtree
from subprocess import call
import zipfile as zf

repo_dir = os.path.expanduser(r"~/LexisNexisCorpus")
content_fn = r"content-zip-titles-2018-04-25.csv" 
zip_dir = os.path.expanduser(r"~/data/content-zip/content/")
errorzips = []



def get_all_state_zips(): 
    names = pd.read_csv(os.path.join(repo_dir, content_fn))
    return names.loc[names["type"] == "states"]["zip"].tolist()

def copy_zip_file(zip_fn): 
    copy2(os.path.join(zip_dir, zip_fn), repo_dir)
    
def delete_zip_file(zip_fn):
    os.remove(os.path.join(repo_dir, zip_fn))
    
def delete_unzipped_folder(directory): 
    rmtree(directory)
    
def unzip_file(zip_fn): 
    zip_ref = zf.ZipFile(os.path.join(repo_dir, zip_fn), 'r')
    zip_ref.extractall(repo_dir)
    zip_ref.close()

if __name__ == "__main__":
    for zipfile in get_all_state_zips(): 
        if zipfile.endswith(".zip"):
            num = zipfile[:-4]
            try:
                tags = dict() 
                print("copying",zipfile)
                copy_zip_file(zipfile)
                print("unzipping",zipfile)
                unzip_file(zipfile)
                print("extracting tags")
                for filename in os.listdir(os.path.join(repo_dir, 'content',num)):
                    if os.path.isfile(os.path.join(repo_dir, 'content',num,filename)):
                        with open(os.path.join(repo_dir, 'content', num, filename)) as infile: 
                            tags[filename] = defaultdict(int)
                            for match in re.findall(r"</.*?>", infile.read()):
                                tags[filename][match[2:-1]] += 1
                print(tags)
                print("deleting",zipfile)
                delete_zip_file(zipfile)
                print("deleting", os.path.join(repo_dir, 'content',num))
                delete_unzipped_folder(os.path.join(repo_dir, 'content',num))
                print("writing tags to", os.path.join(repo_dir, "tags", num+"_tags.json"))
                with open(os.path.join(repo_dir, "tags", num+"_tags.json"), 'w') as outfile:
                    json.dump(tags, outfile, indent = 1)
            except KeyboardInterrupt: 
                exit()
            except:
                errorzips.append(zipfile)

    with open(os.path.join(repo_dir, "error_zips.txt"), 'w') as outfile: 
        outfile.write('\n'.join(errorzips))

>>>>>>> master
