import csv

input_file = 'input.csv'   # Change to your input CSV filename
output_file = 'output.csv' # Change to your desired output filename

with open(input_file, newline='', encoding='utf-8') as infile, \
     open(output_file, 'w', newline='', encoding='utf-8') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    for row in reader:
        if row:  # Ensure row is not