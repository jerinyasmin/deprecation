import os
import string

from bs4 import BeautifulSoup
import yaml
import csv

from openapi_spec_validator import validate_spec


# HERE ALL THE FILES ATE STANDARD

#We can test the descrition from here
directory = "rada-verification/positive"


#following is the files (337 files)
# apis_deprecated = ['APIs/botify.com/1.0.0/swagger.yaml', 'APIs/googleapis.com/run/v1alpha1/swagger.yaml', 'APIs/googleapis.com/blogger/v3/swagger.yaml', 'APIs/googleapis.com/cloudbilling/v1/swagger.yaml', 'APIs/googleapis.com/gamesConfiguration/v1configuration/swagger.yaml', 'APIs/import.io/schedule/1.0/swagger.yaml', 'APIs/googleapis.com/tagmanager/v1/swagger.yaml', 'APIs/shutterstock.com/1.0.15/openapi.yaml', 'APIs/azure.com/compute/2018-06-01/swagger.yaml', 'APIs/docker.com/engine/1.33/swagger.yaml', 'APIs/googleapis.com/vision/v1p1beta1/swagger.yaml', 'APIs/googleapis.com/identitytoolkit/v3/swagger.yaml', 'APIs/googleapis.com/clouduseraccounts/vm_alpha/swagger.yaml', 'APIs/googleapis.com/serviceusage/v1/swagger.yaml', 'APIs/amazonaws.com/ram/2018-01-04/swagger.yaml', 'APIs/googleapis.com/dfareporting/v3.3/swagger.yaml', 'APIs/googleapis.com/firebase/v1beta1/swagger.yaml', 'APIs/azure.com/securityinsights-SecurityInsights/2019-01-01-preview/swagger.yaml', 'APIs/googleapis.com/replicapool/v1beta2/swagger.yaml', 'APIs/googleapis.com/appsactivity/v1/swagger.yaml', 'APIs/azure.com/recoveryservicesbackup-bms/2017-07-01/swagger.yaml', 'APIs/azure.com/machinelearningservices-datastore/2019-08-01/swagger.yaml', 'APIs/googleapis.com/driveactivity/v2/swagger.yaml', 'APIs/vocadb.net/v1/swagger.yaml', 'APIs/amazonaws.com/ec2/2016-11-15/swagger.yaml', 'APIs/amazonaws.com/medialive/2017-10-14/swagger.yaml', 'APIs/amazonaws.com/elasticbeanstalk/2010-12-01/swagger.yaml', 'APIs/atlassian.com/jira/v3/swagger.yaml', 'APIs/here.com/tracking/2.0.0/swagger.yaml', 'APIs/googleapis.com/toolresults/v1beta3firstparty/swagger.yaml', 'APIs/googleapis.com/games/v1/swagger.yaml', 'APIs/googleapis.com/tpu/v1alpha1/swagger.yaml', 'APIs/googleapis.com/oauth2/v2/swagger.yaml', 'APIs/googleapis.com/dfareporting/v3.0/swagger.yaml', 'APIs/amazonaws.com/apigateway/2015-07-09/swagger.yaml', 'APIs/thetvdb.com/2.2.0/swagger.yaml', 'APIs/googleapis.com/bigquerydatatransfer/v1/swagger.yaml', 'APIs/nba.com/1.0.0/swagger.yaml', 'APIs/googleapis.com/bigquery/v2/swagger.yaml', 'APIs/googleapis.com/deploymentmanager/v2beta/swagger.yaml', 'APIs/amazonaws.com/cloudfront/2016-11-25/swagger.yaml', 'APIs/instagram.com/1.0.0/swagger.yaml', 'APIs/googleapis.com/iam/v1/swagger.yaml', 'APIs/googleapis.com/storage/v1beta2/swagger.yaml', 'APIs/nytimes.com/community/3.0.0/swagger.yaml', 'APIs/googleapis.com/storage/v1beta1/swagger.yaml', 'APIs/amazonaws.com/codedeploy/2014-10-06/swagger.yaml', 'APIs/googleapis.com/vision/v1/swagger.yaml', 'APIs/azure.com/containerservices-managedClusters/2017-08-31/swagger.yaml', 'APIs/googleapis.com/appengine/v1beta4/swagger.yaml', 'APIs/amazonaws.com/cloudfront/2017-03-25/swagger.yaml', 'APIs/googleapis.com/pagespeedonline/v1/swagger.yaml', 'APIs/googleapis.com/youtube/v3/swagger.yaml', 'APIs/googleapis.com/clouduseraccounts/alpha/swagger.yaml', 'APIs/googleapis.com/genomics/v1/swagger.yaml', 'APIs/gov.bc.ca/geocoder/2.0.0/openapi.yaml', 'APIs/googleapis.com/container/v1beta1/swagger.yaml', 'APIs/googleapis.com/replicapoolupdater/v1beta1/swagger.yaml', 'APIs/azure.com/signalr/2018-03-01-preview/swagger.yaml', 'APIs/azure.com/containerservice-containerService/2016-03-30/swagger.yaml', 'APIs/googleapis.com/fusiontables/v2/swagger.yaml', 'APIs/googleapis.com/deploymentmanager/v2/swagger.yaml', 'APIs/amazonaws.com/logs/2014-03-28/swagger.yaml', 'APIs/googleapis.com/tpu/v1/swagger.yaml', 'APIs/amazonaws.com/elasticache/2015-02-02/swagger.yaml', 'APIs/bunq.com/1.0/openapi.yaml', 'APIs/azure.com/visualstudio-Csm/2014-04-01-preview/swagger.yaml', 'APIs/amazonaws.com/lambda/2015-03-31/swagger.yaml', 'APIs/billbee.io/v1/swagger.yaml', 'APIs/googleapis.com/datafusion/v1beta1/swagger.yaml', 'APIs/azure.com/apimanagement-apimdeployment/2017-03-01/swagger.yaml', 'APIs/api2cart.com/1.0.0/swagger.yaml', 'APIs/azure.com/search-searchservice/2017-11-11-Preview/swagger.yaml', 'APIs/tomtom.com/search/1.0.0/openapi.yaml', 'APIs/googleapis.com/fusiontables/v1/swagger.yaml', 'APIs/azure.com/containerservices-containerService/2017-07-01/swagger.yaml', 'APIs/citrixonline.com/gotomeeting/1.0.0/swagger.yaml', 'APIs/googleapis.com/reseller/v1/swagger.yaml', 'APIs/wowza.com/1/swagger.yaml', 'APIs/bulksms.com/1.0.0/swagger.yaml', 'APIs/googleapis.com/licensing/v1/swagger.yaml', 'APIs/googleapis.com/calendar/v3/swagger.yaml', 'APIs/googleapis.com/dfareporting/v2.8/swagger.yaml', 'APIs/azure.com/datafactory/2018-06-01/swagger.yaml', 'APIs/azure.com/monitor-serviceDiagnosticsSettings_API/2015-07-01/swagger.yaml', 'APIs/azure.com/recoveryservicessiterecovery-service/2016-08-10/swagger.yaml', 'APIs/googleapis.com/clouduseraccounts/beta/swagger.yaml', 'APIs/googleapis.com/genomics/v1alpha2/swagger.yaml', 'APIs/amazonaws.com/mturk-requester/2017-01-17/swagger.yaml', 'APIs/azure.com/applicationinsights-componentContinuousExport_API/2015-05-01/swagger.yaml', 'APIs/googleapis.com/dns/v2beta1/swagger.yaml', 'APIs/azure.com/databox/2019-09-01/swagger.yaml', 'APIs/googleapis.com/compute/beta/swagger.yaml', 'APIs/googleapis.com/dataproc/v1beta2/swagger.yaml', 'APIs/googleapis.com/fitness/v1/swagger.yaml', 'APIs/googleapis.com/servicemanagement/v1/swagger.yaml', 'APIs/sportsdata.io/nfl-v3-stats/1.0/swagger.yaml', 'APIs/agco-ats.com/v1/swagger.yaml', 'APIs/amazonaws.com/iotthingsgraph/2018-09-06/swagger.yaml', 'APIs/hetras-certification.net/booking/v0/swagger.yaml', 'APIs/amazonaws.com/cloudtrail/2013-11-01/swagger.yaml', 'APIs/googleapis.com/toolresults/v1beta3/swagger.yaml', 'APIs/slack.com/1.2.0/swagger.yaml', 'APIs/getgo.com/gotowebinar/1.0.0/swagger.yaml', 'APIs/googleapis.com/dfareporting/v2.7/swagger.yaml', 'APIs/googleapis.com/genomics/v2alpha1/swagger.yaml', 'APIs/googleapis.com/content/v2/swagger.yaml', 'APIs/googleapis.com/container/v1/swagger.yaml', 'APIs/dracoon.team/4.5.0/swagger.yaml', 'APIs/wmata.com/rail-station/1.0/swagger.yaml', 'APIs/azure.com/eventhub-EventHub/2017-04-01/swagger.yaml', 'APIs/stripe.com/2019-09-09/swagger.yaml', 'APIs/bbc.com/1.0.0/openapi.yaml', 'APIs/amazonaws.com/comprehendmedical/2018-10-30/swagger.yaml', 'APIs/googleapis.com/admin/directory_v1/swagger.yaml', 'APIs/googleapis.com/partners/v2/swagger.yaml', 'APIs/amazonaws.com/firehose/2015-08-04/swagger.yaml', 'APIs/amazonaws.com/servicecatalog/2015-12-10/swagger.yaml', 'APIs/import.io/data/1.0/swagger.yaml', 'APIs/azure.com/search-searchservice/2019-05-06/swagger.yaml', 'APIs/googleapis.com/jobs/v3/swagger.yaml', 'APIs/storecove.com/2.0.1/swagger.yaml', 'APIs/googleapis.com/content/v2.1/swagger.yaml', 'APIs/amazonaws.com/resource-groups/2017-11-27/swagger.yaml', 'APIs/amazonaws.com/elasticmapreduce/2009-03-31/swagger.yaml', 'APIs/azure.com/hdinsight-configurations/2015-03-01-preview/swagger.yaml', 'APIs/googleapis.com/androidpublisher/v1.1/swagger.yaml', 'APIs/netlicensing.io/2.x/swagger.yaml', 'APIs/azure.com/recoveryservices-replicationusages/2016-06-01/swagger.yaml', 'APIs/googleapis.com/pagespeedonline/v5/swagger.yaml', 'APIs/azure.com/monitor-serviceDiagnosticsSettings_API/2016-09-01/swagger.yaml', 'APIs/amazonaws.com/storagegateway/2013-06-30/swagger.yaml', 'APIs/azure.com/containerservices-containerService/2016-03-30/swagger.yaml', 'APIs/jira.local/1.0.0/swagger.yaml', 'APIs/googleapis.com/adsense/v1.4/swagger.yaml', 'APIs/azure.com/containerservices-containerService/2017-01-31/swagger.yaml', 'APIs/azure.com/containerservice-containerService/2017-01-31/swagger.yaml', 'APIs/sportsdata.io/nfl-v3-scores/1.0/swagger.yaml', 'APIs/amazonaws.com/shield/2016-06-02/swagger.yaml', 'APIs/import.io/extraction/1.0/swagger.yaml', 'APIs/azure.com/redis/2015-08-01/swagger.yaml', 'APIs/contribly.com/1.0.0/swagger.yaml', 'APIs/googleapis.com/androidmanagement/v1/swagger.yaml', 'APIs/googleapis.com/oauth2/v1/swagger.yaml', 'APIs/googleapis.com/adexchangebuyer/v1.3/swagger.yaml', 'APIs/azure.com/web-WebApps/2018-11-01/swagger.yaml', 'APIs/azure.com/apimanagement-apimdeployment/2018-01-01/swagger.yaml', 'APIs/anchore.io/0.1.12/swagger.yaml', 'APIs/netatmo.net/1.1.1/swagger.yaml', 'APIs/googleapis.com/tasks/v1/swagger.yaml', 'APIs/azure.com/datalake-analytics-catalog/2016-11-01/swagger.yaml', 'APIs/googleapis.com/drive/v2/swagger.yaml', 'APIs/googleapis.com/sourcerepo/v1/swagger.yaml', 'APIs/googleapis.com/appstate/v1/swagger.yaml', 'APIs/github.com/v3/swagger.yaml', 'APIs/iva-api.com/2.0/swagger.yaml', 'APIs/reverb.com/3.0/swagger.yaml', 'APIs/googleapis.com/webmasters/v3/swagger.yaml', 'APIs/amazonaws.com/email/2010-12-01/swagger.yaml', 'APIs/amazonaws.com/glue/2017-03-31/swagger.yaml', 'APIs/googleapis.com/adexchangeseller/v1/swagger.yaml', 'APIs/googleapis.com/spectrum/v1explorer/swagger.yaml', 'APIs/googleapis.com/sqladmin/v1beta3/swagger.yaml', 'APIs/bungie.net/2.0.0/swagger.yaml', 'APIs/googleapis.com/androidpublisher/v2/swagger.yaml', 'APIs/googleapis.com/remotebuildexecution/v2/swagger.yaml', 'APIs/weatherbit.io/2.0.0/swagger.yaml', 'APIs/amazonaws.com/lightsail/2016-11-28/swagger.yaml', 'APIs/googleapis.com/alertcenter/v1beta1/swagger.yaml', 'APIs/googleapis.com/adexchangeseller/v2.0/swagger.yaml', 'APIs/googleapis.com/content/v2sandbox/swagger.yaml', 'APIs/taxamo.com/1/swagger.yaml', 'APIs/googleapis.com/sqladmin/v1beta4/swagger.yaml', 'APIs/googleapis.com/people/v1/swagger.yaml', 'APIs/googleapis.com/analytics/v2.4/swagger.yaml', 'APIs/nexmo.com/application/1.0.2/openapi.yaml', 'APIs/amazonaws.com/guardduty/2017-11-28/swagger.yaml', 'APIs/hetras-certification.net/hotel/v0/swagger.yaml', 'APIs/amazonaws.com/swf/2012-01-25/swagger.yaml', 'APIs/amazonaws.com/cognito-idp/2016-04-18/swagger.yaml', 'APIs/googleapis.com/adsensehost/v4.1/swagger.yaml', 'APIs/azure.com/visualstudio-Csm/2017-11-01-preview/swagger.yaml', 'APIs/azure.com/servicefabric/6.5.0.36/swagger.yaml', 'APIs/wmata.com/bus-route/1.0/swagger.yaml', 'APIs/googleapis.com/servicenetworking/v1/swagger.yaml', 'APIs/amazonaws.com/s3/2006-03-01/swagger.yaml', 'APIs/whatsapp.local/1.0/openapi.yaml', 'APIs/googleapis.com/doubleclicksearch/v2/swagger.yaml', 'APIs/googleapis.com/remotebuildexecution/v1alpha/swagger.yaml', 'APIs/googleapis.com/youtubeAnalytics/v1beta1/swagger.yaml', 'APIs/googleapis.com/appengine/v1beta5/swagger.yaml', 'APIs/victorops.com/0.0.3/swagger.yaml', 'APIs/googleapis.com/bigtableadmin/v2/swagger.yaml', 'APIs/googleapis.com/surveys/v2/swagger.yaml', 'APIs/googleapis.com/adexchangebuyer/v1.2/swagger.yaml', 'APIs/noosh.com/1.0/swagger.yaml', 'APIs/googleapis.com/vision/v1p2beta1/swagger.yaml', 'APIs/azure.com/monitor-activityLogAlerts_API/2017-03-01-preview/swagger.yaml', 'APIs/adyen.com/MarketPayNotificationService/3/openapi.yaml', 'APIs/googleapis.com/dataproc/v1alpha1/swagger.yaml', 'APIs/azure.com/datalake-store-filesystem/2015-10-01-preview/swagger.yaml', 'APIs/googleapis.com/siteVerification/v1/swagger.yaml', 'APIs/googleapis.com/adsense/v1.3/swagger.yaml', 'APIs/googleapis.com/containeranalysis/v1beta1/swagger.yaml', 'APIs/flat.io/2.8.0/swagger.yaml', 'APIs/googleapis.com/accesscontextmanager/v1beta/swagger.yaml', 'APIs/googleapis.com/plus/v1/swagger.yaml', 'APIs/rbaskets.in/1.0.0/swagger.yaml', 'APIs/googleapis.com/serviceconsumermanagement/v1/swagger.yaml', 'APIs/amazonaws.com/rds/2014-10-31/swagger.yaml', 'APIs/googleapis.com/compute/v1/swagger.yaml', 'APIs/zuora.com/2019-09-19/swagger.yaml', 'APIs/googleapis.com/androidpublisher/v1/swagger.yaml', 'APIs/azure.com/containerservice-containerService/2017-07-01/swagger.yaml', 'APIs/getgo.com/gototraining/1.0.0/swagger.yaml', 'APIs/azure.com/containerservice-containerService/2016-09-30/swagger.yaml', 'APIs/googleapis.com/containeranalysis/v1alpha1/swagger.yaml', 'APIs/googleapis.com/gamesManagement/v1management/swagger.yaml', 'APIs/googleapis.com/adexchangeseller/v1.1/swagger.yaml', 'APIs/googleapis.com/verifiedaccess/v1/swagger.yaml', 'APIs/googleapis.com/pagespeedonline/v4/swagger.yaml', 'APIs/googleapis.com/mirror/v1/swagger.yaml', 'APIs/googleapis.com/serviceusage/v1beta1/swagger.yaml', 'APIs/googleapis.com/dataflow/v1b3/swagger.yaml', 'APIs/nexmo.com/number-insight/1.0.4/openapi.yaml', 'APIs/googleapis.com/jobs/v2/swagger.yaml', 'APIs/amazonaws.com/elastictranscoder/2012-09-25/swagger.yaml', 'APIs/lyft.com/1.0.0/swagger.yaml', 'APIs/googleapis.com/servicenetworking/v1beta/swagger.yaml', 'APIs/googleapis.com/monitoring/v3/swagger.yaml', 'APIs/googleapis.com/urlshortener/v1/swagger.yaml', 'APIs/azure.com/apimanagement-apimdeployment/2018-06-01-preview/swagger.yaml', 'APIs/googleapis.com/playmoviespartner/v1/swagger.yaml', 'APIs/amazonaws.com/codebuild/2016-10-06/swagger.yaml', 'APIs/googleapis.com/books/v1/swagger.yaml', 'APIs/googleapis.com/dialogflow/v2/swagger.yaml', 'APIs/googleapis.com/logging/v2/swagger.yaml', 'APIs/googleapis.com/cloudresourcemanager/v1beta1/swagger.yaml', 'APIs/azure.com/containerservice-managedClusters/2017-08-31/swagger.yaml', 'APIs/transitfeeds.com/1.0.0/swagger.yaml', 'APIs/azure.com/servicefabric/6.4.0.36/swagger.yaml', 'APIs/youneedabudget.com/1.0.0/swagger.yaml', 'APIs/googleapis.com/gmail/v1/swagger.yaml', 'APIs/amazonaws.com/rds-data/2018-08-01/swagger.yaml', 'APIs/googleapis.com/appengine/v1beta/swagger.yaml', 'APIs/googleapis.com/ml/v1beta1/swagger.yaml', 'APIs/googleapis.com/servicecontrol/v1/swagger.yaml', 'APIs/googleapis.com/dfareporting/v3.2/swagger.yaml', 'APIs/googleapis.com/clouddebugger/v2/swagger.yaml', 'APIs/amazonaws.com/opsworkscm/2016-11-01/swagger.yaml', 'APIs/wmata.com/incidents/1.0/swagger.yaml', 'APIs/googleapis.com/testing/v1/swagger.yaml', 'APIs/visagecloud.com/1.1/swagger.yaml', 'APIs/azure.com/hdinsight-configurations/2018-06-01-preview/swagger.yaml', 'APIs/googleapis.com/healthcare/v1alpha2/swagger.yaml', 'APIs/googleapis.com/doubleclickbidmanager/v1/swagger.yaml', 'APIs/googleapis.com/compute/alpha/swagger.yaml', 'APIs/amazonaws.com/cloudfront/2017-10-30/swagger.yaml', 'APIs/azure.com/containerservices-containerService/2016-09-30/swagger.yaml', 'APIs/googleapis.com/logging/v2beta1/swagger.yaml', 'APIs/azure.com/compute/2019-03-01/swagger.yaml', 'APIs/azure.com/sql-tableAuditing/2014-04-01/swagger.yaml', 'APIs/amazonaws.com/discovery/2015-11-01/swagger.yaml', 'APIs/kubernetes.io/v1.17.0/swagger.yaml', 'APIs/azure.com/recoveryservicesbackup-bms/2016-12-01/swagger.yaml', 'APIs/azure.com/visualstudio-PipelineTemplates/2018-08-01-preview/swagger.yaml', 'APIs/googleapis.com/androidenterprise/v1/swagger.yaml', 'APIs/googleapis.com/civicinfo/v2/swagger.yaml', 'APIs/bitbucket.org/2.0/swagger.yaml', 'APIs/googleapis.com/slides/v1/swagger.yaml', 'APIs/googleapis.com/plusDomains/v1/swagger.yaml', 'APIs/googleapis.com/webfonts/v1/swagger.yaml', 'APIs/googleapis.com/clouduseraccounts/vm_beta/swagger.yaml', 'APIs/azure.com/resources-policyAssignments/2016-12-01/swagger.yaml', 'APIs/gitlab.com/v3/swagger.yaml', 'APIs/azure.com/resources-policyAssignments/2017-06-01-preview/swagger.yaml', 'APIs/googleapis.com/serviceuser/v1/swagger.yaml', 'APIs/amazonaws.com/directconnect/2012-10-25/swagger.yaml', 'APIs/googleapis.com/youtubereporting/v1/swagger.yaml', 'APIs/googleapis.com/drive/v3/swagger.yaml', 'APIs/googleapis.com/groupssettings/v1/swagger.yaml', 'APIs/gitea.io/1.1.1/swagger.yaml', 'APIs/googleapis.com/spanner/v1/swagger.yaml', 'APIs/beezup.com/2.0/swagger.yaml', 'APIs/googleapis.com/language/v1beta1/swagger.yaml', 'APIs/googleapis.com/healthcare/v1beta1/swagger.yaml', 'APIs/amazonaws.com/mediapackage/2017-10-12/swagger.yaml', 'APIs/osf.io/2.0/swagger.yaml', 'APIs/paccurate.io/0.1.1/swagger.yaml', 'APIs/crucible.local/1.0.0/swagger.yaml', 'APIs/squareup.com/2.0/swagger.yaml', 'APIs/azure.com/servicefabric-application/2019-03-01/swagger.yaml', 'APIs/amazonaws.com/iot/2015-05-28/swagger.yaml', 'APIs/azure.com/compute/2018-10-01/swagger.yaml', 'APIs/googleapis.com/dlp/v2/swagger.yaml', 'APIs/googleapis.com/remotebuildexecution/v1/swagger.yaml', 'APIs/googleapis.com/androidpublisher/v3/swagger.yaml', 'APIs/amazonaws.com/secretsmanager/2017-10-17/swagger.yaml', 'APIs/googleapis.com/dns/v1beta2/swagger.yaml', 'APIs/googleapis.com/admin/reports_v1/swagger.yaml', 'APIs/azure.com/visualstudio-Projects/2018-08-01-preview/swagger.yaml', 'APIs/googleapis.com/blogger/v2/swagger.yaml', 'APIs/googleapis.com/youtubeAnalytics/v2/swagger.yaml', 'APIs/googleapis.com/jobs/v3p1beta1/swagger.yaml', 'APIs/googleapis.com/pagespeedonline/v2/swagger.yaml', 'APIs/docusign.net/v2/swagger.yaml', 'APIs/googleapis.com/dns/v1/swagger.yaml', 'APIs/amazonaws.com/cloudfront/2018-06-18/swagger.yaml', 'APIs/googleapis.com/groupsmigration/v1/swagger.yaml', 'APIs/rebilly.com/2.1/swagger.yaml', 'APIs/bigoven.com/partner/swagger.yaml', 'APIs/googleapis.com/analytics/v3/swagger.yaml', 'APIs/googleapis.com/sheets/v4/swagger.yaml', 'APIs/amazonaws.com/ssm/2014-11-06/swagger.yaml', 'APIs/npr.org/listening/2/swagger.yaml', 'APIs/setlist.fm/1.0/swagger.yaml', 'APIs/linode.com/4.5.0/openapi.yaml', 'APIs/googleapis.com/dfareporting/v3.1/swagger.yaml', 'APIs/googleapis.com/storage/v1/swagger.yaml', 'APIs/googleapis.com/admin/datatransfer_v1/swagger.yaml', 'APIs/amazonaws.com/pinpoint/2016-12-01/swagger.yaml', 'APIs/googleapis.com/replicapool/v1beta1/swagger.yaml', 'APIs/googleapis.com/customsearch/v1/swagger.yaml', 'APIs/googleapis.com/deploymentmanager/alpha/swagger.yaml', 'APIs/adyen.com/MarketPayNotificationService/4/openapi.yaml', 'APIs/amazonaws.com/cloudfront/2018-11-05/swagger.yaml', 'APIs/googleapis.com/appengine/v1/swagger.yaml', 'APIs/googleapis.com/script/v1/swagger.yaml', 'APIs/googleapis.com/adexchangebuyer/v1.4/swagger.yaml', 'APIs/vimeo.com/3.4/openapi.yaml', 'APIs/googleapis.com/playcustomapp/v1/swagger.yaml', 'APIs/import.io/rss/1.0/swagger.yaml', 'APIs/cloudmersive.com/ocr/v1/swagger.yaml', 'APIs/azure.com/web-WebApps/2018-02-01/swagger.yaml', 'APIs/googleapis.com/discovery/v1/swagger.yaml', 'APIs/import.io/run/1.0/swagger.yaml', 'APIs/azure.com/signalr/2018-10-01/swagger.yaml']

