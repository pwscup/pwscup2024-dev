"""

配布データから攻撃用データを作るプログラムです。
例えば、B32と入力するとB32.csvからB32s.csv, B32a.csv, B32b.csv, B32x.csvを書き出します。

"""

import sys
import csv
import random
import warnings
import argparse

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('org_csv_prefix', help='配布データのprefix(e.g., B32)')
    parser.add_argument('--seed', type=int, help='乱数シードを整数で指定してください')

    args = parser.parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    inname = args.org_csv_prefix
    infile = inname + '.csv'

    # Read the input CSV file
    with open(infile, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        data = list(reader)

    # Separate header and data rows
    header = data[0]
    rows = data[1:]

    # check the columns
    expected_columns = ['Name', 'Gender', 'Age', 'Occupation', 'ZIP-code', '2', '56', '247', '260', '653', '673', '810', '885',
                     '1009', '1073', '1097', '1126', '1525', '1654', '1702', '1750', '1881', '1920', '1967', '2017',
                     '2021', '2043', '2086', '2087', '2093', '2100', '2105', '2138', '2143', '2174', '2193', '2253',
                     '2399', '2628', '2797', '2872', '2968', '3393', '3438', '3439', '3440', '3466', '3479', '3489',
                     '3877', '3889']

    if len(header) == len(expected_columns):
        for i in range(len(expected_columns)):
            if header[i] != expected_columns[i]:
                warnings.warn("想定していないCSVが入力されています")
                break

    else:
        warnings.warn("想定していないCSVが入力されています")

    # Randomly select 50 rows
    selected_rows = random.sample(rows, 50)
    random.shuffle(selected_rows)  # Shuffle the selected rows randomly

    # Write BXXs.csv with selected and shuffled rows
    with open(inname + 's.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(selected_rows)

    # Split into BXXa.csv and BXXb.csv
    first_part = [header[:5]] + [row[:5] for row in selected_rows]
    second_part = [header[5:]] + [row[5:] for row in selected_rows]

    # Write BXXa.csv
    with open(inname + 'a.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(first_part)

    # Write BXXb.csv with random order and modified random column
    with open(inname + 'b.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)

        # Randomize rows excluding the header
        randomized_rows = second_part[1:]
        shuffle_indices = list(range(50))
        sicp = shuffle_indices
        random.shuffle(shuffle_indices)
        # Modify a random column in each row to '*'
        original_values = []
        for idx in shuffle_indices:
            row = randomized_rows[idx]
            random_col_index = random.randint(0, len(row) - 1)
            original_values.append(row[random_col_index])
            row[random_col_index] = '*'

        # Write header and modified rows to BXXb.csv
        writer.writerow(header[5:])
        writer.writerows([randomized_rows[idx] for idx in shuffle_indices])

    # Create BXXans.csv to indicate the swapping of rows
    with open(inname + 'x.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for i in range(50):
            writer.writerow([shuffle_indices[i], original_values[i]])

        # Write the pairs indicating the swapping of rows and original values
#        for i, row in enumerate(randomized_rows, start=1):
#            original_index = selected_rows.index(second_part[i][5:]) + 1  # Get the original index in BXXs.csv (+1 for 1-based index)
#            original_value = second_part[i][random_col_index]  # Get the original value before modification
#            writer.writerow([i, original_index, original_value])

    print("Files generated successfully.")

if __name__ == "__main__":
    main()
