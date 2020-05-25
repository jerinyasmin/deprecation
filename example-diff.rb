require 'swagger/diff'
require 'csv'


api_true = [2]
api_false = [3]

#@todo: check the path string

path_pr = "APIs/azure.com/recoveryservicesbackup-bms/2016-12-01/swagger.yaml"

path_nxt = "APIs/azure.com/recoveryservicesbackup-bms/2017-17-01/swagger.yaml"

diffs = Swagger::Diff::Diff.new(path_pr, path_nxt)

puts diffs.changes

