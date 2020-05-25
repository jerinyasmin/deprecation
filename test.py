import csv

def readFile(filename):
    with open(filename, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        apis = []
        for row in csv_reader:
            api = row[0].replace("\\", "/")
            apis.append(api)
            line_count += 1

    return list(set(apis))


files = readFile("result/dataset.csv")
files2 = readFile("result/RQ1/deprecated_api_1.csv")

for file in files:
    if file not in files2:
        print(file)