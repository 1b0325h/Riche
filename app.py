from flask import Flask, render_template, request, redirect

app = Flask(__name__)

def color_mode():
   value = 0
   if value:
      return 1 #dark
   return 0 #light

def ddg(keywords):
   return "https://duckduckgo.com/&q=" + str(keywords)


@app.route("/")
def index():
   return render_template("index.html", title="Riche",
      color_mode=color_mode())

@app.route("/results", methods=["POST"])
def results():
   if request.form["keywords"]:
      return redirect(ddg(request.form["keywords"]))
   return redirect("/")


if __name__ == "__main__":
   app.run(debug=True)
