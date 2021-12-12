import argparse
import json

def read_txt_file(path_to_file):
    file = open(path_to_file, 'r')
    data = file.read()
    return data
    
def return_json(path_to_file):
    data = read_txt_file(path_to_file)
    return_dict = {
         "text": data
    }
    return json.dumps(data)

if __name__ == "__main__":
    
    # argparse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="enter file name", default="static/minute.txt")
    args = parser.parse_args()

    path_to_file = args.file
    json_data = return_json(path_to_file)
    print(json_data)