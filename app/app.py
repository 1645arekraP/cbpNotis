from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)

@app.route('/')
def index():
    return "<h1>Please, Please Work.</h1>"