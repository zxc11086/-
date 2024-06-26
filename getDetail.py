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
    with open('第8章 网络安全.txt', 'r',encoding='utf-8') as f:
        #按行读取文件
        i = 0
        for line in f:
            i += 1
            #去掉行尾的换行符
            line = line.strip()
            #转为list
            line = line[1:-1].split(', ')
            type = line[1][1:-1]
            #获取详情页的URL
            url = f'https://course.buct.edu.cn/meol/common/question/questionbank/student/detail.jsp?id={line[0]}'
            #发送请求
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            question = ''
            ans = []
            if(type == '单项选择题'):
                question = soup.find('input', type='hidden')
                question = str(i) + '.' + ' [' + type + '] ' + question['value']
                tables = soup.find_all('table', cellspacing='0')
                options = tables[1].find_all('tr')
                for op in options:
                    ip = op.find('input',type='radio')
                    if ip:
                        ttd = op.find('td')
                        label = ttd.find('label').text
                        if(ip.get('checked') != None):
                            label = "***" + label
                        #去除空格
                        label = label.replace(' ', '')
                        #去除换行
                        label = label.replace('\n', '')
                        ans.append(label)
                    else:
                        continue       
            elif(type == '不定项选择题'):
                question = soup.find('input', type='hidden')
                question = str(i) + '.' + ' [' + type + '] ' + question['value']
                tables = soup.find_all('table', cellspacing='0')
                options = tables[1].find_all('tr')
                for op in options:
                    ip = op.find('input',type='checkbox')
                    if ip:
                        label = op.find('label').text
                        if(ip.get('checked') != None):
                            label = "***" + label
                        #去除空格
                        label = label.replace(' ', '')
                        #去除换行
                        label = label.replace('\n', '')
                        ans.append(label)
                    else:
                        continue
            elif(type == '判断题'):
                question = soup.find('input', type='hidden')
                question = str(i) + '.' + ' [' + type + '] ' + question['value']
                options = soup.find_all('input', type='radio')
                if(options[0].get('checked') != None):
                    ans = '正确'
                else:
                    ans = '错误'
            elif(type == '填空题'):               
                tables = soup.find_all('table', cellspacing='0')
                question = tables[1].find('input', type='hidden')
                question = str(i) + '.' + ' [' + type + '] ' + question['value']
                ans = tables[2].find('input', type='hidden')
                ans = ans['value']
                #去除空格
                ans = ans.replace(' ', '')
                #去除换行
                ans = ans.replace('\n', '')
            elif(type == '问答题' or type == '名词解释' or type == '计算题'):
                tables = soup.find_all('table', cellspacing='0')
                question = tables[1].find('input', type='hidden')
                question = str(i) + '.' + ' [' + type + '] ' + question['value']
                ans = tables[2].find('input', type='hidden')
                if(ans == None):
                    ans = ""
                else:
                    ans = ans['value']
                #去除空格
                ans = ans.replace(' ', '')
                #去除换行
                ans = ans.replace('\n', '')           
            else:
                continue
            with open('网络安全.txt', 'a', encoding='utf-8') as f:
                f.write(f'{question}\n')
                #如果ans是list
                if(isinstance(ans, list)):
                    for a in ans:
                        f.write(f'{a}\n')
                else:
                    f.write(f'{ans}\n')
                f.write('\n')
    
           

#主函数
if __name__ == '__main__':
    process()