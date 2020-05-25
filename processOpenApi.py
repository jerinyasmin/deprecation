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


def generateApi():
    folderlist = os.walk(directory)
    res = {}

    def iterdict(d, version, file_location):
        files = []
        count = 0
        countKey = 0
        count_replace = 0
        # print(file_location)
        for k, v in d.items():
            if isinstance(v, dict):
                iterdict(v, version, file_location)
            else:
                if k == "deprecated":
                    if v:
                        # print("key")this is for true
                        countKey += 1
                        results_depr.append(countKey)
                elif k == "description" or k == "summary":
                    if v and "deprecated" in v:
                        count += 1
                        results_depr.append(count)
                        if "recommend" in v or "use" in v:
                            count_replace += 1
                            count_results_replace.append(v)
                            print(len(list(set(count_results_replace))))

        res[file_location] = len(list(set(count_results_replace)))

    for f in folderlist:
        path = f[0].split("\\")

        for fs in f[2]:
            if "swagger" in fs or "openapi" in fs:
                path = f[0].split("\\")
                version = path[-1]
                path = path[:-1]
                path = path[1:]
                path_unique = ("-").join(path)
                file_with_version = {version: fs}

                if path_unique in indexByAPI:
                    value = indexByAPI[path_unique]
                    indexByAPI[path_unique] = [file_with_version] + value
                else:
                    indexByAPI[path_unique] = [file_with_version]

                file_location = f[0] + "/" + fs
                file_location = file_location.replace("\\", '/')

                with open(f[0] + "/" + fs, 'r', encoding="utf-8") as stream:
                    try:
                        data = yaml.safe_load(stream)
                        # print(data["paths"])
                        values = iterdict(data, version, file_location)
                    except yaml.YAMLError as exc:
                        print(exc)

    # print(res)


