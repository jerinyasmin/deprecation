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
results = {}

results_depr = []
count_results_replace = []
file_replace_mentioned = []


# deprecated csv is the distinct files
def getApiName(split_path):
    path = split_path[:-2]
    path = path[1:]
    path_unique = ("_").join(path)

    if path_unique == "googleapis.com_admin":
        path_unique = path_unique + split_path[-2]

    return path_unique


def read(filename="result/RQ1/deprecated_onefile_manual.csv"):
    # filename = "result/RQ1/deprecated_onefile_manual.csv"
    with open(filename, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 1
        apis = []
        for row in csv_reader:
            if line_count > 1:
                api = row[0].replace("\\", "/")
                # if api != "APIs/googleapis.com/tasks/v1/swagger.yaml":
                apis.append(api)

            line_count += 1

    return list(set(apis))

descriptions_text = read("result/RQ1/text_and_file.csv")
# print(descriptions_text)


def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + "\\")
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + "\\")
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out


def find_descriptions(ref, definitions_list):
    descriptions = []
    keys = []

    def find_desc(key):
        keys.append(key)
        for definition in definitions_list:
            if (definition.startswith(key) and definition.endswith("$ref")):
                val = definitions_list[definition]
                ref = val.split("/")[-1]
                # print(ref) check cyclic references
                if key != ref and ref not in keys:
                    find_desc(ref)
            elif (definition.startswith(key) and definition.endswith("description")) or (
                    definition.startswith(key) and definition.endswith("summary")):
                #
                # print(definition)
                desc = definitions_list[definition]
                if bool(desc):
                    desc = " ".join(desc.lower().split())
                    # print(desc)

                    if desc in descriptions_text:
                        # print(desc)
                        descriptions.append(definitions_list[definition])
            else:
                pass

    find_desc(ref)
    # print(descriptions) check

    return descriptions


def find_key_deprecated(ref, definitions_list):
    descriptions = []
    keys = []

    def find_desc(key):
        keys.append(key)
        # print(key)
        for definition in definitions_list:
            if (definition.startswith(key) and definition.endswith("$ref")):
                val = definitions_list[definition]
                ref = val.split("/")[-1]
                # print(ref)
                if key != ref and ref not in keys:
                    find_desc(ref)
            elif definition.startswith(key) and definition.endswith("deprecated"):
                # print("depr:definition")
                desc = definitions_list[definition]
                if bool(desc):
                    # print(desc)
                    descriptions.append(definitions_list[definition])
            else:
                pass

    find_desc(ref)
    # print(descriptions) check
    ln = 0
    if len(descriptions) > 0:
        return True

    # print(ln)
    return False



