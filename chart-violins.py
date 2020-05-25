import csv
import pandas as pd

from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np

# df = pd.read_csv("result/chart/methods_violin.csv")
# df = pd.read_csv("result/chart/rq1_bh_deprecated.csv")
#
# # plt.ylim(0, 1)
# sns.violinplot(x="Deprecated", y="Ratio",
#                     data=df, palette="muted")
#
#
# plt.show()
#
#
#
# def show_values_on_bars(axs):
#     def _show_on_single_plot(ax):
#         for p in ax.patches:
#             _x = p.get_x() + p.get_width() / 2
#             _y = p.get_y() + p.get_height()
#             value = '{:.2f}'.format(p.get_height())
#             ax.text(_x, _y, value, ha="center")
#
#     if isinstance(axs, np.ndarray):
#         for idx, ax in np.ndenumerate(axs):
#             _show_on_single_plot(ax)
#     else:
#         _show_on_single_plot(axs)
#
# fig, ax = plt.subplots(1, 2)
# show_values_on_bars(ax)
#
# plt.show()
#
#
#
# df = sns.load_dataset("tips")
# groupedvalues=df.groupby('day').sum().reset_index()
#
# pal = sns.color_palette("Greens_d", len(groupedvalues))
# rank = groupedvalues["total_bill"].argsort().argsort()
# g=sns.barplot(x='day',y='tip',data=groupedvalues, palette=np.array(pal[::-1])[rank])
#
# for index, row in groupedvalues.iterrows():
#     g.text(row.name,row.tip, round(row.total_bill,2), color='black', ha="center")
#
# plt.show()


# df = sns.load_dataset("tips")
# groupedvalues=df.groupby('day').sum().reset_index()
# groupedvalues=groupedvalues.sort_values('total_bill').reset_index()
# g=sns.barplot(x='day',y='tip',data=groupedvalues, palette="Blues")
#
# plt.show()

df = pd.read_csv("result/chart/rq3-barchart.csv")

df.plot(kind="bar")
# plt.title("Mince Pie Consumption Study")
# plt.xticks(rotation=30)

plt.xlabel("")
plt.ylabel("")
plt.show()


plt.figure(figsize=(5,5))
sns.set(style="whitegrid")
# sns.se
graph = sns.barplot(x='Ratio', y="Number of APIs", data = df)

for p in graph.patches:
        graph.annotate('{:.0f}'.format(p.get_height()), (p.get_x()+0.3, p.get_height()),
                    ha='center', va='bottom',
                    color= 'black')

plt.show()
# f = pd.read_csv("result/chart/rq1-deprecated-bh.csv")
# #
# fig, axes = plt.subplots(figsize=(5,5))
# plt.ylim(0, 1.5)
# # plt.xlabel("Ratio")
# sns.set(style="whitegrid")
# sns.violinplot(data=df, ax = axes, orient ='v')
# # plt.yticks(range(0, 1))
#
# plt.show()
#
#
#
# plotdata = pd.DataFrame({
#     "Always": [13, 2, 1, 1, 0, 0, 0],
#     "Not Always": [4, 96, 5, 4, 2, 1, 1],
#     "Mixed": [0, 4, 0, 0 , 0, 0, 0]
#     # "Google":[13, 4, 0],
#     # "Azure":[2, 96, 4],
#     # "Adyen":[1, 5, 0],
#     # "AWS":[1, 4, 0],
#     # "Microsoft":[0,	2, 0],
#     # "Windows":[0, 1, 0],
#     # "Nexmo": [0, 1,	0]
# },
#     index=["Google", "Azure", "Adyen", "AWS", "Microsoft", "Windows", "Nexmo" ]
# )
# plotdata.plot(kind="bar", stacked = True)
# # plt.title("Mince Pie Consumption Study")
# plt.xticks(rotation=30)
#
# plt.xlabel("")
# plt.ylabel("")
# plt.show()