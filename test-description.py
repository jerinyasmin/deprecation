import os
import string

from bs4 import BeautifulSoup
import yaml
import csv

from openapi_spec_validator import validate_spec


# HERE ALL THE FILES ATE STANDARD

#We can test the descrition from here
directory = "APIs"

#following is the files (337 files)
# apis_deprecated = ['APIs/botify.com/1.0.0/swagger.yaml', 'APIs/googleapis.com/run/v1alpha1/swagger.yaml', 'APIs/googleapis.com/blogger/v3/swagger.yaml', 'APIs/googleapis.com/cloudbilling/v1/swagger.yaml', 'APIs/googleapis.com/gamesConfiguration/v1configuration/swagger.yaml', 'APIs/import.io/schedule/1.0/swagger.yaml', 'APIs/googleapis.com/tagmanager/v1/swagger.yaml', 'APIs/shutterstock.com/1.0.15/openapi.yaml', 'APIs/azure.com/compute/2018-06-01/swagger.yaml', 'APIs/docker.com/engine/1.33/swagger.yaml', 'APIs/googleapis.com/vision/v1p1beta1/swagger.yaml', 'APIs/googleapis.com/identitytoolkit/v3/swagger.yaml', 'APIs/googleapis.com/clouduseraccounts/vm_alpha/swagger.yaml', 'APIs/googleapis.com/serviceusage/v1/swagger.yaml', 'APIs/amazonaws.com/ram/2018-01-04/swagger.yaml', 'APIs/googleapis.com/dfareporting/v3.3/swagger.yaml', 'APIs/googleapis.com/firebase/v1beta1/swagger.yaml', 'APIs/azure.com/securityinsights-SecurityInsights/2019-01-01-preview/swagger.yaml', 'APIs/googleapis.com/replicapool/v1beta2/swagger.yaml', 'APIs/googleapis.com/appsactivity/v1/swagger.yaml', 'APIs/azure.com/recoveryservicesbackup-bms/2017-07-01/swagger.yaml', 'APIs/azure.com/machinelearningservices-datastore/2019-08-01/swagger.yaml', 'APIs/googleapis.com/driveactivity/v2/swagger.yaml', 'APIs/vocadb.net/v1/swagger.yaml', 'APIs/amazonaws.com/ec2/2016-11-15/swagger.yaml', 'APIs/amazonaws.com/medialive/2017-10-14/swagger.yaml', 'APIs/amazonaws.com/elasticbeanstalk/2010-12-01/swagger.yaml', 'APIs/atlassian.com/jira/v3/swagger.yaml', 'APIs/here.com/tracking/2.0.0/swagger.yaml', 'APIs/googleapis.com/toolresults/v1beta3firstparty/swagger.yaml', 'APIs/googleapis.com/games/v1/swagger.yaml', 'APIs/googleapis.com/tpu/v1alpha1/swagger.yaml', 'APIs/googleapis.com/oauth2/v2/swagger.yaml', 'APIs/googleapis.com/dfareporting/v3.0/swagger.yaml', 'APIs/amazonaws.com/apigateway/2015-07-09/swagger.yaml', 'APIs/thetvdb.com/2.2.0/swagger.yaml', 'APIs/googleapis.com/bigquerydatatransfer/v1/swagger.yaml', 'APIs/nba.com/1.0.0/swagger.yaml', 'APIs/googleapis.com/bigquery/v2/swagger.yaml', 'APIs/googleapis.com/deploymentmanager/v2beta/swagger.yaml', 'APIs/amazonaws.com/cloudfront/2016-11-25/swagger.yaml', 'APIs/instagram.com/1.0.0/swagger.yaml', 'APIs/googleapis.com/iam/v1/swagger.yaml', 'APIs/googleapis.com/storage/v1beta2/swagger.yaml', 'APIs/nytimes.com/community/3.0.0/swagger.yaml', 'APIs/googleapis.com/storage/v1beta1/swagger.yaml', 'APIs/amazonaws.com/codedeploy/2014-10-06/swagger.yaml', 'APIs/googleapis.com/vision/v1/swagger.yaml', 'APIs/azure.com/containerservices-managedClusters/2017-08-31/swagger.yaml', 'APIs/googleapis.com/appengine/v1beta4/swagger.yaml', 'APIs/amazonaws.com/cloudfront/2017-03-25/swagger.yaml', 'APIs/googleapis.com/pagespeedonline/v1/swagger.yaml', 'APIs/googleapis.com/youtube/v3/swagger.yaml', 'APIs/googleapis.com/clouduseraccounts/alpha/swagger.yaml', 'APIs/googleapis.com/genomics/v1/swagger.yaml', 'APIs/gov.bc.ca/geocoder/2.0.0/openapi.yaml', 'APIs/googleapis.com/container/v1beta1/swagger.yaml', 'APIs/googleapis.com/replicapoolupdater/v1beta1/swagger.yaml', 'APIs/azure.com/signalr/2018-03-01-preview/swagger.yaml', 'APIs/azure.com/containerservice-containerService/2016-03-30/swagger.yaml', 'APIs/googleapis.com/fusiontables/v2/swagger.yaml', 'APIs/googleapis.com/deploymentmanager/v2/swagger.yaml', 'APIs/amazonaws.com/logs/2014-03-28/swagger.yaml', 'APIs/googleapis.com/tpu/v1/swagger.yaml', 'APIs/amazonaws.com/elasticache/2015-02-02/swagger.yaml', 'APIs/bunq.com/1.0/openapi.yaml', 'APIs/azure.com/visualstudio-Csm/2014-04-01-preview/swagger.yaml', 'APIs/amazonaws.com/lambda/2015-03-31/swagger.yaml', 'APIs/billbee.io/v1/swagger.yaml', 'APIs/googleapis.com/datafusion/v1beta1/swagger.yaml', 'APIs/azure.com/apimanagement-apimdeployment/2017-03-01/swagger.yaml', 'APIs/api2cart.com/1.0.0/swagger.yaml', 'APIs/azure.com/search-searchservice/2017-11-11-Preview/swagger.yaml', 'APIs/tomtom.com/search/1.0.0/openapi.yaml', 'APIs/googleapis.com/fusiontables/v1/swagger.yaml', 'APIs/azure.com/containerservices-containerService/2017-07-01/swagger.yaml', 'APIs/citrixonline.com/gotomeeting/1.0.0/swagger.yaml', 'APIs/googleapis.com/reseller/v1/swagger.yaml', 'APIs/wowza.com/1/swagger.yaml', 'APIs/bulksms.com/1.0.0/swagger.yaml', 'APIs/googleapis.com/licensing/v1/swagger.yaml', 'APIs/googleapis.com/calendar/v3/swagger.yaml', 'APIs/googleapis.com/dfareporting/v2.8/swagger.yaml', 'APIs/azure.com/datafactory/2018-06-01/swagger.yaml', 'APIs/azure.com/monitor-serviceDiagnosticsSettings_API/2015-07-01/swagger.yaml', 'APIs/azure.com/recoveryservicessiterecovery-service/2016-08-10/swagger.yaml', 'APIs/googleapis.com/clouduseraccounts/beta/swagger.yaml', 'APIs/googleapis.com/genomics/v1alpha2/swagger.yaml', 'APIs/amazonaws.com/mturk-requester/2017-01-17/swagger.yaml', 'APIs/azure.com/applicationinsights-componentContinuousExport_API/2015-05-01/swagger.yaml', 'APIs/googleapis.com/dns/v2beta1/swagger.yaml', 'APIs/azure.com/databox/2019-09-01/swagger.yaml', 'APIs/googleapis.com/compute/beta/swagger.yaml', 'APIs/googleapis.com/dataproc/v1beta2/swagger.yaml', 'APIs/googleapis.com/fitness/v1/swagger.yaml', 'APIs/googleapis.com/servicemanagement/v1/swagger.yaml', 'APIs/sportsdata.io/nfl-v3-stats/1.0/swagger.yaml', 'APIs/agco-ats.com/v1/swagger.yaml', 'APIs/amazonaws.com/iotthingsgraph/2018-09-06/swagger.yaml', 'APIs/hetras-certification.net/booking/v0/swagger.yaml', 'APIs/amazonaws.com/cloudtrail/2013-11-01/swagger.yaml', 'APIs/googleapis.com/toolresults/v1beta3/swagger.yaml', 'APIs/slack.com/1.2.0/swagger.yaml', 'APIs/getgo.com/gotowebinar/1.0.0/swagger.yaml', 'APIs/googleapis.com/dfareporting/v2.7/swagger.yaml', 'APIs/googleapis.com/genomics/v2alpha1/swagger.yaml', 'APIs/googleapis.com/content/v2/swagger.yaml', 'APIs/googleapis.com/container/v1/swagger.yaml', 'APIs/dracoon.team/4.5.0/swagger.yaml', 'APIs/wmata.com/rail-station/1.0/swagger.yaml', 'APIs/azure.com/eventhub-EventHub/2017-04-01/swagger.yaml', 'APIs/stripe.com/2019-09-09/swagger.yaml', 'APIs/bbc.com/1.0.0/openapi.yaml', 'APIs/amazonaws.com/comprehendmedical/2018-10-30/swagger.yaml', 'APIs/googleapis.com/admin/directory_v1/swagger.yaml', 'APIs/googleapis.com/partners/v2/swagger.yaml', 'APIs/amazonaws.com/firehose/2015-08-04/swagger.yaml', 'APIs/amazonaws.com/servicecatalog/2015-12-10/swagger.yaml', 'APIs/import.io/data/1.0/swagger.yaml', 'APIs/azure.com/search-searchservice/2019-05-06/swagger.yaml', 'APIs/googleapis.com/jobs/v3/swagger.yaml', 'APIs/storecove.com/2.0.1/swagger.yaml', 'APIs/googleapis.com/content/v2.1/swagger.yaml', 'APIs/amazonaws.com/resource-groups/2017-11-27/swagger.yaml', 'APIs/amazonaws.com/elasticmapreduce/2009-03-31/swagger.yaml', 'APIs/azure.com/hdinsight-configurations/2015-03-01-preview/swagger.yaml', 'APIs/googleapis.com/androidpublisher/v1.1/swagger.yaml', 'APIs/netlicensing.io/2.x/swagger.yaml', 'APIs/azure.com/recoveryservices-replicationusages/2016-06-01/swagger.yaml', 'APIs/googleapis.com/pagespeedonline/v5/swagger.yaml', 'APIs/azure.com/monitor-serviceDiagnosticsSettings_API/2016-09-01/swagger.yaml', 'APIs/amazonaws.com/storagegateway/2013-06-30/swagger.yaml', 'APIs/azure.com/containerservices-containerService/2016-03-30/swagger.yaml', 'APIs/jira.local/1.0.0/swagger.yaml', 'APIs/googleapis.com/adsense/v1.4/swagger.yaml', 'APIs/azure.com/containerservices-containerService/2017-01-31/swagger.yaml', 'APIs/azure.com/containerservice-containerService/2017-01-31/swagger.yaml', 'APIs/sportsdata.io/nfl-v3-scores/1.0/swagger.yaml', 'APIs/amazonaws.com/shield/2016-06-02/swagger.yaml', 'APIs/import.io/extraction/1.0/swagger.yaml', 'APIs/azure.com/redis/2015-08-01/swagger.yaml', 'APIs/contribly.com/1.0.0/swagger.yaml', 'APIs/googleapis.com/androidmanagement/v1/swagger.yaml', 'APIs/googleapis.com/oauth2/v1/swagger.yaml', 'APIs/googleapis.com/adexchangebuyer/v1.3/swagger.yaml', 'APIs/azure.com/web-WebApps/2018-11-01/swagger.yaml', 'APIs/azure.com/apimanagement-apimdeployment/2018-01-01/swagger.yaml', 'APIs/anchore.io/0.1.12/swagger.yaml', 'APIs/netatmo.net/1.1.1/swagger.yaml', 'APIs/googleapis.com/tasks/v1/swagger.yaml', 'APIs/azure.com/datalake-analytics-catalog/2016-11-01/swagger.yaml', 'APIs/googleapis.com/drive/v2/swagger.yaml', 'APIs/googleapis.com/sourcerepo/v1/swagger.yaml', 'APIs/googleapis.com/appstate/v1/swagger.yaml', 'APIs/github.com/v3/swagger.yaml', 'APIs/iva-api.com/2.0/swagger.yaml', 'APIs/reverb.com/3.0/swagger.yaml', 'APIs/googleapis.com/webmasters/v3/swagger.yaml', 'APIs/amazonaws.com/email/2010-12-01/swagger.yaml', 'APIs/amazonaws.com/glue/2017-03-31/swagger.yaml', 'APIs/googleapis.com/adexchangeseller/v1/swagger.yaml', 'APIs/googleapis.com/spectrum/v1explorer/swagger.yaml', 'APIs/googleapis.com/sqladmin/v1beta3/swagger.yaml', 'APIs/bungie.net/2.0.0/swagger.yaml', 'APIs/googleapis.com/androidpublisher/v2/swagger.yaml', 'APIs/googleapis.com/remotebuildexecution/v2/swagger.yaml', 'APIs/weatherbit.io/2.0.0/swagger.yaml', 'APIs/amazonaws.com/lightsail/2016-11-28/swagger.yaml', 'APIs/googleapis.com/alertcenter/v1beta1/swagger.yaml', 'APIs/googleapis.com/adexchangeseller/v2.0/swagger.yaml', 'APIs/googleapis.com/content/v2sandbox/swagger.yaml', 'APIs/taxamo.com/1/swagger.yaml', 'APIs/googleapis.com/sqladmin/v1beta4/swagger.yaml', 'APIs/googleapis.com/people/v1/swagger.yaml', 'APIs/googleapis.com/analytics/v2.4/swagger.yaml', 'APIs/nexmo.com/application/1.0.2/openapi.yaml', 'APIs/amazonaws.com/guardduty/2017-11-28/swagger.yaml', 'APIs/hetras-certification.net/hotel/v0/swagger.yaml', 'APIs/amazonaws.com/swf/2012-01-25/swagger.yaml', 'APIs/amazonaws.com/cognito-idp/2016-04-18/swagger.yaml', 'APIs/googleapis.com/adsensehost/v4.1/swagger.yaml', 'APIs/azure.com/visualstudio-Csm/2017-11-01-preview/swagger.yaml', 'APIs/azure.com/servicefabric/6.5.0.36/swagger.yaml', 'APIs/wmata.com/bus-route/1.0/swagger.yaml', 'APIs/googleapis.com/servicenetworking/v1/swagger.yaml', 'APIs/amazonaws.com/s3/2006-03-01/swagger.yaml', 'APIs/whatsapp.local/1.0/openapi.yaml', 'APIs/googleapis.com/doubleclicksearch/v2/swagger.yaml', 'APIs/googleapis.com/remotebuildexecution/v1alpha/swagger.yaml', 'APIs/googleapis.com/youtubeAnalytics/v1beta1/swagger.yaml', 'APIs/googleapis.com/appengine/v1beta5/swagger.yaml', 'APIs/victorops.com/0.0.3/swagger.yaml', 'APIs/googleapis.com/bigtableadmin/v2/swagger.yaml', 'APIs/googleapis.com/surveys/v2/swagger.yaml', 'APIs/googleapis.com/adexchangebuyer/v1.2/swagger.yaml', 'APIs/noosh.com/1.0/swagger.yaml', 'APIs/googleapis.com/vision/v1p2beta1/swagger.yaml', 'APIs/azure.com/monitor-activityLogAlerts_API/2017-03-01-preview/swagger.yaml', 'APIs/adyen.com/MarketPayNotificationService/3/openapi.yaml', 'APIs/googleapis.com/dataproc/v1alpha1/swagger.yaml', 'APIs/azure.com/datalake-store-filesystem/2015-10-01-preview/swagger.yaml', 'APIs/googleapis.com/siteVerification/v1/swagger.yaml', 'APIs/googleapis.com/adsense/v1.3/swagger.yaml', 'APIs/googleapis.com/containeranalysis/v1beta1/swagger.yaml', 'APIs/flat.io/2.8.0/swagger.yaml', 'APIs/googleapis.com/accesscontextmanager/v1beta/swagger.yaml', 'APIs/googleapis.com/plus/v1/swagger.yaml', 'APIs/rbaskets.in/1.0.0/swagger.yaml', 'APIs/googleapis.com/serviceconsumermanagement/v1/swagger.yaml', 'APIs/amazonaws.com/rds/2014-10-31/swagger.yaml', 'APIs/googleapis.com/compute/v1/swagger.yaml', 'APIs/zuora.com/2019-09-19/swagger.yaml', 'APIs/googleapis.com/androidpublisher/v1/swagger.yaml', 'APIs/azure.com/containerservice-containerService/2017-07-01/swagger.yaml', 'APIs/getgo.com/gototraining/1.0.0/swagger.yaml', 'APIs/azure.com/containerservice-containerService/2016-09-30/swagger.yaml', 'APIs/googleapis.com/containeranalysis/v1alpha1/swagger.yaml', 'APIs/googleapis.com/gamesManagement/v1management/swagger.yaml', 'APIs/googleapis.com/adexchangeseller/v1.1/swagger.yaml', 'APIs/googleapis.com/verifiedaccess/v1/swagger.yaml', 'APIs/googleapis.com/pagespeedonline/v4/swagger.yaml', 'APIs/googleapis.com/mirror/v1/swagger.yaml', 'APIs/googleapis.com/serviceusage/v1beta1/swagger.yaml', 'APIs/googleapis.com/dataflow/v1b3/swagger.yaml', 'APIs/nexmo.com/number-insight/1.0.4/openapi.yaml', 'APIs/googleapis.com/jobs/v2/swagger.yaml', 'APIs/amazonaws.com/elastictranscoder/2012-09-25/swagger.yaml', 'APIs/lyft.com/1.0.0/swagger.yaml', 'APIs/googleapis.com/servicenetworking/v1beta/swagger.yaml', 'APIs/googleapis.com/monitoring/v3/swagger.yaml', 'APIs/googleapis.com/urlshortener/v1/swagger.yaml', 'APIs/azure.com/apimanagement-apimdeployment/2018-06-01-preview/swagger.yaml', 'APIs/googleapis.com/playmoviespartner/v1/swagger.yaml', 'APIs/amazonaws.com/codebuild/2016-10-06/swagger.yaml', 'APIs/googleapis.com/books/v1/swagger.yaml', 'APIs/googleapis.com/dialogflow/v2/swagger.yaml', 'APIs/googleapis.com/logging/v2/swagger.yaml', 'APIs/googleapis.com/cloudresourcemanager/v1beta1/swagger.yaml', 'APIs/azure.com/containerservice-managedClusters/2017-08-31/swagger.yaml', 'APIs/transitfeeds.com/1.0.0/swagger.yaml', 'APIs/azure.com/servicefabric/6.4.0.36/swagger.yaml', 'APIs/youneedabudget.com/1.0.0/swagger.yaml', 'APIs/googleapis.com/gmail/v1/swagger.yaml', 'APIs/amazonaws.com/rds-data/2018-08-01/swagger.yaml', 'APIs/googleapis.com/appengine/v1beta/swagger.yaml', 'APIs/googleapis.com/ml/v1beta1/swagger.yaml', 'APIs/googleapis.com/servicecontrol/v1/swagger.yaml', 'APIs/googleapis.com/dfareporting/v3.2/swagger.yaml', 'APIs/googleapis.com/clouddebugger/v2/swagger.yaml', 'APIs/amazonaws.com/opsworkscm/2016-11-01/swagger.yaml', 'APIs/wmata.com/incidents/1.0/swagger.yaml', 'APIs/googleapis.com/testing/v1/swagger.yaml', 'APIs/visagecloud.com/1.1/swagger.yaml', 'APIs/azure.com/hdinsight-configurations/2018-06-01-preview/swagger.yaml', 'APIs/googleapis.com/healthcare/v1alpha2/swagger.yaml', 'APIs/googleapis.com/doubleclickbidmanager/v1/swagger.yaml', 'APIs/googleapis.com/compute/alpha/swagger.yaml', 'APIs/amazonaws.com/cloudfront/2017-10-30/swagger.yaml', 'APIs/azure.com/containerservices-containerService/2016-09-30/swagger.yaml', 'APIs/googleapis.com/logging/v2beta1/swagger.yaml', 'APIs/azure.com/compute/2019-03-01/swagger.yaml', 'APIs/azure.com/sql-tableAuditing/2014-04-01/swagger.yaml', 'APIs/amazonaws.com/discovery/2015-11-01/swagger.yaml', 'APIs/kubernetes.io/v1.17.0/swagger.yaml', 'APIs/azure.com/recoveryservicesbackup-bms/2016-12-01/swagger.yaml', 'APIs/azure.com/visualstudio-PipelineTemplates/2018-08-01-preview/swagger.yaml', 'APIs/googleapis.com/androidenterprise/v1/swagger.yaml', 'APIs/googleapis.com/civicinfo/v2/swagger.yaml', 'APIs/bitbucket.org/2.0/swagger.yaml', 'APIs/googleapis.com/slides/v1/swagger.yaml', 'APIs/googleapis.com/plusDomains/v1/swagger.yaml', 'APIs/googleapis.com/webfonts/v1/swagger.yaml', 'APIs/googleapis.com/clouduseraccounts/vm_beta/swagger.yaml', 'APIs/azure.com/resources-policyAssignments/2016-12-01/swagger.yaml', 'APIs/gitlab.com/v3/swagger.yaml', 'APIs/azure.com/resources-policyAssignments/2017-06-01-preview/swagger.yaml', 'APIs/googleapis.com/serviceuser/v1/swagger.yaml', 'APIs/amazonaws.com/directconnect/2012-10-25/swagger.yaml', 'APIs/googleapis.com/youtubereporting/v1/swagger.yaml', 'APIs/googleapis.com/drive/v3/swagger.yaml', 'APIs/googleapis.com/groupssettings/v1/swagger.yaml', 'APIs/gitea.io/1.1.1/swagger.yaml', 'APIs/googleapis.com/spanner/v1/swagger.yaml', 'APIs/beezup.com/2.0/swagger.yaml', 'APIs/googleapis.com/language/v1beta1/swagger.yaml', 'APIs/googleapis.com/healthcare/v1beta1/swagger.yaml', 'APIs/amazonaws.com/mediapackage/2017-10-12/swagger.yaml', 'APIs/osf.io/2.0/swagger.yaml', 'APIs/paccurate.io/0.1.1/swagger.yaml', 'APIs/crucible.local/1.0.0/swagger.yaml', 'APIs/squareup.com/2.0/swagger.yaml', 'APIs/azure.com/servicefabric-application/2019-03-01/swagger.yaml', 'APIs/amazonaws.com/iot/2015-05-28/swagger.yaml', 'APIs/azure.com/compute/2018-10-01/swagger.yaml', 'APIs/googleapis.com/dlp/v2/swagger.yaml', 'APIs/googleapis.com/remotebuildexecution/v1/swagger.yaml', 'APIs/googleapis.com/androidpublisher/v3/swagger.yaml', 'APIs/amazonaws.com/secretsmanager/2017-10-17/swagger.yaml', 'APIs/googleapis.com/dns/v1beta2/swagger.yaml', 'APIs/googleapis.com/admin/reports_v1/swagger.yaml', 'APIs/azure.com/visualstudio-Projects/2018-08-01-preview/swagger.yaml', 'APIs/googleapis.com/blogger/v2/swagger.yaml', 'APIs/googleapis.com/youtubeAnalytics/v2/swagger.yaml', 'APIs/googleapis.com/jobs/v3p1beta1/swagger.yaml', 'APIs/googleapis.com/pagespeedonline/v2/swagger.yaml', 'APIs/docusign.net/v2/swagger.yaml', 'APIs/googleapis.com/dns/v1/swagger.yaml', 'APIs/amazonaws.com/cloudfront/2018-06-18/swagger.yaml', 'APIs/googleapis.com/groupsmigration/v1/swagger.yaml', 'APIs/rebilly.com/2.1/swagger.yaml', 'APIs/bigoven.com/partner/swagger.yaml', 'APIs/googleapis.com/analytics/v3/swagger.yaml', 'APIs/googleapis.com/sheets/v4/swagger.yaml', 'APIs/amazonaws.com/ssm/2014-11-06/swagger.yaml', 'APIs/npr.org/listening/2/swagger.yaml', 'APIs/setlist.fm/1.0/swagger.yaml', 'APIs/linode.com/4.5.0/openapi.yaml', 'APIs/googleapis.com/dfareporting/v3.1/swagger.yaml', 'APIs/googleapis.com/storage/v1/swagger.yaml', 'APIs/googleapis.com/admin/datatransfer_v1/swagger.yaml', 'APIs/amazonaws.com/pinpoint/2016-12-01/swagger.yaml', 'APIs/googleapis.com/replicapool/v1beta1/swagger.yaml', 'APIs/googleapis.com/customsearch/v1/swagger.yaml', 'APIs/googleapis.com/deploymentmanager/alpha/swagger.yaml', 'APIs/adyen.com/MarketPayNotificationService/4/openapi.yaml', 'APIs/amazonaws.com/cloudfront/2018-11-05/swagger.yaml', 'APIs/googleapis.com/appengine/v1/swagger.yaml', 'APIs/googleapis.com/script/v1/swagger.yaml', 'APIs/googleapis.com/adexchangebuyer/v1.4/swagger.yaml', 'APIs/vimeo.com/3.4/openapi.yaml', 'APIs/googleapis.com/playcustomapp/v1/swagger.yaml', 'APIs/import.io/rss/1.0/swagger.yaml', 'APIs/cloudmersive.com/ocr/v1/swagger.yaml', 'APIs/azure.com/web-WebApps/2018-02-01/swagger.yaml', 'APIs/googleapis.com/discovery/v1/swagger.yaml', 'APIs/import.io/run/1.0/swagger.yaml', 'APIs/azure.com/signalr/2018-10-01/swagger.yaml']

