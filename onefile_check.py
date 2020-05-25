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
names = read("result/RQ1/deprecated_file.csv")

results = {}
for file_location in names:
    api_unique = getApiName(file_location.split("/"))
    if api_unique in results:
        value = results[api_unique]
        results[api_unique] = [file_location] + value
    else:
        results[api_unique] = [file_location]

sorted_results = {}
one_file = []
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
    else:
        one_file.append("".join(values))


for api in sorted_results:
    files = sorted_results[api]
    last_file = files[len(files) - 1]
    one_file.append(last_file)
print(len(sorted_results))
# print((sorted_results))


print(len(one_file))
# print((one_file))
# for api in sorted_results:
#     print(sorted_results[api])


names_deprecated = read("result/RQ1/deprecated_onefile_manual.csv")
deprecated_bk_changes_prev_api = []
count = 0
for name in names_deprecated:
    if name not in one_file:
        print(name)
        count = count + 1

print(count)