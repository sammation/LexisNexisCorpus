# coding: utf-8 

from extract_all_tags import * 

if __name__ == "__main__": 
	state_counts = pd.read_csv(os.path.join(repo_dir, "state_counts.csv"))
	dates_dir = os.path.join(repo_dir, "dates")
	