#no containerservices and no 3 yaml error files(apis_nc), containerservices removed manually
apis_deprecated = ['APIs/adyen.com/MarketPayNotificationService/3/openapi.yaml', 'APIs/adyen.com/MarketPayNotificationService/4/openapi.yaml', 'APIs/agco-ats.com/v1/swagger.yaml', 'APIs/amazonaws.com/apigateway/2015-07-09/swagger.yaml', 'APIs/amazonaws.com/cloudfront/2016-11-25/swagger.yaml', 'APIs/amazonaws.com/cloudfront/2017-03-25/swagger.yaml', 'APIs/amazonaws.com/cloudfront/2017-10-30/swagger.yaml', 'APIs/amazonaws.com/cloudfront/2018-06-18/swagger.yaml', 'APIs/amazonaws.com/cloudfront/2018-11-05/swagger.yaml', 'APIs/amazonaws.com/cloudtrail/2013-11-01/swagger.yaml', 'APIs/amazonaws.com/codebuild/2016-10-06/swagger.yaml', 'APIs/amazonaws.com/codedeploy/2014-10-06/swagger.yaml', 'APIs/amazonaws.com/cognito-idp/2016-04-18/swagger.yaml', 'APIs/amazonaws.com/comprehendmedical/2018-10-30/swagger.yaml', 'APIs/amazonaws.com/directconnect/2012-10-25/swagger.yaml', 'APIs/amazonaws.com/discovery/2015-11-01/swagger.yaml', 'APIs/amazonaws.com/ec2/2016-11-15/swagger.yaml', 'APIs/amazonaws.com/elasticache/2015-02-02/swagger.yaml', 'APIs/amazonaws.com/elasticbeanstalk/2010-12-01/swagger.yaml', 'APIs/amazonaws.com/elasticmapreduce/2009-03-31/swagger.yaml', 'APIs/amazonaws.com/elastictranscoder/2012-09-25/swagger.yaml', 'APIs/amazonaws.com/email/2010-12-01/swagger.yaml', 'APIs/amazonaws.com/firehose/2015-08-04/swagger.yaml', 'APIs/amazonaws.com/glue/2017-03-31/swagger.yaml', 'APIs/amazonaws.com/guardduty/2017-11-28/swagger.yaml', 'APIs/amazonaws.com/iot/2015-05-28/swagger.yaml', 'APIs/amazonaws.com/iotthingsgraph/2018-09-06/swagger.yaml', 'APIs/amazonaws.com/lambda/2015-03-31/swagger.yaml', 'APIs/amazonaws.com/lightsail/2016-11-28/swagger.yaml', 'APIs/amazonaws.com/logs/2014-03-28/swagger.yaml', 'APIs/amazonaws.com/medialive/2017-10-14/swagger.yaml', 'APIs/amazonaws.com/mediapackage/2017-10-12/swagger.yaml', 'APIs/amazonaws.com/mturk-requester/2017-01-17/swagger.yaml', 'APIs/amazonaws.com/opsworkscm/2016-11-01/swagger.yaml', 'APIs/amazonaws.com/pinpoint/2016-12-01/swagger.yaml', 'APIs/amazonaws.com/ram/2018-01-04/swagger.yaml', 'APIs/amazonaws.com/rds/2014-10-31/swagger.yaml', 'APIs/amazonaws.com/rds-data/2018-08-01/swagger.yaml', 'APIs/amazonaws.com/resource-groups/2017-11-27/swagger.yaml', 'APIs/amazonaws.com/s3/2006-03-01/swagger.yaml', 'APIs/amazonaws.com/secretsmanager/2017-10-17/swagger.yaml', 'APIs/amazonaws.com/servicecatalog/2015-12-10/swagger.yaml', 'APIs/amazonaws.com/shield/2016-06-02/swagger.yaml', 'APIs/amazonaws.com/ssm/2014-11-06/swagger.yaml', 'APIs/amazonaws.com/storagegateway/2013-06-30/swagger.yaml', 'APIs/amazonaws.com/swf/2012-01-25/swagger.yaml', 'APIs/anchore.io/0.1.12/swagger.yaml', 'APIs/api2cart.com/1.0.0/swagger.yaml', 'APIs/atlassian.com/jira/v3/swagger.yaml', 'APIs/azure.com/apimanagement-apimdeployment/2017-03-01/swagger.yaml', 'APIs/azure.com/apimanagement-apimdeployment/2018-01-01/swagger.yaml', 'APIs/azure.com/applicationinsights-componentContinuousExport_API/2015-05-01/swagger.yaml', 'APIs/azure.com/compute/2018-06-01/swagger.yaml', 'APIs/azure.com/compute/2018-10-01/swagger.yaml', 'APIs/azure.com/compute/2019-03-01/swagger.yaml', 'APIs/azure.com/containerservice-containerService/2016-03-30/swagger.yaml', 'APIs/azure.com/containerservice-containerService/2016-09-30/swagger.yaml', 'APIs/azure.com/containerservice-containerService/2017-01-31/swagger.yaml', 'APIs/azure.com/containerservice-containerService/2017-07-01/swagger.yaml', 'APIs/azure.com/containerservice-managedClusters/2017-08-31/swagger.yaml',
                   'APIs/azure.com/databox/2019-09-01/swagger.yaml', 'APIs/azure.com/datafactory/2018-06-01/swagger.yaml', 'APIs/azure.com/datalake-analytics-catalog/2016-11-01/swagger.yaml', 'APIs/azure.com/eventhub-EventHub/2017-04-01/swagger.yaml', 'APIs/azure.com/machinelearningservices-datastore/2019-08-01/swagger.yaml', 'APIs/azure.com/monitor-serviceDiagnosticsSettings_API/2015-07-01/swagger.yaml', 'APIs/azure.com/monitor-serviceDiagnosticsSettings_API/2016-09-01/swagger.yaml', 'APIs/azure.com/recoveryservices-replicationusages/2016-06-01/swagger.yaml', 'APIs/azure.com/recoveryservicesbackup-bms/2016-12-01/swagger.yaml', 'APIs/azure.com/recoveryservicesbackup-bms/2017-07-01/swagger.yaml', 'APIs/azure.com/recoveryservicessiterecovery-service/2016-08-10/swagger.yaml', 'APIs/azure.com/redis/2015-08-01/swagger.yaml', 'APIs/azure.com/resources-policyAssignments/2016-12-01/swagger.yaml', 'APIs/azure.com/search-searchservice/2017-11-11-Preview/swagger.yaml', 'APIs/azure.com/search-searchservice/2019-05-06/swagger.yaml', 'APIs/azure.com/servicefabric/6.4.0.36/swagger.yaml', 'APIs/azure.com/servicefabric/6.5.0.36/swagger.yaml', 'APIs/azure.com/servicefabric-application/2019-03-01/swagger.yaml', 'APIs/azure.com/signalr/2018-10-01/swagger.yaml', 'APIs/azure.com/sql-tableAuditing/2014-04-01/swagger.yaml', 'APIs/azure.com/web-WebApps/2018-02-01/swagger.yaml', 'APIs/azure.com/web-WebApps/2018-11-01/swagger.yaml', 'APIs/bbc.com/1.0.0/openapi.yaml', 'APIs/beezup.com/2.0/swagger.yaml', 'APIs/bigoven.com/partner/swagger.yaml', 'APIs/billbee.io/v1/swagger.yaml', 'APIs/bitbucket.org/2.0/swagger.yaml', 'APIs/botify.com/1.0.0/swagger.yaml', 'APIs/bulksms.com/1.0.0/swagger.yaml', 'APIs/bungie.net/2.0.0/swagger.yaml', 'APIs/bunq.com/1.0/openapi.yaml', 'APIs/citrixonline.com/gotomeeting/1.0.0/swagger.yaml', 'APIs/cloudmersive.com/ocr/v1/swagger.yaml', 'APIs/contribly.com/1.0.0/swagger.yaml', 'APIs/crucible.local/1.0.0/swagger.yaml', 'APIs/docker.com/engine/1.33/swagger.yaml', 'APIs/docusign.net/v2/swagger.yaml', 'APIs/dracoon.team/4.5.0/swagger.yaml', 'APIs/flat.io/2.8.0/swagger.yaml', 'APIs/getgo.com/gototraining/1.0.0/swagger.yaml', 'APIs/getgo.com/gotowebinar/1.0.0/swagger.yaml', 'APIs/gitea.io/1.1.1/swagger.yaml', 'APIs/github.com/v3/swagger.yaml', 'APIs/gitlab.com/v3/swagger.yaml', 'APIs/googleapis.com/adexchangebuyer/v1.2/swagger.yaml', 'APIs/googleapis.com/adexchangebuyer/v1.3/swagger.yaml', 'APIs/googleapis.com/adexchangebuyer/v1.4/swagger.yaml', 'APIs/googleapis.com/adexchangeseller/v1/swagger.yaml', 'APIs/googleapis.com/adexchangeseller/v1.1/swagger.yaml', 'APIs/googleapis.com/adexchangeseller/v2.0/swagger.yaml', 'APIs/googleapis.com/admin/datatransfer_v1/swagger.yaml', 'APIs/googleapis.com/admin/directory_v1/swagger.yaml', 'APIs/googleapis.com/admin/reports_v1/swagger.yaml', 'APIs/googleapis.com/adsense/v1.3/swagger.yaml', 'APIs/googleapis.com/adsense/v1.4/swagger.yaml', 'APIs/googleapis.com/adsensehost/v4.1/swagger.yaml', 'APIs/googleapis.com/analytics/v2.4/swagger.yaml', 'APIs/googleapis.com/analytics/v3/swagger.yaml', 'APIs/googleapis.com/androidenterprise/v1/swagger.yaml', 'APIs/googleapis.com/androidmanagement/v1/swagger.yaml', 'APIs/googleapis.com/androidpublisher/v1/swagger.yaml', 'APIs/googleapis.com/androidpublisher/v1.1/swagger.yaml', 'APIs/googleapis.com/androidpublisher/v2/swagger.yaml', 'APIs/googleapis.com/androidpublisher/v3/swagger.yaml', 'APIs/googleapis.com/appengine/v1/swagger.yaml', 'APIs/googleapis.com/appsactivity/v1/swagger.yaml', 'APIs/googleapis.com/appstate/v1/swagger.yaml', 'APIs/googleapis.com/bigquery/v2/swagger.yaml', 'APIs/googleapis.com/bigquerydatatransfer/v1/swagger.yaml', 'APIs/googleapis.com/bigtableadmin/v2/swagger.yaml', 'APIs/googleapis.com/blogger/v2/swagger.yaml', 'APIs/googleapis.com/blogger/v3/swagger.yaml', 'APIs/googleapis.com/books/v1/swagger.yaml', 'APIs/googleapis.com/calendar/v3/swagger.yaml', 'APIs/googleapis.com/civicinfo/v2/swagger.yaml', 'APIs/googleapis.com/cloudbilling/v1/swagger.yaml', 'APIs/googleapis.com/clouddebugger/v2/swagger.yaml', 'APIs/googleapis.com/compute/v1/swagger.yaml', 'APIs/googleapis.com/container/v1/swagger.yaml', 'APIs/googleapis.com/content/v2/swagger.yaml', 'APIs/googleapis.com/content/v2.1/swagger.yaml', 'APIs/googleapis.com/customsearch/v1/swagger.yaml', 'APIs/googleapis.com/dataflow/v1b3/swagger.yaml', 'APIs/googleapis.com/deploymentmanager/v2/swagger.yaml', 'APIs/googleapis.com/dfareporting/v2.7/swagger.yaml', 'APIs/googleapis.com/dfareporting/v2.8/swagger.yaml', 'APIs/googleapis.com/dfareporting/v3.0/swagger.yaml', 'APIs/googleapis.com/dfareporting/v3.1/swagger.yaml', 'APIs/googleapis.com/dfareporting/v3.2/swagger.yaml', 'APIs/googleapis.com/dfareporting/v3.3/swagger.yaml', 'APIs/googleapis.com/dialogflow/v2/swagger.yaml', 'APIs/googleapis.com/discovery/v1/swagger.yaml', 'APIs/googleapis.com/dlp/v2/swagger.yaml', 'APIs/googleapis.com/dns/v1/swagger.yaml', 'APIs/googleapis.com/doubleclickbidmanager/v1/swagger.yaml', 'APIs/googleapis.com/doubleclicksearch/v2/swagger.yaml', 'APIs/googleapis.com/drive/v2/swagger.yaml', 'APIs/googleapis.com/drive/v3/swagger.yaml', 'APIs/googleapis.com/driveactivity/v2/swagger.yaml', 'APIs/googleapis.com/fitness/v1/swagger.yaml', 'APIs/googleapis.com/fusiontables/v1/swagger.yaml', 'APIs/googleapis.com/fusiontables/v2/swagger.yaml', 'APIs/googleapis.com/games/v1/swagger.yaml', 'APIs/googleapis.com/gamesConfiguration/v1configuration/swagger.yaml', 'APIs/googleapis.com/gamesManagement/v1management/swagger.yaml', 'APIs/googleapis.com/genomics/v1/swagger.yaml', 'APIs/googleapis.com/gmail/v1/swagger.yaml', 'APIs/googleapis.com/groupsmigration/v1/swagger.yaml', 'APIs/googleapis.com/groupssettings/v1/swagger.yaml', 'APIs/googleapis.com/iam/v1/swagger.yaml', 'APIs/googleapis.com/identitytoolkit/v3/swagger.yaml', 'APIs/googleapis.com/jobs/v2/swagger.yaml', 'APIs/googleapis.com/jobs/v3/swagger.yaml', 'APIs/googleapis.com/licensing/v1/swagger.yaml', 'APIs/googleapis.com/logging/v2/swagger.yaml', 'APIs/googleapis.com/mirror/v1/swagger.yaml', 'APIs/googleapis.com/monitoring/v3/swagger.yaml', 'APIs/googleapis.com/oauth2/v1/swagger.yaml', 'APIs/googleapis.com/oauth2/v2/swagger.yaml', 'APIs/googleapis.com/pagespeedonline/v1/swagger.yaml', 'APIs/googleapis.com/pagespeedonline/v2/swagger.yaml', 'APIs/googleapis.com/pagespeedonline/v4/swagger.yaml', 'APIs/googleapis.com/pagespeedonline/v5/swagger.yaml', 'APIs/googleapis.com/partners/v2/swagger.yaml', 'APIs/googleapis.com/people/v1/swagger.yaml', 'APIs/googleapis.com/playcustomapp/v1/swagger.yaml', 'APIs/googleapis.com/playmoviespartner/v1/swagger.yaml', 'APIs/googleapis.com/plus/v1/swagger.yaml', 'APIs/googleapis.com/plusDomains/v1/swagger.yaml', 'APIs/googleapis.com/remotebuildexecution/v1/swagger.yaml', 'APIs/googleapis.com/remotebuildexecution/v2/swagger.yaml', 'APIs/googleapis.com/reseller/v1/swagger.yaml', 'APIs/googleapis.com/script/v1/swagger.yaml', 'APIs/googleapis.com/serviceconsumermanagement/v1/swagger.yaml', 'APIs/googleapis.com/servicecontrol/v1/swagger.yaml', 'APIs/googleapis.com/servicemanagement/v1/swagger.yaml', 'APIs/googleapis.com/servicenetworking/v1/swagger.yaml', 'APIs/googleapis.com/serviceusage/v1/swagger.yaml', 'APIs/googleapis.com/serviceuser/v1/swagger.yaml', 'APIs/googleapis.com/sheets/v4/swagger.yaml', 'APIs/googleapis.com/siteVerification/v1/swagger.yaml', 'APIs/googleapis.com/slides/v1/swagger.yaml', 'APIs/googleapis.com/sourcerepo/v1/swagger.yaml', 'APIs/googleapis.com/spanner/v1/swagger.yaml', 'APIs/googleapis.com/spectrum/v1explorer/swagger.yaml', 'APIs/googleapis.com/storage/v1/swagger.yaml', 'APIs/googleapis.com/surveys/v2/swagger.yaml', 'APIs/googleapis.com/tagmanager/v1/swagger.yaml', 'APIs/googleapis.com/tasks/v1/swagger.yaml', 'APIs/googleapis.com/testing/v1/swagger.yaml', 'APIs/googleapis.com/tpu/v1/swagger.yaml', 'APIs/googleapis.com/urlshortener/v1/swagger.yaml', 'APIs/googleapis.com/verifiedaccess/v1/swagger.yaml', 'APIs/googleapis.com/vision/v1/swagger.yaml', 'APIs/googleapis.com/webfonts/v1/swagger.yaml', 'APIs/googleapis.com/webmasters/v3/swagger.yaml', 'APIs/googleapis.com/youtube/v3/swagger.yaml', 'APIs/googleapis.com/youtubeAnalytics/v2/swagger.yaml', 'APIs/googleapis.com/youtubereporting/v1/swagger.yaml', 'APIs/gov.bc.ca/geocoder/2.0.0/openapi.yaml', 'APIs/here.com/tracking/2.0.0/swagger.yaml', 'APIs/hetras-certification.net/booking/v0/swagger.yaml', 'APIs/hetras-certification.net/hotel/v0/swagger.yaml', 'APIs/import.io/data/1.0/swagger.yaml', 'APIs/import.io/extraction/1.0/swagger.yaml', 'APIs/import.io/rss/1.0/swagger.yaml', 'APIs/import.io/run/1.0/swagger.yaml', 'APIs/import.io/schedule/1.0/swagger.yaml', 'APIs/instagram.com/1.0.0/swagger.yaml', 'APIs/iva-api.com/2.0/swagger.yaml', 'APIs/jira.local/1.0.0/swagger.yaml', 'APIs/kubernetes.io/v1.17.0/swagger.yaml', 'APIs/linode.com/4.5.0/openapi.yaml', 'APIs/lyft.com/1.0.0/swagger.yaml', 'APIs/nba.com/1.0.0/swagger.yaml', 'APIs/netatmo.net/1.1.1/swagger.yaml', 'APIs/netlicensing.io/2.x/swagger.yaml', 'APIs/nexmo.com/application/1.0.2/openapi.yaml', 'APIs/nexmo.com/number-insight/1.0.4/openapi.yaml', 'APIs/noosh.com/1.0/swagger.yaml', 'APIs/npr.org/listening/2/swagger.yaml', 'APIs/nytimes.com/community/3.0.0/swagger.yaml', 'APIs/osf.io/2.0/swagger.yaml', 'APIs/paccurate.io/0.1.1/swagger.yaml', 'APIs/rbaskets.in/1.0.0/swagger.yaml', 'APIs/rebilly.com/2.1/swagger.yaml', 'APIs/reverb.com/3.0/swagger.yaml', 'APIs/setlist.fm/1.0/swagger.yaml', 'APIs/shutterstock.com/1.0.15/openapi.yaml', 'APIs/slack.com/1.2.0/swagger.yaml', 'APIs/sportsdata.io/nfl-v3-scores/1.0/swagger.yaml', 'APIs/sportsdata.io/nfl-v3-stats/1.0/swagger.yaml', 'APIs/squareup.com/2.0/swagger.yaml', 'APIs/storecove.com/2.0.1/swagger.yaml', 'APIs/stripe.com/2019-09-09/swagger.yaml', 'APIs/taxamo.com/1/swagger.yaml', 'APIs/thetvdb.com/2.2.0/swagger.yaml', 'APIs/tomtom.com/search/1.0.0/openapi.yaml', 'APIs/transitfeeds.com/1.0.0/swagger.yaml', 'APIs/victorops.com/0.0.3/swagger.yaml', 'APIs/vimeo.com/3.4/openapi.yaml', 'APIs/visagecloud.com/1.1/swagger.yaml', 'APIs/vocadb.net/v1/swagger.yaml', 'APIs/weatherbit.io/2.0.0/swagger.yaml', 'APIs/whatsapp.local/1.0/openapi.yaml', 'APIs/wmata.com/bus-route/1.0/swagger.yaml', 'APIs/wmata.com/incidents/1.0/swagger.yaml', 'APIs/wmata.com/rail-station/1.0/swagger.yaml', 'APIs/wowza.com/1/swagger.yaml', 'APIs/youneedabudget.com/1.0.0/swagger.yaml', 'APIs/zuora.com/2019-09-19/swagger.yaml']

