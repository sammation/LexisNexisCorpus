# coding: utf-8 

from LNParser import * 
from collections import Counter

if __name__ == "__main__": 
	state_counts = pd.read_csv(os.path.join(repo_dir, "state_counts.csv"))
	dates_dir = os.path.join(repo_dir, "dates")
	all_year_counts = [] 
	errors = [] 

	for fn in os.listdir(dates_dir): 
		try: 
			zp = dict()
			zip_num = fn[:-len("_dates.json")]
			title = state_counts[state_counts["zip"] == zip_num+".zip"].title.item()
			with open(os.path.join(dates_dir, fn)) as json_fp:
				date_map = json.loads(json_fp.read())
			years = [int(date[:4]) for fn, dates in date_map.items() for date in dates]
			year_counts = Counter(years) 
			zp[zip_num] = {"title" : title, "year_counts" : year_counts}
			all_year_counts.append(zp)
		except: 
			errors.append(fn)
		
	with open(os.path.join(repo_dir,"all_year_counts.json"),'w') as outfile: 
		json.dump(all_year_counts, outfile, indent=1)

	if errors: 
		with open(os.path.join(repo_dir,"all_year_counts.errors"), 'w') as outfile: 
			json.dump(errors, outfile)

		
