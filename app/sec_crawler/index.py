import getind as gi 
import getsp as sp 
import file_ops as fops

companies = sp.get_sp_companies()
i = 0
size = len(companies)


for company in companies: 
    
    dict_comp  = gi.build_dict(company)
    if (dict_comp == "not_found"):
        fops.print_error(company)
    else: 
        fops.append_company_json(dict_comp)
    
    i = i + 1
    print("{:.2%}".format(i/size))
    
    


if __name__ == "__main___": 
    pass