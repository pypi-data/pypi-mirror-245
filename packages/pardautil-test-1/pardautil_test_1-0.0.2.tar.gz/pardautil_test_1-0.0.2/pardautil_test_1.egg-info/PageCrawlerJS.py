
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

def extract_data_1(df):
    ls1 = []
    for item in df:
        if "address" in item:
            a = item.split(":")[1].strip(" \"',")
            ls1.append(a)
        # if "rowCode" in item:
        #     a = item.split(":")[1].strip("',")
        #     ls1.append(a)
        if "columnCode" in item:
            a = item.split(":")[1].strip("',")
            ls1.append(a)
        if "\"value\"" in item:
            a = item.split(":")[1].strip(" \"',")
            ls1.append(a)
    data3 = pd.DataFrame([ls1])
    return data3

def clean_script(soup):
    script = soup.find_all('script')
    s = ''
    for s0 in script:
        s0 = s0.text
        s = s0 + s

    len(s)
    pattern = r"datasource = {(.*)\};"
    s = re.findall(pattern, s)[0]
    return s

def extract_data_2(data1):
    ls2 = []
    for i in data1:
        ali = extract_data_1(i)
        ls2.append(ali)
    final = pd.concat(ls2)
    final[0] = final[0].str.replace(r'\D', '', regex=True)
    return final

def extract_table(final):
    ls3 = final[1].unique()
    ls4 = []
    for i in ls3:
        ali = final[final[1] == i][2].reset_index(drop=True).to_frame(name='i')
        ali.index = final[final[1] == i][0]
        ls4.append(ali)
    resalt = pd.concat(ls4, axis=1)
    return(resalt)

def df_cleaner(a):
    if a.shape[1] == 11:
        a = a[a.iloc[:, 0] != "شرح خدمات یا فروش"]
        a = a[a.iloc[:, 0] != "جمع"]
        a = a[a.iloc[:, 0] != '']
        a = a[a.iloc[:, 0].isna() == False]
        a = a.dropna(axis=1, how='all')
        a = a.iloc[:, :8]
        col5 = ['Name', 'ContractDate', 'ContractPeriod', 'StartIncome', 'Edit', 'EditIncome', 'EndMonthSellValue',
                'EndYearIncome']
        a.columns = col5
        a['Unit'] = 0
        a['EndMonthProNum'] = 0
        a['EndMonthSellNum'] = 0
        a['EndMonthSellRate'] = 0
        b = a[['Name', 'Unit', 'EndMonthProNum', 'EndMonthSellNum', 'EndMonthSellRate', 'EndMonthSellValue']]
        b = b.sort_index(ascending=False)

    a = a[a.iloc[:, 0] != "شرح"]
    a = a[a.iloc[:, 0] != "نام محصول"]
    a = a[a.iloc[:, 1] != '']
    a = a.dropna(axis=1, how='all')
    a = a.iloc[:, :21]
    col5 = ['Name', 'Unit', 'StartProNum', 'StartSellNum', 'StartSellRate', 'StartSellValue', 'EditProNum',
            'EditSellNum', 'EditSellValue',
            'StartEditProNum', 'StartEditSellNum', 'StartEditSellRate', 'StartEditSellValue', 'EndMonthProNum',
            'EndMonthSellNum', 'EndMonthSellRate', 'EndMonthSellValue',
            'EndYearProNum', 'EndYearSellNum', 'EndYearSellRate', 'EndYearSellValue']
    a.columns = col5
    b = a[['Name', 'Unit', 'EndMonthProNum', 'EndMonthSellNum', 'EndMonthSellRate', 'EndMonthSellValue', ]]
    b = b.sort_index(ascending=False)

    return b

def extract_final_table(url,num):
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 Edg/95.0.1020.53'}
    html = requests.get(url, headers=headers)
    soup = BeautifulSoup(html.content, "lxml")

    s = clean_script(soup)
    s = s.split('[')[num]
    # s = soup.select('script')[6].text.split('var datasource =')[1].strip(' ').split('[')[num]
    data1 = [item.split(',') for item in s.split('}')]
    final = extract_data_2(data1)
    resalt = extract_table(final)
    resalt = df_cleaner(resalt)
    return resalt



#################################################################################################################

# url = 'https://codal.ir/Reports/Decision.aspx?LetterSerial=rIqg9aMRsPNz0NIpyEO6nQ%3d%3d&rt=2&let=8'
# a =extract_final_table(url,3)
#