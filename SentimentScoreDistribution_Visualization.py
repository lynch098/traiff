import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, BoundaryNorm
import mapclassify
from scipy.stats import gaussian_kde

# 全局字体设置为 Arial
plt.rcParams['font.family'] = 'Arial'

# 1. 读取数据
input_path = r"D:"
df = pd.read_excel(input_path, sheet_name="Sheet1", dtype={'score': float})
scores = df['score'].dropna().values

# 2. 计算 10 类自然断点
classifier = mapclassify.NaturalBreaks(scores, k=10)
breaks = classifier.bins
boundaries = np.concatenate(([scores.min()], breaks))

# 3. 渐变 colormap 与 norm
cmap = LinearSegmentedColormap.from_list('mycmap', ['#55006D', '#FEEEEB'])
norm = BoundaryNorm(boundaries, ncolors=cmap.N, clip=True)

# 4. 画布与布局
fig = plt.figure(figsize=(6, 8))
gs = fig.add_gridspec(3, 1, height_ratios=[3, 1, 0.2], hspace=0.001)

# 4.1 密度图
ax_density = fig.add_subplot(gs[0, 0])
kde = gaussian_kde(scores)
x = np.linspace(scores.min(), scores.max(), 500)
y = kde(x)

for i in range(len(x)-1):
    xi = [x[i], x[i+1]]
    yi = [y[i], y[i+1]]
    color = cmap(norm((x[i]+x[i+1])/2))
    ax_density.fill_between(xi, yi, color=color, linewidth=0)

ax_density.plot(x, y, color='black', lw=1.5)

# 添加参考线并限制高度
refs = [-0.49, 0.02]
y_max = y.max()
ax_density.set_ylim(bottom=-0.1 * y_max, top=y_max * 1.05)
for x0 in refs:
    y0 = float(kde(x0))
    ax_density.plot([x0, x0], [0, y0], color='black', linestyle='--', linewidth=1)
    ax_density.text(x0, -0.05 * y_max, f"{x0:.2f}", ha='center', va='top', fontsize=10)

for spine in ax_density.spines.values():
    spine.set_visible(False)
ax_density.set_xticks([])
ax_density.set_yticks([])

# 4.2 箱型图（中）
ax_box = fig.add_subplot(gs[1, 0], sharex=ax_density)
box = ax_box.boxplot(
    scores,
    vert=False,
    patch_artist=True,
    widths=0.2,  
    boxprops=dict(facecolor='white', edgecolor='black'),
    medianprops=dict(color='red'),
    whiskerprops=dict(color='black'),
    capprops=dict(color='black')
)

for spine in ax_box.spines.values():
    spine.set_visible(False)
ax_box.set_xticks([])
ax_box.set_yticks([])

# 4.3 colorbar（下）
ax_cbar = fig.add_subplot(gs[2, 0])
cbar = plt.colorbar(
    plt.cm.ScalarMappable(norm=norm, cmap=cmap),
    cax=ax_cbar,
    orientation='horizontal',
    boundaries=boundaries,
    spacing='proportional'
)
for spine in ax_cbar.spines.values():
    spine.set_visible(False)

# 刻度
ticks = boundaries[::2]
cbar.set_ticks(ticks)
cbar.set_ticklabels([f"{t:.2f}" for t in ticks])
cbar.ax.xaxis.set_tick_params(rotation=0)
cbar.set_label('Score (Natural Breaks)')

# 5. 保存
output_path = r"D:\"
plt.savefig(output_path, dpi=400, bbox_inches='tight', transparent=True)
plt.close(fig)

print("图已保存到：", output_path)