import xml.etree.ElementTree as ET
import pandas as pd
import re
from translate import translate_name_with_google as translate_name

# Load and parse the XML file
tree = ET.parse('data.xml')  # Make sure 'data.xml' is in the same folder
root = tree.getroot()

print("Starting XML to Excel conversion...")

# Locate the <products> node
products_node = root.find("products")
if products_node is None:
    print("Error: <products> node not found in XML!")
    exit()
# Extrat data from each <product>
def extract_values(text):
    values = {"Voltage (V)": "", "Power (W)": "", "IP Rating": ""}
    
    if text:
        ip_matches = re.findall(r'IP\d+', text)
        if ip_matches:
            values["IP Rating"] = ip_matches[0]  # Capture the first IP value
        matches = re.findall(r'(\d+(?:\.\d+)?(V|W|IP\d+))', text)
        for value in matches:
            match = value[0]
            if match.endswith("V"):
                values["Voltage (V)"] = match  # Extract voltage
            elif match.endswith("W"):
                values["Power (W)"] = match  # Extract power
            
    
    return values

# Extract data from each <product>
data = []
for product in products_node.findall("product"):
    # Extract voltage, power and IP rating
    values = extract_values(product.findtext("ItemDescrUK"))

    product_data = {
        "Code": product.findtext("code", default=""),
        "ItemDescrUK": translate_name(product.findtext("ItemDescrUK", default="")),
        "WholeSalePriceGR": product.findtext("WholeSalePriceGR", default="0").replace(",", "."),
        "RetailEShopPrice": product.findtext("PrRetailEShopPrice", default="0"),
        "HasRecycleTax": product.findtext("HasRecycleTax", default="0"),
        "BarCodeEAN13": product.findtext("BarCodeEAN13", default=""),
        "SumStock": product.findtext("SumStock", default=""),
        "PhotoURL": product.find("photos/photo").text if product.find("photos/photo") is not None else "",
        "Voltage (V)": values["Voltage (V)"],
        "Power (W)": values["Power (W)"],
        "IP Rating": values["IP Rating"],
    }
    
    data.append(product_data)

# Convert extracted data to a pandas DataFrame
df = pd.DataFrame(data)

# Save to Excel
output_filename = "output.xlsx"
df.to_excel(output_filename, index=False)

print(f"Conversion complete! Excel file saved as {output_filename}")
