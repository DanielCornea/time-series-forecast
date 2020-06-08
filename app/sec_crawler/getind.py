import secform as sf
# import mongoc.connect as mc
import datetime
import getsp as sp 
import re




def get_roa(company):
    """ 
        Params: The stock ticker of a company 
        Returns:  the Return of Assets Indicator of a company
        This function is to be used as a template for any other functions
    """
    try : 
        # total liabilities encoding (bear in mind Total Liabilities == Total Assets)
        l_indicator = "us-gaap:LiabilitiesAndStockholdersEquity"
        # net income encoding 
        r_indicator = "us-gaap:ProfitLoss"
        # encoding if the above is not found
        err_indicator = "us-gaap:NetIncomeLoss"
        # getting the link of the XBRL file 
        link = sf.get_xbrl_link(sf.get_cik(company))
        
        xbrl_file = sf.get_xbrl_file(link)
        xbrl_year_end = sf.get_sec_year_end(xbrl_file)
        if (xbrl_year_end == None): 
            xbrl_file = sf.get_xbrl_file(sf.get_error_link(sf.get_cik(company)))
            xbrl_year_end = str(xbrl_file.find(name = re.compile('dei:DocumentPeriodEndDate', re.IGNORECASE | re.MULTILINE)).text)
        lperiod = sf.get_indicator_lperiod(xbrl_year_end, l_indicator, xbrl_file)
        rperiod = sf.get_indicator_lperiod(xbrl_year_end, r_indicator, xbrl_file)

        assets = sf.get_num_indicator(l_indicator, lperiod, xbrl_file)
        revenues = sf.get_num_indicator(r_indicator, rperiod, xbrl_file)
        # print("revenues: ", revenues)
        if revenues == None: 
            revenues = sf.get_num_indicator(err_indicator, sf.get_indicator_lperiod(xbrl_year_end, err_indicator, xbrl_file), xbrl_file)
        
        # print('revenues_before', revenues.find('.'))
        # print('assets_before', assets.find('.'))
        if assets.find('.') > -1 or revenues.find('.') > 1:
            find =  re.compile(r"^[^.]*")
            assets = re.search(find, assets).group(0)
            # print('assets:  ', assets)
            revenues = re.search(find, revenues).group(0)
            # print('revenues:  ', revenues)
        return (company, assets, revenues, int(assets)/int(revenues))
    except : 
        print (str(company) + ": ERROR")
        return ('Company not found', 0, 0, 0)


symbol = 'DIS'

tupple = get_roa(symbol)
print('Company: ', tupple[0])
print('Assets: ', tupple[1])
print('Revenues: ', tupple[2])
print('ROA: ', tupple[3])







if __name__ == "__main___": 
    pass



