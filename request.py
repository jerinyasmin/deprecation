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


def getApiName(split_path):
    path = split_path[:-2]
    path = path[1:]
    path_unique = ("_").join(path)

    if path_unique == "googleapis.com_admin":
        path_unique = path_unique + split_path[-2]

    return path_unique
# deprecated csv is the distinct files
def read(filename = "result/RQ1/deprecated_onefile_manual.csv"):

    with open(filename, mode='r', encoding="utf-8") as csv_file:
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


def find_descriptions(ref, definitions_list):
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
            elif (definition.startswith(key) and definition.endswith("description")) or (definition.startswith(key) and definition.endswith("summary")):
                # print(definition)
                desc = definitions_list[definition]
                if bool(desc):
                    desc = " ".join(desc.lower().split())
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

descriptions_text = read("result/RQ1/text_and_file.csv")

# print(descriptions_text)


def generateRequest():
    apis = read()
    # apis = ['APIs/kubernetes.io/v1.17.0/swagger.yaml']
    # apis = ['APIs/amazonaws.com/cloudtrail/2013-11-01/swagger.yaml']
    # apis = ['APIs/googleapis.com/genomics/v1/swagger.yaml']
    # apis = ['APIs/amazonaws.com/apigateway/2015-07-09/swagger.yaml']
    # apis = ['APIs/googleapis.com/reseller/v1/swagger.yaml']
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
                    # if "responses" in components_values:
                    #     values = (flatten_json(st["components"]["responses"]))  # todo
                    #     definitions = {**values, **definitions}
                    #
                    # if "headers" in components_values:
                    #     values = (flatten_json(st["components"]["headers"]))  # todo
                    #     definitions = {**values, **definitions}

                    if "parameters" in components_values:
                        values = (flatten_json(st["components"]["parameters"]))  # todo
                        definitions = {**values, **definitions}
                if "parameters" in st:
                    params = (flatten_json(st["parameters"]))

                    definitions = {**params, **definitions}

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

                # print(operation_in_endpoint)

                response_refs = []
                endperref = {}
                name_req_params = {}
                for endpoint in paths:
                    endpoint_info = paths[endpoint]
                    value_ref = []

                    for reqtype in endpoint_info:
                        if reqtype != "parameters" and reqtype in methods:  # get / post
                            operation = endpoint+"_"+reqtype
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
                                            endperref[refer[-1]] = prev + [operation]
                                        else:
                                            endperref[refer[-1]] = [operation]
                                            # print(endperref)
                                if value == "parameters":
                                    pairs_value = values[value]

                                    for pair in pairs_value:
                                        for val in pair:
                                        # if "name" == val:
                                            if "deprecated" in val:
                                                is_depr = pair[val]
                                                if is_depr:
                                                    cnt += 1
                                                    res_desc_depr.append(operation)
                                            if 'description' in val or "summary" in val:
                                                # print(val)

                                                desc = pair[val]
                                                if bool(desc):
                                                    desc = " ".join(desc.lower().split())

                                                    if desc in descriptions_text:
                                                        cnt += 1
                                                        # req_param_deprecated.append(pairs_value["name"])
                                                        res_desc_depr.append(operation)
                                                        if desc in descriptions_operation:
                                                            values = descriptions_operation[operation]
                                                            descriptions_operation[operation] = values + [desc.lower()]
                                                        else:
                                                            descriptions_operation[operation] = [desc.lower()]
                                            if '$ref' in val:
                                                ref = pair["$ref"]
                                                refer = ref.split("/")
                                                response_refs.append(refer[-1])
                                                if refer[-1] in endperref:
                                                    prev = endperref[refer[-1]]
                                                    endperref[refer[-1]] = prev + [operation]
                                                else:
                                                    endperref[refer[-1]] = [operation]
                                            if 'schema' in val:
                                                    p_schema = pair["schema"]
                                                    flat_p_vals = flatten_json(p_schema)
                                                    for p_vals in flat_p_vals:
                                                        if p_vals.endswith("deprecated"):
                                                            is_depr = flat_p_vals[p_vals]
                                                            if is_depr:
                                                                cnt += 1
                                                                res_desc_depr.append(operation)
                                                        if p_vals.endswith("description") or p_vals.endswith("summary"):
                                                            desc = flat_p_vals[p_vals]
                                                            # print(desc)
                                                            if bool(desc):
                                                                desc = " ".join(desc.lower().split())

                                                                if desc in descriptions_text:
                                                                    # req_param_deprecated.append(pairs_value["name"])
                                                                    res_desc_depr.append(operation)
                                                                    if desc.lower() in descriptions_operation:
                                                                        values = descriptions_operation[operation]
                                                                        descriptions_operation[operation] = values + [desc.lower()]
                                                                    else:
                                                                        descriptions_operation[operation] = [desc.lower()]

                                                        if p_vals.endswith("$ref"):

                                                            ref = flat_p_vals[p_vals]
                                                            refer = ref.split("/")
                                                            response_refs.append(refer[-1])
                                                            if refer[-1] in endperref:
                                                                prev = endperref[refer[-1]]
                                                                endperref[refer[-1]] = prev + [operation]
                                                            else:
                                                                endperref[refer[-1]] = [operation]
                        else:
                            if reqtype == "parameters":
                                pairs_value = endpoint_info[reqtype]
                                for pair in pairs_value:
                                    # print(pair)
                                    for val in pair:
                                        # if "name" == val:
                                        #     name_req_params[endpoint + "_" + reqtype] = pairs_value[val]
                                        if "deprecated" in val:
                                            is_depr = pair[val]
                                            if is_depr:
                                                cnt += 1
                                                res_desc_depr.append(operation_in_endpoint[endpoint])
                                        if 'description' in val or "summary" in val:
                                            desc = pair[val]
                                            if bool(desc):
                                                desc = " ".join(desc.lower().split())

                                                if desc in descriptions_text:
                                                    cnt += 1
                                                    # req_param_deprecated.append(pairs_value["name"])
                                                    res_desc_depr.append(operation_in_endpoint[endpoint])
                                                    for op in operation_in_endpoint[endpoint]:
                                                        if desc.lower() in descriptions_operation:
                                                            values = descriptions_operation[op]
                                                            descriptions_operation[op] = values + [desc.lower()]
                                                        else:
                                                            descriptions_operation[op] = [desc.lower()]
                                        if '$ref' in val:
                                            ref = pair["$ref"]
                                            refer = ref.split("/")
                                            response_refs.append(refer[-1])
                                            if refer[-1] in endperref:
                                                prev = endperref[refer[-1]]
                                                endperref[refer[-1]] = prev + operation_in_endpoint[endpoint]
                                            else:
                                                endperref[refer[-1]] = operation_in_endpoint[endpoint]
                                        if 'schema' in val:
                                            p_schema = pair["schema"]
                                            flat_p_vals = flatten_json(p_schema)
                                            for p_vals in flat_p_vals:
                                                if p_vals.endswith("deprecated"):
                                                    is_depr = flat_p_vals[p_vals]
                                                    if is_depr:
                                                        cnt += 1
                                                        res_desc_depr.append(operation_in_endpoint[endpoint])
                                                if p_vals.endswith("description") or p_vals.endswith("summary"):
                                                    desc = flat_p_vals[p_vals]
                                                    # print(desc)
                                                    if bool(desc):
                                                        desc = " ".join(desc.lower().split())

                                                        if desc in descriptions_text:
                                                            cnt += 1
                                                            # req_param_deprecated.append(pairs_value["name"])
                                                            res_desc_depr.append(operation_in_endpoint[endpoint])
                                                            if desc.lower() in descriptions_operation:
                                                                values = descriptions_operation[operation]
                                                                descriptions_operation[operation] = values + [desc.lower()]
                                                            else:
                                                                descriptions_operation[operation] = [desc.lower()]

                                                if p_vals.endswith("$ref"):
                                                    ref = flat_p_vals[p_vals]
                                                    refer = ref.split("/")
                                                    response_refs.append(refer[-1])
                                                    if refer[-1] in endperref:
                                                        prev = endperref[refer[-1]]
                                                        endperref[refer[-1]] = prev + operation_in_endpoint[endpoint]
                                                    else:
                                                        endperref[refer[-1]] = operation_in_endpoint[endpoint]

                ln = 0
                res = res_desc_depr
                refs = []
                list_ref_related = {}
                per_req_endpoints = {}
                for ref in list(set(response_refs)):
                    descriptions_ref = find_descriptions(ref, definitions)
                    in_key = find_key_deprecated(ref, definitions)
                    # ln += int(len(descriptions_ref))

                    if len(descriptions_ref) or in_key:
                        res = res + (endperref[ref])   #@todo description
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
                    method_name = method_name_split[len(method_name_split)-1]
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
                res_effected_endpoint[file_location] = unique_operations_deprecated

                results[file_location] = {"count_operation_deprecated": len(unique_operations_deprecated), "count_get": count_get, "count_post": count_post,
                                          "count_put": count_put, "count_delete": count_delete, "count_patch": count_patch, "count_head": count_head,
                                          "count_options": count_options, "count_trace": count_trace, "description operations": descriptions_operation}

                deprecated_descriptions_api[file_location] = descriptions_operation
            except yaml.YAMLError as exc:
                print(exc)

    # print(results)
    # print(deprecated_descriptions_api)

    with open('result/RQ2/deprecated_operation_request.csv', mode='w') as res_file:

        res_writer = csv.writer(res_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
        res_writer.writerow(["api_name", "count deprecated operation",
                             "count_get", "count_post", "count_put", "count_delete",
                             "count_patch", "count_head", "count_options", "count_trace"])
        for api_file in results:
            api_name = getApiName(api_file.split("/"))
            res_writer.writerow(
                [api_name, results[api_file]["count_operation_deprecated"],
                 results[api_file]["count_get"],
                 results[api_file]["count_post"],
                 results[api_file]["count_put"],
                 results[api_file]["count_delete"],
                 results[api_file]["count_patch"],
                 results[api_file]["count_head"],
                 results[api_file]["count_options"],
                 results[api_file]["count_trace"],
                 ])

    with open('result/RQ2/deprecated_operation_descriptions_request.csv', mode='w') as res_file:
        res_writer = csv.writer(res_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
        res_writer.writerow(["api_name", "operation", "description", "operation count for api", "description count"])
        for api_file in deprecated_descriptions_api:
            api_name = getApiName(api_file.split("/"))
            descriptions = deprecated_descriptions_api[api_file]#len is the count of impacted operation
            for operation in descriptions:
                desc = list(set(descriptions[operation]))
                res_writer.writerow(
                    [api_name, operation, desc, len(descriptions), len(desc)]) #@todo is it possible to get multiple sentences


# OpenAPI 2.0                    OpenAPI 3.0
# '#/definitions/User'         → '#/components/schemas/User'
# '#/parameters/offsetParam'   → '#/components/parameters/offsetParam'
# '#/responses/ErrorResponse'  → '#/components/responses/ErrorResponse'

results = generateRequest()
# print(results)

# results = {'APIs/googleapis.com/jobs/v2/swagger.yaml': 7, 'APIs/amazonaws.com/lightsail/2016-11-28/swagger.yaml': 1, 'APIs/googleapis.com/dns/v1/swagger.yaml': 0, 'APIs/googleapis.com/licensing/v1/swagger.yaml': 0, 'APIs/whatsapp.local/1.0/openapi.yaml': 0, 'APIs/googleapis.com/blogger/v3/swagger.yaml': 0, 'APIs/azure.com/databox/2019-09-01/swagger.yaml': 0, 'APIs/iva-api.com/2.0/swagger.yaml': 0, 'APIs/reverb.com/3.0/swagger.yaml': 0, 'APIs/googleapis.com/testing/v1/swagger.yaml': 0, 'APIs/googleapis.com/playmoviespartner/v1/swagger.yaml': 2, 'APIs/flat.io/2.8.0/swagger.yaml': 0, 'APIs/amazonaws.com/discovery/2015-11-01/swagger.yaml': 1, 'APIs/googleapis.com/fusiontables/v2/swagger.yaml': 0, 'APIs/azure.com/eventhub-EventHub/2017-04-01/swagger.yaml': 0, 'APIs/botify.com/1.0.0/swagger.yaml': 2, 'APIs/googleapis.com/adexchangeseller/v2.0/swagger.yaml': 0, 'APIs/azure.com/containerservice-containerService/2017-07-01/swagger.yaml': 0, 'APIs/googleapis.com/doubleclickbidmanager/v1/swagger.yaml': 0, 'APIs/gitlab.com/v3/swagger.yaml': 0, 'APIs/amazonaws.com/mediapackage/2017-10-12/swagger.yaml': 0, 'APIs/crucible.local/1.0.0/swagger.yaml': 0, 'APIs/googleapis.com/gamesManagement/v1management/swagger.yaml': 0, 'APIs/amazonaws.com/email/2010-12-01/swagger.yaml': 0, 'APIs/amazonaws.com/logs/2014-03-28/swagger.yaml': 0, 'APIs/amazonaws.com/comprehendmedical/2018-10-30/swagger.yaml': 0, 'APIs/googleapis.com/androidenterprise/v1/swagger.yaml': 3, 'APIs/googleapis.com/driveactivity/v2/swagger.yaml': 0, 'APIs/tomtom.com/search/1.0.0/openapi.yaml': 3, 'APIs/googleapis.com/storage/v1/swagger.yaml': 0, 'APIs/googleapis.com/admin/directory_v1/swagger.yaml': 0, 'APIs/atlassian.com/jira/v3/swagger.yaml': 18, 'APIs/zuora.com/2019-09-19/swagger.yaml': 7, 'APIs/googleapis.com/admin/datatransfer_v1/swagger.yaml': 0, 'APIs/googleapis.com/cloudbilling/v1/swagger.yaml': 0, 'APIs/amazonaws.com/swf/2012-01-25/swagger.yaml': 3, 'APIs/googleapis.com/clouddebugger/v2/swagger.yaml': 2, 'APIs/googleapis.com/vision/v1/swagger.yaml': 1, 'APIs/amazonaws.com/servicecatalog/2015-12-10/swagger.yaml': 1, 'APIs/lyft.com/1.0.0/swagger.yaml': 1, 'APIs/googleapis.com/servicemanagement/v1/swagger.yaml': 0, 'APIs/googleapis.com/fitness/v1/swagger.yaml': 0, 'APIs/github.com/v3/swagger.yaml': 1, 'APIs/googleapis.com/customsearch/v1/swagger.yaml': 0, 'APIs/visagecloud.com/1.1/swagger.yaml': 0, 'APIs/googleapis.com/pagespeedonline/v5/swagger.yaml': 0, 'APIs/vimeo.com/3.4/openapi.yaml': 0, 'APIs/googleapis.com/playcustomapp/v1/swagger.yaml': 0, 'APIs/amazonaws.com/elasticmapreduce/2009-03-31/swagger.yaml': 2, 'APIs/amazonaws.com/lambda/2015-03-31/swagger.yaml': 0, 'APIs/googleapis.com/serviceuser/v1/swagger.yaml': 0, 'APIs/googleapis.com/tasks/v1/swagger.yaml': 0, 'APIs/googleapis.com/admin/reports_v1/swagger.yaml': 0, 'APIs/billbee.io/v1/swagger.yaml': 0, 'APIs/azure.com/recoveryservices-replicationusages/2016-06-01/swagger.yaml': 0, 'APIs/cloudmersive.com/ocr/v1/swagger.yaml': 0, 'APIs/amazonaws.com/directconnect/2012-10-25/swagger.yaml': 0, 'APIs/azure.com/sql-tableAuditing/2014-04-01/swagger.yaml': 0, 'APIs/amazonaws.com/guardduty/2017-11-28/swagger.yaml': 0, 'APIs/contribly.com/1.0.0/swagger.yaml': 0, 'APIs/googleapis.com/script/v1/swagger.yaml': 1, 'APIs/googleapis.com/serviceusage/v1/swagger.yaml': 0, 'APIs/import.io/rss/1.0/swagger.yaml': 0, 'APIs/azure.com/resources-policyAssignments/2016-12-01/swagger.yaml': 0, 'APIs/import.io/run/1.0/swagger.yaml': 0, 'APIs/azure.com/applicationinsights-componentContinuousExport_API/2015-05-01/swagger.yaml': 2, 'APIs/sportsdata.io/nfl-v3-stats/1.0/swagger.yaml': 0, 'APIs/googleapis.com/doubleclicksearch/v2/swagger.yaml': 2, 'APIs/azure.com/compute/2019-03-01/swagger.yaml': 0, 'APIs/googleapis.com/surveys/v2/swagger.yaml': 3, 'APIs/instagram.com/1.0.0/swagger.yaml': 1, 'APIs/googleapis.com/games/v1/swagger.yaml': 0, 'APIs/googleapis.com/tpu/v1/swagger.yaml': 1, 'APIs/googleapis.com/books/v1/swagger.yaml': 0, 'APIs/googleapis.com/reseller/v1/swagger.yaml': 0, 'APIs/googleapis.com/people/v1/swagger.yaml': 2, 'APIs/amazonaws.com/shield/2016-06-02/swagger.yaml': 0, 'APIs/googleapis.com/compute/v1/swagger.yaml': 103, 'APIs/googleapis.com/serviceconsumermanagement/v1/swagger.yaml': 0, 'APIs/googleapis.com/webfonts/v1/swagger.yaml': 0, 'APIs/amazonaws.com/ec2/2016-11-15/swagger.yaml': 0, 'APIs/api2cart.com/1.0.0/swagger.yaml': 4, 'APIs/googleapis.com/identitytoolkit/v3/swagger.yaml': 0, 'APIs/googleapis.com/youtubereporting/v1/swagger.yaml': 0, 'APIs/googleapis.com/adsense/v1.4/swagger.yaml': 0, 'APIs/shutterstock.com/1.0.15/openapi.yaml': 5, 'APIs/amazonaws.com/apigateway/2015-07-09/swagger.yaml': 0, 'APIs/googleapis.com/youtubeAnalytics/v2/swagger.yaml': 0, 'APIs/azure.com/recoveryservicesbackup-bms/2017-07-01/swagger.yaml': 0, 'APIs/googleapis.com/verifiedaccess/v1/swagger.yaml': 0, 'APIs/azure.com/servicefabric/6.5.0.36/swagger.yaml': 0, 'APIs/azure.com/servicefabric-application/2019-03-01/swagger.yaml': 0, 'APIs/rebilly.com/2.1/swagger.yaml': 4, 'APIs/googleapis.com/spectrum/v1explorer/swagger.yaml': 0, 'APIs/victorops.com/0.0.3/swagger.yaml': 0, 'APIs/googleapis.com/androidmanagement/v1/swagger.yaml': 2, 'APIs/azure.com/redis/2015-08-01/swagger.yaml': 0, 'APIs/googleapis.com/appengine/v1/swagger.yaml': 2, 'APIs/amazonaws.com/elasticbeanstalk/2010-12-01/swagger.yaml': 4, 'APIs/googleapis.com/gamesConfiguration/v1configuration/swagger.yaml': 0, 'APIs/hetras-certification.net/booking/v0/swagger.yaml': 0, 'APIs/amazonaws.com/storagegateway/2013-06-30/swagger.yaml': 0, 'APIs/bungie.net/2.0.0/swagger.yaml': 0, 'APIs/googleapis.com/content/v2.1/swagger.yaml': 2, 'APIs/amazonaws.com/pinpoint/2016-12-01/swagger.yaml': 0, 'APIs/weatherbit.io/2.0.0/swagger.yaml': 0, 'APIs/googleapis.com/spanner/v1/swagger.yaml': 0, 'APIs/amazonaws.com/s3/2006-03-01/swagger.yaml': 0, 'APIs/googleapis.com/civicinfo/v2/swagger.yaml': 0, 'APIs/googleapis.com/container/v1/swagger.yaml': 54, 'APIs/googleapis.com/sourcerepo/v1/swagger.yaml': 0, 'APIs/amazonaws.com/codedeploy/2014-10-06/swagger.yaml': 0, 'APIs/azure.com/apimanagement-apimdeployment/2018-01-01/swagger.yaml': 0, 'APIs/here.com/tracking/2.0.0/swagger.yaml': 0, 'APIs/import.io/extraction/1.0/swagger.yaml': 0, 'APIs/linode.com/4.5.0/openapi.yaml': 7, 'APIs/googleapis.com/dataflow/v1b3/swagger.yaml': 4, 'APIs/googleapis.com/groupsmigration/v1/swagger.yaml': 0, 'APIs/googleapis.com/bigtableadmin/v2/swagger.yaml': 0, 'APIs/googleapis.com/dialogflow/v2/swagger.yaml': 0, 'APIs/googleapis.com/logging/v2/swagger.yaml': 6, 'APIs/amazonaws.com/ssm/2014-11-06/swagger.yaml': 4, 'APIs/wmata.com/incidents/1.0/swagger.yaml': 0, 'APIs/amazonaws.com/elastictranscoder/2012-09-25/swagger.yaml': 0, 'APIs/googleapis.com/appsactivity/v1/swagger.yaml': 0, 'APIs/googleapis.com/analytics/v3/swagger.yaml': 3, 'APIs/googleapis.com/drive/v3/swagger.yaml': 7, 'APIs/amazonaws.com/elasticache/2015-02-02/swagger.yaml': 0, 'APIs/wmata.com/bus-route/1.0/swagger.yaml': 0, 'APIs/bbc.com/1.0.0/openapi.yaml': 1, 'APIs/googleapis.com/androidpublisher/v3/swagger.yaml': 0, 'APIs/googleapis.com/dfareporting/v3.3/swagger.yaml': 7, 'APIs/vocadb.net/v1/swagger.yaml': 0, 'APIs/wmata.com/rail-station/1.0/swagger.yaml': 0, 'APIs/azure.com/datalake-analytics-catalog/2016-11-01/swagger.yaml': 2, 'APIs/jira.local/1.0.0/swagger.yaml': 0, 'APIs/amazonaws.com/resource-groups/2017-11-27/swagger.yaml': 0, 'APIs/googleapis.com/mirror/v1/swagger.yaml': 0, 'APIs/azure.com/machinelearningservices-datastore/2019-08-01/swagger.yaml': 0, 'APIs/osf.io/2.0/swagger.yaml': 0, 'APIs/wowza.com/1/swagger.yaml': 2, 'APIs/anchore.io/0.1.12/swagger.yaml': 1, 'APIs/amazonaws.com/glue/2017-03-31/swagger.yaml': 2, 'APIs/googleapis.com/calendar/v3/swagger.yaml': 7, 'APIs/gov.bc.ca/geocoder/2.0.0/openapi.yaml': 0, 'APIs/netatmo.net/1.1.1/swagger.yaml': 0, 'APIs/nexmo.com/application/1.0.2/openapi.yaml': 0, 'APIs/amazonaws.com/firehose/2015-08-04/swagger.yaml': 2, 'APIs/noosh.com/1.0/swagger.yaml': 0, 'APIs/storecove.com/2.0.1/swagger.yaml': 3, 'APIs/netlicensing.io/2.x/swagger.yaml': 0, 'APIs/azure.com/datafactory/2018-06-01/swagger.yaml': 0, 'APIs/googleapis.com/siteVerification/v1/swagger.yaml': 0, 'APIs/googleapis.com/webmasters/v3/swagger.yaml': 0, 'APIs/rbaskets.in/1.0.0/swagger.yaml': 0, 'APIs/kubernetes.io/v1.17.0/swagger.yaml': 233, 'APIs/amazonaws.com/mturk-requester/2017-01-17/swagger.yaml': 0, 'APIs/googleapis.com/iam/v1/swagger.yaml': 0, 'APIs/googleapis.com/youtube/v3/swagger.yaml': 2, 'APIs/azure.com/recoveryservicessiterecovery-service/2016-08-10/swagger.yaml': 0, 'APIs/googleapis.com/tagmanager/v1/swagger.yaml': 0, 'APIs/setlist.fm/1.0/swagger.yaml': 1, 'APIs/import.io/schedule/1.0/swagger.yaml': 0, 'APIs/googleapis.com/discovery/v1/swagger.yaml': 0, 'APIs/azure.com/web-WebApps/2018-11-01/swagger.yaml': 0, 'APIs/googleapis.com/genomics/v1/swagger.yaml': 0, 'APIs/googleapis.com/servicecontrol/v1/swagger.yaml': 0, 'APIs/sportsdata.io/nfl-v3-scores/1.0/swagger.yaml': 0, 'APIs/paccurate.io/0.1.1/swagger.yaml': 0, 'APIs/amazonaws.com/opsworkscm/2016-11-01/swagger.yaml': 0, 'APIs/googleapis.com/partners/v2/swagger.yaml': 0, 'APIs/bulksms.com/1.0.0/swagger.yaml': 0, 'APIs/amazonaws.com/codebuild/2016-10-06/swagger.yaml': 0, 'APIs/googleapis.com/servicenetworking/v1/swagger.yaml': 0, 'APIs/thetvdb.com/2.2.0/swagger.yaml': 0, 'APIs/nba.com/1.0.0/swagger.yaml': 0, 'APIs/nytimes.com/community/3.0.0/swagger.yaml': 0, 'APIs/azure.com/signalr/2018-10-01/swagger.yaml': 0, 'APIs/googleapis.com/deploymentmanager/v2/swagger.yaml': 1, 'APIs/googleapis.com/sheets/v4/swagger.yaml': 0, 'APIs/adyen.com/MarketPayNotificationService/4/openapi.yaml': 0, 'APIs/googleapis.com/bigquerydatatransfer/v1/swagger.yaml': 2, 'APIs/googleapis.com/bigquery/v2/swagger.yaml': 2, 'APIs/gitea.io/1.1.1/swagger.yaml': 0, 'APIs/googleapis.com/adexchangebuyer/v1.4/swagger.yaml': 2, 'APIs/amazonaws.com/cloudfront/2018-11-05/swagger.yaml': 0, 'APIs/agco-ats.com/v1/swagger.yaml': 0, 'APIs/amazonaws.com/rds-data/2018-08-01/swagger.yaml': 0, 'APIs/stripe.com/2019-09-09/swagger.yaml': 2, 'APIs/transitfeeds.com/1.0.0/swagger.yaml': 0, 'APIs/squareup.com/2.0/swagger.yaml': 2, 'APIs/amazonaws.com/medialive/2017-10-14/swagger.yaml': 0, 'APIs/googleapis.com/urlshortener/v1/swagger.yaml': 0, 'APIs/docusign.net/v2/swagger.yaml': 1, 'APIs/googleapis.com/dlp/v2/swagger.yaml': 0, 'APIs/amazonaws.com/secretsmanager/2017-10-17/swagger.yaml': 1, 'APIs/amazonaws.com/cognito-idp/2016-04-18/swagger.yaml': 0, 'APIs/azure.com/monitor-serviceDiagnosticsSettings_API/2016-09-01/swagger.yaml': 0, 'APIs/bigoven.com/partner/swagger.yaml': 3, 'APIs/googleapis.com/plus/v1/swagger.yaml': 0, 'APIs/hetras-certification.net/hotel/v0/swagger.yaml': 0, 'APIs/amazonaws.com/ram/2018-01-04/swagger.yaml': 0, 'APIs/bitbucket.org/2.0/swagger.yaml': 0, 'APIs/import.io/data/1.0/swagger.yaml': 0, 'APIs/slack.com/1.2.0/swagger.yaml': 1, 'APIs/nexmo.com/number-insight/1.0.4/openapi.yaml': 0, 'APIs/getgo.com/gototraining/1.0.0/swagger.yaml': 0, 'APIs/citrixonline.com/gotomeeting/1.0.0/swagger.yaml': 3, 'APIs/getgo.com/gotowebinar/1.0.0/swagger.yaml': 0, 'APIs/amazonaws.com/iot/2015-05-28/swagger.yaml': 2, 'APIs/docker.com/engine/1.33/swagger.yaml': 0, 'APIs/googleapis.com/remotebuildexecution/v2/swagger.yaml': 0, 'APIs/azure.com/search-searchservice/2019-05-06/swagger.yaml': 0, 'APIs/azure.com/containerservice-managedClusters/2017-08-31/swagger.yaml': 0, 'APIs/npr.org/listening/2/swagger.yaml': 0, 'APIs/youneedabudget.com/1.0.0/swagger.yaml': 0, 'APIs/googleapis.com/slides/v1/swagger.yaml': 0, 'APIs/googleapis.com/monitoring/v3/swagger.yaml': 1, 'APIs/taxamo.com/1/swagger.yaml': 0, 'APIs/googleapis.com/adsensehost/v4.1/swagger.yaml': 3, 'APIs/amazonaws.com/cloudtrail/2013-11-01/swagger.yaml': 0, 'APIs/googleapis.com/gmail/v1/swagger.yaml': 0, 'APIs/googleapis.com/groupssettings/v1/swagger.yaml': 2, 'APIs/googleapis.com/oauth2/v2/swagger.yaml': 0, 'APIs/dracoon.team/4.5.0/swagger.yaml': 8, 'APIs/bunq.com/1.0/openapi.yaml': 7, 'APIs/amazonaws.com/rds/2014-10-31/swagger.yaml': 0, 'APIs/beezup.com/2.0/swagger.yaml': 0, 'APIs/amazonaws.com/iotthingsgraph/2018-09-06/swagger.yaml': 0, 'APIs/googleapis.com/plusDomains/v1/swagger.yaml': 0, 'APIs/googleapis.com/appstate/v1/swagger.yaml': 0}
#
# results = {'APIs/storecove.com/2.0.1/swagger.yaml': 3, 'APIs/googleapis.com/vision/v1/swagger.yaml': 1, 'APIs/jira.local/1.0.0/swagger.yaml': 0, 'APIs/transitfeeds.com/1.0.0/swagger.yaml': 0, 'APIs/wowza.com/1/swagger.yaml': 2, 'APIs/googleapis.com/appengine/v1/swagger.yaml': 2, 'APIs/googleapis.com/civicinfo/v2/swagger.yaml': 0, 'APIs/googleapis.com/identitytoolkit/v3/swagger.yaml': 0, 'APIs/googleapis.com/pagespeedonline/v5/swagger.yaml': 0, 'APIs/googleapis.com/verifiedaccess/v1/swagger.yaml': 0, 'APIs/googleapis.com/sheets/v4/swagger.yaml': 0, 'APIs/googleapis.com/bigtableadmin/v2/swagger.yaml': 2, 'APIs/googleapis.com/siteVerification/v1/swagger.yaml': 0, 'APIs/github.com/v3/swagger.yaml': 1, 'APIs/googleapis.com/webfonts/v1/swagger.yaml': 0, 'APIs/amazonaws.com/ec2/2016-11-15/swagger.yaml': 2, 'APIs/googleapis.com/gamesConfiguration/v1configuration/swagger.yaml': 0, 'APIs/googleapis.com/mirror/v1/swagger.yaml': 0, 'APIs/bbc.com/1.0.0/openapi.yaml': 1, 'APIs/googleapis.com/plusDomains/v1/swagger.yaml': 0, 'APIs/amazonaws.com/glue/2017-03-31/swagger.yaml': 2, 'APIs/azure.com/recoveryservicessiterecovery-service/2016-08-10/swagger.yaml': 0, 'APIs/googleapis.com/webmasters/v3/swagger.yaml': 0, 'APIs/googleapis.com/doubleclickbidmanager/v1/swagger.yaml': 0, 'APIs/amazonaws.com/logs/2014-03-28/swagger.yaml': 0, 'APIs/azure.com/machinelearningservices-datastore/2019-08-01/swagger.yaml': 0, 'APIs/googleapis.com/bigquerydatatransfer/v1/swagger.yaml': 2, 'APIs/amazonaws.com/swf/2012-01-25/swagger.yaml': 3, 'APIs/amazonaws.com/rds-data/2018-08-01/swagger.yaml': 0, 'APIs/azure.com/databox/2019-09-01/swagger.yaml': 0, 'APIs/googleapis.com/logging/v2/swagger.yaml': 6, 'APIs/beezup.com/2.0/swagger.yaml': 0, 'APIs/wmata.com/incidents/1.0/swagger.yaml': 0, 'APIs/botify.com/1.0.0/swagger.yaml': 2, 'APIs/amazonaws.com/comprehendmedical/2018-10-30/swagger.yaml': 0, 'APIs/googleapis.com/sourcerepo/v1/swagger.yaml': 0, 'APIs/adyen.com/MarketPayNotificationService/4/openapi.yaml': 0, 'APIs/taxamo.com/1/swagger.yaml': 1, 'APIs/import.io/run/1.0/swagger.yaml': 0, 'APIs/nba.com/1.0.0/swagger.yaml': 0, 'APIs/amazonaws.com/elasticache/2015-02-02/swagger.yaml': 2, 'APIs/googleapis.com/spanner/v1/swagger.yaml': 0, 'APIs/amazonaws.com/iot/2015-05-28/swagger.yaml': 3, 'APIs/bunq.com/1.0/openapi.yaml': 7, 'APIs/googleapis.com/script/v1/swagger.yaml': 1, 'APIs/amazonaws.com/discovery/2015-11-01/swagger.yaml': 1, 'APIs/googleapis.com/container/v1/swagger.yaml': 54, 'APIs/azure.com/compute/2019-03-01/swagger.yaml': 0, 'APIs/googleapis.com/iam/v1/swagger.yaml': 0, 'APIs/googleapis.com/tagmanager/v1/swagger.yaml': 0, 'APIs/gitea.io/1.1.1/swagger.yaml': 0, 'APIs/amazonaws.com/codebuild/2016-10-06/swagger.yaml': 0, 'APIs/amazonaws.com/iotthingsgraph/2018-09-06/swagger.yaml': 0, 'APIs/amazonaws.com/email/2010-12-01/swagger.yaml': 0, 'APIs/amazonaws.com/shield/2016-06-02/swagger.yaml': 0, 'APIs/googleapis.com/servicenetworking/v1/swagger.yaml': 0, 'APIs/amazonaws.com/codedeploy/2014-10-06/swagger.yaml': 0, 'APIs/googleapis.com/urlshortener/v1/swagger.yaml': 0, 'APIs/googleapis.com/deploymentmanager/v2/swagger.yaml': 1, 'APIs/noosh.com/1.0/swagger.yaml': 0, 'APIs/azure.com/containerservice-managedClusters/2017-08-31/swagger.yaml': 0, 'APIs/googleapis.com/dataflow/v1b3/swagger.yaml': 4, 'APIs/googleapis.com/fitness/v1/swagger.yaml': 0, 'APIs/azure.com/sql-tableAuditing/2014-04-01/swagger.yaml': 0, 'APIs/amazonaws.com/apigateway/2015-07-09/swagger.yaml': 2, 'APIs/azure.com/recoveryservicesbackup-bms/2017-07-01/swagger.yaml': 0, 'APIs/azure.com/apimanagement-apimdeployment/2018-01-01/swagger.yaml': 0, 'APIs/googleapis.com/adexchangebuyer/v1.4/swagger.yaml': 2, 'APIs/import.io/schedule/1.0/swagger.yaml': 0, 'APIs/slack.com/1.2.0/swagger.yaml': 1, 'APIs/whatsapp.local/1.0/openapi.yaml': 0, 'APIs/googleapis.com/clouddebugger/v2/swagger.yaml': 2, 'APIs/sportsdata.io/nfl-v3-stats/1.0/swagger.yaml': 0, 'APIs/googleapis.com/groupsmigration/v1/swagger.yaml': 0, 'APIs/googleapis.com/oauth2/v2/swagger.yaml': 0, 'APIs/amazonaws.com/medialive/2017-10-14/swagger.yaml': 0, 'APIs/googleapis.com/content/v2.1/swagger.yaml': 2, 'APIs/googleapis.com/spectrum/v1explorer/swagger.yaml': 0, 'APIs/iva-api.com/2.0/swagger.yaml': 0, 'APIs/setlist.fm/1.0/swagger.yaml': 1, 'APIs/googleapis.com/gamesManagement/v1management/swagger.yaml': 0, 'APIs/crucible.local/1.0.0/swagger.yaml': 0, 'APIs/billbee.io/v1/swagger.yaml': 0, 'APIs/googleapis.com/cloudbilling/v1/swagger.yaml': 0, 'APIs/googleapis.com/jobs/v2/swagger.yaml': 9, 'APIs/googleapis.com/adsensehost/v4.1/swagger.yaml': 3, 'APIs/wmata.com/rail-station/1.0/swagger.yaml': 0, 'APIs/googleapis.com/androidpublisher/v3/swagger.yaml': 0, 'APIs/googleapis.com/androidenterprise/v1/swagger.yaml': 3, 'APIs/googleapis.com/blogger/v3/swagger.yaml': 0, 'APIs/api2cart.com/1.0.0/swagger.yaml': 4, 'APIs/googleapis.com/people/v1/swagger.yaml': 2, 'APIs/cloudmersive.com/ocr/v1/swagger.yaml': 0, 'APIs/googleapis.com/slides/v1/swagger.yaml': 0, 'APIs/amazonaws.com/elasticmapreduce/2009-03-31/swagger.yaml': 2, 'APIs/import.io/extraction/1.0/swagger.yaml': 0, 'APIs/googleapis.com/fusiontables/v2/swagger.yaml': 0, 'APIs/bulksms.com/1.0.0/swagger.yaml': 0, 'APIs/rbaskets.in/1.0.0/swagger.yaml': 0, 'APIs/amazonaws.com/ssm/2014-11-06/swagger.yaml': 4, 'APIs/amazonaws.com/cognito-idp/2016-04-18/swagger.yaml': 0, 'APIs/thetvdb.com/2.2.0/swagger.yaml': 0, 'APIs/amazonaws.com/resource-groups/2017-11-27/swagger.yaml': 0, 'APIs/import.io/rss/1.0/swagger.yaml': 0, 'APIs/azure.com/resources-policyAssignments/2016-12-01/swagger.yaml': 0, 'APIs/googleapis.com/admin/directory_v1/swagger.yaml': 0, 'APIs/tomtom.com/search/1.0.0/openapi.yaml': 3, 'APIs/instagram.com/1.0.0/swagger.yaml': 1, 'APIs/vocadb.net/v1/swagger.yaml': 0, 'APIs/sportsdata.io/nfl-v3-scores/1.0/swagger.yaml': 0, 'APIs/npr.org/listening/2/swagger.yaml': 0, 'APIs/shutterstock.com/1.0.15/openapi.yaml': 5, 'APIs/googleapis.com/reseller/v1/swagger.yaml': 0, 'APIs/azure.com/servicefabric/6.5.0.36/swagger.yaml': 0, 'APIs/googleapis.com/books/v1/swagger.yaml': 0, 'APIs/azure.com/eventhub-EventHub/2017-04-01/swagger.yaml': 0, 'APIs/amazonaws.com/mediapackage/2017-10-12/swagger.yaml': 0, 'APIs/googleapis.com/appstate/v1/swagger.yaml': 0, 'APIs/googleapis.com/groupssettings/v1/swagger.yaml': 2, 'APIs/hetras-certification.net/hotel/v0/swagger.yaml': 0, 'APIs/googleapis.com/testing/v1/swagger.yaml': 0, 'APIs/googleapis.com/plus/v1/swagger.yaml': 0, 'APIs/amazonaws.com/lambda/2015-03-31/swagger.yaml': 0, 'APIs/googleapis.com/games/v1/swagger.yaml': 0, 'APIs/googleapis.com/adexchangeseller/v2.0/swagger.yaml': 0, 'APIs/rebilly.com/2.1/swagger.yaml': 4, 'APIs/googleapis.com/licensing/v1/swagger.yaml': 0, 'APIs/googleapis.com/dlp/v2/swagger.yaml': 0, 'APIs/azure.com/recoveryservices-replicationusages/2016-06-01/swagger.yaml': 0, 'APIs/import.io/data/1.0/swagger.yaml': 0, 'APIs/gov.bc.ca/geocoder/2.0.0/openapi.yaml': 0, 'APIs/googleapis.com/playmoviespartner/v1/swagger.yaml': 2, 'APIs/azure.com/search-searchservice/2019-05-06/swagger.yaml': 0, 'APIs/googleapis.com/discovery/v1/swagger.yaml': 0, 'APIs/googleapis.com/dns/v1/swagger.yaml': 0, 'APIs/weatherbit.io/2.0.0/swagger.yaml': 0, 'APIs/azure.com/datafactory/2018-06-01/swagger.yaml': 0, 'APIs/amazonaws.com/elasticbeanstalk/2010-12-01/swagger.yaml': 4, 'APIs/azure.com/redis/2015-08-01/swagger.yaml': 0, 'APIs/netatmo.net/1.1.1/swagger.yaml': 0, 'APIs/agco-ats.com/v1/swagger.yaml': 0, 'APIs/atlassian.com/jira/v3/swagger.yaml': 31, 'APIs/linode.com/4.5.0/openapi.yaml': 7, 'APIs/azure.com/web-WebApps/2018-11-01/swagger.yaml': 0, 'APIs/azure.com/applicationinsights-componentContinuousExport_API/2015-05-01/swagger.yaml': 2, 'APIs/amazonaws.com/lightsail/2016-11-28/swagger.yaml': 1, 'APIs/amazonaws.com/rds/2014-10-31/swagger.yaml': 0, 'APIs/googleapis.com/calendar/v3/swagger.yaml': 10, 'APIs/googleapis.com/partners/v2/swagger.yaml': 0, 'APIs/azure.com/servicefabric-application/2019-03-01/swagger.yaml': 0, 'APIs/azure.com/signalr/2018-10-01/swagger.yaml': 0, 'APIs/anchore.io/0.1.12/swagger.yaml': 1, 'APIs/dracoon.team/4.5.0/swagger.yaml': 9, 'APIs/kubernetes.io/v1.17.0/swagger.yaml': 304, 'APIs/gitlab.com/v3/swagger.yaml': 0, 'APIs/azure.com/datalake-analytics-catalog/2016-11-01/swagger.yaml': 2, 'APIs/osf.io/2.0/swagger.yaml': 5, 'APIs/paccurate.io/0.1.1/swagger.yaml': 0, 'APIs/googleapis.com/admin/datatransfer_v1/swagger.yaml': 0, 'APIs/here.com/tracking/2.0.0/swagger.yaml': 1, 'APIs/reverb.com/3.0/swagger.yaml': 8, 'APIs/amazonaws.com/firehose/2015-08-04/swagger.yaml': 2, 'APIs/googleapis.com/tpu/v1/swagger.yaml': 1, 'APIs/squareup.com/2.0/swagger.yaml': 2, 'APIs/googleapis.com/serviceconsumermanagement/v1/swagger.yaml': 0, 'APIs/googleapis.com/remotebuildexecution/v2/swagger.yaml': 0, 'APIs/getgo.com/gototraining/1.0.0/swagger.yaml': 0, 'APIs/googleapis.com/dialogflow/v2/swagger.yaml': 0, 'APIs/googleapis.com/youtube/v3/swagger.yaml': 3, 'APIs/googleapis.com/driveactivity/v2/swagger.yaml': 0, 'APIs/amazonaws.com/servicecatalog/2015-12-10/swagger.yaml': 1, 'APIs/docker.com/engine/1.33/swagger.yaml': 0, 'APIs/docusign.net/v2/swagger.yaml': 1, 'APIs/contribly.com/1.0.0/swagger.yaml': 1, 'APIs/googleapis.com/doubleclicksearch/v2/swagger.yaml': 2, 'APIs/amazonaws.com/secretsmanager/2017-10-17/swagger.yaml': 1, 'APIs/vimeo.com/3.4/openapi.yaml': 0, 'APIs/googleapis.com/serviceusage/v1/swagger.yaml': 0, 'APIs/nytimes.com/community/3.0.0/swagger.yaml': 0, 'APIs/googleapis.com/gmail/v1/swagger.yaml': 0, 'APIs/googleapis.com/servicemanagement/v1/swagger.yaml': 0, 'APIs/nexmo.com/number-insight/1.0.4/openapi.yaml': 0, 'APIs/amazonaws.com/cloudfront/2018-11-05/swagger.yaml': 2, 'APIs/googleapis.com/genomics/v1/swagger.yaml': 0, 'APIs/amazonaws.com/cloudtrail/2013-11-01/swagger.yaml': 0, 'APIs/lyft.com/1.0.0/swagger.yaml': 1, 'APIs/googleapis.com/drive/v3/swagger.yaml': 17, 'APIs/getgo.com/gotowebinar/1.0.0/swagger.yaml': 0, 'APIs/googleapis.com/compute/v1/swagger.yaml': 103, 'APIs/googleapis.com/playcustomapp/v1/swagger.yaml': 0, 'APIs/wmata.com/bus-route/1.0/swagger.yaml': 0, 'APIs/visagecloud.com/1.1/swagger.yaml': 0, 'APIs/bigoven.com/partner/swagger.yaml': 3, 'APIs/amazonaws.com/ram/2018-01-04/swagger.yaml': 0, 'APIs/flat.io/2.8.0/swagger.yaml': 0, 'APIs/googleapis.com/admin/reports_v1/swagger.yaml': 0, 'APIs/amazonaws.com/directconnect/2012-10-25/swagger.yaml': 0, 'APIs/amazonaws.com/elastictranscoder/2012-09-25/swagger.yaml': 0, 'APIs/amazonaws.com/storagegateway/2013-06-30/swagger.yaml': 0, 'APIs/googleapis.com/androidmanagement/v1/swagger.yaml': 2, 'APIs/googleapis.com/tasks/v1/swagger.yaml': 0, 'APIs/googleapis.com/dfareporting/v3.3/swagger.yaml': 7, 'APIs/amazonaws.com/guardduty/2017-11-28/swagger.yaml': 0, 'APIs/googleapis.com/appsactivity/v1/swagger.yaml': 0, 'APIs/googleapis.com/customsearch/v1/swagger.yaml': 0, 'APIs/googleapis.com/surveys/v2/swagger.yaml': 3, 'APIs/stripe.com/2019-09-09/swagger.yaml': 10, 'APIs/victorops.com/0.0.3/swagger.yaml': 0, 'APIs/googleapis.com/adsense/v1.4/swagger.yaml': 0, 'APIs/zuora.com/2019-09-19/swagger.yaml': 7, 'APIs/citrixonline.com/gotomeeting/1.0.0/swagger.yaml': 3, 'APIs/azure.com/containerservice-containerService/2017-07-01/swagger.yaml': 0, 'APIs/hetras-certification.net/booking/v0/swagger.yaml': 0, 'APIs/azure.com/monitor-serviceDiagnosticsSettings_API/2016-09-01/swagger.yaml': 0, 'APIs/googleapis.com/serviceuser/v1/swagger.yaml': 0, 'APIs/googleapis.com/servicecontrol/v1/swagger.yaml': 0, 'APIs/amazonaws.com/mturk-requester/2017-01-17/swagger.yaml': 0, 'APIs/nexmo.com/application/1.0.2/openapi.yaml': 0, 'APIs/netlicensing.io/2.x/swagger.yaml': 2, 'APIs/amazonaws.com/pinpoint/2016-12-01/swagger.yaml': 1, 'APIs/googleapis.com/youtubeAnalytics/v2/swagger.yaml': 0, 'APIs/bungie.net/2.0.0/swagger.yaml': 0, 'APIs/bitbucket.org/2.0/swagger.yaml': 0, 'APIs/googleapis.com/bigquery/v2/swagger.yaml': 2, 'APIs/amazonaws.com/opsworkscm/2016-11-01/swagger.yaml': 0, 'APIs/amazonaws.com/s3/2006-03-01/swagger.yaml': 0, 'APIs/youneedabudget.com/1.0.0/swagger.yaml': 0, 'APIs/googleapis.com/monitoring/v3/swagger.yaml': 1, 'APIs/googleapis.com/youtubereporting/v1/swagger.yaml': 0, 'APIs/googleapis.com/storage/v1/swagger.yaml': 0, 'APIs/googleapis.com/analytics/v3/swagger.yaml': 3}

# {'APIs/azure.com/machinelearningservices-datastore/2019-08-01/swagger.yaml': 8, 'APIs/linode.com/4.5.0/openapi.yaml': 220, 'APIs/bitbucket.org/2.0/swagger.yaml': 182, 'APIs/googleapis.com/dns/v1/swagger.yaml': 21, 'APIs/googleapis.com/container/v1/swagger.yaml': 59, 'APIs/googleapis.com/driveactivity/v2/swagger.yaml': 1, 'APIs/api2cart.com/1.0.0/swagger.yaml': 128, 'APIs/googleapis.com/people/v1/swagger.yaml': 14, 'APIs/docker.com/engine/1.33/swagger.yaml': 105, 'APIs/youneedabudget.com/1.0.0/swagger.yaml': 28, 'APIs/nba.com/1.0.0/swagger.yaml': 91, 'APIs/botify.com/1.0.0/swagger.yaml': 42, 'APIs/instagram.com/1.0.0/swagger.yaml': 27, 'APIs/adyen.com/MarketPayNotificationService/4/openapi.yaml': 14, 'APIs/contribly.com/1.0.0/swagger.yaml': 44, 'APIs/amazonaws.com/mturk-requester/2017-01-17/swagger.yaml': 39, 'APIs/googleapis.com/groupsmigration/v1/swagger.yaml': 1, 'APIs/googleapis.com/licensing/v1/swagger.yaml': 7, 'APIs/hetras-certification.net/booking/v0/swagger.yaml': 19, 'APIs/googleapis.com/playmoviespartner/v1/swagger.yaml': 6, 'APIs/npr.org/listening/2/swagger.yaml': 9, 'APIs/googleapis.com/urlshortener/v1/swagger.yaml': 3, 'APIs/googleapis.com/script/v1/swagger.yaml': 16, 'APIs/amazonaws.com/secretsmanager/2017-10-17/swagger.yaml': 18, 'APIs/amazonaws.com/cloudtrail/2013-11-01/swagger.yaml': 14, 'APIs/googleapis.com/webfonts/v1/swagger.yaml': 1, 'APIs/amazonaws.com/elastictranscoder/2012-09-25/swagger.yaml': 17, 'APIs/zuora.com/2019-09-19/swagger.yaml': 382, 'APIs/amazonaws.com/email/2010-12-01/swagger.yaml': 142, 'APIs/azure.com/resources-policyAssignments/2016-12-01/swagger.yaml': 9, 'APIs/googleapis.com/pagespeedonline/v5/swagger.yaml': 1, 'APIs/agco-ats.com/v1/swagger.yaml': 191, 'APIs/azure.com/datalake-analytics-catalog/2016-11-01/swagger.yaml': 45, 'APIs/here.com/tracking/2.0.0/swagger.yaml': 57, 'APIs/googleapis.com/androidpublisher/v3/swagger.yaml': 56, 'APIs/amazonaws.com/guardduty/2017-11-28/swagger.yaml': 45, 'APIs/amazonaws.com/iot/2015-05-28/swagger.yaml': 178, 'APIs/googleapis.com/iam/v1/swagger.yaml': 24, 'APIs/googleapis.com/gamesConfiguration/v1configuration/swagger.yaml': 13, 'APIs/amazonaws.com/apigateway/2015-07-09/swagger.yaml': 120, 'APIs/amazonaws.com/glue/2017-03-31/swagger.yaml': 123, 'APIs/googleapis.com/servicenetworking/v1/swagger.yaml': 8, 'APIs/getgo.com/gotowebinar/1.0.0/swagger.yaml': 38, 'APIs/googleapis.com/webmasters/v3/swagger.yaml': 9, 'APIs/amazonaws.com/medialive/2017-10-14/swagger.yaml': 31, 'APIs/azure.com/recoveryservicesbackup-bms/2017-07-01/swagger.yaml': 15, 'APIs/squareup.com/2.0/swagger.yaml': 96, 'APIs/amazonaws.com/ec2/2016-11-15/swagger.yaml': 718, 'APIs/googleapis.com/serviceuser/v1/swagger.yaml': 4, 'APIs/googleapis.com/playcustomapp/v1/swagger.yaml': 1, 'APIs/googleapis.com/verifiedaccess/v1/swagger.yaml': 2, 'APIs/amazonaws.com/logs/2014-03-28/swagger.yaml': 39, 'APIs/docusign.net/v2/swagger.yaml': 315, 'APIs/nexmo.com/application/1.0.2/openapi.yaml': 5, 'APIs/amazonaws.com/shield/2016-06-02/swagger.yaml': 18, 'APIs/rebilly.com/2.1/swagger.yaml': 149, 'APIs/lyft.com/1.0.0/swagger.yaml': 16, 'APIs/googleapis.com/oauth2/v2/swagger.yaml': 4, 'APIs/googleapis.com/youtubereporting/v1/swagger.yaml': 8, 'APIs/visagecloud.com/1.1/swagger.yaml': 52, 'APIs/azure.com/servicefabric/6.5.0.36/swagger.yaml': 234, 'APIs/googleapis.com/serviceconsumermanagement/v1/swagger.yaml': 12, 'APIs/jira.local/1.0.0/swagger.yaml': 324, 'APIs/stripe.com/2019-09-09/swagger.yaml': 348, 'APIs/azure.com/recoveryservicessiterecovery-service/2016-08-10/swagger.yaml': 102, 'APIs/googleapis.com/admin/datatransfer_v1/swagger.yaml': 5, 'APIs/googleapis.com/logging/v2/swagger.yaml': 21, 'APIs/googleapis.com/androidmanagement/v1/swagger.yaml': 13, 'APIs/amazonaws.com/codebuild/2016-10-06/swagger.yaml': 19, 'APIs/amazonaws.com/cognito-idp/2016-04-18/swagger.yaml': 100, 'APIs/taxamo.com/1/swagger.yaml': 36, 'APIs/amazonaws.com/iotthingsgraph/2018-09-06/swagger.yaml': 35, 'APIs/bulksms.com/1.0.0/swagger.yaml': 11, 'APIs/googleapis.com/adsense/v1.4/swagger.yaml': 39, 'APIs/azure.com/monitor-serviceDiagnosticsSettings_API/2016-09-01/swagger.yaml': 3, 'APIs/amazonaws.com/firehose/2015-08-04/swagger.yaml': 12, 'APIs/gov.bc.ca/geocoder/2.0.0/openapi.yaml': 16, 'APIs/googleapis.com/siteVerification/v1/swagger.yaml': 7, 'APIs/googleapis.com/plus/v1/swagger.yaml': 9, 'APIs/vimeo.com/3.4/openapi.yaml': 326, 'APIs/import.io/run/1.0/swagger.yaml': 2, 'APIs/googleapis.com/dfareporting/v3.3/swagger.yaml': 204, 'APIs/azure.com/eventhub-EventHub/2017-04-01/swagger.yaml': 43, 'APIs/vocadb.net/v1/swagger.yaml': 117, 'APIs/googleapis.com/tagmanager/v1/swagger.yaml': 49, 'APIs/googleapis.com/adexchangeseller/v2.0/swagger.yaml': 14, 'APIs/azure.com/compute/2019-03-01/swagger.yaml': 109, 'APIs/googleapis.com/youtube/v3/swagger.yaml': 73, 'APIs/amazonaws.com/lightsail/2016-11-28/swagger.yaml': 105, 'APIs/googleapis.com/spectrum/v1explorer/swagger.yaml': 6, 'APIs/amazonaws.com/lambda/2015-03-31/swagger.yaml': 39, 'APIs/wmata.com/incidents/1.0/swagger.yaml': 6, 'APIs/import.io/data/1.0/swagger.yaml': 2, 'APIs/azure.com/web-WebApps/2018-11-01/swagger.yaml': 349, 'APIs/googleapis.com/books/v1/swagger.yaml': 51, 'APIs/googleapis.com/groupssettings/v1/swagger.yaml': 3, 'APIs/sportsdata.io/nfl-v3-scores/1.0/swagger.yaml': 32, 'APIs/azure.com/search-searchservice/2019-05-06/swagger.yaml': 31, 'APIs/sportsdata.io/nfl-v3-stats/1.0/swagger.yaml': 73, 'APIs/hetras-certification.net/hotel/v0/swagger.yaml': 21, 'APIs/azure.com/databox/2019-09-01/swagger.yaml': 16, 'APIs/nytimes.com/community/3.0.0/swagger.yaml': 4, 'APIs/kubernetes.io/v1.17.0/swagger.yaml': 1126, 'APIs/googleapis.com/reseller/v1/swagger.yaml': 17, 'APIs/dracoon.team/4.5.0/swagger.yaml': 170, 'APIs/googleapis.com/gmail/v1/swagger.yaml': 68, 'APIs/import.io/schedule/1.0/swagger.yaml': 4, 'APIs/getgo.com/gototraining/1.0.0/swagger.yaml': 22, 'APIs/anchore.io/0.1.12/swagger.yaml': 86, 'APIs/reverb.com/3.0/swagger.yaml': 162, 'APIs/wowza.com/1/swagger.yaml': 104, 'APIs/wmata.com/rail-station/1.0/swagger.yaml': 16, 'APIs/nexmo.com/number-insight/1.0.4/openapi.yaml': 4, 'APIs/amazonaws.com/comprehendmedical/2018-10-30/swagger.yaml': 11, 'APIs/amazonaws.com/rds/2014-10-31/swagger.yaml': 222, 'APIs/googleapis.com/testing/v1/swagger.yaml': 5, 'APIs/amazonaws.com/resource-groups/2017-11-27/swagger.yaml': 12, 'APIs/googleapis.com/androidenterprise/v1/swagger.yaml': 86, 'APIs/googleapis.com/appstate/v1/swagger.yaml': 5, 'APIs/bigoven.com/partner/swagger.yaml': 68, 'APIs/googleapis.com/civicinfo/v2/swagger.yaml': 5, 'APIs/azure.com/recoveryservices-replicationusages/2016-06-01/swagger.yaml': 1, 'APIs/googleapis.com/calendar/v3/swagger.yaml': 37, 'APIs/amazonaws.com/pinpoint/2016-12-01/swagger.yaml': 79, 'APIs/flat.io/2.8.0/swagger.yaml': 70, 'APIs/googleapis.com/storage/v1/swagger.yaml': 52, 'APIs/googleapis.com/appengine/v1/swagger.yaml': 38, 'APIs/googleapis.com/gamesManagement/v1management/swagger.yaml': 27, 'APIs/shutterstock.com/1.0.15/openapi.yaml': 75, 'APIs/wmata.com/bus-route/1.0/swagger.yaml': 12, 'APIs/amazonaws.com/discovery/2015-11-01/swagger.yaml': 25, 'APIs/googleapis.com/fusiontables/v2/swagger.yaml': 34, 'APIs/noosh.com/1.0/swagger.yaml': 63, 'APIs/googleapis.com/dialogflow/v2/swagger.yaml': 28, 'APIs/googleapis.com/dlp/v2/swagger.yaml': 24, 'APIs/amazonaws.com/elasticache/2015-02-02/swagger.yaml': 92, 'APIs/amazonaws.com/directconnect/2012-10-25/swagger.yaml': 53, 'APIs/googleapis.com/plusDomains/v1/swagger.yaml': 10, 'APIs/amazonaws.com/swf/2012-01-25/swagger.yaml': 37, 'APIs/tomtom.com/search/1.0.0/openapi.yaml': 19, 'APIs/azure.com/servicefabric-application/2019-03-01/swagger.yaml': 19, 'APIs/googleapis.com/clouddebugger/v2/swagger.yaml': 8, 'APIs/amazonaws.com/s3/2006-03-01/swagger.yaml': 88, 'APIs/googleapis.com/cloudbilling/v1/swagger.yaml': 12, 'APIs/amazonaws.com/ram/2018-01-04/swagger.yaml': 17, 'APIs/amazonaws.com/elasticbeanstalk/2010-12-01/swagger.yaml': 88, 'APIs/thetvdb.com/2.2.0/swagger.yaml': 30, 'APIs/googleapis.com/customsearch/v1/swagger.yaml': 2, 'APIs/googleapis.com/blogger/v3/swagger.yaml': 33, 'APIs/crucible.local/1.0.0/swagger.yaml': 79, 'APIs/googleapis.com/spanner/v1/swagger.yaml': 28, 'APIs/amazonaws.com/ssm/2014-11-06/swagger.yaml': 120, 'APIs/bungie.net/2.0.0/swagger.yaml': 94, 'APIs/googleapis.com/sheets/v4/swagger.yaml': 17, 'APIs/rbaskets.in/1.0.0/swagger.yaml': 20, 'APIs/googleapis.com/tpu/v1/swagger.yaml': 12, 'APIs/bunq.com/1.0/openapi.yaml': 392, 'APIs/bbc.com/1.0.0/openapi.yaml': 25, 'APIs/azure.com/datafactory/2018-06-01/swagger.yaml': 76, 'APIs/amazonaws.com/opsworkscm/2016-11-01/swagger.yaml': 16, 'APIs/googleapis.com/compute/v1/swagger.yaml': 480, 'APIs/amazonaws.com/codedeploy/2014-10-06/swagger.yaml': 46, 'APIs/googleapis.com/adsensehost/v4.1/swagger.yaml': 26, 'APIs/googleapis.com/discovery/v1/swagger.yaml': 2, 'APIs/victorops.com/0.0.3/swagger.yaml': 72, 'APIs/storecove.com/2.0.1/swagger.yaml': 21, 'APIs/googleapis.com/servicemanagement/v1/swagger.yaml': 21, 'APIs/beezup.com/2.0/swagger.yaml': 200, 'APIs/googleapis.com/monitoring/v3/swagger.yaml': 24, 'APIs/amazonaws.com/mediapackage/2017-10-12/swagger.yaml': 18, 'APIs/azure.com/apimanagement-apimdeployment/2018-01-01/swagger.yaml': 15, 'APIs/googleapis.com/partners/v2/swagger.yaml': 17, 'APIs/whatsapp.local/1.0/openapi.yaml': 55, 'APIs/amazonaws.com/storagegateway/2013-06-30/swagger.yaml': 73, 'APIs/googleapis.com/drive/v3/swagger.yaml': 46, 'APIs/gitlab.com/v3/swagger.yaml': 358, 'APIs/googleapis.com/servicecontrol/v1/swagger.yaml': 3, 'APIs/netlicensing.io/2.x/swagger.yaml': 40, 'APIs/github.com/v3/swagger.yaml': 244, 'APIs/gitea.io/1.1.1/swagger.yaml': 191, 'APIs/azure.com/signalr/2018-10-01/swagger.yaml': 12, 'APIs/import.io/extraction/1.0/swagger.yaml': 1, 'APIs/azure.com/containerservice-managedClusters/2017-08-31/swagger.yaml': 8, 'APIs/cloudmersive.com/ocr/v1/swagger.yaml': 16, 'APIs/googleapis.com/adexchangebuyer/v1.4/swagger.yaml': 38, 'APIs/azure.com/sql-tableAuditing/2014-04-01/swagger.yaml': 8, 'APIs/googleapis.com/serviceusage/v1/swagger.yaml': 8, 'APIs/googleapis.com/doubleclickbidmanager/v1/swagger.yaml': 9, 'APIs/import.io/rss/1.0/swagger.yaml': 1, 'APIs/slack.com/1.2.0/swagger.yaml': 140, 'APIs/transitfeeds.com/1.0.0/swagger.yaml': 4, 'APIs/netatmo.net/1.1.1/swagger.yaml': 20, 'APIs/googleapis.com/games/v1/swagger.yaml': 53, 'APIs/googleapis.com/admin/directory_v1/swagger.yaml': 113, 'APIs/googleapis.com/content/v2.1/swagger.yaml': 94, 'APIs/googleapis.com/dataflow/v1b3/swagger.yaml': 30, 'APIs/amazonaws.com/elasticmapreduce/2009-03-31/swagger.yaml': 29, 'APIs/azure.com/applicationinsights-componentContinuousExport_API/2015-05-01/swagger.yaml': 5, 'APIs/googleapis.com/bigquery/v2/swagger.yaml': 31, 'APIs/googleapis.com/remotebuildexecution/v2/swagger.yaml': 9, 'APIs/googleapis.com/genomics/v1/swagger.yaml': 2, 'APIs/azure.com/redis/2015-08-01/swagger.yaml': 8, 'APIs/amazonaws.com/cloudfront/2018-11-05/swagger.yaml': 45, 'APIs/googleapis.com/bigquerydatatransfer/v1/swagger.yaml': 12, 'APIs/setlist.fm/1.0/swagger.yaml': 15, 'APIs/googleapis.com/doubleclicksearch/v2/swagger.yaml': 10, 'APIs/billbee.io/v1/swagger.yaml': 67, 'APIs/googleapis.com/admin/reports_v1/swagger.yaml': 6, 'APIs/googleapis.com/deploymentmanager/v2/swagger.yaml': 18, 'APIs/amazonaws.com/servicecatalog/2015-12-10/swagger.yaml': 83, 'APIs/googleapis.com/analytics/v3/swagger.yaml': 88, 'APIs/googleapis.com/mirror/v1/swagger.yaml': 24, 'APIs/googleapis.com/bigtableadmin/v2/swagger.yaml': 22, 'APIs/osf.io/2.0/swagger.yaml': 153, 'APIs/citrixonline.com/gotomeeting/1.0.0/swagger.yaml': 26, 'APIs/googleapis.com/appsactivity/v1/swagger.yaml': 1, 'APIs/googleapis.com/slides/v1/swagger.yaml': 5, 'APIs/iva-api.com/2.0/swagger.yaml': 153, 'APIs/paccurate.io/0.1.1/swagger.yaml': 1, 'APIs/weatherbit.io/2.0.0/swagger.yaml': 64, 'APIs/amazonaws.com/rds-data/2018-08-01/swagger.yaml': 6, 'APIs/googleapis.com/identitytoolkit/v3/swagger.yaml': 20, 'APIs/googleapis.com/youtubeAnalytics/v2/swagger.yaml': 8, 'APIs/googleapis.com/sourcerepo/v1/swagger.yaml': 11, 'APIs/googleapis.com/surveys/v2/swagger.yaml': 8, 'APIs/googleapis.com/vision/v1/swagger.yaml': 23, 'APIs/atlassian.com/jira/v3/swagger.yaml': 317, 'APIs/googleapis.com/fitness/v1/swagger.yaml': 13, 'APIs/googleapis.com/tasks/v1/swagger.yaml': 8, 'APIs/azure.com/containerservice-containerService/2017-07-01/swagger.yaml': 5, 'APIs/googleapis.com/jobs/v2/swagger.yaml': 14}
# results = {'APIs/azure.com/machinelearningservices-datastore/2019-08-01/swagger.yaml': 0, 'APIs/linode.com/4.5.0/openapi.yaml': 1, 'APIs/bitbucket.org/2.0/swagger.yaml': 1, 'APIs/googleapis.com/dns/v1/swagger.yaml': 0, 'APIs/googleapis.com/container/v1/swagger.yaml': 0, 'APIs/googleapis.com/driveactivity/v2/swagger.yaml': 0, 'APIs/api2cart.com/1.0.0/swagger.yaml': 1, 'APIs/googleapis.com/people/v1/swagger.yaml': 1, 'APIs/docker.com/engine/1.33/swagger.yaml': 0, 'APIs/youneedabudget.com/1.0.0/swagger.yaml': 0, 'APIs/nba.com/1.0.0/swagger.yaml': 8, 'APIs/botify.com/1.0.0/swagger.yaml': 0, 'APIs/instagram.com/1.0.0/swagger.yaml': 3, 'APIs/adyen.com/MarketPayNotificationService/4/openapi.yaml': 0, 'APIs/contribly.com/1.0.0/swagger.yaml': 0, 'APIs/amazonaws.com/mturk-requester/2017-01-17/swagger.yaml': 0, 'APIs/googleapis.com/groupsmigration/v1/swagger.yaml': 0, 'APIs/googleapis.com/licensing/v1/swagger.yaml': 0, 'APIs/hetras-certification.net/booking/v0/swagger.yaml': 0, 'APIs/googleapis.com/playmoviespartner/v1/swagger.yaml': 0, 'APIs/npr.org/listening/2/swagger.yaml': 0, 'APIs/googleapis.com/urlshortener/v1/swagger.yaml': 0, 'APIs/googleapis.com/script/v1/swagger.yaml': 0, 'APIs/amazonaws.com/secretsmanager/2017-10-17/swagger.yaml': 3, 'APIs/amazonaws.com/cloudtrail/2013-11-01/swagger.yaml': 0, 'APIs/googleapis.com/webfonts/v1/swagger.yaml': 0, 'APIs/amazonaws.com/elastictranscoder/2012-09-25/swagger.yaml': 1, 'APIs/zuora.com/2019-09-19/swagger.yaml': 0, 'APIs/amazonaws.com/email/2010-12-01/swagger.yaml': 6, 'APIs/azure.com/resources-policyAssignments/2016-12-01/swagger.yaml': 1, 'APIs/googleapis.com/pagespeedonline/v5/swagger.yaml': 0, 'APIs/agco-ats.com/v1/swagger.yaml': 1, 'APIs/azure.com/datalake-analytics-catalog/2016-11-01/swagger.yaml': 5, 'APIs/here.com/tracking/2.0.0/swagger.yaml': 0, 'APIs/googleapis.com/androidpublisher/v3/swagger.yaml': 0, 'APIs/amazonaws.com/guardduty/2017-11-28/swagger.yaml': 0, 'APIs/amazonaws.com/iot/2015-05-28/swagger.yaml': 6, 'APIs/googleapis.com/iam/v1/swagger.yaml': 3, 'APIs/googleapis.com/gamesConfiguration/v1configuration/swagger.yaml': 0, 'APIs/amazonaws.com/apigateway/2015-07-09/swagger.yaml': 0, 'APIs/amazonaws.com/glue/2017-03-31/swagger.yaml': 0, 'APIs/googleapis.com/servicenetworking/v1/swagger.yaml': 0, 'APIs/getgo.com/gotowebinar/1.0.0/swagger.yaml': 0, 'APIs/googleapis.com/webmasters/v3/swagger.yaml': 0, 'APIs/amazonaws.com/medialive/2017-10-14/swagger.yaml': 0, 'APIs/azure.com/recoveryservicesbackup-bms/2017-07-01/swagger.yaml': 0, 'APIs/squareup.com/2.0/swagger.yaml': 2, 'APIs/amazonaws.com/ec2/2016-11-15/swagger.yaml': 0, 'APIs/googleapis.com/serviceuser/v1/swagger.yaml': 0, 'APIs/googleapis.com/playcustomapp/v1/swagger.yaml': 0, 'APIs/googleapis.com/verifiedaccess/v1/swagger.yaml': 0, 'APIs/amazonaws.com/logs/2014-03-28/swagger.yaml': 0, 'APIs/docusign.net/v2/swagger.yaml': 2, 'APIs/nexmo.com/application/1.0.2/openapi.yaml': 0, 'APIs/amazonaws.com/shield/2016-06-02/swagger.yaml': 1, 'APIs/rebilly.com/2.1/swagger.yaml': 0, 'APIs/lyft.com/1.0.0/swagger.yaml': 0, 'APIs/googleapis.com/oauth2/v2/swagger.yaml': 0, 'APIs/googleapis.com/youtubereporting/v1/swagger.yaml': 0, 'APIs/visagecloud.com/1.1/swagger.yaml': 10, 'APIs/azure.com/servicefabric/6.5.0.36/swagger.yaml': 0, 'APIs/googleapis.com/serviceconsumermanagement/v1/swagger.yaml': 0, 'APIs/jira.local/1.0.0/swagger.yaml': 2, 'APIs/stripe.com/2019-09-09/swagger.yaml': 15, 'APIs/azure.com/recoveryservicessiterecovery-service/2016-08-10/swagger.yaml': 0, 'APIs/googleapis.com/admin/datatransfer_v1/swagger.yaml': 0, 'APIs/googleapis.com/logging/v2/swagger.yaml': 0, 'APIs/googleapis.com/androidmanagement/v1/swagger.yaml': 0, 'APIs/amazonaws.com/codebuild/2016-10-06/swagger.yaml': 0, 'APIs/amazonaws.com/cognito-idp/2016-04-18/swagger.yaml': 0, 'APIs/taxamo.com/1/swagger.yaml': 0, 'APIs/amazonaws.com/iotthingsgraph/2018-09-06/swagger.yaml': 3, 'APIs/bulksms.com/1.0.0/swagger.yaml': 0, 'APIs/googleapis.com/adsense/v1.4/swagger.yaml': 0, 'APIs/azure.com/monitor-serviceDiagnosticsSettings_API/2016-09-01/swagger.yaml': 3, 'APIs/amazonaws.com/firehose/2015-08-04/swagger.yaml': 0, 'APIs/gov.bc.ca/geocoder/2.0.0/openapi.yaml': 0, 'APIs/googleapis.com/siteVerification/v1/swagger.yaml': 0, 'APIs/googleapis.com/plus/v1/swagger.yaml': 0, 'APIs/vimeo.com/3.4/openapi.yaml': 0, 'APIs/import.io/run/1.0/swagger.yaml': 0, 'APIs/googleapis.com/dfareporting/v3.3/swagger.yaml': 0, 'APIs/azure.com/eventhub-EventHub/2017-04-01/swagger.yaml': 0, 'APIs/vocadb.net/v1/swagger.yaml': 2, 'APIs/googleapis.com/tagmanager/v1/swagger.yaml': 0, 'APIs/googleapis.com/adexchangeseller/v2.0/swagger.yaml': 0, 'APIs/azure.com/compute/2019-03-01/swagger.yaml': 1, 'APIs/googleapis.com/youtube/v3/swagger.yaml': 0, 'APIs/amazonaws.com/lightsail/2016-11-28/swagger.yaml': 0, 'APIs/googleapis.com/spectrum/v1explorer/swagger.yaml': 0, 'APIs/amazonaws.com/lambda/2015-03-31/swagger.yaml': 1, 'APIs/wmata.com/incidents/1.0/swagger.yaml': 4, 'APIs/import.io/data/1.0/swagger.yaml': 0, 'APIs/azure.com/web-WebApps/2018-11-01/swagger.yaml': 2, 'APIs/googleapis.com/books/v1/swagger.yaml': 0, 'APIs/googleapis.com/groupssettings/v1/swagger.yaml': 0, 'APIs/sportsdata.io/nfl-v3-scores/1.0/swagger.yaml': 2, 'APIs/azure.com/search-searchservice/2019-05-06/swagger.yaml': 0, 'APIs/sportsdata.io/nfl-v3-stats/1.0/swagger.yaml': 2, 'APIs/hetras-certification.net/hotel/v0/swagger.yaml': 0, 'APIs/azure.com/databox/2019-09-01/swagger.yaml': 1, 'APIs/nytimes.com/community/3.0.0/swagger.yaml': 0, 'APIs/kubernetes.io/v1.17.0/swagger.yaml': 216, 'APIs/googleapis.com/reseller/v1/swagger.yaml': 0, 'APIs/dracoon.team/4.5.0/swagger.yaml': 13, 'APIs/googleapis.com/gmail/v1/swagger.yaml': 0, 'APIs/import.io/schedule/1.0/swagger.yaml': 0, 'APIs/getgo.com/gototraining/1.0.0/swagger.yaml': 1, 'APIs/anchore.io/0.1.12/swagger.yaml': 0, 'APIs/reverb.com/3.0/swagger.yaml': 0, 'APIs/wowza.com/1/swagger.yaml': 4, 'APIs/wmata.com/rail-station/1.0/swagger.yaml': 2, 'APIs/nexmo.com/number-insight/1.0.4/openapi.yaml': 0, 'APIs/amazonaws.com/comprehendmedical/2018-10-30/swagger.yaml': 1, 'APIs/amazonaws.com/rds/2014-10-31/swagger.yaml': 0, 'APIs/googleapis.com/testing/v1/swagger.yaml': 0, 'APIs/amazonaws.com/resource-groups/2017-11-27/swagger.yaml': 0, 'APIs/googleapis.com/androidenterprise/v1/swagger.yaml': 0, 'APIs/googleapis.com/appstate/v1/swagger.yaml': 0, 'APIs/bigoven.com/partner/swagger.yaml': 5, 'APIs/googleapis.com/civicinfo/v2/swagger.yaml': 0, 'APIs/azure.com/recoveryservices-replicationusages/2016-06-01/swagger.yaml': 0, 'APIs/googleapis.com/calendar/v3/swagger.yaml': 0, 'APIs/amazonaws.com/pinpoint/2016-12-01/swagger.yaml': 0, 'APIs/flat.io/2.8.0/swagger.yaml': 1, 'APIs/googleapis.com/storage/v1/swagger.yaml': 0, 'APIs/googleapis.com/appengine/v1/swagger.yaml': 0, 'APIs/googleapis.com/gamesManagement/v1management/swagger.yaml': 0, 'APIs/shutterstock.com/1.0.15/openapi.yaml': 0, 'APIs/wmata.com/bus-route/1.0/swagger.yaml': 6, 'APIs/amazonaws.com/discovery/2015-11-01/swagger.yaml': 2, 'APIs/googleapis.com/fusiontables/v2/swagger.yaml': 0, 'APIs/noosh.com/1.0/swagger.yaml': 1, 'APIs/googleapis.com/dialogflow/v2/swagger.yaml': 0, 'APIs/googleapis.com/dlp/v2/swagger.yaml': 0, 'APIs/amazonaws.com/elasticache/2015-02-02/swagger.yaml': 0, 'APIs/amazonaws.com/directconnect/2012-10-25/swagger.yaml': 4, 'APIs/googleapis.com/plusDomains/v1/swagger.yaml': 0, 'APIs/amazonaws.com/swf/2012-01-25/swagger.yaml': 6, 'APIs/tomtom.com/search/1.0.0/openapi.yaml': 5, 'APIs/azure.com/servicefabric-application/2019-03-01/swagger.yaml': 0, 'APIs/googleapis.com/clouddebugger/v2/swagger.yaml': 0, 'APIs/amazonaws.com/s3/2006-03-01/swagger.yaml': 4, 'APIs/googleapis.com/cloudbilling/v1/swagger.yaml': 0, 'APIs/amazonaws.com/ram/2018-01-04/swagger.yaml': 0, 'APIs/amazonaws.com/elasticbeanstalk/2010-12-01/swagger.yaml': 0, 'APIs/thetvdb.com/2.2.0/swagger.yaml': 1, 'APIs/googleapis.com/customsearch/v1/swagger.yaml': 0, 'APIs/googleapis.com/blogger/v3/swagger.yaml': 0, 'APIs/crucible.local/1.0.0/swagger.yaml': 1, 'APIs/googleapis.com/spanner/v1/swagger.yaml': 0, 'APIs/amazonaws.com/ssm/2014-11-06/swagger.yaml': 0, 'APIs/bungie.net/2.0.0/swagger.yaml': 0, 'APIs/googleapis.com/sheets/v4/swagger.yaml': 0, 'APIs/rbaskets.in/1.0.0/swagger.yaml': 9, 'APIs/googleapis.com/tpu/v1/swagger.yaml': 0, 'APIs/bunq.com/1.0/openapi.yaml': 9, 'APIs/bbc.com/1.0.0/openapi.yaml': 1, 'APIs/azure.com/datafactory/2018-06-01/swagger.yaml': 0, 'APIs/amazonaws.com/opsworkscm/2016-11-01/swagger.yaml': 0, 'APIs/googleapis.com/compute/v1/swagger.yaml': 1, 'APIs/amazonaws.com/codedeploy/2014-10-06/swagger.yaml': 5, 'APIs/googleapis.com/adsensehost/v4.1/swagger.yaml': 0, 'APIs/googleapis.com/discovery/v1/swagger.yaml': 0, 'APIs/victorops.com/0.0.3/swagger.yaml': 4, 'APIs/storecove.com/2.0.1/swagger.yaml': 0, 'APIs/googleapis.com/servicemanagement/v1/swagger.yaml': 0, 'APIs/beezup.com/2.0/swagger.yaml': 0, 'APIs/googleapis.com/monitoring/v3/swagger.yaml': 0, 'APIs/amazonaws.com/mediapackage/2017-10-12/swagger.yaml': 1, 'APIs/azure.com/apimanagement-apimdeployment/2018-01-01/swagger.yaml': 2, 'APIs/googleapis.com/partners/v2/swagger.yaml': 0, 'APIs/whatsapp.local/1.0/openapi.yaml': 0, 'APIs/amazonaws.com/storagegateway/2013-06-30/swagger.yaml': 2, 'APIs/googleapis.com/drive/v3/swagger.yaml': 5, 'APIs/gitlab.com/v3/swagger.yaml': 13, 'APIs/googleapis.com/servicecontrol/v1/swagger.yaml': 0, 'APIs/netlicensing.io/2.x/swagger.yaml': 0, 'APIs/github.com/v3/swagger.yaml': 13, 'APIs/gitea.io/1.1.1/swagger.yaml': 2, 'APIs/azure.com/signalr/2018-10-01/swagger.yaml': 0, 'APIs/import.io/extraction/1.0/swagger.yaml': 0, 'APIs/azure.com/containerservice-managedClusters/2017-08-31/swagger.yaml': 1, 'APIs/cloudmersive.com/ocr/v1/swagger.yaml': 1, 'APIs/googleapis.com/adexchangebuyer/v1.4/swagger.yaml': 0, 'APIs/azure.com/sql-tableAuditing/2014-04-01/swagger.yaml': 8, 'APIs/googleapis.com/serviceusage/v1/swagger.yaml': 0, 'APIs/googleapis.com/doubleclickbidmanager/v1/swagger.yaml': 0, 'APIs/import.io/rss/1.0/swagger.yaml': 0, 'APIs/slack.com/1.2.0/swagger.yaml': 1, 'APIs/transitfeeds.com/1.0.0/swagger.yaml': 0, 'APIs/netatmo.net/1.1.1/swagger.yaml': 3, 'APIs/googleapis.com/games/v1/swagger.yaml': 0, 'APIs/googleapis.com/admin/directory_v1/swagger.yaml': 0, 'APIs/googleapis.com/content/v2.1/swagger.yaml': 1, 'APIs/googleapis.com/dataflow/v1b3/swagger.yaml': 0, 'APIs/amazonaws.com/elasticmapreduce/2009-03-31/swagger.yaml': 2, 'APIs/azure.com/applicationinsights-componentContinuousExport_API/2015-05-01/swagger.yaml': 0, 'APIs/googleapis.com/bigquery/v2/swagger.yaml': 0, 'APIs/googleapis.com/remotebuildexecution/v2/swagger.yaml': 0, 'APIs/googleapis.com/genomics/v1/swagger.yaml': 0, 'APIs/azure.com/redis/2015-08-01/swagger.yaml': 0, 'APIs/amazonaws.com/cloudfront/2018-11-05/swagger.yaml': 0, 'APIs/googleapis.com/bigquerydatatransfer/v1/swagger.yaml': 1, 'APIs/setlist.fm/1.0/swagger.yaml': 0, 'APIs/googleapis.com/doubleclicksearch/v2/swagger.yaml': 0, 'APIs/billbee.io/v1/swagger.yaml': 1, 'APIs/googleapis.com/admin/reports_v1/swagger.yaml': 0, 'APIs/googleapis.com/deploymentmanager/v2/swagger.yaml': 0, 'APIs/amazonaws.com/servicecatalog/2015-12-10/swagger.yaml': 0, 'APIs/googleapis.com/analytics/v3/swagger.yaml': 0, 'APIs/googleapis.com/mirror/v1/swagger.yaml': 0, 'APIs/googleapis.com/bigtableadmin/v2/swagger.yaml': 0, 'APIs/osf.io/2.0/swagger.yaml': 4, 'APIs/citrixonline.com/gotomeeting/1.0.0/swagger.yaml': 3, 'APIs/googleapis.com/appsactivity/v1/swagger.yaml': 0, 'APIs/googleapis.com/slides/v1/swagger.yaml': 0, 'APIs/iva-api.com/2.0/swagger.yaml': 3, 'APIs/paccurate.io/0.1.1/swagger.yaml': 0, 'APIs/weatherbit.io/2.0.0/swagger.yaml': 0, 'APIs/amazonaws.com/rds-data/2018-08-01/swagger.yaml': 1, 'APIs/googleapis.com/identitytoolkit/v3/swagger.yaml': 0, 'APIs/googleapis.com/youtubeAnalytics/v2/swagger.yaml': 0, 'APIs/googleapis.com/sourcerepo/v1/swagger.yaml': 0, 'APIs/googleapis.com/surveys/v2/swagger.yaml': 0, 'APIs/googleapis.com/vision/v1/swagger.yaml': 0, 'APIs/atlassian.com/jira/v3/swagger.yaml': 5, 'APIs/googleapis.com/fitness/v1/swagger.yaml': 0, 'APIs/googleapis.com/tasks/v1/swagger.yaml': 0, 'APIs/azure.com/containerservice-containerService/2017-07-01/swagger.yaml': 5, 'APIs/googleapis.com/jobs/v2/swagger.yaml': 3}

# 226
# APIs/hetras-certification.net/hotel/v0/swagger.yaml
# APIs/azure.com/recoveryservices-replicationusages/2016-06-01/swagger.yaml
# APIs/hetras-certification.net/booking/v0/swagger.yaml
# APIs/googleapis.com/youtubereporting/v1/swagger.yaml
# APIs/googleapis.com/testing/v1/swagger.yaml
# 814
# 244
# 210




