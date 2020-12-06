# Team Member: Mingchen Huang, Qihang Huang, Junlong Lu
# UCI ID: 11211979,32514470,22111353

from flask import Flask, flash, redirect, render_template, request, url_for, send_from_directory
from SearchEngine import *

app = Flask(__name__)


query = ""


@app.route("/", methods=['POST', 'GET'])
def hello():
    global query
    if request.method == 'POST':
        query = request.form["query"]
        print("text :", query)
        return redirect(url_for("result", txt=query))
    else:
        return render_template('home.html')


@app.route("/<txt>", methods=['POST', 'GET'])
def result(txt):
    global query
    if request.method == 'POST':
        return redirect(url_for("hello"))
    else:
        [time, result] = interface(query)
        return render_template('result.html', time=time, result=result)


if __name__ == "__main__":
    app.run(debug=True)
