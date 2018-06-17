#!/home/smeshoyrer/amaconda3/bin/python3.6

import os 

data_dir = r"/home/smeshoyrer/LexisNexisCorpus/content/104440/"

for fn in os.listdir(data_dir): 
	file_path = data_dir + fn
	if os.path.isfile(file_path): 
		with open(file_path) as infile: 
			
