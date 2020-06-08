import requests
import re
from bs4 import BeautifulSoup
from xml.etree import ElementTree
import sys





# get CIK number 
def get_cik(company_symbol): 
    """
        Get the cik of a company 

        @params: company_symbol 
        @returns: CIK number as a string

    """
    # defining the URL 
    company_symbol = company_symbol.replace('.', '')
    URL = "https://www.sec.gov/cgi-bin/browse-edgar?CIK={}&owner=exclude&action=getcompany"
    
    # requsting the html file 
    html_doc = requests.get(URL.format(company_symbol))
    
    # soupifying the file 
    soup = BeautifulSoup(html_doc.text, 'html.parser')

    # looking for the pattern of the CIK 
    pattern = re.compile(r'\d{10}')
    return re.search(pattern, str(soup.find("div", {"id": "secBetaGraphic"}))).group()


# in case of error follow this procedure
def get_error_link(CIK):
    # go to the search link 
    URL_search = 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={}&type=10-K&dateb=&owner=exclude&count=10'
    # soupify the request response 
    soup = BeautifulSoup(requests.get(URL_search.format(CIK)).text, 'html.parser')
    # look for 10-k 
    link = soup.find_all(text = "10-K")
  
    # go to the first 10-K 
    
    URL_search = 'https://www.sec.gov' + link[0].parent.find_next('a')['href']
    # soupify the request repsonse 
    soup = BeautifulSoup(requests.get(URL_search).text, 'html.parser')
    
    # look for the file that contains the  'LiabilitiesAndStockholdersEquity' indicator
    links2 = soup.find_all(text = re.compile('.xml', re.IGNORECASE | re.MULTILINE))
    for link in links2: 
        aux_link = link.parent['href']
        html_doc = requests.get('https://www.sec.gov' + aux_link)
        soup2 = BeautifulSoup(html_doc.text, 'lxml')
        if soup2.find(re.compile('us-gaap:LiabilitiesAndStockholdersEquity', re.IGNORECASE | re.MULTILINE)):
            return 'https://www.sec.gov' + link.parent['href']
    

# get XBRL link 
def get_xbrl_link(CIK): 
    # get the first xml foud, in case the first xml is not good get the one with the indicator 
    try :
        # get the first search page link 
            # def the search link for the page where XBRL link should be searched for
        URL_search = 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={}&type=10-K&dateb=&owner=exclude&count=10'
            # get the link for the 10-K form 
        soup = BeautifulSoup(requests.get(URL_search.format(CIK)).text, 'html.parser')

        # get the second link 
            # get the link for the xbrl file 
        URL_search = 'https://www.sec.gov' + soup.find_all(text = "10-K")[0].parent.find_next('a')['href']
        soup = BeautifulSoup(requests.get(URL_search).text, 'html.parser')
        table  = soup.find_all("a", {"href": re.compile('.xml', re.IGNORECASE | re.MULTILINE)})
        return('https://www.sec.gov' + table[0]['href'])

    except: 
        get_error_link(CIK)

# return the file in xml with lxml parsing 
def get_xbrl_file(xbrl_link):
    return BeautifulSoup(requests.get(xbrl_link).text, 'lxml')


# get sec year end 
def get_sec_year_end(xbrl_file): 
    try : 
        year_end = xbrl_file.find(name = re.compile('dei:DocumentPeriodEndDate', re.IGNORECASE | re.MULTILINE))
        return str(year_end.text)
    except: 
        return None    
        
        
# get the year end attribute 
def get_indicator_lperiod(year_end, indicator, xbrl_file): 
    
    values = xbrl_file.find_all(name = re.compile(indicator, re.IGNORECASE | re.MULTILINE))
    for value in values:
        ref_id_tag = xbrl_file.find(name = re.compile('context', re.IGNORECASE | re.MULTILINE), id = str(value.attrs['contextref']))
        re_end = re.search(year_end, str(ref_id_tag))
        if re_end:
            return ref_id_tag.get('id')


# get the last one instance
def get_num_indicator(ind_name, ind_lperiod, xbrl_file):
    try: 
        num = xbrl_file.find(name = re.compile(ind_name, re.IGNORECASE | re.MULTILINE), 
                contextref = ind_lperiod)
        return num.text
    except: 
        return None
        
# company_names = ['AYI', 'A', 'BSX', 'BHF', 'CHD', 'CI', 'XRAY', 'DVN', 'DWDP', 'DPS', 'GGP', 'HRS', 'ITW', 'INTC', 'KEY', 'LLL', 'LUK', 'KORS', 'MCHP', 'NCLH', 'PRGO', 'RSG', 'COL', 'CLX', 'DIS', 'TMK', 'VRSN', 'WYN', 'XRX',
# 'XYL']


# CIK = get_cik(company_name)
# print('get_cik: '+  CIK)
# xbrl_link = get_xbrl_link(get_cik(company_name))
# print('xbrl_link_sec_form: '+  xbrl_link)
# xbrl_file = get_xbrl_file(get_error_link(CIK))
# year_end = get_sec_year_end(xbrl_file)
# print('Year End: ' +  year_end)
# indicator_lperiod = get_indicator_lperiod(year_end, "us-gaap:NetIncomeLoss", xbrl_file)
# print('Indicator lperiod: ' + str(indicator_lperiod))
# print('NUM_indicator: ' + get_num_indicator("us-gaap:NetIncomeLoss",  indicator_lperiod, xbrl_file))


# xbrl_file = get_xbrl_file(xbrl_link)

# # f = open('aes.xml',"w+")
# # f.write(str(xbrl_file))
# # f.close()


# year_end = get_sec_year_end(xbrl_file, CIK)
# if (year_end == None): 
#     xbrl_file = get_xbrl_file(get_error_link(CIK))
#     year_end = str(xbrl_file.find(name = re.compile('dei:DocumentPeriodEndDate', re.IGNORECASE | re.MULTILINE)).text)

#         # year_end = xbrl_file.find(name = re.compile('dei:DocumentPeriodEndDate', re.IGNORECASE | re.MULTILINE))
#         # return str(year_end.text)


# print('get_cik: '+  CIK)
# print('xbrl_link: '+  xbrl_link)
# print('Year End: ' +  year_end)
# indicator_lperiod = get_indicator_lperiod(year_end, "us-gaap:NetIncomeLoss", xbrl_file)

# print('Indicator lperiod: ' + str(indicator_lperiod))

# print('NUM_indicator: ' + get_num_indicator("us-gaap:NetIncomeLoss",  indicator_lperiod, xbrl_file))


if __name__ == "__main___": 
    pass


