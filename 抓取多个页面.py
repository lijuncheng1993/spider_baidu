# 1.http://wz.sun0769.com/index.php/question/questionType?type=4
# 爬取投诉帖子的编号、帖子的url、帖子的标题，和帖子里的内容，并将内容写入到json文件中。
import re
import requests
import json


def parse_response(response):
    title = re.findall(r'<span class="niae2_top">提问：(.*?)</span>', response, re.S)  # 匹配标题
    # print(title[0])
    content = re.findall(r'<td class="txt16_3" >&nbsp;&nbsp;&nbsp;&nbsp;(.+?)</td>', response, re.S)  # 匹配帖子里的内容
    content_text = re.sub(r'<.*?>', '', content[0])
    # print(content_text)
    number = re.findall(r'编号:(\d+)</span></td>', response, re.S)  # 匹配编号
    # print(number)
    result = re.findall(r'网友：(.*?) 发言时间：(\d+-\d+-\d+ \d+:\d+:\d+)', response, re.S)
    # print(result)
    # url = re.findall(r'<span class="school">提问：(.*?)</span>', response, re.S)  # 匹配帖子里的内容
    # if not content_text:
    #     print(res.url)
    items = {
        '标题': title[0],
        '内容': content_text,
        '编号': number,
        '网友': result[0][0],
        '发布时间': result[0][1],
    }
    # print(items)
    return items

def save_items(urls):
    with open('items11.json', 'a', encoding='utf-8') as f:
        for url in urls:
            detail_res = requests.get(url).content.decode('gbk')
            items = parse_response(detail_res)
            # f.write(json.dumps(items))
            f.write(json.dumps(items, ensure_ascii=False) + '\n\n')

if __name__ == '__main__':
    url = 'http://wz.sun0769.com/index.php/question/questionType?page={}'
    for i in  range(0,300,30):
        res = requests.get(url.format(i)).content.decode('gbk')
        urls = re.findall(r'</a> <a href="(.*?shtml)" ', res, re.S)  # 匹配url
        print(urls)
        save_items(urls)