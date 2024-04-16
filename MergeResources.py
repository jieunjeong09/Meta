import pandas as pd
import re
#create DataFrame from resources file
ClinVar = pd.read_csv('clinvar_extract.txt.gz',delimiter='\t',compression='gzip')
# chr	position	ref	allele	gene	sig	consequence
# chr1	17018917	CA	C	SDHB	L__	frameshift_variant
# ...
# chr1	17018939	GC	G	SDHB	P__	frameshift_variant
# ...
# chr1	17018955	G	C	SDHB	_P_	missense_variant
GnomAD = pd.read_csv('GnomAD_patho.txt.gz',delimiter='\t',compression='gzip')
# chr	position	ref	allele	gene	VEP Annotation	ClinVarSig	AF_log10
# chr1	17018815	C	T	SDHB	3_prime_UTR_variant		-6.0105
# chr1	17018817	C	A	SDHB	3_prime_UTR_variant		-5.7187

# merge resources
ClinInfo = pd.merge(ClinVar,GnomAD,on=['chr','position','ref','allele'],how='left')
ClinInfo.to_csv('ClinInfo.csv',sep='\t',index=False)

# compress result
import os
os.system('gzip ClinInfo.csv')


