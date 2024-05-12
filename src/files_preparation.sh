#! bin/bash

# gencode file cleanning containing categories of interest
grep -v "#" data/gencode.v45.annotation.gtf | cut -f1,3-5 | grep -P "gene|exon|CDS" > results/regions.tsv

# file for testing
grep "chr21" results/regions.tsv > results/regions_chr21.tsv

# clinvar file cleaning
 grep -v "#" data/clinvar_20240331.vcf | grep "OMIM" | cut -f1-2 | sort -u > results/clinvar_clean.tsv

# file for testing
awk '$1 == "21"' results/clinvar_clean.tsv > results/clinvar_clean_chr21.tsv
