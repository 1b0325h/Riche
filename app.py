import os

from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect
from flask_assets import Environment, Bundle
from googleapiclient.discovery import build
from hamlish_jinja import HamlishTagExtension



app = Flask(__name__)
mode = True

# dotenv
load_dotenv(".env")
API_KEY = os.environ.get("API_KEY")
SEARCH_ENGINE_ID = os.environ.get("SEARCH_ENGINE_ID")

# Hamlish settings
app.jinja_env.add_extension(HamlishTagExtension)
app.jinja_env.hamlish_enable_div_shortcut = True
app.jinja_env.hamlish_mode = "indented"

# Sass settings
assets = Environment(app)
assets.url = app.static_url_path
sass = Bundle("sass/blank.sass", "sass/style.sass",
              filters="sass", output="css/all.css")
assets.register("css_all", sass)



def search(keyword):
    service = build("customsearch", "v1", developerKey=API_KEY)
    response = service.cse().list(q=keyword,
                                  cx=SEARCH_ENGINE_ID,
                                  lr="lang_ja",
                                  num=10,
                                  start=1).execute()

    titles, links, urls, snippets = [[] for _ in range(4)]
    for i in response["items"]:
        titles.append(i["title"])
        links.append(i["link"])
        urls.append(i["formattedUrl"])
        snippets.append(i["snippet"])

    return titles, links, urls, snippets


def render(mode):
    return render_template("index.haml", mode=int(mode))


@app.route("/", methods=["GET", "POST"])
def index():
    global mode
    if request.method == "POST":
        if request.form["value"] in "True":
            mode = True
        else:
            mode = False
        return render(mode)
    else:
        return render(mode)


@app.route("/results", methods=["GET", "POST"])
def results():
    if keyword := request.form["keyword"]:
        if keyword[0] == "!":
            return redirect(f"https://duckduckgo.com/&q={keyword}")
        elif keyword[0] == "?":
            return redirect(f"https://www.google.com/search?q={keyword[1:]}")
        else:
            titles, links, urls, snippets = search(keyword)
            return render_template("results.haml", mode=int(mode),
                                   titles=titles, links=links,
                                   urls=urls, snippets=snippets,
                                   value=keyword, items=len(titles))
    else:
        return redirect("/")



if __name__ == "__main__":
    app.run(port=50000)
