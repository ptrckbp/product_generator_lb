# Adjust Products Table

This project processes a products table by combining it with property and pivot data, extracting clean durations, and adding property IDs.

---

## 🧱 Project Structure

```
adjust_products_project/
├── data/
│   ├── products.csv
│   ├── hidden_products.csv
│   └── landing_pages.csv
├── src/
│   ├── adjust_products.py
│   └── test_property_links.py
├── output/
│   └── adjusted_products.csv  (created when you run it)
├── run.py
└── requirements.txt
```

---

## ✅ How to Use

### 1. Clone or download this repo and navigate into the folder

```bash
cd adjust_products_project
```

Add the data files in ./data
hidden_products.csv <- this has the blacklisted products for each landing_page
landing_pages.csv <- landing page names and locations for properties
products.csv <- products file taken from CMS. 

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

### 3. Activate the virtual environment

- macOS/Linux:
  ```bash
  source .venv/bin/activate
  ```

- Windows:
  ```bash
  .venv\Scripts\Activate.ps1
  ```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the script

```bash
python run.py
```

The result will be saved to:

```
output/adjusted_products.csv
```

---

## 🧪 Test

The test automatically runs after processing. It checks whether all product/property pairs from the pivot table are accounted for in the final output.

---

## 📄 Requirements

- Python 3.8+
- pandas

