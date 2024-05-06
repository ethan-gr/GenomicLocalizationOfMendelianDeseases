# =======================================================
# IMPORTS

import pandas as pd
import matplotlib.pyplot as plt

# =======================================================
# MAIN

#reading file to dataframe
path = "results\counts.tsv"
data = pd.read_csv(path,sep="\t")

# =======================================================
# PIE PLOTS

labels = ['intergenic', 'genic', 'exon', 'CDS']
colors = ['olivedrab', 'rosybrown', 'gray', 'saddlebrown']

fig, axs = plt.subplots(5, 5, figsize=(16,16))
#fig.suptitle('Distribution of Mutations per region, per chromosome')

for i in range(len(data)):
    row = i // 5
    col = i % 5
    chr = list(data.iloc[i])
    chr_name = chr[0]
    chr.pop(0)
    axs[row, col].pie(chr, labels = labels, colors=colors)
    axs[row, col].title.set_text(chr_name)

axs[-1, -1].axis('off')

plt.savefig("Figures\pie_plots.png")

plt.close()

# =======================================================
# BOX PLOT

box = plt.boxplot(data[labels], labels=labels, patch_artist=True)
for patch, color in zip(box['boxes'], colors):
    patch.set_facecolor(color)

plt.ylabel('Number of Mutations')

plt.savefig(r"Figures\box_plot.png")

plt.close()
