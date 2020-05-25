import os
from bs4 import BeautifulSoup
import yaml
import csv

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "My Project-c2d2a74eea9a.json"

# directory = "APIs/whatsapp.local/1.0/openapi.yaml"
# directory = "APIs/beezup.com/2.0"
directory = "APIs"
# directory = "APIs/azure.com/sql-deprecated/2014-04-01/swagger.yaml"

count = 0
methods = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']

# folderlist = os.walk(directory)
api_list = []
indexByAPI = {}

results_depr = []
count_results_replace = []
file_replace_mentioned = []

# deprecated csv is the distinct files
def read(filename = "result/RQ1/deprecated_onefile_manual.csv"):

    with open(filename, mode='r', encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 1
        apis = []
        for row in csv_reader:
            if line_count > 1:
                api = row[0].replace("\\", "/")
                apis.append(api)

            line_count += 1

    return list(set(apis))


def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '\\')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '\\')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out


def getApiName(split_path):
    path = split_path[:-2]
    path = path[1:]
    path_unique = ("_").join(path)

    if path_unique == "googleapis.com_admin":
        path_unique = path_unique + split_path[-2]

    return path_unique
# OpenAPI 3.0 supports get, post, put, patch, delete, head, options, and trace


def checkPathOpenApi():
    apis = read()

    # apis = ['APIs/kubernetes.io/v1.17.0/swagger.yaml']
    # apis = ['APIs/jira.local/1.0.0/swagger.yaml']
    result_deprecated_in_path = {}
    count_result_deprecated_in_operation = {}
    result_all_path = {}
    result_count_all_operation = {}
    endpoints_api = {}
    count_endpoints_api = {}
    deprecated_descriptions_api = {}

    count_method_info = {}
    for api in apis:
        deprecated_path_with_operation = []
        deprecated_descriptions = {}

        # check if this is in deprecated_lists
        with open(api, 'r', encoding="utf-8") as stream:
            path_flatten_values = []
            all_paths = []
            endpointswithoutmethods = []

            try:
                data = yaml.safe_load(stream)
                paths = data["paths"]
                path_flatten_values = flatten_json(paths)
            except yaml.YAMLError as exc:
                print(exc)
            for path in path_flatten_values:

                splitted_values = path.split("\\")
                endpoint = splitted_values[0]
                method = splitted_values[1]

                value = path_flatten_values[path]
                path_with_operation = endpoint + "_" + method
                endpointswithoutmethods.append(endpoint)

                # this block is for direct deprecated path
                if method in methods:  # this is for direct path
                    if path_with_operation not in all_paths:  # all endpoints with operation
                        all_paths.append(path_with_operation)
                    deprecation_check_in = splitted_values[2].lower()
                    checkDescription(deprecation_check_in, path_with_operation, value,
                                                        deprecated_path_with_operation, deprecated_descriptions)

        count_get = 0
        count_post = 0
        count_put = 0
        count_delete = 0
        count_patch = 0
        count_head = 0
        count_options = 0
        count_trace = 0

        # print(descriptions_operation)
        unique_desc = list(set(deprecated_path_with_operation))

        # for operation in descriptions_operation:
        for each_operation in unique_desc:
            method_name_split = each_operation.split("_")
            method_name = method_name_split[len(method_name_split) - 1]
            if method_name == "get":
                count_get = count_get + 1
            if method_name == "post":
                count_post = count_post + 1
            if method_name == "put":
                count_put = count_put + 1
            if method_name == "delete":
                count_delete = count_delete + 1
            if method_name == "patch":
                count_patch = count_patch + 1
            if method_name == "head":
                count_head = count_head + 1
            if method_name == "options":
                count_options = count_options + 1
            if method_name == "trace":
                count_trace = count_trace + 1

        result_deprecated_in_path[api] = list(set(deprecated_path_with_operation))
        count_result_deprecated_in_operation[api] = len(list(set(deprecated_path_with_operation)))
        result_all_path[api] = list(set(all_paths))  # with operation
        result_count_all_operation[api] = len(list(set(all_paths)))  # with operation
        endpoints_api[api] = list(set(endpointswithoutmethods))
        count_endpoints_api[api] = len(list(set(endpointswithoutmethods)))
        deprecated_descriptions_api[api] = deprecated_descriptions
        count_method_info[api] = {"count_get": count_get, "count_post": count_post,
                                          "count_put": count_put, "count_delete": count_delete, "count_patch": count_patch, "count_head": count_head,
                                          "count_options": count_options, "count_trace": count_trace}


    print(result_count_all_operation)
    print(count_result_deprecated_in_operation)
    # print(deprecated_descriptions_api[api])
    
    
    with open('result/RQ2/deprecated_operation.csv', mode='w') as res_file:
        res_writer = csv.writer(res_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
        res_writer.writerow(["api_name", "count all operation", "count deprecated operation",
                             "count_get", "count_post", "count_put", "count_delete",
                             "count_patch", "count_head", "count_options", "count_trace"])
        for api_file in count_result_deprecated_in_operation:
            api_name = getApiName(api_file.split("/"))
            res_writer.writerow([api_name, result_count_all_operation[api_file], count_result_deprecated_in_operation[api_file],
                                 count_method_info[api_file]["count_get"],
                                 count_method_info[api_file]["count_post"],
                                 count_method_info[api_file]["count_put"],
                                 count_method_info[api_file]["count_delete"],
                                 count_method_info[api_file]["count_patch"],
                                 count_method_info[api_file]["count_head"],
                                 count_method_info[api_file]["count_options"],
                                 count_method_info[api_file]["count_trace"]

                                 ])

    print(len(deprecated_descriptions_api))
    with open('result/RQ2/deprecated_operation_descriptions.csv', mode='w') as res_file:
        res_writer = csv.writer(res_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
        res_writer.writerow(["api_name", "operation", "description", "operation count for api", "description count"])
        for api_file in deprecated_descriptions_api:
            api_name = getApiName(api_file.split("/"))
            descriptions = deprecated_descriptions_api[api_file]
            for operation in descriptions:
                desc = list(set(descriptions[operation]))
                res_writer.writerow(
                    [api_name, operation, desc, len(descriptions), len(desc)]) #@todo is it possible to get multiple sentences

    return count_result_deprecated_in_operation


descriptions_text = read("result/RQ1/text_and_file.csv")
def checkDescription(key_to_check, path_with_operation, value, result, deprecated_descriptions):
    # if key_to_check == "summary":
    #     if text_value in descriptions_text:
    #         result.append(path_with_operation)
    #         if path_with_operation in deprecated_descriptions:
    #             value_desc = deprecated_descriptions[path_with_operation]
    #             deprecated_descriptions[path_with_operation] = [value] + value_desc
    #
    #         else:
    #             deprecated_descriptions[path_with_operation] = [value]

    if key_to_check == "description" or key_to_check == "summary":
        if value:
            text_value = value.lower()
            text_value = " ".join(text_value.split())

            if text_value in descriptions_text:
                result.append(path_with_operation)
                if path_with_operation in deprecated_descriptions:
                    value_desc = deprecated_descriptions[path_with_operation]
                    deprecated_descriptions[path_with_operation] = [value] + value_desc

                else:
                    deprecated_descriptions[path_with_operation] = [value]


    if "deprecated" in key_to_check.lower():
        if bool(value):
            result.append(path_with_operation)

    # return result

# checkPathOpenApi()


def countMethods():
    results = {}
    apis = read()

    for api in apis:

        with open(api, 'r', encoding="utf-8") as stream:
            path_flatten_values = []
            all_paths = []
            endpointswithoutmethods = []

            try:
                data = yaml.safe_load(stream)
                paths = data["paths"]
                path_flatten_values = flatten_json(paths)
            except yaml.YAMLError as exc:
                print(exc)
            for path in path_flatten_values:

                splitted_values = path.split("\\")
                endpoint = splitted_values[0]
                method = splitted_values[1]

                value = path_flatten_values[path]
                path_with_operation = endpoint + "_" + method
                endpointswithoutmethods.append(endpoint)

                # this block is for direct deprecated path
                if method in methods:  # this is for direct path
                    if path_with_operation not in all_paths:  # all endpoints with operation
                        all_paths.append(path_with_operation)

            count_get = 0
            count_post = 0
            count_put = 0
            count_delete = 0
            count_patch = 0
            count_head = 0
            count_options = 0
            count_trace = 0

            for each_operation in all_paths:
                method_name_split = each_operation.split("_")
                method_name = method_name_split[len(method_name_split) - 1]
                if method_name == "get":
                    count_get = count_get + 1
                if method_name == "post":
                    count_post = count_post + 1
                if method_name == "put":
                    count_put = count_put + 1
                if method_name == "delete":
                    count_delete = count_delete + 1
                if method_name == "patch":
                    count_patch = count_patch + 1
                if method_name == "head":
                    count_head = count_head + 1
                if method_name == "options":
                    count_options = count_options + 1
                if method_name == "trace":
                    count_trace = count_trace + 1

            results[api] = {"total": len(all_paths), "count_get": count_get, "count_post": count_post,
                            "count_put": count_put, "count_delete": count_delete, "count_patch": count_patch,
                            "count_head": count_head,
                            "count_options": count_options, "count_trace": count_trace}

    with open('result/RQ2/total_operation_methods.csv', mode='w') as res_file:
        res_writer = csv.writer(res_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL,
                                lineterminator="\n")
        res_writer.writerow(["api_name", "count all operation",
                             "total_get", "total_post", "total_put", "total_delete",
                             "total_patch", "total_head", "total_options", "total_trace"])
        for api_file in results:
            api_name = getApiName(api_file.split("/"))
            res_writer.writerow(
                [api_name, results[api_file]["total"],
                 results[api_file]["count_get"],
                 results[api_file]["count_post"],
                 results[api_file]["count_put"],
                 results[api_file]["count_delete"],
                 results[api_file]["count_patch"],
                 results[api_file]["count_head"],
                 results[api_file]["count_options"],
                 results[api_file]["count_trace"]
                 ])


# checkPathOpenApi()
# countMethods()




results = {}

def getTotalOperations():
    apis = read('result/chart/rq1_bh_deprecated.csv')
    for api in apis:
        with open(api, 'r', encoding="utf-8") as stream:
            path_flatten_values = []
            all_paths = []
            endpointswithoutmethods = []

            try:
                data = yaml.safe_load(stream)
                paths = data["paths"]
                path_flatten_values = flatten_json(paths)
            except yaml.YAMLError as exc:
                print(exc)
            for path in path_flatten_values:

                splitted_values = path.split("\\")
                endpoint = splitted_values[0]
                method = splitted_values[1]

                value = path_flatten_values[path]
                path_with_operation = endpoint + "_" + method
                endpointswithoutmethods.append(endpoint)

                # this block is for direct deprecated path
                if method in methods:  # this is for direct path
                    if path_with_operation not in all_paths:  # all endpoints with operation
                        all_paths.append(path_with_operation)

            results[api] = len(list(set(all_paths)))

    with open('result/chart/rq1_bh_deprecated_operations_total.csv', mode='w', encoding="utf-8") as res_file:
        res_writer = csv.writer(res_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
        res_writer.writerow(["File", "TotalOp"])
        for api in results:
            res_writer.writerow([api, results[api]])

getTotalOperations()

