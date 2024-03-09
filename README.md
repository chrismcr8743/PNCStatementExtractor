# PNCStatementExtractor

## Overview
PNCStatementExtractor is a Python tool designed to automate the extraction of transaction data from PNC Bank's monthly statement PDFs. It parses through the statements to collect details about deposits and withdrawals, then compiles and exports this information into an Excel file. This tool aims to simplify financial tracking and analysis by providing a structured and easily accessible view of your banking transactions.

## Features
- **PDF Parsing**: Automatically reads through PDF statements to find transaction data.
- **Transaction Categorization**: Identifies and categorizes transactions into deposits and withdrawals.
- **Data Extraction**: Extracts dates, amounts, and descriptions of transactions.
- **Excel Export**: Compiles all transactions into an organized Excel spreadsheet.
- **Date Handling**: Ensures transactions are associated with the correct statement period.

## Prerequisites
Before using PNCStatementExtractor, ensure you have the following installed:
- Python 3.11
- Required Python packages: `PyPDF2`, `pandas`

You can install the necessary packages using the following command:
```bash
pip install PyPDF2 pandas
