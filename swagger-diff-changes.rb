require 'swagger/diff'
require 'csv'


#@todo: check the path string
path_pr = "APIs/azure.com/containerservice-managedClusters/2019-08-01/swagger.yaml"
path_nxt = "APIs/azure.com/containerservice-managedClusters/2019-06-01/swagger.yaml"
diffs = Swagger::Diff::Diff.new(path_pr, path_nxt)

#puts diffs.changes

values = diffs.changes
#puts values
change_ep = values[:removed_endpoints]
change_req = values[:removed_request_params]
change_resp = values[:removed_response_attributes]

impacted_operations = []

change_ep.each do |key, value|
    impacted_operations.append(key)
end
change_req.each do |key, value|
    impacted_operations.append(key)
end
change_resp.each do |key, value|
    impacted_operations.append(key)
end

operations = impacted_operations.uniq

puts operations.length
