import csv

input_csv_file = 'C:/Users/damian.damjanovic/Documents/Drop Ship/Temp/4 June 2024/hnds_rate_table_incl_gst_2024-05-31_(O-O).csv'
output_csv_file = 'C:/Users/damian.damjanovic/Documents/Drop Ship/Temp/4 June 2024/output.csv'

with open(input_csv_file, mode='r', newline='') as infile:
    reader = csv.DictReader(infile)
    data = []
    for row in reader:
        post_code = row["POSTCODE"]
        product_code = row["HNDS SKU"]
        price = row["SHIPPING (INC GST)"]
        id_value = f"{product_code}{post_code}"
        message = ""
        data.append([post_code, product_code, price, id_value, message])

header = ["postCode", "productCode", "price", "id", "message"]

with open(output_csv_file, mode='w', newline='') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(header)

    for row in data:
        quoted_row = [f'"{item}"' for item in row]
        writer.writerow(quoted_row)

print(f"CSV file '{output_csv_file}' has been created successfully.")
