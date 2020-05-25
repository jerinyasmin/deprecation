import csv
import os
import random
import re

from bs4 import BeautifulSoup


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


directory = "alldesc-standard"
folder_list = os.walk(directory)

descriptions_api = {}


all_descriptions = []


for f in folder_list:
    for fs in f[2]:
        file_location = f[0] + "/" + fs

        if ".csv" in file_location:
            descriptions = read(file_location)
            for description in descriptions:
                # if "will be deprecated" not in description and "may be deprecated" not in description:
                    all_descriptions.append(description)

                    if description in descriptions_api:
                        values = descriptions_api[description]
                        descriptions_api[description] = values + [file_location]

                    else:
                        descriptions_api[description] = [file_location]



print(len(descriptions_api))
print(len(all_descriptions))
print(len(list(set(all_descriptions))))





def checkAlternate(value):
    #instead check: 233
    #see survey cost inste  #replace by @todo recommend but not "don't recommeend, call the ,please see for the preferred method????, instead of using + please, check only instead, please, merged into, keep it unspecified


    #returns an array of one or more targets associated with a deployment. this method works with all compute types and should be used instead of the deprecated batchgetdeploymentinstances. the maximum number of targets that can be returned is 25.  the type of targets returned depends on the deployment's compute platform:     ec2/on-premises: information about ec2 instance targets.     aws lambda: information about lambda functions targets.     amazon ecs: information about amazon ecs service targets.
    #

    # if "instead" in value and "use " not in value:
    #     print(value)
    # value = "post /stream_targets/add/ is deprecated. to add a stream target, use post /stream_targets instead."
    if "instead of the deprecated" in value:
        print(value)

    if "instead of using" in value and "please" in value:
        print(value)
    if "instead of using" in value:
        print(value)

    if "deprecated after" in value:
        print(value)

    if "call" in value:
        print(value)
    if "see" in value:
        print(value)

    # if "instead" in value and ("call" not in value and "set" not in value and "use" not in value and "see" not in value and "recommend" not in value):
    #     print(value)

    if ("recommend" in value and "don't recommend" in value)  or "use " in value or "deprecated by" in value or "in favor of" in value or "replaced by" in value or ("instead of using" in value and "please" in value) or ("instead" in value) or ("merged into" in value) :
        return True
    return False

def checkTime(description):
    # description = 'gateway address for the default "bridge" network.<p><br /></p>> **deprecated**: this field is only propagated when attached to the> default "bridge" network. use the information from the "bridge"> network inside the `networks` map instead, which contains the same> information. this field was deprecated in docker 1.9 and is scheduled> to be removed in docker 17.12.0'

    # todo: add version number will be removed in the next release
    result = ""
    # future release future api version
    values = description.split(" ")

    for value in values:
        if "future release" in value:
            result = result + "future release "

        if "future api version" in value:
            result = result + "future api version "

        # if "will be removed" in value: version number

        # print(value)
        # digit = re.findall('(\d+)', value)
        if value.isdigit():
            if len(value) == 4:
                result = result + value + " "   #this is for year

        if "removed" in description:
            if not value.isdigit() and any(c.isdigit() for c in value):
                print("yes")
                print(value)
                result = result + value + " "  # this is for version

        # if digit:
        #     for dg in digit:
        #
        #         if len(dg) == 4:
        #             print(dg)
        #             if 2030> int(dg) > 2015:
        #                 result = result + dg + " "
        #         if "removed" in value:
        #             result = result + dg + " " #this is for version

        months = [" january", " february", " march ", " april ", " may ", " jun", " jul", " aug", " sept", " oct", " nov", " december "]

        for month in months:
            if month in value:
                result = result + month


    if len(result):
        return result

    return False

def checkLink(description):
    # description = 'gateway address for the default "bridge" network.<p><br /></p>> **deprecated**: this field is only propagated when attached to the> default "bridge" network. use the information from the "bridge"> network inside the `networks` map instead, which contains the same> information. this field was deprecated in docker 1.9 and is scheduled> to be removed in docker 17.12.0'
    # link for what, migration guide, deprecation notice, example (/reference/)
    # urls = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', value)
    # print(description)
    values = description.split(" ")

    result = ""

    for value in values:
        # print(value)
        # match = re.search("(?P<url>https?://[^\s]+)", value)
        urls = re.findall('http://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', value)
        if len(urls):
            result = result + " ".join(urls) + " "
        elif "/change" in value or "/migration" in value or "/guide" in value:
            result = result + value + " "

        # elif "/doc/" in value or "/reference/" in value:
        #     # print(value)
        #     result = result + value + " "

    if result:
        return result

    return False

# @todo
def checkExample(value):

    # https://swagger.io/docs/specification/adding-examples/

    if "example" in value:
        return True

    return False
# @todo
def checkReason(value):

    return False

def checkInfoType(value):
    result = ""

    # with link or without link
    if "release note" in value:
        result = result + "release note"

    if "migration" in value:
        result = result + "migration"

    # @todo: check deprecation notice


    if result:
        return result
    return False

# checkLink("test")
# myString = "This is my tweet check it out http://tinyurl.com/blah/yrryt http://text 2017 20170605 35.89"
# # match = re.findall("(https?://(?:[-\w.]|(?:%[\da-fA-F]{6}))+)", myString)
# urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', myString)
#
# print(urls)
# if match is not None:
#     print(match.group("url"))


# @todo: only warning versus **???is there any warning header?, warning output,,,X-API-Warn....https://zapier.com/engineering/api-geriatrics/
def checkWarning(value):

    if "warning" in value:
        return True
    return False
# deprecated, no longer?????
# note

descriptions_info = list(set(all_descriptions))
random.shuffle(descriptions_info)


for description in descriptions_api:
        soup = BeautifulSoup(description, features="lxml")
        description_text = soup.get_text()
        description_lower = description_text.lower()
        alternate = checkAlternate(description_lower)


# with open('result/shuffled_descriptions.csv', mode='w', encoding='utf-8') as res_file:
#     res_writer = csv.writer(res_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
#     for description in descriptions_info:
#         res_writer.writerow([description])


# with open('result/descriptions_api_detailed2.csv', mode='w', encoding='utf-8') as res_file:
#     res_writer = csv.writer(res_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
#     res_writer.writerow(["description", "api", "count_occurance", "alternate", "time", "link", "info type"])
#
#     for description in descriptions_api:
#         soup = BeautifulSoup(description)
#         description_text = soup.get_text()
#         description_lower = description_text.lower()
#         alternate = checkAlternate(description_lower)
#         time = checkTime(description_lower)
#         link = checkLink(description_lower)
#         info_type = checkInfoType(description_lower)
#         # example = checkExample(description_lower)
#         # warning = checkWarning(description_lower)
#
#         res_writer.writerow([description, descriptions_api[description], len(descriptions_api[description]), alternate, time, link, info_type])

