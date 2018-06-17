from collections import defaultdict
import re
import os
import json

tags = dict()
repo_dir = r"/home/smeshoyrer/LexisNexisCorpus/"
data_dir = repo_dir + r"content/104440"

for i, fn in enumerate(os.listdir(data_dir)):
    with open(os.path.join(data_dir, fn)) as infile: 
        tags[fn] = defaultdict(int)
        for match in re.findall(r"</.*?>", infile.read()): 
            tags[fn][match[2:-1]] += 1

with open(repo_dir + "104440_tags.json",'w') as outfile: 
    json.dump(tags, outfile, indent = 1)
    
