from unicodedata import east_asian_width
import urllib.parse
import time

from flask import Flask, render_template, request, redirect
from hamlish_jinja import HamlishTagExtension
from bs4 import BeautifulSoup
import requests


SITE = "https://www.google.co.jp/search"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebK"\
           "it/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"}


app = Flask(__name__)

app.jinja_env.add_extension(HamlishTagExtension)
app.jinja_env.hamlish_enable_div_shortcut = True
app.jinja_env.hamlish_mode = "indented"

mode = True


def search(keyword):

   def _logging(s):
      cnvtime = time.strftime("%Y/%m/%d %H:%M:%S", time.strptime(time.ctime()))
      print(f"[{cnvtime}] {s}")

   def _replacement(s):
      return s.replace("\n", "").replace("\r", "")

   def _letters(s):
      return sum(2 if east_asian_width(_) in "FWA" else 1 for _ in s)

   _logging(f"Search for '{keyword}'.")

   r = requests.get(SITE, params={"q": keyword}, headers=HEADERS, timeout=5.0)
   soup = BeautifulSoup(r.content, "html.parser")

   titles, links, urls, snippets = [[] for _ in range(4)]

   yurubf = soup.select(".yuRUbf > a")
   for i in yurubf[:7]:
      url = entry = contents = ""

      url = i.get("href").replace("/url?q=", "").split("&sa=U")[0]
      url = urllib.parse.unquote(urllib.parse.unquote(url))
      if "http://" in url or "https://" in url:
         try:
            entry = requests.get(url, headers=HEADERS, timeout=5.0)
            t = entry.elapsed.total_seconds()
            _logging(f"- {t} *({url})")
            entry.encoding = "utf-8"
         except: continue
         links.append(url)

         contents = BeautifulSoup(entry.text, "html.parser")

         if contents.select("title"):
            titles.append(_replacement(contents.select("title")[0].get_text()))
         else:
            titles.append(url)

         if contents.select("body"):
            if _letters((body := contents.select("body")[0].get_text())) > 200:
               snippets.append(body[:200] + "...")
            else:
               snippets.append(body)
         else:
            snippets.append("...")

   for i in links:
      if _letters(i) > 72:
         urls.append(i[:42] + "...")
      else:
         urls.append(i)

   return (titles, links, urls, snippets)


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
   if (keyword := request.form["keyword"]):
      if keyword[0] == "!":
         return redirect(f"https://duckduckgo.com/&q={keyword}")
      elif keyword[0] == "?":
         return redirect(f"https://www.google.com/search?q={keyword[1:]}")
      else:
         titles, links, urls, snippets = search(keyword)
         return render_template("results.haml", mode=int(mode), titles=titles,
                                links=links, urls=urls, snippets=snippets,
                                value=keyword, items=len(titles))
   else:
      return redirect("/")


if __name__ == "__main__":
   app.run(port=50000, debug=True)
