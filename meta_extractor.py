import arxiv
import argparse
from pdf2image import convert_from_path
import json
import datetime
import os
import glob

parser = argparse.ArgumentParser()
parser.add_argument('-arxiv', type=str, default="2010.04595")

args = parser.parse_args()

def pdf2jpg(f, prefix, dpi):
  images = convert_from_path(f, dpi=dpi, jpegopt={
    "quality": 100,
    "progressive": True,
    "optimize": True
  }, fmt='jpeg')
  for i, img in enumerate(images):
    img.save(f.replace(".pdf", "_%s%02d.jpg" % (prefix, i)), quality=95)
    print(img)

def myconverter(o):
  if isinstance(o, datetime.datetime):
    return o.__str__()
  elif isinstance(o, arxiv.Result.Author):
    print(o.name)
    return o.name

def meta_extract(fid):
  name_without_v = fid.split("v")[0]

  search = arxiv.Search(id_list=[name_without_v])
  paper = next(search.get())

  js = {"title": paper.title,
        "entry_id": paper.entry_id,
        "updated": paper.updated,
        "published": paper.published,
        "authors": paper.authors,
        "summary": paper.summary.replace("\n", " "),
        # "comment": paper.comment,
        # "journal_ref": paper.journal_ref,
        # "doi": paper.doi,
        # "primary_category": paper.primary_category,
        # "categories": paper.categories,
        # "links": paper.links,
        "pdf_url": paper.pdf_url}

  path = "papers/" + name_without_v
  if not os.path.exists(path):
    os.mkdir(path)

  paper.download_pdf(dirpath = path, filename="paper.pdf")
  pdf2jpg(path + "/paper.pdf", "m", 150)
  pdf2jpg(path + "/paper.pdf", "s", 80)

  fo = open(path + "/meta_auto.txt", "w")
  fo.write(json.dumps(js, default=myconverter, indent=4))
  fo.close()
  # print(paper.title)
  # print(paper.entry_id)
  # print(paper.entry_id)
  print(js)
  # print(json.dumps(paper))

def rejpeg():
  for d in os.listdir("papers/"):
    print(d)
    pdf2jpg(f"papers/{d}/paper.pdf", "m", 150)
    pdf2jpg(f"papers/{d}/paper.pdf", "s", 80)

# for f in glob.glob("papers/*/*.png"):
  # os.system("rm " + f)
# print()
# rejpeg()


# pdf2jpg("papers/2012.03927/paper.pdf", "m", 150)
# pdf2jpg("papers/2010.04595/paper.pdf", "s", 80)
meta_extract(args.arxiv)