#no containerservices and no 3 yaml error files(apis_nc), containerservices removed manually
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

indexByAPI = {}

def readFile(filename):
    with open(filename, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 1
        apis = []
        for row in csv_reader:
            if line_count > 1:
                api = row[0].replace("\\", "/")
                apis.append(api)

            line_count += 1

    return list(set(apis))


def getApiName(split_path):
    path = split_path[:-2]
    path = path[1:]
    path_unique = ("_").join(path)

    if path_unique == "googleapis.com_admin":
        path_unique = path_unique + split_path[-2]

    return path_unique


all_descriptions = []


def get_different_form_deprecated(text):
    # text = text.replace("\r\n", " ")
    #
    # text = text.replace("\n", " ")
    text = " ".join(text.split())

    split_text = text.split(" ")
    if len(split_text) == 1:
        value_ch = text.translate(str.maketrans('', '', string.punctuation))
        if value_ch != "deprecated":
            print(value_ch)
            return False   #this is for typedeprecatedfault

    total_deprecated = 0
    count = 0
    # if "marked as `deprecated`" in text:
    #     print("`deprecated` text")
    #     print(text)
    #     return False

    for value in split_text:
        # value_ch = value.translate(str.maketrans('', '', string.punctuation))
        value = value.replace(",", "")
        value = value.replace(".", "")
        value = value.replace(":", "")
        if "deprecate" in value:
            all_descriptions.append(text)
            total_deprecated = total_deprecated + 1
            if value == '\"deprecated\"':
                count = count + 1
            # elif value == '* `deprecated` - ':
            #     count = count + 1
            elif value == "\'deprecated\'":
                count = count + 1

    if count == total_deprecated:
        print("out")  #2
        print(text)
        return False


    return True

def findAPIDeprecated():
    results = []
    desc_api = []
    key_api = []
    text_description = {}
    folderlist = os.walk(directory)
    for f in folderlist:
        for fs in f[2]:
            file_location = f[0] + "/" + fs

            depr_desc = []
            depr_desc_key = []
            depr_key = []
            with open(file_location, 'r', encoding="utf-8") as stream:
                api_unique = fs.replace("_swagger.yaml", "")
                api_unique = api_unique.replace("_openapi.yaml", "")
                # api_unique = api_unique.split("_")
                # print(api_unique)
                # api_unique = api_unique[:-1]
                # print(api_unique)
                # api_unique = "_".join(api_unique)
                # print(api_unique)

                try:
                    data_stream = yaml.safe_load(stream)

                    data = flatten_json(data_stream)
                    for key in data:
                        if key.endswith("description") or key.endswith("summary"):
                            split_values = key.split("_")
                            # print(key)
                            if ("deprecat" in key.lower()) and (
                                    "&deprecated!" not in key.lower()):  # deprecated_description, deprecation
                                print(key)
                                print(file_location)
                                print(data[key])
                            else:
                                if api_unique == "zuora.com" and key.startswith("info"):
                                    pass
                                else:
                                    value = data[key]
                                    if isinstance(value, str):
                                        value = value.lower()
                                        if value and "deprecate" in value:
                                            if get_different_form_deprecated(value):
                                                value = " ".join(value.split())
                                                if api_unique in text_description:
                                                    values = text_description[api_unique]
                                                    text_description[api_unique] = values + [value]

                                                else:
                                                    text_description[api_unique] = [value]

                                                # text_description.append(value)
                                                depr_desc.append(value)
                                                depr_desc_key.append(key)

                                                if key.endswith("summary"):
                                                    print(value)
                                                    print("IN summary")
                        if key.endswith("deprecated"):
                            value = data[key]
                            if isinstance(value, bool) and value:
                                depr_key.append(key)
                    if len(depr_desc):
                        desc_api.append(file_location)
                    if len(depr_key):
                        key_api.append(file_location)
                    if len(depr_desc) or len(depr_key):
                        results.append(file_location)
                except yaml.YAMLError as exc:
                    print(api_unique)
                    print(exc)
        # print(text_description)

        # with open('result/validate-rada/description_to_check.csv', mode='w') as res_file:
        #     res_writer = csv.writer(res_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL,
        #                             lineterminator="\n")
        #     res_writer.writerow(["api", "description"])
        #
        #     for file in text_description:
        #         res_writer.writerow([file, text_description[file]])

        with open('result/validate-rada/descriptions.csv', mode='w') as res_file:
            res_writer = csv.writer(res_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL,
                                    lineterminator="\n")
            res_writer.writerow(["api", "description"])

            for api in text_description:
                values = text_description[api]
                for value in values:
                    res_writer.writerow([api, value])

        apis = []
        for api in text_description:
            apis.append(api)
        with open('result/validate-rada/api.csv', mode='w') as res_file:
            res_writer = csv.writer(res_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL,
                                    lineterminator="\n")
            res_writer.writerow(["api"])

            for api in apis:
                res_writer.writerow([api])

# findAPIDeprecated()
print("============================================")
# read("result/chart/chart_deprecated_operations_merged.csv")

filename = "result/chart/chart_deprecated_operation_merged.csv"

apis = read("result/validate-rada/api.csv")

def checkCountOperation():
    count_all = 0
    count_depr = 0
    with open(filename, mode='r', encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 1
        for row in csv_reader:
            if line_count > 1:
                api = row[1]

                if api in apis:
                    count_all = int(row[2]) + count_all

                    count_depr = int(row[3]) + count_depr

            line_count += 1

    print(count_all)
    print(count_depr)


checkCountOperation()