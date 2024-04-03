# Objective

The inputs are .vcf files of genetic variants from a whole exome assay where
we use only the colums with data in this example (ID not used):
```
#CHROM  POS     ID      REF     ALT     QUAL    FILTER  
chr1    12807   .       C       T       6       PASS   
chr1    13079   .       C       G       0.60    RefCall
chr1    13418   .       G       A       1.50    RefCall
```

The main task is to augment this file with columns needed in an ACGM compliant
report.  This also means that we eliminate unnecessary rows, i.e. those that
do not have ACGM significance.  ACGM has a set of rules, and we may have
variants how to interpret them.  The additional colums should include the following (if possible):

- Clinical signifigance based on ACMG criteria
- ACMG classification
- Population frequence from gnomAD, ExAC and TGP
- Functional annotation and predicted impact on protein function
- Supporting evidence from databases like ClinVar and HGMD

# Data sources

1: ACGM, file `ACGM_SG_v3.2`, recent version of genes of reportable variants
source: ACMG SF v3.2 list for reporting of secondary findings in clinical exome and genome sequencing (Genetics in Medicine, June 22, 2023)
This table lists genes that may be included in ACMG compliant reports, variants affecting other genes lack clear medical recommendation about patient treatment.  Each listed gene is associated with a disease, and a group of diseases, additionally, diseases have *inheritance patterns*.

Resource 2: clinvar_20240312.vcf.gz, current version of clinvar
source: `https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/`
file `clinvar_20240325.vcf.gz`
This resource provides **Clinical Significance** with three types of evidence: standard, conflicting (differing assessment), by inclusion (linked by genetic disequillibrium to variants, perhaps unknown, causing the disease).  As recommended, we will report only `Pathogenic` or `Likely Pathogenic` with indication of the type of evidence. 
Each variant 
ACMG Classification, ClinVar Significance, gnomAD AF,
Consequence, e.g.Missense, frameshift
Inheritance Pattern

Resource 1: ACGM_SG_v3.2, recent version of genes of reportable variants
source: ACMG SF v3.2 list for reporting of secondary findings in clinical 
	exome and genome sequencing (Genetics in Medicine, June 22, 2023)

ACGM_list.py creates
ACGM_list.txt has lines: gene inherit
inherit can be
	AD = autosomal dominant,
	AR = autosomal recessive,
	XL = X-chromosome linked

Resource 2: clinvar_20240312.vcf.gz, current version of clinvar
source: NCBI

Resource 2: clinvar_20240312.vcf.gz, current version of clinvar

Chromosome conventions and order:

gzcat clinvar_20240312.vcf.gz | awk '/^[1-9A-Z]/{if ($1 != c){c=$1;print c}}'
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
X
Y

gzcat no* | awk '/^c/{if ($1 != c){c=$1;print c}}'
chr1
chr2
chr3
chr4
chr5
chr6
chr7
chr8
chr9
chr10
chr11
chr12
chr13
chr14
chr15
chr16
chr17
chr18
chr19
chr20
chr21
chr22
chrX
chrY

gzcat no* | grep ^c | awk '{C[$6 " " $7]++}END{for (i in C) print i, C[i]}' | sort -n > temp
