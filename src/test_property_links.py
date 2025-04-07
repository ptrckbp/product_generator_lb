import pandas as pd
from typing import List, Tuple

def test_property_ids_coverage(products_df: pd.DataFrame, hidden_products_df: pd.DataFrame) -> None:
    hidden_products_df = hidden_products_df.rename(columns={
        "Landing Page ID": "property_id",
        "Product ID To Hide": "product_id"
    })

    product_id_map = products_df.set_index("productId")["propertyIds"].to_dict()

    missing_products = []
    mismatched_properties = []

    for _, row in hidden_products_df.iterrows():
        product_id = row["product_id"]
        property_id = str(row["property_id"])

        if product_id not in product_id_map:
            missing_products.append((product_id, property_id))
        elif property_id not in product_id_map[product_id]:
            mismatched_properties.append((product_id, property_id))

    # Results
    if missing_products:
        print("❌ The following productIds from the pivot table are missing from the products table:")
        for pid, prop_id in missing_products:
            print(f"  - Product ID {pid} (missing) → should have Property ID {prop_id}")
    else:
        print("✅ All productIds from the pivot table exist in the products table.")

    if mismatched_properties:
        print("\n❌ Some products are missing required propertyIds:")
        for pid, prop_id in mismatched_properties:
            print(f"  - Product ID {pid} is missing Property ID {prop_id}")
    else:
        print("✅ All product/property relationships are fully covered.")
