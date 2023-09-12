from flask import Flask, render_template
import mistune
from read import getNewestMD, getNewestList, getPassageByid, getNewList

app = Flask(__name__)

from markdown_it import MarkdownIt
from mdit_py_plugins.front_matter import front_matter_plugin
from mdit_py_plugins.footnote import footnote_plugin

md = (
    MarkdownIt('commonmark' ,{'breaks':True,'html':True})
    .use(front_matter_plugin)
    .use(footnote_plugin)
    .enable('table')
)

def generate_html_list(data):
    data.reverse()
    data1 = data[1:]
    html = "<ul>\n"
    count = len(data)
    for item in data1:
        title = item[0]
        link = "/p/" + str(count)
        html += f"<li><a href='{link}'>{title}</a></li>\n"
        count -= 1
    html += "</ul>"
    return html

introDuction = """
<p>最近发现Github上有很多很好的期刊，但是无奈环境受限无法随时随地查看这些期刊，于是写了一个Python Flask+爬虫的综合小项目。会定期更新文章列表并爬去GitHub仓库的期刊。用户可以选择喜欢的期刊并阅读。如果你觉得这个项目还可以，欢迎去Github点一个Star～</p>
"""

@app.route("/")
def index():
    # 调用 getNewestMD 函数获取 Markdown 内容
    markdown_list = generate_html_list(getNewList())
    
    # 渲染模板并传递 HTML 内容
    return render_template("index.html", content=introDuction+markdown_list, namer="主页")

@app.route("/save")
def save():
    getNewestList()
    html = "<h1>保存成功！</h1>"
    return render_template("index.html", content=html)

@app.route('/p/<string:idx>')
def readPassage(idx):
    # 调用 getNewestMD 函数获取 Markdown 内容
    markdown_text, name = getPassageByid(idx)
    html_text = md.render(markdown_text)
    

    # 渲染模板并传递 HTML 内容
    return render_template("index.html", content=html_text, namer=name)

if __name__ == "__main__":
    app.run()
