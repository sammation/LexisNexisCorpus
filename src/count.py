from extract_all_tags import * 


if __name__ == "__main__":
    zip_content = pd.read_csv(os.path.join(repo_dir, content_fn))
    states = zip_content.loc[zip_content["type"]=="states"] 

    counts = {}
    for zip_file in get_all_state_zips(): 
        num = zip_file[:-4] 
        with open(os.path.join(repo_dir,"tags") + num+"_tags.json") as injson:
            curr_tags = json.load(injson)


