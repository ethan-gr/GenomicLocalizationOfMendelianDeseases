#! bin/bash

# file cleanning
grep -v "#" data/gencode.v45.annotation.gtf | cut -f1,3-5 | grep -P "gene|exon|CDS" > results/regions.tsv

# file for testing
grep "chr21" results/regions.tsv > results/regions_chr21.tsv