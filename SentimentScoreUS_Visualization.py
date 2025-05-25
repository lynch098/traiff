import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 全局字体
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['axes.unicode_minus'] = False

# ——— 1. 读取主数据并绘制箱线图 & 散点 ———
df = pd.read_excel(
    r"D:\",
    sheet_name="BOTTOM"
)

# 指定的州顺序
state_order = [
    'FL', 'NC', 'OK', 'ID', 'MT', 'PA', 'DC', 'AZ', 'NJ', 'IN', 'WV', 'TX', 
    'MN', 'AR', 'SC', 'MS', 'IL', 'DE', 'NY', 'HI', 'IA', 'UT', 'RI', 'WY', 'KS'
]

# ——— 定义两组州及对应颜色 ———
group1 = ['PA', 'DC', 'NJ', 'MN', 'IL', 'DE', 'NY', 'HI', 'RI']
group2 = ['FL', 'NC', 'OK', 'ID', 'MT', 'AZ', 'IN', 'WV', 'TX', 'AR', 'SC', 'MS', 'IA', 'UT', 'WY', 'KS']

plt.figure(figsize=(3, 6), dpi=400)
ax = plt.gca()

# 箱线图
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

# ——— 方法二：分两次绘制散点 ———
# 第一组：
sns.stripplot(
    data=df[df['state'].isin(group1)],
    y="state", x="score",
    jitter=1, edgecolor="white",
    size=1, color='#FFFFBE',
    zorder=0, dodge=False,
    ax=ax,
    order=state_order
)

# 第二组：
sns.stripplot(
    data=df[df['state'].isin(group2)],
    y="state", x="score",
    jitter=1, edgecolor="white",
    size=1, color='#CECCE5',
    zorder=0, dodge=False,
    ax=ax,
    order=state_order
)

# 绘制灰色虚线参考线
ax.axvline(x=0, color='gray', linestyle='--', linewidth=1)

# 设置x轴范围和刻度
ax.set_xlim(-1.0, 1.0)
ax.set_xticks([-1.0, -0.5, 0, 0.5, 1.0])
ax.set_xticklabels(['-1.0', '-0.5', '0', '0.5', '1.0'])
# 设置y轴标签在右侧
ax.yaxis.tick_right()
ax.yaxis.set_label_position('right')

# 去除额外留白
ax.margins(y=0.5)
plt.tight_layout(pad=0.1)

# ——— 2. 读取 politic sheet，计算各州 score 均值 ———
df_p = pd.read_excel(
    r"D:\",
    sheet_name="politic"
)
mean_scores = df_p.groupby('state')['score'].mean()

# 按主图的 y 轴顺序取值
mean_vals = [mean_scores.get(s, np.nan) for s in state_order]

# 绘制均值连线和点
ax.plot(
    mean_vals,               # x 轴：均值
    state_order,             # y 轴：州名（分类坐标）
    marker='o',
    linestyle='-',
    linewidth=1,
    markersize=3,
    color='black',
)
#%% 5 保存并展示
output_dir = r"D:\"
os.makedirs(output_dir, exist_ok=True)
plt.savefig(f"{output_dir}/test1_bottomc.png", dpi=400)
plt.show()