apis_nc = ['APIs/azure.com/cognitiveservices-LUIS-Programmatic/v2.0/swagger.yaml', 'APIs/azure.com/sql-deprecated/2014-04-01/swagger.yaml', 'APIs/epa.gov/eff/1.0.0/swagger.yaml']
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
    # files_dataset_standard = readFile("result/dataset_file.csv")
    files_dataset_standard = readFile("result/RQ1/deprecated_onefile_manual.csv")
    apis = []

    desc_api = []
    key_api = []

    for file in files_dataset_standard:
        api_name = getApiName(file.split("/"))
        apis.append(api_name)

    print(len(list(set(apis))))

    deprecated_apis_and_files = {}

    text_description = {}

    for file_location in files_dataset_standard:

        # print(file_location)
        depr_desc = []
        depr_desc_key = []
        depr_key = []
        with open(file_location, 'r', encoding="utf-8") as stream:
            api_unique = getApiName(file_location.split("/"))
            # yaml.add_constructor(':', "")

            try:
                data_stream = yaml.safe_load(stream)
                # try:
                #     validate_spec(data_stream)
                # except:
                #     print("fl:" + file_location)
                data = flatten_json(data_stream)
                for key in data:
                    if key.endswith("description") or key.endswith("summary"):
                        split_values = key.split("_")
                        # print(key)
                        if ("deprecat" in key.lower()) and ("&deprecated!" not in key.lower()):    #deprecated_description, deprecation
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

                                            if value in text_description:
                                                value_file = text_description[value]
                                                text_description[value] = [file_location] + value_file
                                            else:
                                                text_description[value] = [file_location]
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
                    if api_unique in deprecated_apis_and_files:
                        value = deprecated_apis_and_files[api_unique]
                        deprecated_apis_and_files[api_unique] = [file_location] + value
                    else:
                        deprecated_apis_and_files[api_unique] = [file_location]
            except yaml.YAMLError as exc:
                print(api_unique)
                print(exc)
    print(len(list(set(results))))
    print("description")
    print(len(list(set(text_description))))
    # print((list(set(text_description))))
    print("desc file")
    print(len(list(set(desc_api))))
    desc_apis = []
    key_apis = []
    for fl in list(set(desc_api)):
        api_name = getApiName(fl.split("/"))
        desc_apis.append(api_name)
    # print((list(set(desc_api))))
    print("desc api")
    print(len(list(set(desc_apis))))
    apis_for_alternate = readFile("result/RQ3/alternate.csv")

    print("not in:")
    for api in list(set(desc_apis)):
        if api not in apis_for_alternate:
            print(api)


    print("depre key")

    print(len(list(set(key_api))))
    for fl in list(set(key_api)):
        api_name = getApiName(fl.split("/"))
        key_apis.append(api_name)

    print(len(list(set(key_apis))))
    # print((list(set(key_apis))))
    # print((list(set(desc_api))))

    print("-------------------------------------------")

    for key_api in key_apis:
        if key_api not in desc_apis:
            print(key_api)


    print("-------------------------------------------")


    print(len(list(set(list(set(desc_apis)) + list(set(key_apis))))))
    print(len(list(set(list(set(desc_api)) + list(set(key_api))))))


    count_common = 0
    for api in key_apis:
        if api in desc_apis:
            print(api)
            count_common = count_common + 1

    print(count_common)

    count_common = 0
    for api in key_api:
        if api in desc_api:
            print(api)
            count_common = count_common + 1

    print(count_common)

    # for text in text_description:
    #     print(text)
    #     print("-----------")
    #     print(text_description[text])

    # This will be used when dataset_file will be used for swagger-diff
    # with open('result/RQ1/deprecated_file.csv', mode='w', encoding="utf-8") as res_file:
    #     res_writer = csv.writer(res_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
    #     res_writer.writerow(["File having deprecated"])
    #     for api_file in results:
    #         res_writer.writerow([api_file])
    #
    # with open('result/RQ1/deprecated_api.csv', mode='w', encoding="utf-8") as res_file:
    #     res_writer = csv.writer(res_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
    #     res_writer.writerow(["api_unique", "files deprecated", "count deprecated files"])
    #
    #     for api_unique in deprecated_apis_and_files:
    #         values = deprecated_apis_and_files[api_unique]
    #         res_writer.writerow([api_unique, ", ".join(values), len(values), len(list(set(values)))]) #for double check list-set used
    #
    #
    # with open('result/RQ1/text_and_file.csv', mode='w', encoding="utf-8") as res_file:
    #     res_writer = csv.writer(res_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
    #     res_writer.writerow(["text", "File having deprecated"])
    #     for desc in text_description:
    #         values = ", ".join(text_description[desc])
    #         res_writer.writerow([desc, values])
    #






