import os
import re

filePath = 'clinvar.vcf';
outputfile = open('clinvar.csv','w');

################################################
#			     Helper Methods                #
################################################
def extractInfoString( info ):
	result = []

	clinallele_index = " ".join( clinallele_re.search( info ).group(1).split(",") )
	diseases = " ".join( disease_re.search(info).group(1).split(",") )
	clinsigs = " ".join( clinsig_re.search(info).group(1).split(',') )
	clinrevstats = " ".join( clinrevstat_re.search(info).group(1).split(",") )
	clinaccs = " ".join( clinacc_re.search(info).group(1).split(",") )
	gene_group = gene_re.search(info)

	if gene_group :
		gene = "".join( gene_group.group(1) )
	else:
		gene = ""


#Adding global unique identifier
    clinaccs = clinaccs.split('|')[0];
    clinaccs = clinaccs.split(' ')[0];
    clinaccs = "https://www.ncbi.nlm.nih.gov/clinvar/" + clinaccs;

    result.append( clinallele_index.replace('\n','') )
	result.append( diseases.replace('\n','') )
	result.append( clinsigs.replace('\n','') )
	result.append( clinrevstats.replace('\n','') )
	result.append( clinaccs.replace('\n','') )
	result.append( gene );

	return result

def listToCSVRow( dataList ):

	row = ""
	for item in dataList:
		item = item.replace(',','')
		row += ',' + item

	return row[1:]



################################################
#			Fields in Info We Need             #
################################################
clinallele_re = re.compile("CLNALLE=(-?\d+)")
disease_re = re.compile("CLNDBN=([^;]*)")
clinsig_re = re.compile("CLNSIG=([^;]*)")
clinrevstat_re = re.compile("CLNREVSTAT=([^;]*)")
clinacc_re = re.compile("CLNACC=([^;]*)")
gene_re = re.compile("GENEINFO=(\w+)")


fixed_tittle = "CHROM,POS,ID,REF,ALT,QUAL,FILTER"
info_tittle = "CLNALLE,CLNDBN,CLNSIG,CLNREVSTAT,CLNACC,GENEINFO"

full_tittle = fixed_tittle + ',' + info_tittle;

outputfile.write(full_tittle + os.linesep)


################################################
#			       Start Parsing               #
################################################
with open( filePath ) as f:
	for line in f:
		if line.startswith("#",0, 2):
			continue;
		fieldList = line.split('\t')
		fixedList = fieldList[0:7];
		infoString = fieldList[7];
		infoList = extractInfoString( infoString )
		row = listToCSVRow( fixedList + infoList )
		outputfile.write( row + os.linesep)






