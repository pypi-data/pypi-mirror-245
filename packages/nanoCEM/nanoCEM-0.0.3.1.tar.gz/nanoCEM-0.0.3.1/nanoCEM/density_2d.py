import pandas as pd
import numpy as np

import plotnine as p9
from matplotlib import pyplot as plt
plt.rcParams['pdf.fonttype'] = 42

results_path='f5c_result_rna'
df = pd.read_csv(results_path+'/Current_feature.csv')
# 创建PCA对象，并指定降维后的维度
df = df[df['position']==2030]
from scipy.stats import zscore
df['Mean'] = zscore(df['Mean'] )
df['Median'] = zscore(df['Median'] )
df['STD'] = zscore(df['STD'] )
df['Dwell time'] = zscore(np.log10(df['Dwell time']) )

from sklearn.decomposition import PCA
pca = PCA(n_components=2)
new_df = pd.DataFrame(pca.fit_transform(df[['Mean','Median','STD','Dwell time']]))
new_df.columns=['PC1','PC2']
new_df = pd.concat([new_df,df['type'].reset_index()], axis =1)
plot = p9.ggplot(new_df, p9.aes(x='PC1', y='PC2',color='type'))\
    + p9.theme_bw() \
    + p9.ylim(-4,4) \
    + p9.xlim(-4,4) \
    + p9.stat_density_2d()\
    + p9.scale_color_manual(values={"Sample": "#F57070", "Control": "#9F9F9F", "Single": "#a3abbd"})\
    + p9.geom_point() \
    + p9.theme(
        figure_size=(5, 5),
        panel_grid_minor=p9.element_blank(),
        axis_text=p9.element_text(size=13),
        axis_title=p9.element_text(size=13),
        title=p9.element_text(size=13),
        legend_position='bottom',
        legend_title=p9.element_blank(),
        strip_text=p9.element_text(size=13),
        strip_background=p9.element_rect(alpha=0),
    )
plot.save(filename=results_path + "/zscore_density.pdf", dpi=300)
print(plot)

#
# plot = p9.ggplot(df, p9.aes(x='Mean',color='type'))\
#     + p9.theme_bw() \
#     + p9.geom_density() \
#     + p9.scale_color_manual(values={"Sample": "#F57070", "Control": "#9F9F9F", "Single": "#a3abbd"})\
#     + p9.theme(
#         figure_size=(5, 5),
#         panel_grid_minor=p9.element_blank(),
#         axis_text=p9.element_text(size=13),
#         axis_title=p9.element_text(size=13),
#         title=p9.element_text(size=13),
#         legend_position='bottom',
#         legend_title=p9.element_blank(),
#         strip_text=p9.element_text(size=13),
#         strip_background=p9.element_rect(alpha=0),
#     )
# plot.save(filename=results_path + "/mean_density.pdf", dpi=300)
# print(plot)

