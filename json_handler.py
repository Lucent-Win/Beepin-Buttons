import json

def fix_dir(path):
	#converts windows \ into / 
    new_path = path.replace("\\", r"/")
    return new_path


def open_json(json_path):
    if not json_path.lower().endswith(('.json')):
        raise Exception("open_file cannot open non .json files.")
        return {}
    try:
        path = fix_dir(json_path) # create filepath
        file = open(path)
        data_stream = file.read()
        data = json.loads(data_stream)
        return data
    except Exception as e:
        print("Error loading " + str(json_path) + ": " + str(e))
        return {}


def save_json(json_path,data_array):
    try:
        file_path = fix_dir(json_path)
        file = open(file_path, 'w')    
        write_data = json.dumps(data_array) #write everything at once. 
        file.write(write_data)        
    except:
        print("Could not save " + str(json_path))
        return
