#%% 1 导入库和设置
import matplotlib.pyplot as plt
from matplotlib import rcParams
import matplotlib as mpl
import pandas as pd
import numpy as np
import os

# 设置工作路径
file_path = r"D:\"
os.chdir(file_path)

# 设置字体
rcParams['font.family'] = 'Arial'
rcParams['axes.unicode_minus'] = False

# 读取数据并进行预处理
df = pd.read_excel("public data cata.xlsx", sheet_name="NORMAL2", index_col="SOC")

# 选择要绘图的列
stack_cols  = ['negative', 'neutral', 'positive']
scatter_col = 'number'
score_col   = 'score'
df = df.dropna(subset=stack_cols + [scatter_col, score_col])
df[stack_cols] = df[stack_cols].div(df[stack_cols].sum(axis=1), axis=0) * 100

# 基础颜色
redColor    = '#d96558'
orangeColor = '#FD8B6B'
greenColor  = '#FFD39A'
grayColor   = '#bfbfbf'

# 为 score 列设置 colormap 和归一化
cmap = plt.get_cmap('RdPu')
norm = mpl.colors.Normalize(vmin=-1, vmax=1)
reversed_cmap = cmap.reversed()

#%% 2 绘制主图和框架
fig = plt.figure(figsize=(4, 5), dpi=1200)
ax = plt.gca()
ax.set_aspect(1)
original_order = list(df.index)

# 布局参数
heightmy    = 0.92
lwmy        = 1
gap_width   = 0.2 
frame_width = 2.5 
subframe_w  = 0.92 

# 计算总宽度以调整 xlim
total_width = frame_width + gap_width + subframe_w + gap_width + subframe_w + 1.2
plt.xlim(0, total_width)
plt.ylim(0.5, len(original_order) + 0.5)
plt.gca().invert_yaxis()

# 绘制 stacked bar
for i, country in enumerate(original_order, start=1):
    d = df.loc[country]
    # 画三段 stacked
    widths = (d[stack_cols] / 100 * frame_width).values
    ax.barh(i, widths[0], left=0,                   color=redColor,    height=heightmy)
    ax.barh(i, widths[1], left=widths[0],           color=orangeColor, height=heightmy)
    ax.barh(i, widths[2], left=widths[0]+widths[1], color=greenColor,  height=heightmy)
    # 国家标签
    ax.text(-0.6, i, country, fontsize=9, ha="center", va="center")
    # 堆叠边框
    ax.barh([i], width=[frame_width], left=0,
            color="none", edgecolor="gray", height=heightmy, lw=lwmy)
    # 第一列：number 散点框
    x1 = frame_width + gap_width
    rect1 = plt.Rectangle((x1, i-heightmy/2), subframe_w, heightmy,
                          facecolor="none", edgecolor="gray", lw=lwmy)
    ax.add_artist(rect1)
    # 第二列：score 色带框 & 填充
    x2 = x1 + subframe_w + gap_width
    color_val = reversed_cmap(norm(d[score_col]))  # 对应 -1 ~ 1
    rect2 = plt.Rectangle((x2, i-heightmy/2), subframe_w, heightmy,
                          facecolor=color_val, edgecolor="gray", lw=lwmy)
    ax.add_artist(rect2)

#%% 3 绘制 number 散点
max_num   = 89140
normal_sz = 400
cent1     = frame_width + gap_width + subframe_w/2
ax.scatter([cent1]*len(df), range(1, len(df)+1),
           s=df[scatter_col]/max_num * normal_sz,
           color=grayColor, zorder=3)

#%% 4 样式微调 & 色标
ax.spines[["left","right","top"]].set_visible(False)
ax.spines["bottom"].set_color("none")
ax.set_xticks([0, frame_width/2, frame_width], labels=["0","50","100"])
ax.set_yticks([])
ax.hlines(ax.get_ylim()[0], -0.2, frame_width, lw=3, color="black", zorder=50)
plt.tight_layout()

#%% 5 保存并展示
output_dir = r"D:\"
os.makedirs(output_dir, exist_ok=True)
plt.savefig(f"{output_dir}/country.png",
            bbox_inches='tight', dpi=1200)
plt.show()
