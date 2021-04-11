import unicodedata
import time
import urllib.parse

from flask import Flask, render_template, request, redirect
from bs4 import BeautifulSoup
import requests


app = Flask(__name__)
mode = 1
site = "https://www.google.co.jp/search"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) A"\
           "ppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.19"\
           "8 Safari/537.36"}


def search(keyword):
   timeln('Search for "{}".'.format(keyword))
   r = requests.get(site, params={"q": keyword},
                    headers=headers, timeout=5.0)
   soup = BeautifulSoup(r.content, "html.parser")
   title, link, url, snippet = [[] for _ in range(4)]

   yurubf = soup.select(".yuRUbf > a")
   for i in yurubf[:10]:
      si = ri = mi = ""
      si = i.get("href").replace("/url?q=", "").split("&sa=U")[0]
      si = urllib.parse.unquote(urllib.parse.unquote(si))
      if "http://" in si or "https://" in si:
         try:
            ri = requests.get(si, headers=headers, timeout=5.0)
            t = ri.elapsed.total_seconds()
            timeln("- {} *({})".format(t, si))
            ri.encoding = "utf-8"
         except: continue
         link.append(si)
         mi = BeautifulSoup(ri.text, "html.parser")
         if mi.select("title"):
            title.append(replacement(mi.select("title")[0].get_text()))
         else: title.append(si)
         if mi.select("body"):
            if letters((b := mi.select("body")[0].get_text())) > 200:
               snippet.append(b[:200] + "...")
            else: snippet.append(b)
         else: snippet.append("...")

   for i in link:
      if letters(i) > 72:
         url.append(i[:42] + "...")
      else: url.append(i)

   return (title, link, url, snippet)


def letters(text):
   c = 0
   for i in text:
      if unicodedata.east_asian_width(i) in "FWA":
         c += 2
      else: c += 1
   return c


def replacement(s):
   return s.replace("\n", "").replace("\r", "")


def timeln(s):
   cnvtime = time.strftime("%Y/%m/%d %H:%M:%S",
                           time.strptime(time.ctime()))
   print("[{}] {}".format(cnvtime, s))


def render(mode):
   return render_template("index.html", mode=mode)


@app.route("/", methods=["GET", "POST"])
def index():
   global mode
   if request.method == "POST":
      if int(request.form["value"]):
         mode = 1
      else: mode = 0
      return render(mode)
   else: return render(mode)


@app.route("/results", methods=["GET", "POST"])
def results():
   if (keyword := request.form["keyword"]):
      if keyword[0] == "!":
         return redirect("https://duckduckgo.com/&q=" + str(keyword))
      else:
         title, link, url, snippet = search(keyword)
         return render_template("results.html", mode=mode, title=title,
                                link=link, url=url, snippet=snippet,
                                value=keyword, iter=len(title))
   else:
      return redirect("/")


if __name__ == "__main__":
   app.run(port=50000)
