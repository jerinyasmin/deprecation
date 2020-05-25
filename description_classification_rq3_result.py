import csv
import os
import random
import re

from bs4 import BeautifulSoup
from sklearn.metrics import precision_recall_fscore_support as pr
only_keys = ['amazonaws.com_elastictranscoder', 'azure.com_resources-policyAssignments'
,'amazonaws.com_lambda'
, 'azure.com_containerservice-containerService'
, 'billbee.io'
, 'cloudmersive.com_ocr'
, 'amazonaws.com_shield'
, 'azure.com_containerservice-managedClusters'
, 'amazonaws.com_s3'
, 'gitea.io'
, 'adyen.com_MarketPayNotificationService'
, 'rbaskets.in'
, 'visagecloud.com'
, 'tomtom.com_search'
, 'netatmo.net'
, 'bitbucket.org']


alternate_infos = {}
op_infos = {}
infos = ['bulksms.com', 'gov.bc.ca_geocoder', 'nexmo.com_application', 'nytimes.com_community']

op_infos['bulksms.com'] = 11 #reason
op_infos['gov.bc.ca_geocoder'] = 16 #more info
op_infos['nexmo.com_application'] = 5
op_infos['nytimes.com_community'] = 4



# alternate_infos['bulksms.com'] = 11 #reason
# alternate_infos['gov.bc.ca_geocoder'] = 16 #more info
# alternate_infos['nexmo.com_application'] = 5
# alternate_infos['nytimes.com_community'] = 0

alternate_infos['bulksms.com'] = 11 #reason
alternate_infos['gov.bc.ca_geocoder'] = 0 #more info
alternate_infos['nexmo.com_application'] = 0
alternate_infos['nytimes.com_community'] = 0


# alternate_infos['bulksms.com'] = 0 #reason
# alternate_infos['gov.bc.ca_geocoder'] = 16 #more info
# alternate_infos['nexmo.com_application'] = 0
# alternate_infos['nytimes.com_community'] = 0


def checkAlternate(value):
    if ("recommend" in value and "don't recommend" not in value) or ("use " in value) or "deprecated by" in value or "in favor of" in value or "replaced by" in value or ("instead" in value) or ("merged into" in value) or ("see" in value and "preferred" in value):
        return True

    return False

def checkTime(description):
    # description = 'gateway address for the default "bridge" network.<p><br /></p>> **deprecated**: this field is only propagated when attached to the> default "bridge" network. use the information from the "bridge"> network inside the `networks` map instead, which contains the same> information. this field was deprecated in docker 1.9 and is scheduled> to be removed in docker 17.12.0'

    # todo: add version number will be removed in the next release
    result = ""
    # future release future api version
    values = description.split(" ")

    if ("removed in" in description or "planned" in description) and ("future" not in description):
        return True

    if "next release" in description:
        return True

    if "next version" in description or "next api" in description:
        return True

    return False

def checkReason(description):
    if "due to" in description:
        return True

    return False

def checkInfoType(description):
    result = ""

    # with link or without link
    if "release note" in description:
        return True

    # result = result + "release note"

    if "migration" in description:
        # print(description)

        return True

    if "changelog" in description:
        # print(description)
        return True

    if "for details" in description and "see" in description:
        # print(description)
        return True

    if "for more information" in description:
        return True

    return False


# all descriptions means descriptions with deprecated
def read(filename):
    with open(filename, mode='r', encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        result = []
        for row in csv_reader:
            if len(row):
                value = row[0]
                result.append(value)
            line_count += 1
    return result

#
total_deprecated_operations = {}
def read_total(filename):
    with open(filename, mode='r', encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count > 0:
                if len(row):
                    api_name = row[1]
                    count_operations_deprecated = row[3]
                    total_deprecated_operations[api_name] = count_operations_deprecated
            line_count += 1

    return total_deprecated_operations

descriptions_api = {}

def read_info(filename):
    with open(filename, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        result = {}
        # try:
        for row in csv_reader:
            if line_count > 0:
                try:
                    if len(row):
                        api_name = row[0]
                        operation = row[1]
                        texts = row[2]
                        text_per_op = [{operation: texts}]
                        if api_name in result:
                            values = result[api_name]
                            result[api_name] = values + text_per_op
                        else:
                            result[api_name] = text_per_op
                except:
                    print("error")

            line_count += 1
    return result

alternates = {}
alternates_test = {}
count = 0

all_descriptions = []

results_op = read_info("result/RQ2/deprecated_operation_descriptions.csv")
print(len(results_op))
alternate_found_file = {}
for api in results_op:
    founds = []
    desc_ops = results_op[api]
    for desc_op in desc_ops:
        for operation in desc_op:
            texts = desc_op[operation]
            alternate_found = checkReason(texts)
            if alternate_found:
                founds.append(operation)

    alternate_found_file[api] = list(set(founds))
    # print(len(alternate_found_file[api]))

print(len(alternate_found_file))

results_op_req = read_info("result/RQ2/deprecated_operation_descriptions_request.csv")
alternate_found_file_request = {}
for api in results_op_req:
    founds = []
    desc_ops = results_op_req[api]
    for desc_op in desc_ops:
        for operation in desc_op:
            texts = desc_op[operation]
            # alternate_found = checkAlternate(texts)
            alternate_found = checkReason(texts)
            if alternate_found:
                founds.append(operation)

    alternate_found_file_request[api] = list(set(founds))

print(len(alternate_found_file_request))
results_op_resp = read_info("result/RQ2/deprecated_operation_descriptions_response.csv")
alternate_found_file_response = {}
for api in results_op_resp:
    founds = []
    desc_ops = results_op_resp[api]
    for desc_op in desc_ops:
        for operation in desc_op:
            texts = desc_op[operation]
            # alternate_found = checkAlternate(texts)
            alternate_found = checkReason(texts)
            if alternate_found:
                founds.append(operation)

    alternate_found_file_response[api] = list(set(founds))


total_deprecated_operations = read_total("result/RQ2/deprecated_operation_all_bk.csv")


final_count_alternate = {}

ratio_alternate = {}

apis = []
for api in results_op:
    apis.append(api)

for api in results_op_req:
    apis.append(api)

for api in results_op_resp:
    apis.append(api)

print(len(list(set(apis))))


with open('result/RQ3/reason.csv', mode='w', encoding="utf-8") as res_file:
    res_writer = csv.writer(res_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
    res_writer.writerow(["api", "total deprecated operations", "found", "ratio"])
    for api in list(set(apis)):
        operations = []

        if api in alternate_found_file:
            operations = operations + alternate_found_file[api]
        if api in alternate_found_file_response:
            operations = operations + alternate_found_file_response[api]
        if api in alternate_found_file_request:
            operations = operations + alternate_found_file_request[api]

        final_count_alternate[api] = len(list(set(operations)))
        total_alt = len(list(set(operations)))
        total = total_deprecated_operations[api]
        # print(total)
        # print(final_count_alternate[api])
        if total != 0:
            ratio = int(final_count_alternate[api])/int(total)
            # ratio_alternate[api] = int(final_count_alternate[api])/int(total)
        else:
            ratio = 0
            ratio_alternate[api] = 0

        res_writer.writerow([api, total, total_alt, ratio])

    for api in only_keys:
        total = total_deprecated_operations[api]
        res_writer.writerow([api, total, 0, 0])

    for api in infos:
        total = op_infos[api]
        total_alt = alternate_infos[api]
        ratio = int(total_alt) / int(total)
        res_writer.writerow([api, total, total_alt, ratio])








