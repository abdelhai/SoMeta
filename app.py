from flask import Flask, jsonify, send_file, Response
from lxml import etree
import urllib2
import helpers
from PIL import Image
import io
from flask import make_response
import mimetypes

app = Flask(__name__)
XHTML_NAMESPACE = "http://www.w3.org/1999/xhtml"

@app.route("/")
def index():
    return """<h3>Enter a url after slash to get the metadata.</h3>
    <b>Options:</b>
    <ul>
    <li>http://127.0.0.1:5000/github.com (all meta data)</li>
    <li>http://127.0.0.1:5000/links/github.com (all link tags)</li>
    <li>http://127.0.0.1:5000/logo/github.com (logo)</li>
    <li>http://127.0.0.1:5000/images/github.com (images)</li>
    <li>http://127.0.0.1:5000/og/github.com (open graph data)</li>
    <li>http://127.0.0.1:5000/twitter/github.com (open graph data)</li>
    </ul>

    This is an experiment, bugs and errors are normal. Have fun ;)
    """

@app.route("/<path:url>")
def meta(url):
    html_tree = helpers.open_url(url)
    meta = helpers.get_meta(html_tree)
    dict = {'meta': meta}
    return jsonify(dict)

@app.route("/links/<path:url>")
def links(url):
    html_tree = helpers.open_url(url)
    links = helpers.get_links(html_tree)
    dict = {'links': links}
    return jsonify(dict)

@app.route("/og/<path:url>")
def og(url):
    html_tree = helpers.open_url(url)
    og = helpers.get_og(html_tree)
    return jsonify(og)

@app.route("/twitter/<path:url>")
def twitter(url):
    html_tree = helpers.open_url(url)
    twitter = helpers.get_twitter(html_tree)
    return jsonify(twitter)

@app.route("/logo/<path:url>", methods = ['GET'])
def logo(url):
    html_tree = helpers.open_url(url)
    img_url = helpers.get_logo(html_tree)
    image = urllib2.urlopen(img_url)
    mime_type = image.info()['Content-Type']


    return Response(image, status=200, mimetype=mime_type)

@app.route("/images/<path:url>")
def images(url):
    html_tree = helpers.open_url(url)
    images = helpers.get_images(html_tree)
    dict = {'images': images}
    return jsonify(dict)


if __name__ == "__main__":
    app.run(debug=True)
