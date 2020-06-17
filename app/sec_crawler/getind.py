import secform as sf
# import mongoc.connect as mc
import datetime
import getsp as sp 
import re
import time
import file_ops as fops


def get_prev_assets(company):
    try:
        l_indicator = "us-gaap:LiabilitiesAndStockholdersEquity"
        link = sf.get_prev_xbrl_link(sf.get_cik(company), level = 2)           
        xbrl_file = sf.get_xbrl_file(link)
        xbrl_year_end = sf.get_sec_year_end(xbrl_file)
        if (xbrl_year_end == None): 
            xbrl_file = sf.get_xbrl_file(sf.get_error_link(sf.get_cik(company)))
            xbrl_year_end = str(xbrl_file.find(name = re.compile('dei:DocumentPeriodEndDate', re.IGNORECASE | re.MULTILINE)).text)

        lperiod = sf.get_indicator_lperiod(xbrl_year_end, l_indicator, xbrl_file)
        assets = sf.get_num_indicator(l_indicator, lperiod, xbrl_file)
        return assets



    except :
        print("No puedo compilar!")
        return 0


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
        cogs_indicator = "us-gaap:CostOfGoodsAndServicesSold"
        # print('Latest is FALSE', latest)
        # getting the link of the XBRL file 
        cik = sf.get_cik(company)
        if (latest == False) :
            link = sf.get_prev_xbrl_link(cik)           
        else: 
            link = sf.get_xbrl_link(cik)
        
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
        number_of_shares = sf.get_num_no_period(number_of_shares_indicator, xbrl_file)
        cogs = sf.get_num_no_period(cogs_indicator, xbrl_file)


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
                long_debt_term,             # 4
                current_liabilities,        # 5
                current_assets,             # 6
                number_of_shares,           # 7
                cogs,                       # 8
                cik)                        # 9
    except : 
        return 0
def build_dict(company):
    try:
        inds = get_roa(company)
        prev_inds = get_roa(company, latest=False)
        dict1 = {
            'company'               : inds[0], 
            'assets'                : inds[1],
            'revenues'              : inds[2],
            'net_cash_flow'         : inds[3],
            'long_debt_term'        : inds[4],   
            'current_liabilities'   : inds[5], 
            'current_assets'        : inds[6],
            'number_of_shares'      : inds[7],
            'cogs'                  : inds[8],
            'prev_assets'           : prev_inds[1],
            'prev_revenues'         : prev_inds[2],
            'prev_net_cash_flow'    : prev_inds[3], 
            'prev_long_debt_term'   : prev_inds[4], 
            'prev_current_liabilities'  : prev_inds[5], 
            'prev_current_assets'       : prev_inds[6], 
            'number_of_shares'          : prev_inds[7], 
            'prev_cogs'                 : prev_inds[8],
            'prev_prev_assets'          : get_prev_assets(company)
        }

        return  dict1
    except : 
        return "not_found"

#############################################################################################################
################################################# Testing ###################################################
#############################################################################################################
# symbol = 'DIS'

# start_time = time.time()
# dict1 = build_dict(company=symbol)
# print(dict1)
# fops.append_company_json(dict1)
# print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == "__main___": 
    pass