findAPIDeprecated()

# print(len(list(set(all_descriptions))))
print("============================================")
# generateInfoDeprecated("result/RQ1/deprecated_api.csv", "result/dataset/dataset.csv" )


# 265 files from 226 APIs, 887 sentences, 244 files from 210 have desc, 51 files from 47 API

#
# C:\Users\jerin\AppData\Local\Programs\Python\Python37\python.exe "C:/UNI-MS/API HOTSPOTS/API HOTSPOTS/apibot-master/deprecation/april/latest-rqone.py"
# 226
# deprecated operation
# IN summary
# deprecated operation
# IN summary
# deprecated operation
# IN summary
# deprecated operation
# IN summary
# definitions_DocumentationRule_properties_deprecationDescription_description
# APIs/googleapis.com/serviceconsumermanagement/v1/swagger.yaml
# Deprecation description of the selected element(s). It can be provided if
# an element is marked as `deprecated`.
# deprecated: get organizers
# IN summary
# deprecated. please use "article", which is a new format for food glossary articles, which separates out the images.
# IN summary
# get all the images for a recipe. deprecated. please use /recipe/{recipeid}/photos.
# IN summary
# delete a review by recipeid and reviewid. deprecated. please see recipe/review/{reviewid} for the preferred method. (we are moving from an integer-based id system to a guid-style string-based id system for reviews and replies.)
# IN summary
# get a given review - deprecated. see recipe/review/{reviewid} for the current usage. beginning in january 2017, bigoven moded from an integer-based id system to a guid-style string-based id system for reviews and replies. we are also supporting more of a "google play" style model for reviews and replies. that is, there are top-level reviews and then an unlimited list of replies (which do not carry star ratings) underneath existing reviews. also, a given user can only have one review per recipe. existing legacy endpoints will continue to work, but we strongly recommend you migrate to using the newer endpoints listed which do not carry the "deprecated" flag.
# IN summary
# http put (update) a recipe review. deprecated. please see recipe/review/{reviewid} put for the new endpoint. we are moving to a string-based primary key system, no longer integers, for reviews and replies.
# IN summary
# definitions_DocumentationRule_properties_deprecationDescription_description
# APIs/googleapis.com/serviceuser/v1/swagger.yaml
# Deprecation description of the selected element(s). It can be provided if an
# element is marked as `deprecated`.
# out
# <p>modifies the staging labels attached to a version of a secret. staging labels are used to track a version as it progresses through the secret rotation process. you can attach a staging label to only one version of a secret at a time. if a staging label to be added is already attached to another version, then it is moved--removed from the other version first and then attached to this one. for more information about staging labels, see <a href="https://docs.aws.amazon.com/secretsmanager/latest/userguide/terms-concepts.html#term_staging-label">staging labels</a> in the <i>aws secrets manager user guide</i>. </p> <p>the staging labels that you specify in the <code>versionstage</code> parameter are added to the existing list of staging labels--they don't replace it.</p> <p>you can move the <code>awscurrent</code> staging label to this version by including it in this call.</p> <note> <p>whenever you move <code>awscurrent</code>, secrets manager automatically moves the label <code>awsprevious</code> to the version that <code>awscurrent</code> was removed from.</p> </note> <p>if this action results in the last label being removed from a version, then the version is considered to be 'deprecated' and can be deleted by secrets manager.</p> <p> <b>minimum permissions</b> </p> <p>to run this command, you must have the following permissions:</p> <ul> <li> <p>secretsmanager:updatesecretversionstage</p> </li> </ul> <p> <b>related operations</b> </p> <ul> <li> <p>to get the list of staging labels that are currently associated with a version of a secret, use <code> <a>describesecret</a> </code> and examine the <code>secretversionstostages</code> response value. </p> </li> </ul>
# definitions_ListSecretVersionIdsRequest_properties_IncludeDeprecated_description
# APIs/amazonaws.com/secretsmanager/2017-10-17/swagger.yaml
# (Optional) Specifies that you want the results to include versions that do not have any staging labels attached to them. Such versions are considered deprecated and are subject to deletion by Secrets Manager as needed.
# definitions_io.k8s.api.events.v1beta1.Event_properties_deprecatedCount_description
# APIs/kubernetes.io/v1.17.0/swagger.yaml
# Deprecated field assuring backward compatibility with core.v1 Event type
# definitions_io.k8s.api.events.v1beta1.Event_properties_deprecatedFirstTimestamp_description
# APIs/kubernetes.io/v1.17.0/swagger.yaml
# Deprecated field assuring backward compatibility with core.v1 Event type
# definitions_io.k8s.api.events.v1beta1.Event_properties_deprecatedLastTimestamp_description
# APIs/kubernetes.io/v1.17.0/swagger.yaml
# Deprecated field assuring backward compatibility with core.v1 Event type
# definitions_io.k8s.api.events.v1beta1.Event_properties_deprecatedSource_description
# APIs/kubernetes.io/v1.17.0/swagger.yaml
# Deprecated field assuring backward compatibility with core.v1 Event type
# deprecated: get historical meetings by group
# IN summary
# deprecated: get historical meetings
# IN summary
# deprecated: get meetings by organizer
# IN summary
# start capturing network packets for the site (to be deprecated).
# IN summary
# start capturing network packets for the site (to be deprecated).
# IN summary
# definitions_DocumentationRule_properties_deprecationDescription_description
# APIs/googleapis.com/servicemanagement/v1/swagger.yaml
# Deprecation description of the selected element(s). It can be provided if
# an element is marked as `deprecated`.
# definitions_DocumentationRule_properties_deprecationDescription_description
# APIs/googleapis.com/servicenetworking/v1/swagger.yaml
# Deprecation description of the selected element(s). It can be provided if
# an element is marked as `deprecated`.
# out
# the result of the revision check. possible values are: - "ok" - the revision being used is current. - "deprecated" - there is currently a newer version available, but the revision being used still works. - "invalid" - the revision being used is not supported in any released version.
# paths_/{project}/global/images/{image}/deprecate_post_description
# APIs/googleapis.com/compute/v1/swagger.yaml
# Sets the deprecation status of an image.
#
# If an empty request body is given, clears the deprecation status instead.
# paths_/{project}/global/images/{image}/deprecate_post_parameters_1_description
# APIs/googleapis.com/compute/v1/swagger.yaml
# Image name.
# paths_/{project}/global/images/{image}/deprecate_post_parameters_2_description
# APIs/googleapis.com/compute/v1/swagger.yaml
# Project ID for this request.
# paths_/{project}/global/images/{image}/deprecate_post_parameters_3_description
# APIs/googleapis.com/compute/v1/swagger.yaml
# An optional request ID to identify requests. Specify a unique request ID so that if you must retry your request, the server will know to ignore the request if it has already been completed.
#
# For example, consider a situation where you make an initial request and the request times out. If you make the request again with the same request ID, the server can check if original operation with the same request ID was received, and if so, will ignore the second request. This prevents clients from accidentally creating duplicate commitments.
#
# The request ID must be a valid UUID with the exception that zero UUID is not supported (00000000-0000-0000-0000-000000000000).
# paths_/{project}/global/images/{image}/deprecate_post_responses_200_description
# APIs/googleapis.com/compute/v1/swagger.yaml
# Successful response
# definitions_AcceleratorType_properties_deprecated_description
# APIs/googleapis.com/compute/v1/swagger.yaml
# [Output Only] The deprecation status associated with this accelerator type.
# definitions_DeprecationStatus_description
# APIs/googleapis.com/compute/v1/swagger.yaml
# Deprecation status for a public resource.
# definitions_DeprecationStatus_properties_deleted_description
# APIs/googleapis.com/compute/v1/swagger.yaml
# An optional RFC3339 timestamp on or after which the state of this resource is intended to change to DELETED. This is only informational and the status will not change unless the client explicitly changes it.
# definitions_DeprecationStatus_properties_deprecated_description
# APIs/googleapis.com/compute/v1/swagger.yaml
# An optional RFC3339 timestamp on or after which the state of this resource is intended to change to DEPRECATED. This is only informational and the status will not change unless the client explicitly changes it.
# definitions_DeprecationStatus_properties_obsolete_description
# APIs/googleapis.com/compute/v1/swagger.yaml
# An optional RFC3339 timestamp on or after which the state of this resource is intended to change to OBSOLETE. This is only informational and the status will not change unless the client explicitly changes it.
# definitions_DeprecationStatus_properties_replacement_description
# APIs/googleapis.com/compute/v1/swagger.yaml
# The URL of the suggested replacement for a deprecated resource. The suggested replacement resource must be the same kind of resource as the deprecated resource.
# definitions_DeprecationStatus_properties_state_description
# APIs/googleapis.com/compute/v1/swagger.yaml
# The deprecation state of this resource. This can be ACTIVE, DEPRECATED, OBSOLETE, or DELETED. Operations which communicate the end of life date for an image, can use ACTIVE. Operations which create a new resource using a DEPRECATED resource will return successfully, but with a warning indicating the deprecated resource and recommending its replacement. Operations which use OBSOLETE or DELETED resources will be rejected and result in an error.
# definitions_DiskType_properties_deprecated_description
# APIs/googleapis.com/compute/v1/swagger.yaml
# [Output Only] The deprecation status associated with this disk type.
# definitions_Image_properties_deprecated_description
# APIs/googleapis.com/compute/v1/swagger.yaml
# The deprecation status associated with this image.
# definitions_MachineType_properties_deprecated_description
# APIs/googleapis.com/compute/v1/swagger.yaml
# [Output Only] The deprecation status associated with this machine type.
# definitions_NodeType_properties_deprecated_description
# APIs/googleapis.com/compute/v1/swagger.yaml
# [Output Only] The deprecation status associated with this node type.
# definitions_Region_properties_deprecated_description
# APIs/googleapis.com/compute/v1/swagger.yaml
# [Output Only] The deprecation status associated with this region.
# definitions_Zone_properties_deprecated_description
# APIs/googleapis.com/compute/v1/swagger.yaml
# [Output Only] The deprecation status associated with this zone.
# paths_/thing-types/{thingTypeName}/deprecate_post_description
# APIs/amazonaws.com/iot/2015-05-28/swagger.yaml
# Deprecates a thing type. You can not associate new things with deprecated thing type.
# paths_/thing-types/{thingTypeName}/deprecate_post_responses_200_description
# APIs/amazonaws.com/iot/2015-05-28/swagger.yaml
# Success
# paths_/thing-types/{thingTypeName}/deprecate_post_responses_480_description
# APIs/amazonaws.com/iot/2015-05-28/swagger.yaml
# ResourceNotFoundException
# paths_/thing-types/{thingTypeName}/deprecate_post_responses_481_description
# APIs/amazonaws.com/iot/2015-05-28/swagger.yaml
# InvalidRequestException
# paths_/thing-types/{thingTypeName}/deprecate_post_responses_482_description
# APIs/amazonaws.com/iot/2015-05-28/swagger.yaml
# ThrottlingException
# paths_/thing-types/{thingTypeName}/deprecate_post_responses_483_description
# APIs/amazonaws.com/iot/2015-05-28/swagger.yaml
# UnauthorizedException
# paths_/thing-types/{thingTypeName}/deprecate_post_responses_484_description
# APIs/amazonaws.com/iot/2015-05-28/swagger.yaml
# ServiceUnavailableException
# paths_/thing-types/{thingTypeName}/deprecate_post_responses_485_description
# APIs/amazonaws.com/iot/2015-05-28/swagger.yaml
# InternalFailureException
# paths_/thing-types/{thingTypeName}/deprecate_post_parameters_0_description
# APIs/amazonaws.com/iot/2015-05-28/swagger.yaml
# The name of the thing type to deprecate.
# paths_/thing-types/{thingTypeName}/deprecate_post_parameters_1_schema_properties_undoDeprecate_description
# APIs/amazonaws.com/iot/2015-05-28/swagger.yaml
# Whether to undeprecate a deprecated thing type. If <b>true</b>, the thing type will not be deprecated anymore and you can associate it with things.
# definitions_DeprecateThingTypeResponse_description
# APIs/amazonaws.com/iot/2015-05-28/swagger.yaml
# The output for the DeprecateThingType operation.
# definitions_DeprecateThingTypeRequest_properties_undoDeprecate_description
# APIs/amazonaws.com/iot/2015-05-28/swagger.yaml
# Whether to undeprecate a deprecated thing type. If <b>true</b>, the thing type will not be deprecated anymore and you can associate it with things.
# definitions_DeprecateThingTypeRequest_description
# APIs/amazonaws.com/iot/2015-05-28/swagger.yaml
# The input for the DeprecateThingType operation.
# definitions_ThingTypeMetadata_properties_deprecationDate_description
# APIs/amazonaws.com/iot/2015-05-28/swagger.yaml
# The date and time when the thing type was deprecated.
# definitions_MarketplaceLabel_properties_deprecatedMarketplaceDealParty_description
# APIs/googleapis.com/adexchangebuyer/v1.4/swagger.yaml
# Information about the party that created the label.
# definitions_BuildBazelRemoteExecutionV2ServerCapabilities_properties_deprecatedApiVersion_description
# APIs/googleapis.com/remotebuildexecution/v2/swagger.yaml
# Earliest RE API version supported, including deprecated versions.
# game stats by season (deprecated, use team game stats instead)
# IN summary
# game stats by week (deprecated, use team game stats instead)
# IN summary
# components_schemas_ImagePrivate_properties_deprecated_description
# APIs/linode.com/4.5.0/openapi.yaml
# Whether or not this Image is deprecated. Will only be True for deprecated public Images.
#
# components_schemas_ImagePublic_properties_deprecated_description
# APIs/linode.com/4.5.0/openapi.yaml
# Whether or not this Image is deprecated. Will only be true for deprecated public Images.
#
# paths_/#X-Amz-Target=IotThingsGraphFrontEndService.DeprecateFlowTemplate_post_description
# APIs/amazonaws.com/iotthingsgraph/2018-09-06/swagger.yaml
# Deprecates the specified workflow. This action marks the workflow for deletion. Deprecated flows can't be deployed, but existing deployments will continue to run.
# paths_/#X-Amz-Target=IotThingsGraphFrontEndService.DeprecateFlowTemplate_post_responses_200_description
# APIs/amazonaws.com/iotthingsgraph/2018-09-06/swagger.yaml
# Success
# paths_/#X-Amz-Target=IotThingsGraphFrontEndService.DeprecateFlowTemplate_post_responses_480_description
# APIs/amazonaws.com/iotthingsgraph/2018-09-06/swagger.yaml
# InvalidRequestException
# paths_/#X-Amz-Target=IotThingsGraphFrontEndService.DeprecateFlowTemplate_post_responses_481_description
# APIs/amazonaws.com/iotthingsgraph/2018-09-06/swagger.yaml
# ThrottlingException
# paths_/#X-Amz-Target=IotThingsGraphFrontEndService.DeprecateFlowTemplate_post_responses_482_description
# APIs/amazonaws.com/iotthingsgraph/2018-09-06/swagger.yaml
# InternalFailureException
# paths_/#X-Amz-Target=IotThingsGraphFrontEndService.DeprecateFlowTemplate_post_responses_483_description
# APIs/amazonaws.com/iotthingsgraph/2018-09-06/swagger.yaml
# ResourceNotFoundException
# paths_/#X-Amz-Target=IotThingsGraphFrontEndService.DeprecateSystemTemplate_post_description
# APIs/amazonaws.com/iotthingsgraph/2018-09-06/swagger.yaml
# Deprecates the specified system.
# paths_/#X-Amz-Target=IotThingsGraphFrontEndService.DeprecateSystemTemplate_post_responses_200_description
# APIs/amazonaws.com/iotthingsgraph/2018-09-06/swagger.yaml
# Success
# paths_/#X-Amz-Target=IotThingsGraphFrontEndService.DeprecateSystemTemplate_post_responses_480_description
# APIs/amazonaws.com/iotthingsgraph/2018-09-06/swagger.yaml
# InvalidRequestException
# paths_/#X-Amz-Target=IotThingsGraphFrontEndService.DeprecateSystemTemplate_post_responses_481_description
# APIs/amazonaws.com/iotthingsgraph/2018-09-06/swagger.yaml
# ThrottlingException
# paths_/#X-Amz-Target=IotThingsGraphFrontEndService.DeprecateSystemTemplate_post_responses_482_description
# APIs/amazonaws.com/iotthingsgraph/2018-09-06/swagger.yaml
# InternalFailureException
# paths_/#X-Amz-Target=IotThingsGraphFrontEndService.DeprecateSystemTemplate_post_responses_483_description
# APIs/amazonaws.com/iotthingsgraph/2018-09-06/swagger.yaml
# ResourceNotFoundException
# definitions_DeprecateFlowTemplateRequest_properties_id_description
# APIs/amazonaws.com/iotthingsgraph/2018-09-06/swagger.yaml
# <p>The ID of the workflow to be deleted.</p> <p>The ID should be in the following format.</p> <p> <code>urn:tdm:REGION/ACCOUNT ID/default:workflow:WORKFLOWNAME</code> </p>
# definitions_DeprecateSystemTemplateRequest_properties_id_description
# APIs/amazonaws.com/iotthingsgraph/2018-09-06/swagger.yaml
# <p>The ID of the system to delete.</p> <p>The ID should be in the following format.</p> <p> <code>urn:tdm:REGION/ACCOUNT ID/default:system:SYSTEMNAME</code> </p>
# definitions_UploadEntityDefinitionsRequest_properties_deprecateExistingEntities_description
# APIs/amazonaws.com/iotthingsgraph/2018-09-06/swagger.yaml
# A Boolean that specifies whether to deprecate all entities in the latest version before uploading the new <code>DefinitionDocument</code>. If set to <code>true</code>, the upload will create a new namespace version.
# deprecated. set client subscription status for an update group.
# IN summary
# game stats by season (deprecated, use team game stats instead)
# IN summary
# game stats by week (deprecated, use team game stats instead)
# IN summary
# definitions_DocumentationRule_properties_deprecationDescription_description
# APIs/googleapis.com/serviceusage/v1/swagger.yaml
# Deprecation description of the selected element(s). It can be provided if
# an element is marked as `deprecated`.
# definitions_KeyRangeLocation_properties_deprecatedPersistentDirectory_description
# APIs/googleapis.com/dataflow/v1b3/swagger.yaml
# DEPRECATED. The location of the persistent state for this range, as a
# persistent directory in the worker local filesystem.
# deprecated, please use 1.1 version
# IN summary
# deprecated. gets a tag by name.
# IN summary
# start capturing network packets for the site (to be deprecated).
# IN summary
# start capturing network packets for the site (to be deprecated).
# IN summary
# definitions_NotificationConfigurationDeprecated_properties_TopicConfiguration_description
# APIs/amazonaws.com/s3/2006-03-01/swagger.yaml
# <p/>
# definitions_NotificationConfigurationDeprecated_properties_QueueConfiguration_description
# APIs/amazonaws.com/s3/2006-03-01/swagger.yaml
# <p/>
# definitions_NotificationConfigurationDeprecated_properties_CloudFunctionConfiguration_description
# APIs/amazonaws.com/s3/2006-03-01/swagger.yaml
# <p/>
# definitions_TopicConfigurationDeprecated_properties_Events_description
# APIs/amazonaws.com/s3/2006-03-01/swagger.yaml
# <p/>
# definitions_TopicConfigurationDeprecated_properties_Event_description
# APIs/amazonaws.com/s3/2006-03-01/swagger.yaml
# Bucket event for which to send notifications.
# definitions_TopicConfigurationDeprecated_properties_Topic_description
# APIs/amazonaws.com/s3/2006-03-01/swagger.yaml
# Amazon SNS topic to which Amazon S3 will publish a message to report the specified events for the bucket.
# definitions_TopicConfigurationDeprecated_description
# APIs/amazonaws.com/s3/2006-03-01/swagger.yaml
# <p/>
# definitions_QueueConfigurationDeprecated_properties_Events_description
# APIs/amazonaws.com/s3/2006-03-01/swagger.yaml
# <p/>
# definitions_QueueConfigurationDeprecated_properties_Queue_description
# APIs/amazonaws.com/s3/2006-03-01/swagger.yaml
# <p/>
# definitions_QueueConfigurationDeprecated_description
# APIs/amazonaws.com/s3/2006-03-01/swagger.yaml
# <p/>
# definitions_DataSourceParameter_properties_deprecated_description
# APIs/googleapis.com/bigquerydatatransfer/v1/swagger.yaml
# If true, it should not be used in new transfers, and it should not be
# visible to users.
# **deprecated** revokes an authorization token.
# IN summary
# **deprecated** creates an authorization token.
# IN summary
# paths_/#X-Amz-Target=SimpleWorkflowService.DeprecateActivityType_post_description
# APIs/amazonaws.com/swf/2012-01-25/swagger.yaml
# <p>Deprecates the specified <i>activity type</i>. After an activity type has been deprecated, you cannot create new tasks of that activity type. Tasks of this type that were scheduled before the type was deprecated continue to run.</p> <note> <p>This operation is eventually consistent. The results are best effort and may not exactly reflect recent updates and changes.</p> </note> <p> <b>Access Control</b> </p> <p>You can use IAM policies to control this action's access to Amazon SWF resources as follows:</p> <ul> <li> <p>Use a <code>Resource</code> element with the domain name to limit the action to only specified domains.</p> </li> <li> <p>Use an <code>Action</code> element to allow or deny permission to call this action.</p> </li> <li> <p>Constrain the following parameters by using a <code>Condition</code> element with the appropriate keys.</p> <ul> <li> <p> <code>activityType.name</code>: String constraint. The key is <code>swf:activityType.name</code>.</p> </li> <li> <p> <code>activityType.version</code>: String constraint. The key is <code>swf:activityType.version</code>.</p> </li> </ul> </li> </ul> <p>If the caller doesn't have sufficient permissions to invoke the action, or the parameter values fall outside the specified constraints, the action fails. The associated event attribute's <code>cause</code> parameter is set to <code>OPERATION_NOT_PERMITTED</code>. For details and example IAM policies, see <a href="https://docs.aws.amazon.com/amazonswf/latest/developerguide/swf-dev-iam.html">Using IAM to Manage Access to Amazon SWF Workflows</a> in the <i>Amazon SWF Developer Guide</i>.</p>
# paths_/#X-Amz-Target=SimpleWorkflowService.DeprecateActivityType_post_responses_200_description
# APIs/amazonaws.com/swf/2012-01-25/swagger.yaml
# Success
# paths_/#X-Amz-Target=SimpleWorkflowService.DeprecateActivityType_post_responses_480_description
# APIs/amazonaws.com/swf/2012-01-25/swagger.yaml
# UnknownResourceFault
# paths_/#X-Amz-Target=SimpleWorkflowService.DeprecateActivityType_post_responses_481_description
# APIs/amazonaws.com/swf/2012-01-25/swagger.yaml
# TypeDeprecatedFault
# paths_/#X-Amz-Target=SimpleWorkflowService.DeprecateActivityType_post_responses_482_description
# APIs/amazonaws.com/swf/2012-01-25/swagger.yaml
# OperationNotPermittedFault
# paths_/#X-Amz-Target=SimpleWorkflowService.DeprecateDomain_post_description
# APIs/amazonaws.com/swf/2012-01-25/swagger.yaml
# <p>Deprecates the specified domain. After a domain has been deprecated it cannot be used to create new workflow executions or register new types. However, you can still use visibility actions on this domain. Deprecating a domain also deprecates all activity and workflow types registered in the domain. Executions that were started before the domain was deprecated continues to run.</p> <note> <p>This operation is eventually consistent. The results are best effort and may not exactly reflect recent updates and changes.</p> </note> <p> <b>Access Control</b> </p> <p>You can use IAM policies to control this action's access to Amazon SWF resources as follows:</p> <ul> <li> <p>Use a <code>Resource</code> element with the domain name to limit the action to only specified domains.</p> </li> <li> <p>Use an <code>Action</code> element to allow or deny permission to call this action.</p> </li> <li> <p>You cannot use an IAM policy to constrain this action's parameters.</p> </li> </ul> <p>If the caller doesn't have sufficient permissions to invoke the action, or the parameter values fall outside the specified constraints, the action fails. The associated event attribute's <code>cause</code> parameter is set to <code>OPERATION_NOT_PERMITTED</code>. For details and example IAM policies, see <a href="https://docs.aws.amazon.com/amazonswf/latest/developerguide/swf-dev-iam.html">Using IAM to Manage Access to Amazon SWF Workflows</a> in the <i>Amazon SWF Developer Guide</i>.</p>
# paths_/#X-Amz-Target=SimpleWorkflowService.DeprecateDomain_post_responses_200_description
# APIs/amazonaws.com/swf/2012-01-25/swagger.yaml
# Success
# paths_/#X-Amz-Target=SimpleWorkflowService.DeprecateDomain_post_responses_480_description
# APIs/amazonaws.com/swf/2012-01-25/swagger.yaml
# UnknownResourceFault
# paths_/#X-Amz-Target=SimpleWorkflowService.DeprecateDomain_post_responses_481_description
# APIs/amazonaws.com/swf/2012-01-25/swagger.yaml
# DomainDeprecatedFault
# paths_/#X-Amz-Target=SimpleWorkflowService.DeprecateDomain_post_responses_482_description
# APIs/amazonaws.com/swf/2012-01-25/swagger.yaml
# OperationNotPermittedFault
# paths_/#X-Amz-Target=SimpleWorkflowService.DeprecateWorkflowType_post_description
# APIs/amazonaws.com/swf/2012-01-25/swagger.yaml
# <p>Deprecates the specified <i>workflow type</i>. After a workflow type has been deprecated, you cannot create new executions of that type. Executions that were started before the type was deprecated continues to run. A deprecated workflow type may still be used when calling visibility actions.</p> <note> <p>This operation is eventually consistent. The results are best effort and may not exactly reflect recent updates and changes.</p> </note> <p> <b>Access Control</b> </p> <p>You can use IAM policies to control this action's access to Amazon SWF resources as follows:</p> <ul> <li> <p>Use a <code>Resource</code> element with the domain name to limit the action to only specified domains.</p> </li> <li> <p>Use an <code>Action</code> element to allow or deny permission to call this action.</p> </li> <li> <p>Constrain the following parameters by using a <code>Condition</code> element with the appropriate keys.</p> <ul> <li> <p> <code>workflowType.name</code>: String constraint. The key is <code>swf:workflowType.name</code>.</p> </li> <li> <p> <code>workflowType.version</code>: String constraint. The key is <code>swf:workflowType.version</code>.</p> </li> </ul> </li> </ul> <p>If the caller doesn't have sufficient permissions to invoke the action, or the parameter values fall outside the specified constraints, the action fails. The associated event attribute's <code>cause</code> parameter is set to <code>OPERATION_NOT_PERMITTED</code>. For details and example IAM policies, see <a href="https://docs.aws.amazon.com/amazonswf/latest/developerguide/swf-dev-iam.html">Using IAM to Manage Access to Amazon SWF Workflows</a> in the <i>Amazon SWF Developer Guide</i>.</p>
# paths_/#X-Amz-Target=SimpleWorkflowService.DeprecateWorkflowType_post_responses_200_description
# APIs/amazonaws.com/swf/2012-01-25/swagger.yaml
# Success
# paths_/#X-Amz-Target=SimpleWorkflowService.DeprecateWorkflowType_post_responses_480_description
# APIs/amazonaws.com/swf/2012-01-25/swagger.yaml
# UnknownResourceFault
# paths_/#X-Amz-Target=SimpleWorkflowService.DeprecateWorkflowType_post_responses_481_description
# APIs/amazonaws.com/swf/2012-01-25/swagger.yaml
# TypeDeprecatedFault
# paths_/#X-Amz-Target=SimpleWorkflowService.DeprecateWorkflowType_post_responses_482_description
# APIs/amazonaws.com/swf/2012-01-25/swagger.yaml
# OperationNotPermittedFault
# typedeprecatedfault
# paths_/#X-Amz-Target=SimpleWorkflowService.UndeprecateActivityType_post_description
# APIs/amazonaws.com/swf/2012-01-25/swagger.yaml
# <p>Undeprecates a previously deprecated <i>activity type</i>. After an activity type has been undeprecated, you can create new tasks of that activity type.</p> <note> <p>This operation is eventually consistent. The results are best effort and may not exactly reflect recent updates and changes.</p> </note> <p> <b>Access Control</b> </p> <p>You can use IAM policies to control this action's access to Amazon SWF resources as follows:</p> <ul> <li> <p>Use a <code>Resource</code> element with the domain name to limit the action to only specified domains.</p> </li> <li> <p>Use an <code>Action</code> element to allow or deny permission to call this action.</p> </li> <li> <p>Constrain the following parameters by using a <code>Condition</code> element with the appropriate keys.</p> <ul> <li> <p> <code>activityType.name</code>: String constraint. The key is <code>swf:activityType.name</code>.</p> </li> <li> <p> <code>activityType.version</code>: String constraint. The key is <code>swf:activityType.version</code>.</p> </li> </ul> </li> </ul> <p>If the caller doesn't have sufficient permissions to invoke the action, or the parameter values fall outside the specified constraints, the action fails. The associated event attribute's <code>cause</code> parameter is set to <code>OPERATION_NOT_PERMITTED</code>. For details and example IAM policies, see <a href="https://docs.aws.amazon.com/amazonswf/latest/developerguide/swf-dev-iam.html">Using IAM to Manage Access to Amazon SWF Workflows</a> in the <i>Amazon SWF Developer Guide</i>.</p>
# paths_/#X-Amz-Target=SimpleWorkflowService.UndeprecateActivityType_post_responses_200_description
# APIs/amazonaws.com/swf/2012-01-25/swagger.yaml
# Success
# paths_/#X-Amz-Target=SimpleWorkflowService.UndeprecateActivityType_post_responses_480_description
# APIs/amazonaws.com/swf/2012-01-25/swagger.yaml
# UnknownResourceFault
# paths_/#X-Amz-Target=SimpleWorkflowService.UndeprecateActivityType_post_responses_481_description
# APIs/amazonaws.com/swf/2012-01-25/swagger.yaml
# TypeAlreadyExistsFault
# paths_/#X-Amz-Target=SimpleWorkflowService.UndeprecateActivityType_post_responses_482_description
# APIs/amazonaws.com/swf/2012-01-25/swagger.yaml
# OperationNotPermittedFault
# paths_/#X-Amz-Target=SimpleWorkflowService.UndeprecateDomain_post_description
# APIs/amazonaws.com/swf/2012-01-25/swagger.yaml
# <p>Undeprecates a previously deprecated domain. After a domain has been undeprecated it can be used to create new workflow executions or register new types.</p> <note> <p>This operation is eventually consistent. The results are best effort and may not exactly reflect recent updates and changes.</p> </note> <p> <b>Access Control</b> </p> <p>You can use IAM policies to control this action's access to Amazon SWF resources as follows:</p> <ul> <li> <p>Use a <code>Resource</code> element with the domain name to limit the action to only specified domains.</p> </li> <li> <p>Use an <code>Action</code> element to allow or deny permission to call this action.</p> </li> <li> <p>You cannot use an IAM policy to constrain this action's parameters.</p> </li> </ul> <p>If the caller doesn't have sufficient permissions to invoke the action, or the parameter values fall outside the specified constraints, the action fails. The associated event attribute's <code>cause</code> parameter is set to <code>OPERATION_NOT_PERMITTED</code>. For details and example IAM policies, see <a href="https://docs.aws.amazon.com/amazonswf/latest/developerguide/swf-dev-iam.html">Using IAM to Manage Access to Amazon SWF Workflows</a> in the <i>Amazon SWF Developer Guide</i>.</p>
# paths_/#X-Amz-Target=SimpleWorkflowService.UndeprecateDomain_post_responses_200_description
# APIs/amazonaws.com/swf/2012-01-25/swagger.yaml
# Success
# paths_/#X-Amz-Target=SimpleWorkflowService.UndeprecateDomain_post_responses_480_description
# APIs/amazonaws.com/swf/2012-01-25/swagger.yaml
# UnknownResourceFault
# paths_/#X-Amz-Target=SimpleWorkflowService.UndeprecateDomain_post_responses_481_description
# APIs/amazonaws.com/swf/2012-01-25/swagger.yaml
# DomainAlreadyExistsFault
# paths_/#X-Amz-Target=SimpleWorkflowService.UndeprecateDomain_post_responses_482_description
# APIs/amazonaws.com/swf/2012-01-25/swagger.yaml
# OperationNotPermittedFault
# paths_/#X-Amz-Target=SimpleWorkflowService.UndeprecateWorkflowType_post_description
# APIs/amazonaws.com/swf/2012-01-25/swagger.yaml
# <p>Undeprecates a previously deprecated <i>workflow type</i>. After a workflow type has been undeprecated, you can create new executions of that type. </p> <note> <p>This operation is eventually consistent. The results are best effort and may not exactly reflect recent updates and changes.</p> </note> <p> <b>Access Control</b> </p> <p>You can use IAM policies to control this action's access to Amazon SWF resources as follows:</p> <ul> <li> <p>Use a <code>Resource</code> element with the domain name to limit the action to only specified domains.</p> </li> <li> <p>Use an <code>Action</code> element to allow or deny permission to call this action.</p> </li> <li> <p>Constrain the following parameters by using a <code>Condition</code> element with the appropriate keys.</p> <ul> <li> <p> <code>workflowType.name</code>: String constraint. The key is <code>swf:workflowType.name</code>.</p> </li> <li> <p> <code>workflowType.version</code>: String constraint. The key is <code>swf:workflowType.version</code>.</p> </li> </ul> </li> </ul> <p>If the caller doesn't have sufficient permissions to invoke the action, or the parameter values fall outside the specified constraints, the action fails. The associated event attribute's <code>cause</code> parameter is set to <code>OPERATION_NOT_PERMITTED</code>. For details and example IAM policies, see <a href="https://docs.aws.amazon.com/amazonswf/latest/developerguide/swf-dev-iam.html">Using IAM to Manage Access to Amazon SWF Workflows</a> in the <i>Amazon SWF Developer Guide</i>.</p>
# paths_/#X-Amz-Target=SimpleWorkflowService.UndeprecateWorkflowType_post_responses_200_description
# APIs/amazonaws.com/swf/2012-01-25/swagger.yaml
# Success
# paths_/#X-Amz-Target=SimpleWorkflowService.UndeprecateWorkflowType_post_responses_480_description
# APIs/amazonaws.com/swf/2012-01-25/swagger.yaml
# UnknownResourceFault
# paths_/#X-Amz-Target=SimpleWorkflowService.UndeprecateWorkflowType_post_responses_481_description
# APIs/amazonaws.com/swf/2012-01-25/swagger.yaml
# TypeAlreadyExistsFault
# paths_/#X-Amz-Target=SimpleWorkflowService.UndeprecateWorkflowType_post_responses_482_description
# APIs/amazonaws.com/swf/2012-01-25/swagger.yaml
# OperationNotPermittedFault
# definitions_DeprecateActivityTypeInput_properties_domain_description
# APIs/amazonaws.com/swf/2012-01-25/swagger.yaml
# The name of the domain in which the activity type is registered.
# definitions_DeprecateActivityTypeInput_properties_activityType_description
# APIs/amazonaws.com/swf/2012-01-25/swagger.yaml
# The activity type to deprecate.
# definitions_DeprecateDomainInput_properties_name_description
# APIs/amazonaws.com/swf/2012-01-25/swagger.yaml
# The name of the domain to deprecate.
# definitions_DeprecateWorkflowTypeInput_properties_domain_description
# APIs/amazonaws.com/swf/2012-01-25/swagger.yaml
# The name of the domain in which the workflow type is registered.
# definitions_DeprecateWorkflowTypeInput_properties_workflowType_description
# APIs/amazonaws.com/swf/2012-01-25/swagger.yaml
# The workflow type to deprecate.
# definitions_UndeprecateActivityTypeInput_properties_domain_description
# APIs/amazonaws.com/swf/2012-01-25/swagger.yaml
# The name of the domain of the deprecated activity type.
# definitions_UndeprecateActivityTypeInput_properties_activityType_description
# APIs/amazonaws.com/swf/2012-01-25/swagger.yaml
# The activity type to undeprecate.
# definitions_UndeprecateDomainInput_properties_name_description
# APIs/amazonaws.com/swf/2012-01-25/swagger.yaml
# The name of the domain of the deprecated workflow type.
# definitions_UndeprecateWorkflowTypeInput_properties_domain_description
# APIs/amazonaws.com/swf/2012-01-25/swagger.yaml
# The name of the domain of the deprecated workflow type.
# definitions_UndeprecateWorkflowTypeInput_properties_workflowType_description
# APIs/amazonaws.com/swf/2012-01-25/swagger.yaml
# The name of the domain of the deprecated workflow type.
# definitions_ActivityTypeInfo_properties_deprecationDate_description
# APIs/amazonaws.com/swf/2012-01-25/swagger.yaml
# If DEPRECATED, the date and time <a>DeprecateActivityType</a> was called.
# definitions_WorkflowTypeInfo_properties_deprecationDate_description
# APIs/amazonaws.com/swf/2012-01-25/swagger.yaml
# If the type is in deprecated state, then it is set to the date when the type was deprecated.
# definitions_TagPaginationInfo_properties_deprecation_warning_description
# APIs/instagram.com/1.0.0/swagger.yaml
# The deprication warning, if information is available
# 265
# description
# 887
# desc file
# 244
# desc api
# 210
# depre key
# 51
# 47
# 226
# 265
# wowza.com
# linode.com
# vocadb.net
# victorops.com
# iva-api.com
# citrixonline.com_gotomeeting
# azure.com_monitor-serviceDiagnosticsSettings_API
# amazonaws.com_comprehendmedical
# getgo.com_gototraining
# dracoon.team
# stripe.com
# osf.io
# amazonaws.com_discovery
# shutterstock.com
# whatsapp.local
# amazonaws.com_codedeploy
# azure.com_sql-tableAuditing
# azure.com_databox
# api2cart.com
# amazonaws.com_iot
# amazonaws.com_elasticmapreduce
# bbc.com
# beezup.com
# amazonaws.com_mediapackage
# nba.com
# amazonaws.com_directconnect
# squareup.com
# amazonaws.com_rds-data
# instagram.com
# azure.com_datalake-analytics-catalog
# github.com
# 31
# APIs/wowza.com/1/swagger.yaml
# APIs/getgo.com/gototraining/1.0.0/swagger.yaml
# APIs/whatsapp.local/1.0/openapi.yaml
# APIs/api2cart.com/1.0.0/swagger.yaml
# APIs/amazonaws.com/rds-data/2018-08-01/swagger.yaml
# APIs/azure.com/datalake-analytics-catalog/2016-11-01/swagger.yaml
# APIs/citrixonline.com/gotomeeting/1.0.0/swagger.yaml
# APIs/amazonaws.com/discovery/2015-11-01/swagger.yaml
# APIs/shutterstock.com/1.0.15/openapi.yaml
# APIs/amazonaws.com/iot/2015-05-28/swagger.yaml
# APIs/amazonaws.com/elasticmapreduce/2009-03-31/swagger.yaml
# APIs/beezup.com/2.0/swagger.yaml
# APIs/nba.com/1.0.0/swagger.yaml
# APIs/amazonaws.com/mediapackage/2017-10-12/swagger.yaml
# APIs/linode.com/4.5.0/openapi.yaml
# APIs/victorops.com/0.0.3/swagger.yaml
# APIs/amazonaws.com/comprehendmedical/2018-10-30/swagger.yaml
# APIs/dracoon.team/4.5.0/swagger.yaml
# APIs/azure.com/databox/2019-09-01/swagger.yaml
# APIs/azure.com/sql-tableAuditing/2014-04-01/swagger.yaml
# APIs/bbc.com/1.0.0/openapi.yaml
# APIs/amazonaws.com/directconnect/2012-10-25/swagger.yaml
# APIs/squareup.com/2.0/swagger.yaml
# APIs/vocadb.net/v1/swagger.yaml
# APIs/iva-api.com/2.0/swagger.yaml
# APIs/osf.io/2.0/swagger.yaml
# APIs/amazonaws.com/codedeploy/2014-10-06/swagger.yaml
# APIs/instagram.com/1.0.0/swagger.yaml
# APIs/stripe.com/2019-09-09/swagger.yaml
# APIs/github.com/v3/swagger.yaml
# 30
# ============================================
#
# Process finished with exit code 0
apis_for_alternate = readFile("result/RQ3/alternate.csv")
