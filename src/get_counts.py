

# =======================================================
# FUNCTIONS

def is_in_ranges(x: int, rangesList: list) -> bool:
    """finds if a number is in a lis of organized ranges"""
    for my_range in rangesList:
        if x in my_range: return True
    return False
    
def genomic_region(chr: str, pos: int) -> str:
    """find the region annotation for a position in a genome"""

    if is_in_ranges(pos, genome_regions[chr]['gene']):
        if is_in_ranges(pos, genome_regions[chr]['exon']):
            if is_in_ranges(pos, genome_regions[chr]['CDS']):
                return 'CDS'
            else: return 'exonic'
        else: return 'genic'
    else: return 'intergenic'

# =======================================================
# GENOMOIC REGIONS OBTENTION

genome_regions = {}
entities = ['gene', 'exon', 'CDS']

# Read regeions and seve into dict
with open('results/regions.tsv', 'r') as file:
    for line in file:
        chr, entity, start, stop = line.strip().split('\t')

        if chr not in genome_regions.keys():
            genome_regions[chr] = {entity_type: list() for entity_type in entities}
        genome_regions[chr][entity].append((int(start), int(stop)))

# modifify and process regions info
for chr in genome_regions.keys():
    for entity in entities:

        # sort regions deleting duplicates
        genome_regions[chr][entity] = sorted(list(set(genome_regions[chr][entity])))
        
        # delete redundancies
        my_ranges = genome_regions[chr][entity]
        non_redundant_ranges = [my_ranges[0]]

        for i in range(len(my_ranges)-1):

            if my_ranges[i][0] - non_redundant_ranges[-1][1] > 0:
                non_redundant_ranges.append(my_ranges[i])
            else:
                new_range = (non_redundant_ranges[-1][0], my_ranges[i][1])
                non_redundant_ranges.pop()
                non_redundant_ranges.append(new_range)
            
        genome_regions[chr][entity] = [range(start, stop) for start, stop in non_redundant_ranges]


# =======================================================
# MENDELIAN DESEASES MUTATION POSITION OBTENTION

# extract positions from clinvar by chromosome
clinvar_positions = {}
with open('results/clinvar_clean.tsv', 'r') as file:
    for line in file:
        chromosome, position = line.strip().split('\t')
        chromosome = f'chr{chromosome}'
        
        if chromosome not in clinvar_positions.keys():
            clinvar_positions[chromosome] = [int(position)]
        else: clinvar_positions[chromosome].append(int(position))


# =======================================================
# GET COUNTS

# counts for mutations in each genomic class
counts = {}
for chr in clinvar_positions.keys():
    
    if chr not in genome_regions.keys(): break

    if chr not in counts.keys():
        counts[chr] = {x: 0 for x in ['intergenic', 'genic', 'exonic', 'CDS']}

    for pos in clinvar_positions[chr]:
        counts[chr][genomic_region(chr, pos)] += 1

# save information into file
with open("results/counts.tsv", "w") as f:
    print('chr\tintergenic\tgenic\texon\tCDS', file=f)
    for chr in counts.keys():
        print(f"{chr}\t{counts[chr]['intergenic']}\t{counts[chr]['genic']}\t{counts[chr]['exonic']}\t{counts[chr]['CDS']}", file=f)
