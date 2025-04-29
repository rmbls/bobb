import pandas as pd
import PySimpleGUI as sg
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt = "%H:%M:%S")

def printTitle():
    print("="*50)
    print("L'AGENCE - Spreadsheet Converter")
    print("="*50)
    print()
    print("Please select a file...")
    print()

def select_files():
    file_path = sg.popup_get_file(
        "Pick a File",
        file_types=(
            ("Excel Files", "*.xlsx;*.xls"),
            ("CSV Files", "*.csv"),
            ("All Files", "*.*")
        ),
        no_window=True
    )
    logging.info(f"Selected file: {file_path}")
    return file_path

def update_file(file_path):
    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    elif file_path.endswith(".xlsx") or file_path.endswith(".xls"):
        df = pd.read_excel(file_path)
    else:
        input("Unsupported file format. This program only supports CSV and Excel files. Press any key to exit.")
        return None
    logging.info("Processing file...")
    logging.info(f"{len(df)} rows in file.")
    
    #Add new blank columns
    df["SEO Title"] = ""
    df["Parent SKU"] = ""
    df["Shopify Handle"] = ""
    df["Related Products Display"] = ""
    df["Option Attributes"] = ""
    
    df = pd.concat([pd.DataFrame([0]), df], ignore_index=True)
    rowProcessed = 0

    logging.info("Updating File...")

    for index, row in df.iterrows():
        #Format Existing Rows
        df.loc[index,'Seas'] = f"season: {row['Seas']}"
        df.loc[index, 'SEO Title'] = f"L'AGENCE - {str(row['Style Desc']).title()} in {str(row['Clr Desc']).title()}"
        if row['Country of Origin Description'] == "UNITED STATES":
            df.loc[index,'Content Description'] = f"[\"{str(row['Content Description']).title().replace('  ',' ')}\",\"Made in Los Angeles\"]"
        else:
            df.loc[index,'Content Description'] = f"[\"{str(row['Content Description']).title().replace('  ',' ')}\",\"Imported\"]"
        df.loc[index,"Clr Desc"] = str(row["Clr Desc"]).title()
        df.loc[index,"Style Desc"] = str(row["Style Desc"]).title()
        df.loc[index,"UPC Code"] = str(row["UPC Code"]).replace(".0","")
        df.loc[index,"Prod Type Desc"] = str(row["Prod Type Desc"]).lower()
        
        #Set up Parent
        tempHandle = f"{str(row['Style Desc']).lower().replace(' ','-').replace('/','-')}-{str(row['Clr Desc']).lower().replace(' ','-').replace('/','-')}"
        parentSku = str(row['Sty-Clr-Siz'])[:str(row['Sty-Clr-Siz']).rfind('-')]
        if index >0 and parentSku != df.loc[index-1,"Parent SKU"]:
            df.loc[index - 0.5] = df.loc[index]
            df.loc[index -0.5, "Sty-Clr-Siz"] = parentSku
            df.loc[index -0.5, "Shopify Handle"] = tempHandle
            df.loc[index -0.5, "Clr Desc"] = ""
            df.loc[index -0.5, "Size"] = ""
            df.loc[index -0.5, "Related Products Display"] = "only manual"
            df.loc[index -0.5, "Option Attributes"] = "color|size"
            df.loc[index, "Parent SKU"] = parentSku
        else:
            df.loc[index, "Parent SKU"] = parentSku
        
        rowProcessed += 1
        if str(rowProcessed).endswith('0'):
            logging.info(f"{rowProcessed} rows processed...")

    #Drop Unnecesary Columns
    df.drop([
        'Country of Origin Description'
        ],axis = 1, inplace = True)

    #Rename Columns for Catsy
    df.rename(columns = {
        'Sty-Clr-Siz': 'Item ID',
        'Style Desc':'Name',
        'Clr Desc':'Color',
        'Prod Type Desc':'Product Type',
        'MSRP': 'Price',
        'Seas': 'Tags',
        'Country': 'Country Code',
        'Content Description': 'composition',
        'Wght/Unit': 'Weight'
        }, inplace = True)

    df["Compare At Price"] = df["Price"]
    df["Vendor"] = "L'AGENCE"
    df["lagencefashion Shopify Status"] = "active"
    df["Weight Unit"] = "lb"
    df["lagencefashion Requires Shipping"] = "true"


    df.drop(0, axis = 1, inplace=True)
    df = df.loc[1:]
    df.sort_index(inplace=True)
    df.reset_index(drop=True, inplace=True)    
    
    filename = os.path.basename(file_path).split('.')[0]
    fullPath = os.path.dirname(file_path)
    logging.info(f"Saving updated file as {filename} - Updated for Catsy.xlsx")
    df.to_excel(f"{filename} - Updated for Catsy.xlsx", index = False)
    logging.info("File updated successfully.")
    print(f"\nUpdated file saved to: \n{os.path.join(fullPath, f'{filename} - Updated for Catsy.xlsx')}\n")
    input("Press Enter to exit.")
    

def main():
    printTitle()
    update_file(select_files())

if __name__ == "__main__":
    main()
