from src.adjust_products import adjust_products
from src.test_property_links import test_property_ids_coverage
from src.generate_properties import generate_properties
import pandas as pd
import sys

# File paths
products_path = "data/products.csv"
hidden_path = "data/hidden_products.csv"
landing_path = "data/landing_pages.csv"
properties_output_path = "output/properties.csv"
products_output_path = "output/adjusted_products.csv"

# Run product transformation
final_df = adjust_products(products_path, hidden_path, landing_path)
final_df.to_csv(products_output_path, index=False)
print(f"✅ Saved to {products_output_path}")

# Run test
hidden_df = pd.read_csv(hidden_path)
test_property_ids_coverage(final_df, hidden_df)

# Generate properties table
generate_properties(landing_path, properties_output_path)

# Optional: Log the max row size in kilobytes
row_sizes_kb = final_df.apply(lambda row: sys.getsizeof(row.to_json()), axis=1) / 1024
print(f"📦 Max row size: {row_sizes_kb.max():.2f} KB")