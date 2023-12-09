import requests
import json
from StockId import get_stock_id_4
from tqdm import tqdm
import concurrent.futures
import re
import persian
import pandas as pd
# from PageCrawlerSlelnium import extract_table_selenium
# from PageCrawlerJS import extract_final_table



def select_product_stock(stock_id):
    ls1 = ['مواد و محصولات دارويي', 'منسوجات', 'محصولات كاغذي',
          'محصولات غذايي و آشاميدني به جز قند و شكر', 'محصولات شيميايي',
          'محصولات چوبي', 'ماشين آلات و دستگاه هاي برقي',
          'ماشين آلات و تجهيزات', 'لاستيك و پلاستيك', 'كاشي و سراميك',
          'قند و شكر', 'فلزات اساسي', 'فراورده هاي نفتي، كك و سوخت هسته اي',
          'عرضه برق، گاز، بخاروآب گرم', 'سيمان، آهك و گچ',
          'ساير محصولات كاني غيرفلزي', 'ساخت محصولات فلزي',
          'ساخت دستگاه ها و وسايل ارتباطي', 'زراعت و خدمات وابسته',
          'دباغي، پرداخت چرم و ساخت انواع پاپوش', 'خودرو و ساخت قطعات',
          'انتشار، چاپ و تكثير',
          'استخراج كانه هاي فلزي', 'استخراج ساير معادن', 'استخراج زغال سنگ']

    stock_id = stock_id[stock_id['Group'].isin(ls1)]

    ls2 = ['حفاری', 'والبر', 'میدکو', 'تپمپي', 'پترول', 'ونیرو', 'تيپيكو', 'پرشیا','ورنا', 'ونفت', 'وملی', 'ومعادن', 'وبشهر', 'وتوکا', 'وپترو', 'وپخش', 'وتوشه', 'میدکو']

    stock_id = stock_id[~stock_id['Symbol'].isin(ls2)]
    k =(~stock_id['Symbol'].isin(ls2))+stock_id['Group'].isin(ls1)
    stock_id['Class'] = 0
    stock_id.loc[k, 'Class'] = 1
    stock_id = stock_id[stock_id['Symbol'].str[-1] != "ح"]

    return stock_id

##################

def page_ditector():
    url = "https://search.codal.ir/api/search/v2/q?&Audited=true&AuditorRef=-1&Category=3&Childs=true&CompanyState=-1&CompanyType=-1&Consolidatable=true&IsNotAudited=false&Length=-1&LetterType=58&Mains=true&NotAudited=true&NotConsolidatable=true&PageNumber=1&Publisher=false&TracingNo=-1&search=true"
    r = requests.get(url, timeout=15, headers = {
        'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
        } )
    Page = json.loads(r.text)['Page']
    return Page

def codal_crwaler_url(page):
    for i in range(100):
        try:
            url = "https://search.codal.ir/api/search/v2/q?&Audited=true&AuditorRef=-1&Category=3&Childs=true&CompanyState=-1&CompanyType=-1&Consolidatable=true&IsNotAudited=false&Length=-1&LetterType=58&Mains=true&NotAudited=true&NotConsolidatable=true&PageNumber={}&Publisher=false&TracingNo=-1&search=true".format(page)
            r = requests.get(url, headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
            "Accept-Encoding": "*",
            "Connection": "keep-alive"
            } )
            Letters = json.loads(r.text)['Letters']
            result = pd.DataFrame(Letters)
            result = result[['Symbol', 'Title', 'SentDateTime', 'PublishDateTime', 'Url']]


            k1 = result[result.Title.str.contains("اصلاحیه")]
            k1['Edit'] = '1'
            k2 = result[~result.Title.str.contains("اصلاحیه")]
            k2['Edit'] = '0'
            result = pd.concat([k1, k2])

            result['MainDate'] = result['Title'].str.replace('(اصلاحیه)', '')
            result['MainDate'] = result['MainDate'].str[-10:].str.replace('/','')
            # result['MainDate'] = result['MainDate'].astype('int').astype(str)

            result['Url'] = 'https://codal.ir' + result['Url']
            result = result.dropna()
            break
        except:
            pass

    return result


########################### tables


def speed_loader(function,ls,thread):
    with concurrent.futures.ThreadPoolExecutor(max_workers=thread) as executor:
        results = list(tqdm(executor.map(function, ls), total=len(ls), desc="Fetching URLs"))
        return results

########################################################################################

def codal_crwaler():
    page = page_ditector()
    ls1 = []
    for i in tqdm(range(1,page+1)):
        a = codal_crwaler_url(i)
        ls1.append(a)
    result = pd.concat(ls1 , axis = 0 , ignore_index = False)
    return result


def codal_speed_crwaler_url():
    page = page_ditector()
    # page = 1400
    pages = list(range(1, page + 1))
    Stock_url = speed_loader(codal_crwaler_url,pages,20)
    Stock_url1 = pd.concat(Stock_url, axis=0, ignore_index=False)
    return Stock_url1


def remove_edited(df):
    df = df.sort_values(by='Edited')
    df = df.drop_duplicates(subset=['key', 'Name', 'Fund', 'Id', 'Period'],keep='last')
    df = df.drop('Edited',axis=1)

    return df

df = codal_speed_crwaler_url()
df = remove_edited(df)


df.to_csv("step1.csv",index=False)