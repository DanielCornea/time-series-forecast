
import json
def print_error(company) :
    with open("erros.txt", "a") as myfile:
        myfile.write(company)
    myfile.close()

def append_company_json(dict):
    with open("piotrosky_score.txt", "a") as myfile:
        myfile.write(json.dumps(dict))
    myfile.close()