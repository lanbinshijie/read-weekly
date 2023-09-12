from flask import Flask, render_template
import markdown
from read import getNewestMD, getNewestList

app = Flask(__name__)

@app.route("/")
def index():
    # 调用 getNewestMD 函数获取 Markdown 内容
    markdown_text, name = getNewestMD()

    # 将 Markdown 转换为 HTML
    html = markdown.markdown(markdown_text)

    # 渲染模板并传递 HTML 内容
    return render_template("index.html", content=html, namer=name)

@app.route("/save")
def save():
    getNewestList()
    html = "<h1>保存成功！</h1>"
    return render_template("index.html", content=html)

if __name__ == "__main__":
    app.run()
