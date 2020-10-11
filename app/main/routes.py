from flask import Flask,render_template, request
import json
from . import main


@main.route('/', methods=['GET'])
def index():
    return render_template("base.html")

# Example of loading a page by url, preferable through ajax in js
@main.route('/example', methods=['GET'])
def example():
    return render_template("base.html")

@main.route("/getPage", methods=['GET'])
def renderPage():
    type = request.args.get('type')
    if type not in ['home', 'credits', 'blog']:
        print("invalid page")

    return render_template(type + ".html")

@main.route('/run_ajax', methods=['GET'])
def getEpisode():
    # data wil contain eps, discount, etc
    data = json.loads(request.args.get('data'))


    # return video url
    return json.dumps(["/static/videos/animation_2.mp4"])
