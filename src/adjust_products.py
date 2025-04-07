import pandas as pd
import json
import re
from typing import List, Tuple, Optional

def load_data(products_path: str, hidden_products_path: str, landing_pages_path: str) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    products = pd.read_csv(products_path, quoting=1, on_bad_lines='skip')
    hidden_products = pd.read_csv(hidden_products_path)
    landing_pages = pd.read_csv(landing_pages_path)
    return products, hidden_products, landing_pages

def normalize_hidden_products(hidden_df: pd.DataFrame) -> pd.DataFrame:
    return hidden_df.rename(columns={
        "Landing Page ID": "property_id",
        "Product ID To Hide": "product_id"
    })

def attach_property_ids(products_df: pd.DataFrame, hidden_df: pd.DataFrame) -> pd.DataFrame:
    product_to_properties = (
        hidden_df.groupby("product_id")["property_id"]
        .apply(lambda ids: list(map(str, ids.unique())))
        .to_dict()
    )
    products_df["propertyIds"] = products_df["productId"].apply(
        lambda pid: product_to_properties.get(pid, [])
    )
    return products_df

def parse_duration_string(duration_str: str) -> Tuple[Optional[int], Optional[int]]:
    if not isinstance(duration_str, str):
        raise ValueError("Duration must be a string.")

    duration_str = duration_str.lower().strip()
    duration_str = duration_str.replace(" to ", "-").replace("–", "-")

    # Strip fuzzy prefixes
    duration_str = re.sub(r"^(approximately|approx|about|around|from)\s+", "", duration_str)
    # Normalize "or" and "and" to dash
    duration_str = re.sub(r"\s+(or|and)\s+", "-", duration_str)
    # Normalize units
    duration_str = duration_str.replace("mins", "minutes").replace("min", "minutes")

    units = {"minute": 1, "minutes": 1, "hour": 60, "hours": 60, "day": 1440, "days": 1440}

    # Explicitly fail on unsupported words like "rental"
    if "rental" in duration_str:
        raise ValueError(f"Invalid duration: contains banned word 'rental'")

    # Accept common synonyms
    if duration_str == "full day":
        return 1440, 1440
    if duration_str == "half day":
        return 720, 720

    # Handle compound durations like "1 hour 30 minutes"
    compound_match = re.findall(r"(\d*\.?\d+)\s*(minutes?|hours?|days?)", duration_str)
    if len(compound_match) >= 1:
        try:
            minutes_total = sum(float(num) * units[unit] for num, unit in compound_match)
            return int(minutes_total), int(minutes_total)
        except:
            pass

    # Case: "x+ unit" → min only
    match_plus = re.match(r"^(\d*\.?\d+)\+\s*(minutes?|hours?|days?)$", duration_str)
    if match_plus:
        val = float(match_plus.group(1))
        unit = match_plus.group(2)
        return int(val * units[unit]), None

    # Case: range like "1-2 hours"
    match_range = re.match(r"^(\d*\.?\d+)-(\d*\.?\d+)\s*(minutes?|hours?|days?)$", duration_str)
    if match_range:
        min_val = float(match_range.group(1))
        max_val = float(match_range.group(2))
        unit = match_range.group(3)
        multiplier = units[unit]
        return int(min_val * multiplier), int(max_val * multiplier)

    # Case: "1.5 hours"
    match_single = re.match(r"^(\d*\.?\d+)\s*(minutes?|hours?|days?)$", duration_str)
    if match_single:
        val = float(match_single.group(1))
        unit = match_single.group(2)
        return int(val * units[unit]), int(val * units[unit])

    raise ValueError(f"Unrecognized duration format: '{duration_str}'")

def extract_durations(products_df: pd.DataFrame) -> pd.DataFrame:
    def safe_parse_duration(x):
        if pd.isna(x):
            return pd.Series([None, None])
        try:
            return pd.Series(parse_duration_string(str(x)))
        except ValueError as e:
            print(f"[duration error] '{x}' → {e}. Please fix the data in your CMS.")
            return pd.Series([None, None])

    products_df[["min_duration", "max_duration"]] = products_df["duration"].apply(safe_parse_duration)
    return products_df.drop(columns=["duration"])

def convert_json_columns(products_df: pd.DataFrame) -> pd.DataFrame:
    def safe_parse(val):
        try:
            return json.loads(val)
        except Exception:
            return []
    products_df["images"] = products_df["images"].apply(safe_parse)
    products_df["related_ids"] = products_df["related_ids"].apply(safe_parse)
    return products_df

def finalize_types(products_df: pd.DataFrame) -> pd.DataFrame:
    def parse_price(value):
        try:
            if isinstance(value, str) and '-' in value:
                value = value.split('-')[0]
            return float(value)
        except Exception:
            return float('nan')

    products_df["price"] = products_df["price"].apply(parse_price)

    # Encode arrays as JSON so they're not stringified Python lists
    for col in ["images", "related_ids", "propertyIds"]:
        products_df[col] = products_df[col].apply(json.dumps)

    return products_df

def adjust_products(products_path: str, hidden_path: str, landing_path: str) -> pd.DataFrame:
    products, hidden, landing = load_data(products_path, hidden_path, landing_path)
    hidden = normalize_hidden_products(hidden)
    products = attach_property_ids(products, hidden)
    products = extract_durations(products)
    products = convert_json_columns(products)
    products = finalize_types(products)
    return products
