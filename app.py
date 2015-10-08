from flask import Flask, request, jsonify, send_file, Response, render_template, redirect, url_for
from lxml import etree
import urllib2
import helpers
from PIL import Image
import io
from flask import make_response
import mimetypes

app = Flask(__name__)
XHTML_NAMESPACE = "http://www.w3.org/1999/xhtml"

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        if 'all' in request.form:
            return redirect(url_for('meta', url=url))
        elif 'og' in request.form:
            return redirect(url_for('og', url=url))
        elif 'twitter' in request.form:
            return redirect(url_for('twitter', url=url))
        elif 'images' in request.form:
            return redirect(url_for('images', url=url))
        elif 'logo' in request.form:
            return redirect(url_for('logo', url=url))
    return render_template('index.html')

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
    app.run(debug=True, port=33507)
