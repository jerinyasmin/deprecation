import csv
import pandas as pd

# df1 = pd.read_csv("result/chart/chart_deprecated_operation_merged.csv")
# df = pd.read_csv("result/RQ1/breaking_changes_in_deprecated_list.csv")
#
# changes = pd.read_csv("result/RQ1/changes_in_prev.csv")
# files = pd.read_csv("result/RQ1/deprecated_file.csv")
#
# files_api = []
#
# for index, row in files.iterrows():
#     # print(row['count_follower'])
#     files_api.append(row['File having deprecated'])
#
#
# with open('result/chart/rq1_bh_deprecated.csv', mode='w', encoding="utf-8") as res_file:
#     res_writer = csv.writer(res_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
#     res_writer.writerow(["Version", "Length", "Behavior"])
#
#     for index, row in changes.iterrows():
#         version = row['File']
#         ln = row['Length']
#
#         value = "Not follow"
#
#         if version in files_api:
#             value = "Follow"
#
#         res_writer.writerow([version, ln, value])
#
# apis = []
# for index, row in df.iterrows():
#     # print(row['count_follower'])
#     # print(row["api"])
#     if row['count_follower'] > 0:
#         apis.append(row['api'])
#
# print(len(apis))
# deprecated = {}
# apis_all = []
# for index, row in df1.iterrows():
#     # print(row)
#     ratio = row["ratio"]
#     api = row['api']
#     apis_all.append(api)
#
#     if api in apis:
#         deprecated[api] = ratio
#         # print(api)
#     # else:
#     #     print(api)
#
# # deprecated["adyen.com_MarketPayNotificationService"] = 0.142857143
# for api in apis:
#     if api not in apis_all:
#         print(api)
# print(deprecated)
# print(len(deprecated))

# with open('result/chart/rq1-deprecated-bh.csv', mode='w', encoding="utf-8") as res_file:
#     res_writer = csv.writer(res_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
#     res_writer.writerow(["api", "Ratio"])
#
#     for api in deprecated:
#         res_writer.writerow([api, deprecated[api]])

def read(filename, row_num):
    with open(filename, mode='r', encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        apis = []
        for row in csv_reader:
            if line_count > 0:
                api = row[row_num]
                apis.append(api)

            line_count += 1

    return apis
#
# # ratios = read('result/chart/rq2.csv', 2)
ratios = read('result/chart/rq3.csv', 3) #alt
# ratios = read('result/chart/time.csv', 3)
#
count_ratio_0 = 0
count_ratio_100 = 0
count_ratio_25 = 0
count_ratio_50 = 0
count_ratio_75 = 0
count_last = 0


print(len(ratios))
for ratio in ratios:
    ratio = float(ratio)
    if ratio == 0:
        count_ratio_0 = count_ratio_0 + 1
    if 0 < ratio < 0.25:
        count_ratio_25 = count_ratio_25 + 1
    if 0.25 <= ratio < 0.5:
        count_ratio_50 = count_ratio_50 + 1
    if 0.5 <= ratio < 0.75:
        count_ratio_75 = count_ratio_75 + 1
    if 0.75 <= ratio < 1:
        count_ratio_100 = count_ratio_100 + 1
    if ratio == 1:
        count_last = count_last + 1


print(count_ratio_0)
print(count_ratio_25)
print(count_ratio_50)
print(count_ratio_75)
print(count_ratio_100)
print(count_last)

#
# with open('result/chart/time-barchart.csv', mode='w', encoding="utf-8") as res_file:
#     res_writer = csv.writer(res_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
#     res_writer.writerow(["Range", "Count"])
#     if count_ratio_0 != 0:
#         res_writer.writerow(["(0, 0)", count_ratio_0])
#     res_writer.writerow(["(0, 0.25)", count_ratio_25])
#     res_writer.writerow(["(0.25, 0.5))", count_ratio_50])
#     res_writer.writerow(["(0.5, 0.75)", count_ratio_75])
#     res_writer.writerow(["(0.75, 1)", count_ratio_100])
#     res_writer.writerow(["1", count_last])
#
