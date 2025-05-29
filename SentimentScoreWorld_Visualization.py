"""
Credits     : Portions of this code were written with the assistance of ChatGPT o3.
"""
#%% 1 Import libraries and settings
import matplotlib.pyplot as plt
from matplotlib import rcParams
import matplotlib as mpl
import pandas as pd
import numpy as np
import os

file_path = r"D:\"
os.chdir(file_path)

rcParams['font.family'] = 'Arial'
rcParams['axes.unicode_minus'] = False

# Load and preprocess data
df = pd.read_excel("public data cata.xlsx", sheet_name="NORMAL2", index_col="SOC")

# Select columns for plotting
stack_cols  = ['negative', 'neutral', 'positive']
scatter_col = 'number'
score_col   = 'score'
df = df.dropna(subset=stack_cols + [scatter_col, score_col])
df[stack_cols] = df[stack_cols].div(df[stack_cols].sum(axis=1), axis=0) * 100

# Define base colors
redColor    = '#d96558'
orangeColor = '#FD8B6B'
greenColor  = '#FFD39A'
grayColor   = '#bfbfbf'

# Set up colormap and normalization for score
cmap = plt.get_cmap('RdPu')
norm = mpl.colors.Normalize(vmin=-1, vmax=1)
reversed_cmap = cmap.reversed()

#%% 2  Create main figure and layout
fig = plt.figure(figsize=(4, 5), dpi=1200)
ax = plt.gca()
ax.set_aspect(1)
original_order = list(df.index)

# Layout parameters
heightmy    = 0.92
lwmy        = 1
gap_width   = 0.2 
frame_width = 2.5 
subframe_w  = 0.92 

# Calculate total width for x-axis limits
total_width = frame_width + gap_width + subframe_w + gap_width + subframe_w + 1.2
plt.xlim(0, total_width)
plt.ylim(0.5, len(original_order) + 0.5)
plt.gca().invert_yaxis()

# Draw stacked bars and frame components
for i, country in enumerate(original_order, start=1):
    d = df.loc[country]
    # Compute widths for three segments
    widths = (d[stack_cols] / 100 * frame_width).values
    ax.barh(i, widths[0], left=0,                   color=redColor,    height=heightmy)
    ax.barh(i, widths[1], left=widths[0],           color=orangeColor, height=heightmy)
    ax.barh(i, widths[2], left=widths[0]+widths[1], color=greenColor,  height=heightmy)
    # Country label
    ax.text(-0.6, i, country, fontsize=9, ha="center", va="center")
    # Draw border around stacked bar
    ax.barh([i], width=[frame_width], left=0,
            color="none", edgecolor="gray", height=heightmy, lw=lwmy)
    # Draw rectangle for number scatter plot area
    x1 = frame_width + gap_width
    rect1 = plt.Rectangle((x1, i-heightmy/2), subframe_w, heightmy,
                          facecolor="none", edgecolor="gray", lw=lwmy)
    ax.add_artist(rect1)
    # Draw rectangle for score color ribbon
    x2 = x1 + subframe_w + gap_width
    color_val = reversed_cmap(norm(d[score_col]))  # 对应 -1 ~ 1
    rect2 = plt.Rectangle((x2, i-heightmy/2), subframe_w, heightmy,
                          facecolor=color_val, edgecolor="gray", lw=lwmy)
    ax.add_artist(rect2)

#%% 3 Plot scatter for 'number'
max_num   = 89140
normal_sz = 400
cent1     = frame_width + gap_width + subframe_w/2
ax.scatter([cent1]*len(df), range(1, len(df)+1),
           s=df[scatter_col]/max_num * normal_sz,
           color=grayColor, zorder=3)

#%% 4 Style adjustments and colorbar
ax.spines[["left","right","top"]].set_visible(False)
ax.spines["bottom"].set_color("none")
ax.set_xticks([0, frame_width/2, frame_width], labels=["0","50","100"])
ax.set_yticks([])
ax.hlines(ax.get_ylim()[0], -0.2, frame_width, lw=3, color="black", zorder=50)
plt.tight_layout()

#%% 5 Save and display the figure
output_dir = r"D:\"
os.makedirs(output_dir, exist_ok=True)
plt.savefig(f"{output_dir}/country.png",
            bbox_inches='tight', dpi=1200)
plt.show()
