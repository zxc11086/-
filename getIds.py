import requests
import json
from bs4 import BeautifulSoup
from collections import defaultdict

headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'cookie': 'JSESSIONID=9F92484C61A908FE80C3A3276486C6F2.TM1; DWRSESSIONID=d47zQsnDQ3CtQZgTyvEJYoZUb1p; _ga=GA1.1.2144615691.1693909398; Hm_lvt_242c27c7689290b81407f20c9264ca25=1718079989,1718099757,1718177609,1718185250; Hm_lvt_17b563784d03d91c8d275255939159fc=1718079989,1718099758,1718177609,1718185251; Hm_lpvt_17b563784d03d91c8d275255939159fc=1718186530; _ga_7YS8WBPT93=GS1.1.1718185251.71.1.1718186530.0.0.0; Hm_lpvt_242c27c7689290b81407f20c9264ca25=1718186784'

}


def process():
    content = ''
    with open('pages.json', 'r',encoding='utf-8') as f:
        content = f.read()
    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(content, 'html.parser')

    # 存储分类链接的字典
    category_links = defaultdict(list)

    # 查找所有tr标签
    tr_tags = soup.find_all('tr')

    # 遍历每个tr标签
    for tr in tr_tags:
        td_tags = tr.find_all('td')
        if(len(td_tags) < 4):
            continue
        category = td_tags[3].text.strip()
        link_tag = td_tags[0].find('a')
        if link_tag:
            link = link_tag['href']
            type = td_tags[1].text.strip()
            category_links[category].append([int(link[14:]),type])

    #分类保存到文件
    for category, links in category_links.items():
        print(f"{category}:")
        with open(f"{category}.txt", 'w', encoding='utf-8') as f:
            for link in links:
                f.write(f"{link}\n")
           

#主函数
if __name__ == '__main__':
    process()