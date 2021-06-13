from flask import Flask
import os
import json
from datetime import datetime
import glob

app = Flask(__name__,
            static_folder="papers/")


cols = ["Title", "Authors", "Published", "Updated", "PDF", "Tags", "Comments", "Abstract"]
def generateTable(lst):
  out = "<table id='table_paper' class='display'>"
  out += "<thead><tr>"
  for col in cols:
    out += "<th>" + col + "</th>"
  out += "</tr></thead>"
  out += "<tbody>"
  for l in lst:
    out += "<tr class='tr_paper' data-folder='" + l[0] + "' data-pages='" + str(l[2]) + "'>"
    out += "<td class='td_title'>" + l[1]['title'] + "</td>"
    out += "<td>" + ", ".join(l[1]['authors']) + "</td>"
    out += "<td>" + datetime.fromisoformat(l[1]['published']).strftime("%Y-%m-%d") + "</td>"
    out += "<td>" + datetime.fromisoformat(l[1]['updated']).strftime("%Y-%m-%d") + "</td>"
    out += "<td>" + l[1]['pdf_url'] + "</td>"
    out += "<td>Tags</td>"
    out += "<td>Comments</td>"
    out += "<td style='white-space: nowrap; max-width: 300px; overflow: hidden; text-overflow: ellipsis;'>" + l[1]['summary'] + "</td>"
    out += "</tr>"
  out += "</tbody></table>"
  return out


def getMeta(pid):
  f = open("papers/" + pid + "/meta_auto.txt", "r")
  js = json.loads(f.read())
  f.close()
  return js

def getPaperList():
  lst = []
  for d in os.listdir("papers"):
    if os.path.exists("papers/" + d + "/paper.pdf"):
      js = getMeta(d)
      pages = len(glob.glob("papers/" + d + "/paper_s*.jpg"))
      lst.append((d, js, pages))
  return lst

def loadTemplate(f="main.html"):
  with open(f, "r") as f:
    return f.read()

def repTem(template, tag, st):
  return template.replace("{" + tag + "}", st)

@app.route("/paper/<path:subpath>")
def getPaper(subpath):
  out = outm = ""
  pages = sorted(glob.glob("papers/" + subpath + "/paper_s*.jpg"))
  pages_m = sorted(glob.glob("papers/" + subpath + "/paper_m*.jpg"))
  for page in pages:
    out += f"<img width='300px' class='paper_page' src='/{page}'>"

  for page in pages_m:
    outm += f"<img width='900px' class='paper_page' src='/{page}'>"

  template = loadTemplate("paper.html")
  template = repTem(template, "SMALL", out)
  template = repTem(template, "MEDIUM", outm)
  return template

@app.route("/")
def hello():
  lst = getPaperList()
  template = loadTemplate()
  template = repTem(template, "TABLE", generateTable(lst))
  return template
  # return "<br>".join([x[1]["title"] for x in lst])
