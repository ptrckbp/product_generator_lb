import pandas as pd

def generate_properties(landing_pages_path: str, output_path: str) -> None:
    landing_pages = pd.read_csv(landing_pages_path)

    # Create the new properties DataFrame with propertyId as string
    properties = pd.DataFrame({
        "propertyId": landing_pages["Landing Page ID"].astype(str),
        "description": "",
        "name": landing_pages["Landing Page Name"],
        "location": landing_pages["Location Name"],
        "landing_page_url": landing_pages["Partner Destination URL"]
    })

    # Save to CSV
    properties.to_csv(output_path, index=False)
    print(f"✅ Saved properties to {output_path}")

# Example usage:
# generate_properties("data/landing_pages.csv", "output/properties.csv")
