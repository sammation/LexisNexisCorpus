from extract_all_tags import * 
import pandas as pd
from pathlib import Path

start = 0
dest_path = Path("/mnt/usb-10T-1/Data-eta2103/export/")

if __name__ == "__main__": 
	zipfiles = [z for z in get_all_state_zips() if z.endswith(".zip")]
	for i, zf in enumerate(zipfiles[start:]): 
		print("----------------------------") 
		print("Starting zipfile {0}/{1}".format(i + start, len(zipfiles)))
		try: 
			print("Copying",zf)
			copy_zip_file(zf)
			print("Unzipping",zf)
			unzip_file(zf) 
			print("Extracting cases") 
			extract_cases(os.path.join(repo_dir,'content',zf[:-4]))
			print("Deleting",zf) 
			delete_zip_file(zf)
			print("Deleting zip dir",zf) 
			delete_unzipped_folder(os.path.join(repo_dir,'content',zf[:-4]))
		except Exception as e: 
			print("Error in coppying, unzipping, or deleting") 
			print(repr(e))
			# 
