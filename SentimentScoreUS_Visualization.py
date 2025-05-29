"""
Credits     : Portions of this code were written with the assistance of ChatGPT o3.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

plt.rcParams['font.family'] = 'Arial'
plt.rcParams['axes.unicode_minus'] = False

#%% 1 Read main dataset and plot boxplot & scatter
df = pd.read_excel(
    r"D:\",
    sheet_name="BOTTOM"
)

# Specified order of states
state_order = []

# Define two groups of states and their colors
group1 = []
group2 = []

plt.figure(figsize=(3, 6), dpi=400)
ax = plt.gca()

# Draw boxplot
sns.boxplot(
    data=df, y="state", x="score",
    width=0.25, zorder=10,
    boxprops={'facecolor':'none','zorder':10},
    whiskerprops={'linewidth':2,'zorder':10},
    flierprops=dict(marker='o', color='red', markersize=1, markeredgewidth=1),
    dodge=False,
    ax=ax,
    order=state_order
)

#%% 2 draw scatter in two passes
# First group:
sns.stripplot(
    data=df[df['state'].isin(group1)],
    y="state", x="score",
    jitter=1, edgecolor="white",
    size=1, color='#FFFFBE',
    zorder=0, dodge=False,
    ax=ax,
    order=state_order
)

# Second group:
sns.stripplot(
    data=df[df['state'].isin(group2)],
    y="state", x="score",
    jitter=1, edgecolor="white",
    size=1, color='#CECCE5',
    zorder=0, dodge=False,
    ax=ax,
    order=state_order
)

# Draw a gray dashed reference line at x=0
ax.axvline(x=0, color='gray', linestyle='--', linewidth=1)

# Set x-axis limits and ticks
ax.set_xlim(-1.0, 1.0)
ax.set_xticks([-1.0, -0.5, 0, 0.5, 1.0])
ax.set_xticklabels(['-1.0', '-0.5', '0', '0.5', '1.0'])
# Set y-axis label and ticks
ax.yaxis.tick_right()
ax.yaxis.set_label_position('right')

ax.margins(y=0.5)
plt.tight_layout(pad=0.1)

#%% 3 Read the "politic" sheet and compute mean score per state
df_p = pd.read_excel(
    r"D:\",
    sheet_name="politic"
)
mean_scores = df_p.groupby('state')['score'].mean()

# Retrieve mean values in the order of the main plot’s y-axis
mean_vals = [mean_scores.get(s, np.nan) for s in state_order]

# Plot the mean scores as a line with markers
ax.plot(
    mean_vals, 
    state_order, 
    marker='o',
    linestyle='-',
    linewidth=1,
    markersize=3,
    color='black',
)

#%% 4 Save and show the figure
output_dir = r"D:\"
os.makedirs(output_dir, exist_ok=True)
plt.savefig(f"{output_dir}/test1_bottomc.png", dpi=400)
plt.show()
