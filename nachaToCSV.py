import nacha
import csv

nacha_file_path = ""
csv_file_path = ""

# Clear the CSV file by truncating it to size 0
with open(csv_file_path, 'w') as csvfile:
    csvfile.truncate()

# Create a list to store the records
records = []

# open the nacha file
with open(nacha_file_path, 'r') as fo:
    reader = nacha.Reader(fo, include_terminal=True)
    for record, terminal in reader:
        # Append the record to the list
        records.append(record)

# Get the unique keys from all records
keys = list(set().union(*(record.keys() if isinstance(record, dict) else record._fields for record in records)))

# Write the records to the CSV file
with open(csv_file_path, 'w') as csvfile:
    writer = csv.writer(csvfile, lineterminator='\n')

    # Write the header row
    writer.writerow(keys)
    # individual row
    row = []
    # stores each individual row
    rows = []
    # Write the values for each record
    for record in records:
        if isinstance(record, dict):
            row = [record.get(key, '') for key in keys]
        else:
            row = [getattr(record, key, '') for key in keys]
        rows.append(row)

    # merge rows
    final_row = [''] * len(row)
    for row in rows:
        for i in range(0, len(row)):
            if row[i] != '':
                final_row[i] = row[i]

    writer.writerow(final_row)