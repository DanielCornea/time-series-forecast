from datapackage import Package

def get_sp_companies(): 
    package = Package('https://datahub.io/core/s-and-p-500-companies/datapackage.json')

    # make a list of companies
    for resource in package.resources:
        if resource.descriptor['datahub']['type'] == 'derived/csv':
            sp_list = resource.read()
            
    # make a dicitionary of companies 
    sp_dict = {}
    for comp in sp_list: 
            sp_dict[comp[0]] = (comp[1], comp[2])

    return sp_dict