def generateResponse():
    apis = read()
    # apis = ['APIs/nba.com/1.0.0/swagger.yaml']

    # apis = ['APIs/docker.com/engine/1.33/swagger.yaml']

    # apis = ['APIs/kubernetes.io/v1.17.0/swagger.yaml']
    # apis = ['APIs/amazonaws.com/cognito-idp/2016-04-18/swagger.yaml']
    # apis = ['APIs/amazonaws.com/cloudtrail/2013-11-01/swagger.yaml']
    # apis = ['APIs/googleapis.com/genomics/v1/swagger.yaml']
    # apis = ['APIs/amazonaws.com/apigateway/2015-07-09/swagger.yaml']
    # apis = ['APIs/googleapis.com/reseller/v1/swagger.yaml']
    # apis = ['APIs/amazonaws.com/cloudfront/2018-11-05/swagger.yaml']
    # apis = ['APIs/amazonaws.com/guardduty/2017-11-28/swagger.yaml']#cyclic

    res_endpoint_resp = {}
    res_desc_per_file = {}
    res_effected_endpoint = {}
    res_effected_endpoint_ln = {}
    deprecated_descriptions_api = {}

    for api in apis:
        # print(api)
        file_location = api
        # definitions = []
        res_desc_depr = []
        req_param_deprecated = []
        descriptions_operation = {}

        with open(api, 'r', encoding="utf-8") as stream:
            try:
                st = yaml.safe_load(stream)
                if "definitions" in st and "components" in st:
                    print("both")
                if "definitions" in st:
                    definitions = (flatten_json(st["definitions"]))

                elif "components" in st:
                    components_values = st["components"]
                    if "schemas" in components_values:
                        definitions = (flatten_json(st["components"]["schemas"]))  # todo
                    if "responses" in components_values:
                        values = (flatten_json(st["components"]["responses"]))  # todo
                        definitions = {**values, **definitions}

                    if "headers" in components_values:
                        values = (flatten_json(st["components"]["headers"]))  # todo
                        definitions = {**values, **definitions}

                if "responses" in st:
                    responses = (flatten_json(st["responses"]))
                    definitions = {**responses, **definitions}

                    # print('Dictionary 3 :')
                    # print(definitions)
                    # print(definitions)
                    # definitions = definitions.update(params)
                    # print(params)
                cnt = 0
                paths = st["paths"]
                path_flatten_values = flatten_json(paths)
                operation_in_endpoint = {}
                for path in path_flatten_values:
                    splitted_values = path.split("\\")
                    endpoint = splitted_values[0]
                    method = splitted_values[1]
                    if method in methods:
                        operation_api = endpoint + "_" + method
                        if endpoint in operation_in_endpoint:
                            values = operation_in_endpoint[endpoint]
                            operation_in_endpoint[endpoint] = values + [operation_api]
                        else:
                            operation_in_endpoint[endpoint] = [operation_api]

                response_refs = []
                endperref = {}
                name_req_params = {}
                for endpoint in paths:
                    endpoint_info = paths[endpoint]
                    value_ref = []

                    for reqtype in endpoint_info:
                        if reqtype != "parameters" and reqtype in methods:  # get / post
                            operation = endpoint + "_" + reqtype
                            values = endpoint_info[reqtype]
                            for value in values:
                                if value == "responses":
                                    code_values = values[value]
                                    for code in code_values:
                                        flat_values = flatten_json(code_values[code])
                                        for key_v in flat_values:
                                            if key_v.endswith("deprecated"):
                                                is_depr = flat_values[key_v]
                                                if is_depr:
                                                    print(api)
                                                    print(is_depr)
                                                    print((key_v))
                                                    print(key_v)
                                                    cnt += 1
                                                    res_desc_depr.append(operation)
                                            if key_v.endswith("description") or key_v.endswith("summary"):
                                                desc = flat_values[key_v]
                                                if bool(desc):
                                                    desc = " ".join(desc.lower().split())
                                                    if desc in descriptions_text:
                                                        print(api)
                                                        print(desc)
                                                        print(key_v)

                                                        res_desc_depr.append(operation)
                                                        if desc.lower() in descriptions_operation:
                                                            values = descriptions_operation[operation]
                                                            descriptions_operation[operation] = values + [desc.lower()]
                                                        else:
                                                            descriptions_operation[operation] = [desc.lower()]

                                            if key_v.endswith("$ref"):
                                                value_ref = flat_values[key_v]
                                                if value_ref:
                                                    # ref = p_vals["$ref"]
                                                    refer = value_ref.split("/")

                                                    response_refs.append(refer[-1])
                                                    # print(response_refs)
                                                    if refer[-1] in endperref:
                                                        prev = endperref[refer[-1]]
                                                        endperref[refer[-1]] = prev + [operation]
                                                    else:
                                                        endperref[refer[-1]] = [operation]

                ln = 0
                res = res_desc_depr
                refs = []
                list_ref_related = {}
                # print(endperref)
                # print(definitions)
                for ref in list(set(response_refs)):
                    descriptions_ref = find_descriptions(ref, definitions)
                    # print(descriptions_ref)
                    in_key = find_key_deprecated(ref, definitions)
                    # ln += int(len(descriptions_ref))

                    if len(descriptions_ref) or in_key:
                        res = res + (endperref[ref])  # @todo description
                        refs.append(ref)

                    # @todo: check
                    if len(descriptions_ref):
                        for op in endperref[ref]:
                            for desc in descriptions_ref:
                                if desc.lower() in descriptions_operation:
                                    values = descriptions_operation[op]
                                    descriptions_operation[op] = values + [desc.lower()]
                                else:
                                    descriptions_operation[op] = [desc.lower()]

                list_ref_related[file_location] = refs
                # print(file_location)
                unique_operations_deprecated = list(set(res))

                count_get = 0
                count_post = 0
                count_put = 0
                count_delete = 0
                count_patch = 0
                count_head = 0
                count_options = 0
                count_trace = 0

                # print(descriptions_operation)

                # for operation in descriptions_operation:
                for each_operation in unique_operations_deprecated:
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

                res_effected_endpoint_ln[file_location] = len(unique_operations_deprecated)
                # print(res_effected_endpoint_ln[file_location])
                res_effected_endpoint[file_location] = unique_operations_deprecated

                results[file_location] = {"count_operation_deprecated": len(unique_operations_deprecated),
                                          "count_get": count_get, "count_post": count_post,
                                          "count_put": count_put, "count_delete": count_delete,
                                          "count_patch": count_patch, "count_head": count_head,
                                          "count_options": count_options, "count_trace": count_trace,
                                          "description operations": descriptions_operation}

                deprecated_descriptions_api[file_location] = descriptions_operation
            except yaml.YAMLError as exc:
                print(exc)

    # print(results)
    # print(deprecated_descriptions_api)

    # with open('result/RQ2/deprecated_operation_response.csv', mode='w') as res_file:
    #
    #     res_writer = csv.writer(res_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
    #     res_writer.writerow(["api_name", "count deprecated operation",
    #                          "count_get", "count_post", "count_put", "count_delete",
    #                          "count_patch", "count_head", "count_options", "count_trace"])
    #     for api_file in results:
    #         api_name = getApiName(api_file.split("/"))
    #         res_writer.writerow(
    #             [api_name, results[api_file]["count_operation_deprecated"],
    #              results[api_file]["count_get"],
    #              results[api_file]["count_post"],
    #              results[api_file]["count_put"],
    #              results[api_file]["count_delete"],
    #              results[api_file]["count_patch"],
    #              results[api_file]["count_head"],
    #              results[api_file]["count_options"],
    #              results[api_file]["count_trace"]
    #              ])
    #
    # with open('result/RQ2/deprecated_operation_descriptions_response.csv', mode='w') as res_file:
    #     res_writer = csv.writer(res_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
    #     res_writer.writerow(["api_name", "operation", "description", "operation count for api", "description count"])
    #     for api_file in deprecated_descriptions_api:
    #         api_name = getApiName(api_file.split("/"))
    #         descriptions = deprecated_descriptions_api[api_file]  # len is the count of impacted operation
    #         for operation in descriptions:
    #             desc = list(set(descriptions[operation]))
    #             res_writer.writerow(
    #                 [api_name, operation, desc, len(descriptions),
    #                  len(desc)])  # @todo is it possible to get multiple sentences