# deprecated csv is the distinct files
def read():
    with open('findings/march/base/deprecated.csv', mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        apis = []
        for row in csv_reader:
            if line_count == 0:
                # print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                api = row[3].replace("\\", "/")
                apis.append(api)
                line_count += 1

    apis = ['APIs/kubernetes.io/v1.17.0/swagger.yaml']

    return list(set(apis))



def getApiName(path):
    path = path[:-2]
    path = path[1:]
    path_unique = ("_").join(path)

    return path_unique


def calculateTotalEndPoints():
    apis = read()
    apis = ["APIs/amazonaws.com/opsworkscm/2016-11-01/swagger.yaml"]
    count_endpoint = {}
    for api in apis:
        with open(api, 'r', encoding="utf-8") as stream:
            try:
                data = yaml.safe_load(stream)
                paths = data["paths"]
                for path in paths:
                    endpoint = path
                    if path in methods:
                        operation = methods[path]
                count_endpoint[api] = len(paths)
            except yaml.YAMLError as exc:
                print(exc)

    print(count_endpoint)

    return count_endpoint


def getEndpointsDeprecated():
    # apis = read()
    apis = ['APIs/kubernetes.io/v1.17.0/swagger.yaml']
    result = {}
    endpoint_deprecated_api = {}
    endpoints_deprecated_api = {}
    for api in apis:
        file_location = api
        # check if this is in deprecated_lists
        with open(api, 'r', encoding="utf-8") as stream:
            count = 0
            endpoints_deprecated = []
            try:
                data = yaml.safe_load(stream)
                paths = data["paths"]
                # print(file_location)

                for endpoint in paths:
                    endpoint_info = paths[endpoint]
                    # print(endpoint_info)
                    for reqtype in endpoint_info:
                        if reqtype != "parameters":
                            values = endpoint_info[reqtype]
                            for value in values:
                                if value == "deprecated":
                                    is_depr = values[value]
                                    if is_depr:
                                        count += 1
                                        endpoints_deprecated.append(endpoint)
                                elif value == "description" or value == "summary":
                                    desc = values[value]
                                    # if "deprecated" in desc and "will be deprecated" not in desc:
                                    if "deprecated" in desc:
                                        endpoints_deprecated.append(endpoint)
                                        count += 1
                result[file_location] = count
                endpoint_deprecated_api[file_location] = len(list(set(endpoints_deprecated)))
                endpoints_deprecated_api[file_location] = (list(set(endpoints_deprecated)))
            except yaml.YAMLError as exc:
                print(exc)

    return endpoint_deprecated_api


def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
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
        print(key)
        for definition in definitions_list:
            if (definition.startswith(key + "_items") or definition.startswith(
                    key + "_properties")) and definition.endswith("$ref"):
                val = definitions_list[definition]
                ref = val.split("/")[-1]
                # print(ref)
                if key != ref and ref not in keys:
                    find_desc(ref)
            elif definition.startswith(key) and definition.endswith("description"):
                # print(definition)
                desc = definitions_list[definition]
                if bool(desc) and "deprecated" in desc.lower():
                    print(desc)
                    descriptions.append(definitions_list[definition])
            elif definition.startswith(key) and definition.endswith("deprecated"):
                # print("depr:definition")
                desc = definitions_list[definition]
                if bool(desc):
                    print(desc)
                    descriptions.append(definitions_list[definition])
            else:
                pass

    find_desc(ref)
    # print(descriptions) check
    ln = 0
    if len(descriptions) > 0:
        ln = 1

    # print(ln)
    return ln


def generateResponse():
    res_endpoint_resp = {}
    # apis = read()
    apis = ['APIs/kubernetes.io/v1.17.0/swagger.yaml']

    res_desc_per_file = {}
    res_effected_endpoint = {}
    res_effected_endpoint_ln = {}
    for api in apis:
        definitions = []
        res_desc_depr = []
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
                    # definitions = (flatten_json(st["components"]["schemas"]))

                cnt = 0
                paths = st["paths"]
                response_refs = []
                endperref = {}
                for endpoint in paths:
                    # if endpoint == '/api/v1/namespaces/{namespace}/replicationcontrollers/{name}':
                        value_ref = []
                        endpoint_info = paths[endpoint]
                        for reqtype in endpoint_info:
                            if reqtype != "parameters":
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
                                                    if val == "description":
                                                        desc = pairs_value["description"]
                                                    else:
                                                        desc = pairs_value["summary"]
                                                    if "deprecated" in desc:
                                                        cnt += 1
                                                        res_desc_depr.append(endpoint)
                                                    # check if deprecated
                                                elif val == "schema":
                                                    p_vals = pairs_value["schema"]
                                                    if "$ref" in p_vals:
                                                        ref = p_vals["$ref"]
                                                        refer = ref.split("/")
                                                        response_refs.append(refer[-1])
                                                        if refer[-1] in endperref:
                                                            prev = endperref[refer[-1]]
                                                            endperref[refer[-1]] = prev + [endpoint]
                                                        else:
                                                            endperref[refer[-1]] = [endpoint]
                                                elif val == "content":
                                                    flat_values = flatten_json(pairs_value["content"])
                                                    for key_v in flat_values:
                                                        if key_v.endswith("$ref"):
                                                            value_ref = flat_values[key_v]

                                                    # p_vals = pairs_value["schema"]
                                                    # p_vals = pairs_value["content"]["application/json"]["schema"]
                                                    if value_ref:
                                                        refer = value_ref.split("/")
                                                        response_refs.append(refer[-1])
                                                        if refer[-1] in endperref:
                                                            prev = endperref[refer[-1]]
                                                            endperref[refer[-1]] = prev + [endpoint]
                                                        else:
                                                            endperref[refer[-1]] = [endpoint]

                ln = 0
                res = res_desc_depr
                refs = []
                list_ref_related = {}
                per_req_endpoints = {}
                # print(list(set(response_refs)))
                # response_refs = ['io.k8s.apimachinery.pkg.apis.meta.v1.Status']
                response_refs = []
                for ref in list(set(response_refs)):
                    ln += int(find_descriptions(ref, definitions))
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

    return res_effected_endpoint_ln


def generateRequest():
    apis = read()
    res_endpoint_resp = {}
    res_desc_per_file = {}
    res_effected_endpoint = {}
    res_effected_endpoint_ln = {}

    for api in apis:
        file_location = api
        definitions = []
        res_desc_depr = []
        req_param_deprecated = []
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
                name_req_params = {}
                # value_ref = {}
                for endpoint in paths:
                    endpoint_info = paths[endpoint]
                    value_ref = []

                    for reqtype in endpoint_info:
                        if reqtype != "parameters":  # get / post
                            values = endpoint_info[reqtype]
                            for value in values:
                                if value == "requestBody":
                                    flat_values = flatten_json(values["requestBody"])
                                    for key_v in flat_values:
                                        if key_v.endswith("$ref"):
                                            value_ref = flat_values[key_v]
                                        # elif
                                    # print(flat_values)
                                    # p_vals = values["requestBody"]["content"]["application/json"]["schema"]
                                    if value_ref:
                                        # ref = p_vals["$ref"]
                                        refer = value_ref.split("/")

                                        response_refs.append(refer[-1])
                                        # print(response_refs)
                                        if refer[-1] in endperref:
                                            prev = endperref[refer[-1]]
                                            endperref[refer[-1]] = prev + [endpoint]
                                        else:
                                            endperref[refer[-1]] = [endpoint]
                                            # print(endperref)
                                if value == "parameters":
                                    pairs_value = values[value]
                                    print(pairs_value)
                                    for val in pairs_value:
                                        if "name" == val:
                                            name_req_params[endpoint + "_" + reqtype] = pairs_value[val]
                                        if "deprecated" in val:
                                            is_depr = pairs_value[val]
                                            if is_depr:
                                                cnt += 1
                                                res_desc_depr.append(endpoint)
                                        elif 'description' in val:
                                            desc = val['description']
                                            if "deprecated" in desc:
                                                cnt += 1
                                                req_param_deprecated.append(pairs_value["name"])
                                                res_desc_depr.append(endpoint)
                                        if 'schema' in val:
                                            p_vals = val["schema"]
                                            if "$ref" in p_vals:
                                                ref = val["schema"]["$ref"]
                                                refer = ref.split("/")
                                                response_refs.append(refer[-1])
                                                if refer[-1] in endperref:
                                                    prev = endperref[refer[-1]]
                                                    endperref[refer[-1]] = prev + [endpoint]
                                                else:
                                                    endperref[refer[-1]] = [endpoint]
                        else:
                            pairs_value = values[value]
                            print(pairs_value)
                            for val in pairs_value:
                                if "name" == val:
                                    name_req_params[endpoint + "_" + reqtype] = pairs_value[val]
                                if "deprecated" in val:
                                    is_depr = pairs_value[val]
                                    if is_depr:
                                        cnt += 1
                                        res_desc_depr.append(endpoint)
                                elif 'description' in val:
                                    desc = val['description']
                                    if "deprecated" in desc:
                                        cnt += 1
                                        res_desc_depr.append(endpoint)
                                if 'schema' in val:
                                    p_vals = val["schema"]
                                    if "$ref" in p_vals:
                                        ref = val["schema"]["$ref"]
                                        refer = ref.split("/")
                                        response_refs.append(refer[-1])
                                        if refer[-1] in endperref:
                                            prev = endperref[refer[-1]]
                                            endperref[refer[-1]] = prev + [endpoint]
                                        else:
                                            endperref[refer[-1]] = [endpoint]
                ln = 0
                res = res_desc_depr
                refs = []
                list_ref_related = {}
                per_req_endpoints = {}
                for ref in list(set(response_refs)):
                    ln += int(find_descriptions(ref, definitions))
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

    return res_effected_endpoint


#

# print(getEndpointsDeprecated())

def checkAlternate():
    apis = read()
    result_endpoint = {}
    result_parametrs = {}

    for api in apis:
        file_location = api
        result_in_path = []
        result_in_parameter = []

        # check if this is in deprecated_lists
        with open(api, 'r', encoding="utf-8") as stream:
            # print(file_location)

            path_flatten_values = []
            definitions = []
            components_values = []
            try:
                data = yaml.safe_load(stream)
                paths = data["paths"]

                path_flatten_values = flatten_json(paths)

                if "definitions" in data:
                    definitions = (flatten_json(data["definitions"]))
                elif "components" in data:
                    components_values = (flatten_json(data["components"]["schemas"]))
                # print(file_location)
            except yaml.YAMLError as exc:
                print(exc)

            for component in components_values:
                print(component)

            for path in path_flatten_values:
                # print(path)
                if path.endswith("description") or path.endswith("summary"):
                    desc_text = path_flatten_values[path]
                    # print(path)
                    # print(desc_text)
                    if desc_text and "deprecated" in desc_text and ("use" in desc_text or "recommend" in desc_text):
                        result_in_path.append({path: desc_text})
            if len(result_in_path) > 0:
                result_endpoint[api] = result_in_path

            for definition in definitions:
                if definition.endswith("description") or definition.endswith("summary"):
                    desc_text = definitions[definition]
                    # print(path)
                    # print(desc_text)
                    if desc_text and "deprecated" in desc_text and ("use" in desc_text or "recommend" in desc_text):
                        result_in_parameter.append({path: desc_text})
            if len(result_in_parameter) > 0:
                result_parametrs[api] = result_in_parameter

    # print(result_endpoint)
    replacement_endpoint = False

    replacement_parameters = False

# checkAlternate()

# OpenAPI 3.0 supports get, post, put, patch, delete, head, options, and trace

def checkPathOpenApi():
    # apis = read()

    apis = ['APIs/kubernetes.io/v1.17.0/swagger.yaml']

    result_deprecated_in_path = {}
    count_result_deprecated_in_path = {}
    result_all_path = {}
    result_count_all_path = {}
    endpoints_api = {}
    count_endpoints_api = {}
    for api in apis:
        deprecated_paths = []

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
                splitted_values = path.split("_")
                endpoint = splitted_values[0]
                operation = splitted_values[1]

                value = path_flatten_values[path]
                path_with_operation = endpoint + "_" + operation
                endpointswithoutmethods.append(endpoint)

                # this block is for direct deprecated path
                if operation in methods:  # this is for direct path
                    if path_with_operation not in all_paths:  # all endpoints with operation
                        all_paths.append(path_with_operation)
                    deprecation_check_in = splitted_values[2].lower()
                    deprecated_paths = checkDescription(deprecation_check_in, path_with_operation, value,
                                                        deprecated_paths)

        result_deprecated_in_path[api] = list(set(deprecated_paths))
        count_result_deprecated_in_path[api] = len(list(set(deprecated_paths)))
        result_all_path[api] = list(set(all_paths))  # with operation
        result_count_all_path[api] = len(list(set(all_paths)))  # with operation
        endpoints_api[api] = list(set(endpointswithoutmethods))
        count_endpoints_api[api] = len(list(set(endpointswithoutmethods)))

    # print(result_deprecated_in_path)
    print(count_result_deprecated_in_path)

    return count_result_deprecated_in_path


def checkDescription(key_to_check, path_with_operation, value, result):
    if key_to_check == "summary":
        if "deprecated" in value.lower():
            result.append(path_with_operation)

    if key_to_check == "description":
        if "deprecated" in value.lower():
            result.append(path_with_operation)

    if "deprecated" in key_to_check.lower():
        if bool(value):
            result.append(path_with_operation)

    return result


def ref_descriptions(ref, definitions_list):
    descriptions = []
    keys = []

    def find_desc(key):
        keys.append(key)
        for definition in definitions_list:
            if (definition.startswith(key + "_items") or definition.startswith(
                    key + "_properties")) and definition.endswith("$ref"):
                val = definitions_list[definition]
                ref = val.split("/")[-1]
                # print(ref)
                if key != ref and ref not in keys:
                    find_desc(ref)
            elif definition.startswith(key) and definition.endswith("description"):
                # print(definition)
                desc = definitions_list[definition]
                if bool(desc) and "deprecated" in desc.lower():
                    # print(desc)
                    descriptions.append(definitions_list[definition])
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
        ln = 1
    return ln

# OpenAPI 2.0                    OpenAPI 3.0
# '#/definitions/User'         → '#/components/schemas/User'
# '#/parameters/offsetParam'   → '#/components/parameters/offsetParam'
# '#/responses/ErrorResponse'  → '#/components/responses/ErrorResponse'

# checkPathOpenApi()  # directly deprecated apis

# generateApiFromDeprecated()
# read()
# generateApiFromDeprecated()
# pip install openapi-spec-validator
# from prance import ResolvingParser
# # parser = ResolvingParser('APIs/whatsapp.local/1.0/openapi.yaml', backend = 'openapi-spec-validator')
# parser = ResolvingParser('APIs/kubernetes.io/v1.17.0/swagger.yaml', backend='swagger-spec-validator')
# print(parser.specification) # contains fully resolved specs as a dict


checkPathOpenApi()
# print(generateResponse())
