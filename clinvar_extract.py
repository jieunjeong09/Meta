import gzip
import re
import csv
colnames = [ "chr", "position", "ref", "allele", "gene", "InhPat", "sig", "conseq" ]
f_in = "clinvar_20240312.vcf.gz"
fout = "clinvar_extract.txt.gz"
fout = open(fout,"wt")
writ = csv.DictWriter(fout, fieldnames=colnames, delimiter="\t",lineterminator='\n')
writ.writeheader()
InhPat = {}
row = {}

def Patho(x):
  if re.search(r"Pathogenic\b",x): return "P"  # r may be needed for \b
  if re.search("Likely_pathogenic",x): return "L"
  return "_"

f = open("ACMG_table.txt","rt") # processed resource file
ACMG = []
for line in f:
  x = line.split()
  ACMG.append(x[0])
  InhPat[x[0]] = x[1]
f.close()

f = gzip.open("clinvar_20240312.vcf.gz","rt")
for line in f:
  if re.match("#",line) : continue # skip explanation lines
  # skip line if no info on "Pathogenic" or "Likely Pathogenic"
  if not re.search(r"[pP]athogenic\b",line): continue # skip if Pat
  x = line.split()
  y = x[7].split(";")
  sig_d = sig_c = sig_i = "_"
  for z in y:
    B = re.split(r'[=:|]',z)
    if B[0] == "GENEINFO":
      row["gene"] = B[1]
    elif B[0] == "MC":
      row["conseq"] = B[3]
    elif B[0] == "CLNSIG":
      sig_d = Patho(z)
    elif B[0] == "CLNSIGCONF":
      sig_c = Patho(z)
    elif B[0] == "CLNSIGINCL":
      sig_i = Patho(z)
  if not row["gene"] in ACMG: continue
  row["chr"] = "chr"+x[0]
  row["position"] = x[1]
  row["ref"] = x[3]
  row["allele"] = x[4]
  row["InhPat"] = InhPat[row["gene"]]
  row["sig"] = sig_d+sig_c+sig_i
  writ.writerow(row)
