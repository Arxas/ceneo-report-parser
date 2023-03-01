import csv
import pandas

output = {}
total_cost = 0

with open("raport.csv", newline="", encoding="utf-8-sig") as csv_file:
    data = csv.reader(csv_file, delimiter=",")
    for row in data:
        cost = float(row[1].split(" ")[0])
        total_cost += cost
        if row[0] in output:
            output[row[0]]["cost"] += cost
            output[row[0]]["count"] += 1
        else:
            output[row[0]] = {"count": 1, "cost": cost}

with open("temp.csv", "w", encoding="utf=8", newline="") as csv_file:
    writer = csv.writer(csv_file, delimiter=",", quoting=csv.QUOTE_MINIMAL)
    for key, value in output.items():
        rounded_value = "%.2f" % value["cost"]
        line = [key, value["count"], rounded_value]
        writer.writerow(line, )

csv_file_pd = pandas.read_csv("temp.csv", header=None, encoding="utf-8", delimiter=",")
header = ["pozycja", "ilość przeklików", "koszt całkowity"]
csv_file_pd.to_excel("podsumowanie.xlsx", header=header, index=None, encoding="utf-8")