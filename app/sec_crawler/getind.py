import secform as sf
# import mongoc.connect as mc
import datetime
import getsp as sp 
import re




def get_roa(company, latest=True):
    """ 
        Params: 
                - The stock ticker of a company
                - latest, boolean,  True for the last filling
                                    False for the previous filling
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
        # net cash flow encoding 
        net_cash_flow_indicator = "us-gaap:NetCashProvidedByUsedInOperatingActivities"
        long_debt_term_indicator = "us-gaap:LongTermDebtNoncurrent"
        current_assets_indicator =  "us-gaap:AssetsCurrent"
        current_liabilities_indicator = "us-gaap:LiabilitiesCurrent"
        number_of_shares_indicator = "dei:EntityCommonStockSharesOutstanding"
        print('Latest is FALSE', latest)
        # getting the link of the XBRL file 
        if (latest == False) :
            link = sf.get_prev_xbrl_link(sf.get_cik(company))           
        else: 
            link = sf.get_xbrl_link(sf.get_cik(company))
        
        xbrl_file = sf.get_xbrl_file(link)
        xbrl_year_end = sf.get_sec_year_end(xbrl_file)
        if (xbrl_year_end == None): 
            xbrl_file = sf.get_xbrl_file(sf.get_error_link(sf.get_cik(company)))
            xbrl_year_end = str(xbrl_file.find(name = re.compile('dei:DocumentPeriodEndDate', re.IGNORECASE | re.MULTILINE)).text)
        lperiod = sf.get_indicator_lperiod(xbrl_year_end, l_indicator, xbrl_file)
        rperiod = sf.get_indicator_lperiod(xbrl_year_end, r_indicator, xbrl_file)
        fperiod = sf.get_indicator_lperiod(xbrl_year_end, net_cash_flow_indicator, xbrl_file)
        speriod = sf.get_indicator_lperiod(xbrl_year_end, number_of_shares_indicator, xbrl_file)
       
        assets = sf.get_num_indicator(l_indicator, lperiod, xbrl_file)
        revenues = sf.get_num_indicator(r_indicator, rperiod, xbrl_file)
        net_cash_flow = sf.get_num_indicator(net_cash_flow_indicator, fperiod, xbrl_file)
        long_debt_term = sf.get_num_indicator(long_debt_term_indicator, lperiod, xbrl_file)
        current_assets = sf.get_num_indicator(current_assets_indicator, lperiod, xbrl_file)
        current_liabilities = sf.get_num_indicator(current_liabilities_indicator, lperiod, xbrl_file)
        number_of_shares = sf.get_num_indicator_shares(number_of_shares_indicator, xbrl_file)

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
        return (
                company,                    # 0
                assets,                     # 1          
                revenues,                   # 2 
                net_cash_flow,              # 3 
                int(assets)/int(revenues),  # 4 
                long_debt_term,             # 5
                current_liabilities,        # 6
                current_assets,             # 7
                number_of_shares,           # 8
                latest)                     # 9
    except : 
        print (str(company) + ": ERROR")
        return ('Company not found', 0, 0, 0, False)

#############################################################################################################
################################################# Testing ###################################################
#############################################################################################################
symbol = 'MSFT'

tupple = get_roa(symbol)
print('Company: ', tupple[0])
print('Assets: ', tupple[1])
print('Revenues: ', tupple[2])
print('Net Cash Flow: ', tupple[3])
print('ROA: ', tupple[4])
print('Long Term Debt', tupple[5])
print('Current Liabilities', tupple[6])
print('Current Assets', tupple[7])
print('Number of Shares: ', tupple[8])
print('latest: ', tupple[9])
print('Latest is False here')
tupple = get_roa(symbol, latest=False)
print('Company: ', tupple[0])
print('Assets: ', tupple[1])
print('Revenues: ', tupple[2])
print('Net Cash Flow: ', tupple[3])
print('ROA: ', tupple[4])
print('Long Term Debt', tupple[5])
print('Current Liabilities', tupple[6])
print('Current Assets', tupple[7])
print('Number of Shares: ', tupple[8])
print('latest: ', tupple[9])

if __name__ == "__main___": 
    pass




