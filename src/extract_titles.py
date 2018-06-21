#!/home/smeshoyrer/anaconda3/bin/python3.6

import re
import os
import json

title_re = re.compile(r"<title>.*<\title>")
start_idx = len("<title>")
end_idx = len(r"<\title>")

content_dir = "home/smeshoyrer/LexisNexisCorpus/content/"

titles = dict()

for fn in os.listdir(r"/home/smeshoyrer/LexisNexisCorpus/content/104440/"): 
	with open(r"/home/smeshoyrer/LexisNexisCorpus/content/104440/"+fn) as infile: 
		titles[fn] = list()
		for match in title_re.findall(infile.read()):
			print(str(match))
			titles[fn].append(match[start_idx:-end_idx])
		

with open("/home/smeshoyrer/LexisNexisCorpus/titles.txt") as outfile: 
	outfile.write(json.dumps(titles))
			 
		
