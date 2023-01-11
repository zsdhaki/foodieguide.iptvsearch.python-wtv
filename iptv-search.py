import requests
from bs4 import BeautifulSoup
import re
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

channel=input("请输入要搜索的频道名称：")
pages=int(input("请输入要搜索的页码数（总计）："))

with open("result.txt", "w", encoding='utf-8') as f:
    for page in range(1, pages+1): # loop through the pages you want to scrape
        url = f'https://www.foodieguide.com/iptvsearch/?page={page}&s={channel}'
        response = requests.get(url, headers=headers)
        response.encoding = response.apparent_encoding
        soup = BeautifulSoup(response.text, 'html.parser')

        #find all tr tags
        tr_tags = soup.find_all('tr')

        for tr_tag in tr_tags:
            td_tags = tr_tag.find_all('td')
            if len(td_tags)>=3:
                #Get the first and the third td tag
                first_td = td_tags[0].text
                third_td = td_tags[2].text
                # Join the two td tags' content
                result = first_td + "," + third_td
                print("Writing: ", result) # print the result before write to file
                f.write(result + "\n")
    print(f"----------页 {page} 已写入----------")

print("----------写入完成，开始格式化----------")

# 打开文件
with open('result.txt', 'r',encoding='utf-8') as f:
    content = f.read()

# 使用正则表达式匹配日期格式
new_content = re.sub(r'\d{2}-\d{2}-\d{4} checked', '', content)

#去掉所有空格
content = content.replace(" ","")



#过滤空行
lines = [i for i in new_content.split('\n') if i]
new_content = ""

#将每两行合并为一行
for i in range(0, len(lines), 2):
    new_content += lines[i]+lines[i+1]+'\n'

# 去掉所有Tab
new_content = new_content.replace("\t","")

# 打开文件，并写入替换后的内容
with open('result.txt', 'w',encoding='utf-8') as f:
    f.write(new_content)
print("----------格式化完成----------")