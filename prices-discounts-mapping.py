import csv

def load_mapping(file_path, key_column, value_column):
    mapping = {}
    with open(file_path, mode='r') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            mapping[row[key_column]] = row[value_column]
    return mapping

def map_prices(rows, price_mapping):
    # Map the prices
    for row in rows:
        for key in row.keys():
            if key.startswith('price_id_') and row[key] in price_mapping:
                row[key] = price_mapping[row[key]]

def map_discounts(rows, discount_mapping):
    # Map the discounts
    for row in rows:
        if row['discount_id'] in discount_mapping:
            row['discount_id'] = discount_mapping[row['discount_id']]

def main():
    input_file = 'paddle_migration_output.csv'
    mapping_file = 'prices-discounts-mapping-ref.csv'
    output_file = 'paddle_migration_output_mapped.csv'

    # Load the input CSV
    with open(input_file, mode='r') as infile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        rows = list(reader)

    # Ask the user if they want to map prices
    map_prices_choice = input("Do you want to map prices? (y/n): ").strip().lower()
    if map_prices_choice == 'y':
        price_mapping = load_mapping(mapping_file, 'stripe_price_id', 'paddle_price_id')
        map_prices(rows, price_mapping)
        print("Prices mapped successfully.")

    # Ask the user if they want to map discounts
    map_discounts_choice = input("Do you want to map discounts? (y/n): ").strip().lower()
    if map_discounts_choice == 'y':
        discount_mapping = load_mapping(mapping_file, 'stripe_discount_id', 'paddle_discount_id')
        map_discounts(rows, discount_mapping)
        print("Discounts mapped successfully.")

    # Write the output CSV
    with open(output_file, mode='w', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Output saved to {output_file}")

if __name__ == "__main__":
    main()
