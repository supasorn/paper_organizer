from multiprocessing import Pool
import os

def f(x):
  print(x)
  os.system("python meta_extractor.py -arxiv=" + x)

with open("tmp.txt", "r") as fi:
  fs = [x.strip() for x in fi.readlines()]

with Pool(10) as p:
  p.map(f, fs)

print(fs)
