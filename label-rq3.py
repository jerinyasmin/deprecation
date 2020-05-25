import csv

def read(filename):
    with open(filename, mode='r', encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        apis = []
        for row in csv_reader:
            if line_count > 0:
                api = row[5].replace("\\", "/")
                apis.append(api)

            line_count += 1
        # print(f'Processed {line_count} lines.')
    # print(len(list(set(apis))))
    return list(set(apis))

texts = read('result/RQ3/labels/categories.csv')




with open('result/RQ3/labels/shuffled-evaluate-tool.csv', mode='w', encoding="utf-8") as res_file:
    res_writer = csv.writer(res_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
    res_writer.writerow(["alt", "time", "info", "reason", "deprecation time","text"])
    with open('result/RQ3/labels/shuffled-evaluate.csv', mode='r', encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0

        for row in csv_reader:#
            if line_count > 0:
                description = row[5]

                description = " ".join(description.split())
#
                if description not in texts:
                  res_writer.writerow([row[0], row[1], row[2], row[3], row[4], description])

            line_count += 1
