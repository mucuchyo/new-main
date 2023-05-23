# -*- coding: utf-8 -*-
import subprocess
from flask import Flask, render_template
import sys
app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/inn")
def inn():
    return render_template("inn.html")

@app.route("/jic")
def jic():
    return render_template("jic.html")

@app.route("/ja")
def ja():
    return render_template("ja.html")

@app.route("/data")
def data():
    return render_template("data.html")


@app.route('/run_code')
def run_code():
    cmd = ['python', 'C:\\capstone\\Impact\\Impact\\pythonProject\\GazeTracking\\example.py']
    result = subprocess.check_output(cmd, universal_newlines=True)
    return result



if __name__ == "__main__":
    app.run()
