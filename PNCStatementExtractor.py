import os
import re
import PyPDF2
import csv
from typing import List, Tuple
import pandas as pd
from datetime import datetime

def extract_transactions_from_pdf(pdf_path: str) -> List[Tuple[str, str, str, str]]:
    transactions = []  # Initialize an empty list to store transactions
    # Compile a regular expression pattern for matching transaction lines (date, amount, description)
    pattern = re.compile(r'^(\d{2}/\d{2})\s+([\d,]+\.\d{2})\s+(.*)')
    current_section = None  # Variable to keep track of the current section of the bank statement
    
    # Open the PDF file
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)             # Create a PDF reader object
        for page in reader.pages:                   # Iterate through each page in the PDF
            text = page.extract_text()              # Extract text from the current page
            lines = text.split('\n')                # Split the text into lines
            for line in lines:                      # Iterate through each line
                # Check if the line indicates the start of a new section
                if 'Banking/Debit Card Withdrawals and Purchases' in line:
                    current_section = 'withdrawal'  # Update the current section
                elif 'Deposits and Other Additions' in line:
                    current_section = 'deposit'     # Update the current section
                
                # Try to match the line with the transaction pattern
                match = pattern.match(line)
                if match:  # If a match is found
                    date, amount, description = match.groups()  # Extract the date, amount, and description
                    # Depending on the section, format and add the transaction to the list
                    if current_section == 'withdrawal':
                        transactions.append((date, '-', amount, description))
                    elif current_section == 'deposit':
                        transactions.append((date, amount, '-', description))
                    
    return transactions  # Return the list of transactions

def write_transactions_to_csv(transactions: List[Tuple[str, str, str, str]], csv_path: str):
    # Open a new CSV file for writing
    with open(csv_path, 'w', newline='') as file:
        writer = csv.writer(file)         # Create a CSV writer object
        # Write the header row to the CSV file
        writer.writerow(['File Date', 'Transaction Date', 'Withdrawal Amount', 'Deposit Amount', 'Description'])
        for transaction in transactions:  # Iterate through each transaction
            writer.writerow(transaction)  # Write the transaction as a row in the CSV file

def extract_date_from_filename(filename: str) -> datetime:
    # Use regular expression to extract the date from the filename
    match = re.search(r'Statement_(\w{3})_(\d{2})_(\d{4})\.pdf', filename)
    if match:  # If a match is found
        # Convert the extracted date to a datetime object
        return datetime.strptime(f"{match.group(1)} {match.group(2)} {match.group(3)}", '%b %d %Y')
    return None  # Return None if no date is found in the filename

def extract_and_compile_data(folder_path: str) -> pd.DataFrame:
    all_transactions = []  # Initialize an empty list to store all transactions from all files
    for filename in os.listdir(folder_path):                            # Iterate through each file in the directory
        if filename.endswith('.pdf'):                                   # Check if the file is a PDF
            file_date = extract_date_from_filename(filename)            # Extract the date from the filename
            if file_date:                                               # If a date was successfully extracted
                pdf_path = os.path.join(folder_path, filename)          # Construct the full path to the PDF file
                transactions = extract_transactions_from_pdf(pdf_path)  # Extract transactions from the PDF
                for transaction in transactions:                        # Iterate through each transaction
                    # Format the transaction date to include the year from the file date
                    transaction_date = f"{transaction[0]}/{file_date.year}"
                    # Add the transaction to the list, including the file date
                    all_transactions.append([file_date.strftime('%Y-%m-%d'), transaction_date, transaction[1], transaction[2], transaction[3]])
    
    # Convert the list of transactions to a DataFrame
    df = pd.DataFrame(all_transactions, columns=['File Date', 'Transaction Date', 'Withdrawal Amount', 'Deposit Amount', 'Description'])
    # Convert the 'Transaction Date' column to datetime format
    df['Transaction Date'] = pd.to_datetime(df['Transaction Date'], format='%m/%d/%Y')
    # Sort the DataFrame by transaction date
    df = df.sort_values(by=['Transaction Date'])
    return df  # Return the DataFrame


# Specify the directory containing the PDF statements
directory_path = '/Users/PDF'
# Extract and compile data from all PDFs in the directory
compiled_data = extract_and_compile_data(directory_path)

# Specify the path for the output Excel file
output_excel_path = '/Users/compiled_transactions.xlsx'
# Write the compiled data to an Excel file
compiled_data.to_excel(output_excel_path, index=False)