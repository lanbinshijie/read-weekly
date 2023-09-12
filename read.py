import requests
import markdown
import re
from bs4 import BeautifulSoup
import json
import hashlib

def saveNewList(lists):
    with open("lists.json", "w") as f:
        f.write(json.dumps(lists))

def getNewList():
    with open("lists.json", "r") as f:
        a = f.read()
        return json.loads(a)

def storePassage(name, content):
    # 将文件名md5后取前8位存入passages文件夹下，后缀名是md，内容为content
    hash_name = hashlib.md5(name.encode()).hexdigest()[:8]
    file_name = f"passages/{hash_name}.md"
    with open(file_name, "w") as f:
        f.write(content)

def getPassage(name, url):
    # 返回name对应的文章
    # 如果name哈希取前八位后加上md的后缀名，在passages文件夹下，直接返回passage的内容
    # 否则去getPassageFromInternet获取文章内容。
    hash_name = hashlib.md5(name.encode()).hexdigest()[:8]
    file_name = f"passages/{hash_name}.md"
    try:
        with open(file_name, "r") as f:
            print("有文件")
            return f.read()
    except FileNotFoundError:
        content = getPassageFromInternet(url)
        storePassage(name,content)
        return content
        

def getPassageFromInternet(url):
    # print("https://raw.githubusercontent.com/ascoders/weekly/master/"+url[1:])
    response = requests.get("https://raw.githubusercontent.com/ascoders/weekly/master/"+url[1:])
    newest_markdown_text = response.content.decode()
    print("获取一个新的文件了")
    return newest_markdown_text


def getNewestMD():
    newest_md_name = getNewList()[-1][0]
    newest_md_url = getNewList()[-1][1]
    # 获取最新的文章，通过名字
    return getPassage(newest_md_name, newest_md_url), newest_md_name

def getNewestList():
    # 发起 HTTP 请求获取 Markdown 内容
    response = requests.get("https://raw.githubusercontent.com/ascoders/weekly/master/readme.md")
    markdown_text = response.content.decode()

    # 使用 markdown 库解析 Markdown 文本
    html = markdown.markdown(markdown_text)

    # 提取所有链接
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find_all('a')

    linker = []

    # 打印链接
    for link in links:
        linker.append((link.text, link['href']))

    # 按标题中的数字进行排序
    sorted_linker = sorted(linker, key=lambda x: int(re.search(r'^(\d+)', x[0]).group()) if re.search(r'^(\d+)', x[0]) else float('inf'))

    # 删除没有数字的元组
    sorted_linker = [link for link in sorted_linker if re.search(r'^\d+', link[0])]

    saveNewList(sorted_linker)
