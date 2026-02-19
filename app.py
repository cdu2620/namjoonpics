from flask import Flask, render_template, redirect, url_for, request, session
import requests
from bs4 import BeautifulSoup
import serpapi
import random

app = Flask(__name__)

def get_google_search():
    imgs = []
    params = {
    "engine": "google",
    "q": "namjoon",
    "api_key": "280be8e2dc88b7f74ea5e1e4c2f24ec73b141a25c5a55810ae776172e141da06"
    }
    search = serpapi.search(params)
    results = search.get_dict()
    inline_images = results["inline_images"]
    for img in inline_images:
        imgs.append(img["image"])
    return imgs

def duck_duck_go():
    imgs = []
    params = {
    "engine": "duckduckgo",
    "q": "namjoon",
    "api_key": "280be8e2dc88b7f74ea5e1e4c2f24ec73b141a25c5a55810ae776172e141da06"
    }
    search = serpapi.search(params)
    inline_images = search["inline_images"]
    for img in inline_images:
        imgs.append(img["image"])
    return imgs

def kpopping():
    all_imgs = []
    url = "https://kpopping.com/kpics/gender-all/category-all/idol-RM/group-any/order"
    response = requests.get(url)
    html = response.content

    # Parse the HTML
    soup = BeautifulSoup(html, "html.parser")
    imgs = soup.find_all("div", {"class": "cell"})
    for img in imgs:
        children = img.findChildren("img")
        for child in children:
            child['src'] = child['src'].replace("300", "800")
            url = "https://kpopping.com" + child['src'].split("?")[0]
            all_imgs.append(url)
    return all_imgs


@app.route('/')
def login():
    all_imgs = []
    # google = get_google_search()
    ddg = duck_duck_go()
    kpop = kpopping()
    # all_imgs.extend(google)
    all_imgs.extend(ddg)
    all_imgs.extend(kpop)
    index = random.randint(0, len(all_imgs)-1)
    return render_template('index.html', namjoon=all_imgs[index])