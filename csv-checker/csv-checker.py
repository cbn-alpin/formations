import csv

csvfilepath = "data/FR8201720_habitats_donnees_V4.csv"
mandatory_columns = [
    "01idhab",
    "02idpolhab",
    "03numsite",
    "04cdhab",
    "05lbhab",
    "06rechab",
    "07surfhab",
    "08calrecha",
    "09habdom",
    "10cohabpol",
    "11cdhabref",
    "12lball",
    "13autall",
    "14lbsal",
    "15autsal",
    "16lbass",
    "17autass",
    "18formveg",
    "19stadhhab",
    "20cdn2000",
    "21lbn2000",
    "22cdcahab",
    "23lbcahab",
    "24cdcb",
    "25lbcb",
    "26cdeunis",
    "27lbeunis",
    "28cddynhab",
    "29lbdynhab",
    "30cdusagpr",
    "31lbusagpr",
    "32plusages",
    "33cddegprh",
    "34lbdegprh",
    "35pldeghab",
    "36cdedchab",
    "37lbedchab",
    "38cdgest",
    "39lbgest",
    "40plgest",
    "41cdrestau",
    "42lbrestau",
    "43cdhabori",
    "44cocbn",
    "45evalcbn",
    "46uuidhab",
    "47uuidpol",
]

def main():
    print(csvfilepath)
    with open(csvfilepath, newline="", encoding="windows-1252") as csvfile:
        csv.register_dialect("natura2000", delimiter=";")

        reader = csv.reader(csvfile, dialect="natura2000")
        # columns = list(reader)[0].keys()
        for row in reader:
            header = row
            break

        check_columns_count(header)
        check_mandatory_columns(header)
        check_columns_position(header)

        output = {}
        # Rembobiner la position de la tête de lecture sur le fichier
        csvfile.seek(0)
        dictreader = csv.DictReader(csvfile, dialect="natura2000")
        for row in dictreader:
            list_columns_values(row, output)

        render_analyse(output)


def check_columns_count(header):
    column_count = len(header)
    expected_column_count = len(mandatory_columns)
    if column_count != expected_column_count:
        print(f"ERROR: {column_count} columns finded. {expected_column_count} columns expected.")
    else:
        print(f"OK: {column_count} columns finded. {expected_column_count} columns expected.")


def check_mandatory_columns(header):
    for column in mandatory_columns:
        if column not in header:
            print(f"ERROR: column '{column}' is not in csv file !")


def check_columns_position(header):
    for idx, column in enumerate(header):
        if column == '':
            continue
        #print(f"{idx + 1}: {column} --> {int(column[0:2])}")
        position = idx + 1
        expected_position = int(column[0:2])
        if position != expected_position:
            print(f"ERROR: column '{column}' position is {position} but must be {expected_position}.")

def list_columns_values(row, output):
    for key, value in row.items():
        if key not in output:
            output[key] = []

        if value not in output[key]:
            output[key].append(value)

def render_analyse(output):
    with open("report.txt", "w") as file:
        for column, values in output.items():
            print(f"{column.capitalize()}:", file=file)
            for value in values:
                print(f"\t{value}", file=file)

main()
