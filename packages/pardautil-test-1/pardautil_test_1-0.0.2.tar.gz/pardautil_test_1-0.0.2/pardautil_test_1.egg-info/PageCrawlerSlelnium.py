import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


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
    b = a[['Name', 'Unit', 'EndMonthProNum', 'EndMonthSellNum', 'EndMonthSellRate', 'EndMonthSellValue' ]]
    b = b[b.Unit.isna()==False]
    cols = ['EndMonthProNum', 'EndMonthSellNum', 'EndMonthSellRate', 'EndMonthSellValue']
    for clo in cols:
        b[clo] = b[clo].str.replace(",", "")
        b[clo] = b[clo].str.replace("(", "-")
        b[clo] = b[clo].str.replace(")", "")
        b[clo] = b[clo].fillna(0)
        try:
            b[clo] = b[clo].astype('int64')
        except:
            b[clo] = b[clo].astype('float64')

    return b

def extract_table_selenium(url):
    op = webdriver.ChromeOptions()
    op.add_argument('--headless')
    op.add_argument('--no-sendbox')
    op.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service=Service(),options=op)
    table=driver.get(url)
    driver.maximize_window()
    table = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '(//table)[1]'))).get_attribute("outerHTML")
    df = pd.read_html(table)[0]

    df = df_cleaner(df)
    return df

# url = 'https://codal.ir/Reports/Decision.aspx?LetterSerial=rIqg9aMRsPNz0NIpyEO6nQ%3d%3d&rt=2&let=8'
# df = extract_table_selenium(url)

