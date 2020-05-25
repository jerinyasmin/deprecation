import csv

def read(filename):
    with open(filename, mode='r', encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        apis = []
        for row in csv_reader:
            if line_count > 0:
                api = row[0].replace("\\", "/")
                apis.append(api)

            line_count += 1
        # print(f'Processed {line_count} lines.')
    # print(len(list(set(apis))))
    return list(set(apis))






# with open('result/.csv', mode='w', encoding="utf-8") as res_file:
#     res_writer = csv.writer(res_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
#     res_writer.writerow(["text", "File having deprecated"])
#
#
#
# with open('result/.csv', mode='w', encoding="utf-8") as res_file:
#     res_writer = csv.writer(res_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
#     res_writer.writerow(["text", "File having deprecated"])
#
#         # res_writer.writerow([desc, values])
#



