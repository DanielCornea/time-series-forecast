import json 
import file_ops as fops
import pandas as pd
file1 = 'piotrosky_score.txt'

comps = []
for line in open(file1, 'r'):
    comps.append(json.loads(line))

dict_final = {}
for comp in comps : 
    dict_final[comp['company']] = list(comp.values())

# print(dict_final)
df = pd.DataFrame.from_dict(dict_final, orient='index')



df.columns = ['company','assets',  'revenues', 'net_cash_flow','long_debt_term','current_liabilities','current_assets','number_of_shares','cogs','prev_assets','prev_revenues','prev_net_cash_flow','prev_long_debt_term','prev_current_liabilities','prev_current_assets','prev_cogs','prev_prev_assets']
df.to_csv('piotroski.csv')
 