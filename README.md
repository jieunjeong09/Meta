# Objective

The inputs are .vcf files of genetic variants from a whole exome assay where
we use only the colums shown here:
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

**1:** ACGM, file ACGM_SG_v3.2, recent version of genes of reportable variants
Paper: ACMG SF v3.2 list for reporting of secondary findings in clinical exome and genome sequencing (Genetics in Medicine, June 22, 2023)

source: https://www.gimjournal.org/action/showFullTableHTML?isHtml=true&tableId=tbl1&pii=S1098-3600%2823%2900879-1

ACGM lists 81 genes that may be included in ACMG compliant reports, variants affecting other genes lack clear medical recommendation about patient treatment.  Each listed gene is associated with a disease, and a group of diseases, additionally, diseases have **inheritance patterns**:
- AD = autosomal dominant,
- AR = autosomal recessive,
- XL = X-chromosome linked

**2:** ClinVar,
file clinvar_20240325.vcf.gz
source: https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/

ClinVar provides **Clinical Significance** with three types of evidence: standard, conflicting (differing assessment), by inclusion (linked by genetic disequillibrium to variants, perhaps unknown, causing the disease).  As recommended, we will report only `Pathogenic` or `Likely Pathogenic` with indication of the type of evidence. 
ClinVar also provides **Consequence** which is a functional annotation, impact on the protein product of the gene, e.g. *missense mutation*.  Concerning Allele Frequency or AF, Clinvar provides several types like ExAC, but only for ca. 5% of variants, so we will not rely on ClinVar for AF.

**3:** GnomAD, browser allows to download a file for 80 of ACGM genes:
https://gnomad.broadinstitute.org/gene/ENSG00000155657?dataset=gnomad_r4
One ACGM gene, titin or TTN, is very long and the number of variants exceeds the constraints of the interactive site, so we downloaded entire file on whole exome of Chr 2 and use tabix to extract the part that contains TTN.  Thus we have a different format for TTN.

GnomAD provides allele frequency AF, Clinical Significance and Consequence, and in the case of the latter two, user can compare if they agree.  We will check if this is always the case.
# Processing resources
## ACGM
The source table was copy-paste moved to file `ACMG_SG_v3.2` and edited for easier processing.  Then we created tab-separated `ACMG_table.txt` by running `ACMG_table.py`: gene, inheritance pattern, disorder, class of disorders:
```
APC	AD	Familial adenomatous polyposis	cancer
RET	AD	Familial medullary thyroid cancer/multiple endocrine neoplasia 2	cancer
BRCA1	AD	Hereditary breast and/or ovarian cancer	cancer
BRCA2	AD	Hereditary breast and/or ovarian cancer	cancer
```
## ClinVar
From our resource file, we filtered the rows and "columns" for our reports, thus creating clinvar_extract.txt by running `awk -f clinvar_extract.awk` (we will change it to Python) 
```
chrom pos reference allele gene ACM consequence
```
The first five columns allow to connect the table with other resources, ACMG using `gene`, while the fist four columns allow to join the data with gnomAD and input assay.  We keep only those rows which may be used in report, i.e. `gene` is on ACMG list and significance field include either `Pathogenic` or `Likely Pathogenic`. 

The first entry in ClinVar that includes those significance types is CLNSIG, which is either a single type or informs about conflicting assessment.  In the latter case, those multiple significance types are in CLNSIGCONF.  Additionally, CLINSIGINCL lists significance type diagnosed indirectly from the variant because of its inclusion in a longer allele connected with disorder phenotype.  Preliminarily, we use three characters for significance, each P (Pathogenic), L (Likely pathogenic) or _ (neither) that can be found (or not) from those three entries.

Consequence describes the type of change, typically in the DNA code of the protein product, if the change is described as several charactistics, we report only the first one but we signal the presence of others with SO.
```
chr1  17022705   CTG   C   SDHB  P__  nonsense,SO
chr1  17022711   TC    T   SDHB  P__  frameshift_variant
chr1  17022719   C     T   SDHB  P__  nonsense
chr1  45330512   T     C   MUTYH _P_  intron_variant
chr1  45330513   TA    T   MUTYH L__  splice_donor_variant
```
Actually, out of 49,290 rows, there are only 60 where CLNSIGINCL is present, and only 4 where it makes a difference, eg. L_P rather than P_P or P_L, so we may decide to drop it, and perhaps include other aspect of significance like "small penetration"
## GnomAD
GnomAD data base primary data files whole exome variants are very large, download alone may take an hour per chromosome, so whenever possible, we downloaded
using gene queries.  TTN file could not be downloaded, it is a very large gene, and mutations can be pathogenic in cardiovascular disorder.  
