from natsort import natsorted, ns
import csv
from packaging import version


# Retrieve multi versions files, arrange it api specific, and sort them
# sorted_values = natsorted(['v1', 'v1.1'])
# print(sorted_values)

def getApiName(split_path):
    path = split_path[:-2]
    path = path[1:]
    path_unique = ("_").join(path)

    if path_unique == "googleapis.com_admin":
        path_unique = path_unique + split_path[-2]

    return path_unique


def read(filename):
    with open(filename, mode='r', encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        apis = []
        for row in csv_reader:
            if line_count > 0:
                api = row[0].replace("\\", "/")
                apis.append(api)

            line_count += 1
        # print(f'Processed {line_count} lines.')
    # print(len(list(set(apis))))
    return list(set(apis))


names = read("result/dataset/dataset_file.csv")

results = {}
for file_location in names:
    api_unique = getApiName(file_location.split("/"))
    if api_unique in results:
        value = results[api_unique]
        results[api_unique] = [file_location] + value
    else:
        results[api_unique] = [file_location]

sorted_results = {}
for result in results:
    values = results[result]
    if len(values) > 1:
        sorted_values = natsorted(values)
        versions = []
        version_files = {}
        sorted_version_files = []
        for val in values:
            version_split = val.split("/")
            version = version_split[len(version_split) - 2]
            version_files[version] = val
            versions.append(version)
        sorted_by_version = natsorted(versions)

        for version_sorted in sorted_by_version:
            sorted_version_files.append(version_files[version_sorted])
        sorted_results[result] = sorted_version_files

diff_prev = read("result/RQ1/from_ruby_text_prev.csv")
names_deprecated = read("result/RQ1/deprecated_file.csv")
deprecated_bk_changes_prev_api = []
false_prev_api = []
files = []
deprecated_organization = {}
non_deprecated_organization = {}

deprecated_organization_api = {}
non_deprecated_organization_api = {}

for file in diff_prev:
    api_name = getApiName(file.split("/"))
    false_prev_api.append(api_name)
    api_unique = getApiName(file.split("/"))
    organization_split = api_unique.split("_")
    organization = organization_split[0]
    if file in names_deprecated:
        files.append(file)

        deprecated_bk_changes_prev_api.append(api_unique)

        if organization in deprecated_organization:
            values = deprecated_organization[organization]
            deprecated_organization[organization] = values + [file]
        else:
            deprecated_organization[organization] = [file]
        if organization in deprecated_organization_api:
            values = deprecated_organization_api[organization]
            deprecated_organization_api[organization] = values + [api_unique]
        else:
            deprecated_organization_api[organization] = [api_unique]
    else:
        if organization in non_deprecated_organization:
            values = non_deprecated_organization[organization]
            non_deprecated_organization[organization] = values + [file]
        else:
            non_deprecated_organization[organization] = [file]

        if organization in non_deprecated_organization_api:
            values = non_deprecated_organization_api[organization]
            non_deprecated_organization_api[organization] = values + [api_unique]
        else:
            non_deprecated_organization_api[organization] = [api_unique]

orgs = []
cnt = 0
for org in deprecated_organization_api:
    print(org)
    # cnt = cnt + (len(list(set(deprecated_organization_api[org]))))
    orgs.append(org)
    print(len(list(set(deprecated_organization_api[org]))))
    if "google" in org:
        print(list(set(deprecated_organization_api[org])))

print("================================================")

for org in non_deprecated_organization_api:
    print(org)
    print(non_deprecated_organization_api[org])
    orgs.append(org)
    print(len(list(set(non_deprecated_organization_api[org]))))

print(len(list(set(orgs))))
print((list(set(orgs))))
print("================================================")

print(len(list(set(deprecated_bk_changes_prev_api))))
print(len(list(set(false_prev_api))))
print(len(list(set(files))))

# 20 common for openapi 2, another is openapi 3(marketplace)
true_files = read("result/RQ1/true_ruby.csv")

print(len(list(set(true_files))))

false_files = read("result/RQ1/false_ruby.csv")

print(len(list(set(false_files))))

all_files = true_files + false_files
print(len(list(set(all_files))))

api_names = []
for file in list(set(all_files)):
    api_unique = getApiName(file.split("/"))
    api_names.append(api_unique)

# print(list(set(api_names)))
print(len(list(set(api_names))))

api_names = []
for file in list(set(false_files)):
    api_unique = getApiName(file.split("/"))
    api_names.append(api_unique)

# print(list(set(api_names)))
print(len(list(set(api_names))))

false_apis = list(set(api_names))
print(len(list(set(false_apis))))
print((list(set(false_apis))))

print("testing")

api_names = []
for file in list(set(true_files)):
    api_unique = getApiName(file.split("/"))
    api_names.append(api_unique)

# print(list(set(api_names)))
print(len(list(set(api_names))))
print((list(set(api_names))))
count = 0

for api in list(set(api_names)):
    if api in false_apis:
        count = count + 1

print(count)

# multi_deprecated_files =
api_names_from_multi_deprecated = []
api_info_multi_deprecated = {}
with open("result/RQ1/deprecated_multi.csv", mode='r', encoding="utf-8") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    apis = []
    for row in csv_reader:
        if line_count > 0:
            apis_deprecated = row[4].split(", ")
            api_name_deprecated = row[0]
            api_names_from_multi_deprecated.append(api_name_deprecated)
            api_info_multi_deprecated[api_name_deprecated] = {"org": row[1], "standard_files": row[2], "st_file_count": row[3],
                                                              "deprecated_files": row[4], "count_deprecated_files": row[5]}
            for api in apis_deprecated:
                apis.append(api)

        line_count += 1

files_prev = read("result/RQ1/from_ruby_text_prev_deprecated.csv")

deprecated_files = read("result/RQ1/deprecated_file.csv")
deprecated_prev = []
non_deprecated_prev = []
prev_files_breaking_changes = {}

for file in files_prev:
    api_name = getApiName(file.split("/"))
    if api_name in prev_files_breaking_changes:
        values = prev_files_breaking_changes[api_name]
        prev_files_breaking_changes[api_name] = values + [file]
    else:
        prev_files_breaking_changes[api_name] = [file]

    if file in deprecated_files:
        deprecated_prev.append(api_name)
    else:
        non_deprecated_prev.append(api_name)

print("=============================================================")
# print(prev_files_breaking_changes)

print("-----------------------------------------------------")
prev_files_breaking_changes_from_deprecated = {}
print(api_names_from_multi_deprecated)
print(len(api_names_from_multi_deprecated))
for api_name in prev_files_breaking_changes:
    if api_name in api_names_from_multi_deprecated:
        if api_name in prev_files_breaking_changes_from_deprecated:
            values = prev_files_breaking_changes_from_deprecated[api_name]
            prev_files_breaking_changes_from_deprecated[api_name] = values + prev_files_breaking_changes[api_name]
        else:
            prev_files_breaking_changes_from_deprecated[api_name] = prev_files_breaking_changes[api_name]

# with open('result/RQ1/breaking_changes_in_deprecated_list.csv', mode='w', encoding="utf-8") as res_file:
#     res_writer = csv.writer(res_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
#     res_writer.writerow(["api", "organization", "all standard files", "count standard files", "File having deprecated", "count of deprecated files", "breaking changes prev files","count breaking files prev", "follower files", "count_follower"])
#     for api_name in prev_files_breaking_changes_from_deprecated:
#         breaking_changes_files_count = len(prev_files_breaking_changes_from_deprecated[api_name])
#         files = prev_files_breaking_changes_from_deprecated[api_name]
#         files = list(set(files))
#         count_follow = 0
#         files_follow = []
#         for file in files:
#             if file in deprecated_files:
#                 count_follow = count_follow + 1
#                 files_follow.append(file)
#         print(len(files))
#         res_writer.writerow([api_name, api_info_multi_deprecated[api_name]["org"], api_info_multi_deprecated[api_name]["standard_files"],
#                              api_info_multi_deprecated[api_name]["st_file_count"], api_info_multi_deprecated[api_name]["deprecated_files"],
#                              api_info_multi_deprecated[api_name]["count_deprecated_files"],
#                              files, len(files), files_follow, len(list(set(files_follow)))
#                              ])

deprecated_follow_information = {}


# api_info_multi_deprecated[api_name_deprecated] = {"org": row[1], "standard_files": row[2], "st_file_count": row[3],
#                                                               "deprecated_files": row[4], "count_deprecated_files": row[5]}



deprecated_prev = (list(set(deprecated_prev)))
non_deprecated_prev = (list(set(non_deprecated_prev)))

print(len(list(set(deprecated_prev))))
print(len(list(set(non_deprecated_prev))))


apis_always_depre = []
apis_mixed = []


for api in deprecated_prev:
    if api not in non_deprecated_prev:
        # print(api)
        apis_always_depre.append(api)
    else:
        apis_mixed.append(api)

apis_always_not = []
for apis in non_deprecated_prev:
    if api not in deprecated_prev:
        apis_always_not.append(api)


print(len(list(set(apis_always_depre))))
print(len(list(set(apis_mixed))))
print("mixed")
print((list(set(apis_mixed))))
print(len(list(set(apis_always_not))))

print(len(apis_always_depre))  # 16
print(len(apis_mixed))  # 4
