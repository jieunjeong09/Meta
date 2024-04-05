import csv
t = "\t"
in_file = open("ACMG_SG_v3.2","r")
out_file = open("ACMG_table.ttt","w")
colnames = [ "gene", "inheritance", "disorder", "group"]
writ = csv.DictWriter(out_file, fieldnames=colnames, delimiter="\t")
writ.writeheader()
row = {}

import re
for line in in_file:
  line = line.strip()
  a = line.split(sep="\t")
  if re.match("Genes",line):
    row["group"] = re.sub(" phenotypes","",re.sub("Genes related to ","",line))
  elif re.match("[A-Z]",line):
    row["disorder"] = line
  else:
    a = line.split(sep="\t")
    ll = len(a)
    if ll < 3: continue
    if ll > 3: row["inheritance"] = a[3]
    row["gene"] = re.sub("[a-z]$","",a[2])
    writ.writerow(row)
