from lxml import etree
import urllib2
from PIL import Image
import operator

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}


def right_url(url):
    if 'http' in url:
        return url
    else:
        return "http://{0}".format(url)

REAL_URL = ''

def open_url(url):
    global REAL_URL
    url = right_url(url)
    # proxy = urllib2.ProxyHandler({"http":"http://183.131.151.208:80"})
    # opener = urllib2.build_opener(proxy)
    # urllib2.install_opener(opener)
    try:
        req = urllib2.Request(url, headers=hdr)
        source = urllib2.urlopen(req).read()
        REAL_URL = urllib2.urlopen(req).geturl()
        html_tree = etree.HTML(source)
    except urllib2.URLError:
        return ''
    
    return html_tree

def get_meta(html_tree):
    meta_list = []
    if html_tree:
        for meta in html_tree.iterfind(".//meta"):
            meta_list.append(dict(zip(meta.attrib.keys(), meta.attrib.values())))

    return meta_list

def get_links(html_tree):
    links_list = []
    if html_tree:
        for link in html_tree.iterfind(".//link"):
            links_list.append(dict(zip(link.attrib.keys(), link.attrib.values())))

    return links_list

def get_og(html_tree):
    meta_list = get_meta(html_tree)
    og_list = []
    og_dict = dict()
    for i in enumerate(meta_list):
        if len(meta_list[i]) >= 2 and 'property' in meta_list[i].keys() and 'content' in meta_list[i].keys() and 'og:' in meta_list[i]['property']:
            property = meta_list[i]['property']
            content = meta_list[i]['content']
            og_list.append([property, content])
    for a, b in og_list:
        a = a.strip('og:').replace(':','_')
        og_dict[a] = b
    return og_dict

def get_twitter(html_tree):
    meta_list = get_meta(html_tree)
    twitter_list = []
    twitter_dict = dict()
    for i in range(len(meta_list)):
        if len(meta_list[i]) >= 2 and 'property' in meta_list[i].keys() and 'content' in meta_list[i].keys() and 'twitter:' in meta_list[i]['property']:
            property = meta_list[i]['property']
            content = meta_list[i]['content']
            twitter_list.append([property, content])
    for a, b in twitter_list:
        a = a.replace(':','_')
        twitter_dict[a] = b
    return twitter_dict

def fix_img_url(image_href):
    if image_href.startswith('http'):
        image_url = image_href
    elif image_href.startswith('//'):
        image_url = 'http:' + image_href
    else:
        if REAL_URL.endswith('/'):
            image_url = REAL_URL[:-1] + image_href
        else:
            image_url = REAL_URL + image_href
    return image_url
        
    

def get_apple_icons(html_tree):
    apple_icons = []
    for icon in html_tree.iterfind('.//link[@rel="apple-touch-icon"]'):
        if not icon.attrib['href'].startswith('http'):
            if REAL_URL.endswith('/'):
                icon = REAL_URL[:-1] + icon.attrib['href']
            else:
                icon = REAL_URL + icon.attrib['href']
        else:
            icon = icon.attrib['href']

        apple_icons.append(icon)
    if apple_icons:
        return apple_icons[0]
    else:
        return 'https://docs.python.org/2/_static/py.png'

def get_icons(html_tree):
    icons = html_tree.findall('.//link[@rel="icon"]') + html_tree.findall('.//link[@rel="shortcut icon"]')+ html_tree.findall('.//link[@rel="icon shortcut"]')
    icon_list = []

    for icon in icons:

        icon_list.append(icon.attrib['href'])

    return icon_list

def get_images(html_tree):
    links = get_links(html_tree)
    image_list = []
    for link in links:
        if 'href' in link.keys() and 'rel' in link.keys():
            if '.png' in link['href'] or '.ico' in link['href'] or '.jpg' in link['href'] or '.jpeg' in link['href']:
                image_url = fix_img_url(link['href'])
                image_list.append(image_url)
        else:
            pass

    return image_list

def get_logo(html_tree):
    images = get_images(html_tree)
    logos = dict()
    sorted_logos = None
    if images:
        for image in images:
            file = urllib2.urlopen(image)
            im = Image.open(file)
            image_size = im.size[0] + im.size[1]
            logos[image] = image_size
        sorted_logos = sorted(logos.items(), key=operator.itemgetter(1))

    if sorted_logos:
        return sorted_logos[-1][0]
    else:
        return 'https://dry-harbor-7371.herokuapp.com/avatars/100/nologo'
