# libraries
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


# set seaborn whitegrid theme
sns.set(style="whitegrid")

# load dataset from github and convert it to a long format
data = pd.read_csv("pattern_distribution.tsv", sep="\t", header=0)
data = data.sort_values(by=['Language', 'Trimming', 'Count'])
# set seaborn whitegrid theme
sns.set(style="whitegrid")

# using small multiple
# create a grid 
g = sns.FacetGrid(data, col='Language', col_wrap=2, hue="Language")

# grouped violin
g = g.map(
	sns.scatterplot, x=data.index, y=data["Count"], hue=data["Trimming"],
	alpha=0.5, legend=True, size=0.5, palette="colorblind"
	)
# control the title of each facet
g = g.set_titles("{col_name}")

# show the graph
plt.show()
