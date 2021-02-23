from flask import Flask, render_template, request, redirect

app = Flask(__name__)
mode = 0

def render(mode):
   return render_template("index.html", mode=mode)

@app.route("/", methods=["GET", "POST"])
def index():
   global mode
   if request.method == "POST":
      if int(request.form["value"]):
         mode = 1
      else:
         mode = 0
      return render(mode)
   else:
      return render(mode)
   
@app.route("/results", methods=["POST"])
def results():
   if request.form["keyword"]:
      return redirect("https://duckduckgo.com/&q="
         + str(request.form["keyword"]))
   else:
      return redirect("/")


if __name__ == "__main__":
   app.run()
