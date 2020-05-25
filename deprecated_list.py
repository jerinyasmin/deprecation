import os
from shutil import copyfile
import csv


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

apis = read("result/RQ1/deprecated_onefile_manual.csv")
directory = "APIs"

folderlist = os.walk(directory)
result = {}
endpoint_deprecated_api = {}

for f in folderlist:
    for fs in f[2]:
        file_location = f[0] + "/" + fs
        file_location = file_location.replace("\\", '/')
        api_name = getApiName(file_location.split("/"))

        if ("swagger" in fs or "openapi" in fs) and file_location in apis:
            dst = "result/testing/" + api_name + "_" + fs
            copyfile(file_location, dst)