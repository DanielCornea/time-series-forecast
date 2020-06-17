
import json
def print_error(company) :
    with open("erros.txt", "a") as myfile:
        myfile.write(company + '\n')
    myfile.close()

def append_company_json(dict1):
    with open("piotrosky_score.txt", "a") as myfile:
        myfile.write(json.dumps(dict1))
        myfile.write('\n')
    myfile.close()

def read_json_file(file_json):
    with open(file_json) as f:
        data = json.load(f)
    return data
