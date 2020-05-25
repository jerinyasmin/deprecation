import csv
import os
import random
import re

from bs4 import BeautifulSoup
from sklearn.metrics import precision_recall_fscore_support as pr

from sklearn.metrics import accuracy_score


def result(original, test):
    bPrecis, bRecall, bFscore, bSupport = pr(original, test, average='binary')

    count_tp = 0
    count_tn = 0
    count_fp = 0
    count_fn = 0
    for ind, value in enumerate(test):
        if value == original[ind]: #true
            if value: #true, so tp
                count_tp = count_tp + 1
            else:
                count_tn = count_tn + 1
        else:
            if value:
                count_fp = count_fp + 1
            else:
                count_fn = count_fn + 1

def checkAlternate(value):
    #instead check: 233
    #see survey cost inste  #replace by @todo recommend but not "don't recommeend, call the ,please see for the preferred method????, instead of using + please, check only instead, please, merged into, keep it unspecified


    #returns an array of one or more targets associated with a deployment. this method works with all compute types and should be used instead of the deprecated batchgetdeploymentinstances. the maximum number of targets that can be returned is 25.  the type of targets returned depends on the deployment's compute platform:     ec2/on-premises: information about ec2 instance targets.     aws lambda: information about lambda functions targets.     amazon ecs: information about amazon ecs service targets.
    #

    # if "instead" in value and "use " not in value:
    #     print(value)
    # value = "post /stream_targets/add/ is deprecated. to add a stream target, use post /stream_targets instead."
    # if "instead of the deprecated" in value:
    #     print(value)

    # if "instead of using" in value and "please" in value:
    #     print(value)
    # if "instead of using" in value:
    #     print(value)

    # if "instead" in value and ("specify" in value):
    #     print(value)

    # if "use " in value and ("call" not in value and "set" not in value and "instead" not in value and "see" not in value and "recommend" not in value):
    #     print(value)
    # value = "(deprecated) your aws account id, which you assigned to an external id key in an iam trust policy. amazon pinpoint previously used this value to assume an iam role when importing endpoint definitions, but we removed this requirement. we don't recommend use of external ids for iam roles that are assumed by amazon pinpoint."
    if ("recommend " in value and "don't recommend" not in value) or ("use " in value) or "deprecated by" in value or "in favor of" in value or "replaced by" in value or ("instead" in value) or ("merged into" in value) or ("see" in value and "preferred" in value):
        return True

    return False

def checkDeprecatedTime(description):
    if ("deprecated in" in description or "deprecated as of" in description) and "deprecated in favor" not in description:
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

    # for value in values:
    #
    #     # if "will be removed" in value: version number
    #
    #     # print(value)
    #     # digit = re.findall('(\d+)', value)
    #     if value.isdigit():
    #         if len(value) == 4:
    #             result = result + value + " "   #this is for year
    #
    #
    #     # if digit:
    #     #     for dg in digit:
    #     #
    #     #         if len(dg) == 4:
    #     #             print(dg)
    #     #             if 2030> int(dg) > 2015:
    #     #                 result = result + dg + " "
    #     #         if "removed" in value:
    #     #             result = result + dg + " " #this is for version
    #
    #     months = [" january", " february", " march ", " april ", " may ", " jun", " jul", " aug", " sept", " oct", " nov", " december "]
    #
    #     for month in months:
    #         if month in value:
    #             result = result + month


    # if len(result):
    #     return True

    return False

def checkLink(description):
    # description = 'gateway address for the default "bridge" network.<p><br /></p>> **deprecated**: this field is only propagated when attached to the> default "bridge" network. use the information from the "bridge"> network inside the `networks` map instead, which contains the same> information. this field was deprecated in docker 1.9 and is scheduled> to be removed in docker 17.12.0'
    # link for what, migration guide, deprecation notice, example (/reference/)
    # urls = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', value)
    # print(description)
    #
    # urls = re.findall('https://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', description)
    # if len(urls):
    #     return True
    # description = 'no http resource was found that matches the request uri'


    if "http:" in description or "https:" in description:
        return True
    elif "/change" in description or "/migration" in description or "/guide" in description:
        # print("yes")
        print(description)

        return True

    # values = description.split(" ")
    #
    # result = ""
    #
    # for value in values:
    #     # print(value)
    #     # match = re.search("(?P<url>https?://[^\s]+)", value)
    #     urls = re.findall('http://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', value)
    #     if len(urls):
    #         return True
    #     elif "/change" in value or "/migration" in value or "/guide" in value:
    #         return True

    return False

# @todo
def checkExample(value):

    # https://swagger.io/docs/specification/adding-examples/

    if "example" in value:
        return True

    return False
# @todo
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

    # if "for details" in description and "see" in description:
    #     # print(description)
    #     return True

    # if "for more information" in description:
    #     return True


    # result = result + "migration"

    # @todo: check deprecation notice


    # if result:
    #     return result
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
descriptions_api = {}


#
# directory = "alldesc-standard"
# folder_list = os.walk(directory)
alternates = {}
alternates_test = {}
count = 0


with open("result/RQ3/labels/shuffled-evaluate-tool.csv", mode='r', encoding="utf-8") as csv_file:
# with open("result/RQ3/labels/categories.csv", mode='r', encoding="utf-8") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    result = []
    alternate_original = []
    alternate_test = []
    for row in csv_reader:
        if line_count > 0 and line_count < 252:
            description = row[5]
            # files = row[1]

            # original = row[0]
            # original = row[1]
            original = row[3]
            # original = row[3]
            # original = row[3]
            # original = row[6]
            # original = " ".split(original)
            # print(len(original))

            if len(original)>=2:
                original = True
            else:
                original = False

            alternate_original.append(original)
            # descriptions_api[description] = files
            alternates[description] = original

            # soup = BeautifulSoup(description)
            # description_text = soup.get_text()
            description_text = description
            # test_value = checkAlternate(description_text)
            #
            #
            # test_value = checkTime(description_text)
            # test_value = checkLink(description_text)
            test_value = checkReason(description_text)
            # test_value = checkInfoType(description_text)
            alternates_test[description] = test_value
            alternate_test.append(test_value)

            if test_value:
                if original:
                    print("correct")
                else:
                    print("should be false:")
                    print(description)
                    print(original)
                    count = count + 1
            else:
                if original:
                    print("should be true:")

                    print(description)
                    print(original)
                    count = count + 1


        line_count += 1
    print("RESULT COUNT")
    print(count)

    bPrecis, bRecall, bFscore, bSupport = pr(alternate_original, alternate_test, average='binary')

    print ("accuracy", accuracy_score(alternate_original, alternate_test))


    print(bPrecis)
    print(bRecall)
    print(bFscore)

# descriptions_api = {}


all_descriptions = []


