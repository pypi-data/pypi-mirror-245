
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import xgboost
import shap

plt.rcParams['pdf.fonttype'] = 42
results_path='f5c_result_rna'
df = pd.read_csv(results_path+'/Current_feature.csv')
kmer_size=2
df = df[(df['position']>=2030-kmer_size)&(df['position']<=2030+kmer_size)]
grouped_df = df.groupby('Read_ID')
result_list=[]
for key,temp in grouped_df:
    item = temp[['Mean','STD','Median','Dwell time']].values
    item = item.reshape(-1,).tolist()
    item.append(temp['type'].values[0])
    if len(item)<20:
        continue
    result_list.append(item)
df = pd.DataFrame(result_list)
result_col = (kmer_size*2+1)*4
df[result_col+1] = df[result_col].apply(lambda x: 1 if x=='Sample' else 0)
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
pos_list = [str(num) for num in list(range(0,result_col+2))]
df.columns=pos_list
X_train, X_test, y_train, y_test = train_test_split(df[[str(num) for num in list(range(0,result_col))]], df[str(result_col+1)], test_size=0.3, random_state=42)

# 创建SVM分类器


# train an XGBoost model
model = xgboost.XGBClassifier()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
# explain the model's predictions using SHAP
# (same syntax works for LightGBM, CatBoost, scikit-learn, transformers, Spark, etc.)
explainer = shap.Explainer(model)
shap_values = explainer(X_train)
print(accuracy)
y_pred = model.predict_proba(X_test)[:,1]
prediction_df = pd.DataFrame({'y_test': y_test, 'y_pred': y_pred})
prediction_df['y_test'] = prediction_df['y_test'].apply(lambda x: 'Sample' if x==1 else 'Control')
import plotnine as p9
category = pd.api.types.CategoricalDtype(categories=['Sample', "Control"], ordered=True)
prediction_df['y_test'] = prediction_df['y_test'].astype(category)
# visualize the first prediction's explanation
plot = p9.ggplot(prediction_df, p9.aes(x='y_test', y="y_pred",fill='y_test')) \
            +p9.scale_fill_manual(values={"Sample": "#F57070", "Control": "#9F9F9F", "Single": "#a3abbd"})\
           + p9.theme_bw() \
           + p9.labs(x='',y='Prediction')\
           + p9.geom_boxplot(width=0.6)\
           + p9.theme(
        figure_size=(4, 4),
        panel_grid_minor=p9.element_blank(),
        axis_text=p9.element_text(size=13),
        axis_title=p9.element_text(size=13),
        title=p9.element_text(size=13),
        legend_position='none',
        legend_title=p9.element_blank(),
        strip_text=p9.element_text(size=13),
        strip_background=p9.element_rect(alpha=0),
    )
print(plot)
plot.save(filename=results_path + "/prediction_barplot.pdf", dpi=300)
plot = p9.ggplot(prediction_df, p9.aes(fill='y_test', x="y_pred")) \
    +p9.scale_fill_manual(values={"Sample": "#F57070", "Control": "#9F9F9F", "Single": "#a3abbd"})\
           + p9.theme_bw() \
           + p9.labs(x='Prediction',y='Density')\
           + p9.geom_density(alpha=0.5)\
           + p9.theme(
        figure_size=(4,4),
        panel_grid_minor=p9.element_blank(),
        axis_text=p9.element_text(size=13),
        axis_title=p9.element_text(size=13),
        title=p9.element_text(size=13),
        legend_position='bottom',
        legend_title=p9.element_blank(),
        strip_text=p9.element_text(size=13),
        strip_background=p9.element_rect(alpha=0),
    )
print(plot)

plot.save(filename=results_path + "/prediction_distribution.pdf", dpi=300)
from sklearn.decomposition import PCA

# 示例数据

