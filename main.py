import csv
import os

import click
import pandas


def parse_ceneo_report(report_path):
    output = {}
    xlsx_file = pandas.read_excel(report_path, header=None)
    for _, row in xlsx_file.iterrows():
        if "Ilość przejść" in row.tolist()[2]:
            continue
        item, cost = row.tolist()[2:4]
        if item in output:
            output[item]["cost"] += float(cost)
            output[item]["count"] += 1
        else:
            output[item] = {"count": 1, "cost": float(cost)}
    input()
    return output


def write_xlsx_report(parsed_report):
    temp_csv_file = "temp.csv"
    with open(temp_csv_file, "w", encoding="utf=8", newline="") as csv_file:
        writer = csv.writer(csv_file, delimiter=",", quoting=csv.QUOTE_MINIMAL)
        for key, value in parsed_report.items():
            rounded_value = "%.2f" % value["cost"]
            line = [key, value["count"], rounded_value]
            writer.writerow(line, )
    convert_csv_to_xlsx(temp_csv_file, ["pozycja", "ilość kliknięć", "koszt całkowity"], "podsumowanie")
    os.remove(temp_csv_file)


def convert_csv_to_xlsx(csv_file_path, header, file_name):
    csv_file_pd = pandas.read_csv(csv_file_path, header=None, encoding="utf-8", delimiter=",")
    csv_file_pd.to_excel(f"{file_name}.xlsx", header=header, index=False)


@click.command()
@click.argument("report")
def main(report):
    output = parse_ceneo_report(report)
    write_xlsx_report(output)


if __name__ == '__main__':
    main()