# OpenAPI 2.0                    OpenAPI 3.0
# '#/definitions/User'         → '#/components/schemas/User'
# '#/parameters/offsetParam'   → '#/components/parameters/offsetParam'
# '#/responses/ErrorResponse'  → '#/components/responses/ErrorResponse' @todo

generateResponse()




def generateResponsePrev():
    res_endpoint_resp = {}
    # apis = read()
    # apis = ['APIs/kubernetes.io/v1.17.0/swagger.yaml']
    # apis = ['APIs/bungie.net/2.0.0/swagger.yaml']
    apis = ['APIs/getgo.com/gotowebinar/1.0.0/swagger.yaml']
    apis = ['APIs/googleapis.com/dialogflow/v2/swagger.yaml']
    apis = ['APIs/nba.com/1.0.0/swagger.yaml']

    res_desc_per_file = {}
    res_effected_endpoint = {}
    res_effected_endpoint_ln = {}
    for api in apis:
        definitions = []
        res_desc_depr = []
        descriptions_operation = {}

        file_location = api
        with open(api, 'r', encoding="utf-8") as stream:
            try:
                st = yaml.safe_load(stream)
                if "definitions" in st and "components" in st:
                    print("both")
                if "definitions" in st:
                    definitions = (flatten_json(st["definitions"]))
                elif "components" in st:
                    components_values = st["components"]
                    if "schemas" in components_values:
                        definitions = (flatten_json(st["components"]["schemas"]))  # todo
                    else:
                        definitions = (flatten_json(st["components"]))  # todo

                cnt = 0
                paths = st["paths"]
                response_refs = []
                endperref = {}
                for endpoint in paths:
                    # if endpoint == '/api/v1/namespaces/{namespace}/replicationcontrollers/{name}':
                    value_ref = []
                    endpoint_info = paths[endpoint]
                    for reqtype in endpoint_info:
                        if reqtype != "parameters" and reqtype in methods:

                            operation = endpoint + "_" + reqtype
                            values = endpoint_info[reqtype]
                            for value in values:
                                if value == "responses":
                                    code_values = values[value]
                                    for code in code_values:
                                        pairs_value = code_values[code]
                                        for val in pairs_value:
                                            if val == "deprecated":
                                                is_depr = pairs_value["deprecated"]
                                                if is_depr:
                                                    cnt += 1
                                                    res_desc_depr.append(endpoint)
                                            if val == "description" or val == "summary":
                                                desc = pairs_value[val]
                                                if bool(desc) and desc.lower() in descriptions_text:
                                                    cnt += 1
                                                    # req_param_deprecated.append(pairs_value["name"])
                                                    res_desc_depr.append(operation)
                                                    if desc.lower() in descriptions_operation:
                                                        values = descriptions_operation[operation]
                                                        descriptions_operation[operation] = values + [desc.lower()]
                                                    else:
                                                        descriptions_operation[operation] = [desc.lower()]
                                                # check if deprecated
                                            elif val == "schema":
                                                p_vals = pairs_value["schema"]
                                                p_vals = flatten_json(p_vals)
                                                # print(p_vals)
                                                for p_val in p_vals:
                                                    if p_val.endswith("$ref"):
                                                        ref = p_vals[p_val]
                                                        refer = ref.split("/")
                                                        response_refs.append(refer[-1])
                                                        if refer[-1] in endperref:
                                                            prev = endperref[refer[-1]]
                                                            endperref[refer[-1]] = prev + [operation]
                                                        else:
                                                            endperref[refer[-1]] = [operation]
                                            elif val == "content":
                                                flat_values = flatten_json(pairs_value["content"])
                                                for key_v in flat_values:
                                                    if key_v.endswith("$ref"):
                                                        value_ref = flat_values[key_v]
                                                if value_ref:
                                                    refer = value_ref.split("/")
                                                    response_refs.append(refer[-1])
                                                    if refer[-1] in endperref:
                                                        prev = endperref[refer[-1]]
                                                        endperref[refer[-1]] = prev + [operation]
                                                    else:
                                                        endperref[refer[-1]] = [operation]

                ln = 0
                res = res_desc_depr
                refs = []
                list_ref_related = {}
                per_req_endpoints = {}
                # print(endperref)

                for ref in list(set(response_refs)):
                    # ln += int(find_descriptions(ref, definitions))
                    if find_descriptions(ref, definitions):
                        res = res + (endperref[ref])
                        refs.append(ref)
                    per_req_endpoints[ref] = list(set(res))

                res_endpoint_resp[file_location] = ln + cnt
                res_desc_per_file[file_location] = cnt

                list_ref_related[file_location] = refs

                res_effected_endpoint_ln[file_location] = len(list(set(res)))
                res_effected_endpoint[file_location] = (list(set(res)))
            except yaml.YAMLError as exc:
                print(exc)

    print(res_effected_endpoint_ln)
    return res_effected_endpoint_ln
