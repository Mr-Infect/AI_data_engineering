import pandas as pd
import numpy as np
import re
import nltk
from nltk.corpus import stopwords
from sklearn.impute import KNNImputer
from langdetect import detect  # For language detection
import emoji  # For emoji removal
import os

# Install necessary libraries (run in your terminal)
# pip install pandas numpy nltk scikit-learn langdetect emoji

# Download stopwords (run once)
nltk.download('stopwords', quiet=True)
stop_words = set(stopwords.words('english'))  # Or your desired language

def clean_data(input_file, output_file, output_format="csv", preferred_directory="."):
    try:
        if input_file.endswith('.csv'):
            df = pd.read_csv(input_file)
        elif input_file.endswith('.json'):
            df = pd.read_json(input_file)
        else:
            print("Unsupported file format. Please provide a CSV or JSON file.")
            return
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        return

    # Handling Missing Values
    for col in df.columns:
        if df[col].isnull().any():
            if pd.api.types.is_numeric_dtype(df[col]):
                imputer = KNNImputer(n_neighbors=5)
                df[col] = imputer.fit_transform(df[[col]])
            else:
                df[col].fillna("Unknown", inplace=True)

    # Text Cleaning
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].astype(str)
        df[col] = df[col].str.lower()
        df[col] = df[col].str.replace(r'<.*?>', '', regex=True)
        df[col] = df[col].str.replace(r'[^\w\s]', '', regex=True)
        df[col] = df[col].str.replace(r'\d+', '', regex=True)
        df[col] = df[col].str.replace(r'\s+', ' ', regex=True).str.strip()
        df[col] = df[col].apply(lambda x: ''.join(c for c in x if c not in emoji.UNICODE_EMOJI))
        df[col] = df[col].apply(lambda x: ' '.join([word for word in x.split() if word not in stop_words]))

        # Language Detection & Filtering
        try:
            df = df[df[col].apply(lambda x: detect(x) == 'en')]
        except:
            pass

    # Handling Duplicates
    df.drop_duplicates(inplace=True)

    # Data Type Conversion
    for col in df.columns:
        if col.lower().startswith("date"):
            df[col] = pd.to_datetime(df[col], errors='coerce')
        elif pd.api.types.is_numeric_dtype(df[col]):
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Outlier Handling
    for col in df.select_dtypes(include=np.number).columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        df = df[(df[col] >= Q1 - 1.5 * IQR) & (df[col] <= Q3 + 1.5 * IQR)]

    # Saving Cleaned Data
    output_path = os.path.join(preferred_directory, output_file)
    if output_format.lower() == "csv":
        df.to_csv(output_path, index=False)
    elif output_format.lower() == "json":
        df.to_json(output_path, orient='records', indent=4)
    else:
        print("Invalid output format. Saving as CSV.")
        df.to_csv(output_path, index=False)

    print(f"Cleaned data saved to {output_path}")

# --- Interactive Prompt ---
if __name__ == "__main__":
    input_file = input("Enter the path of the file to be cleaned (CSV or JSON): ").strip()
    output_format = input("Enter the desired output format (csv or json): ").strip().lower()
    output_file = input(f"Enter the name of the output file (with .{output_format} extension): ").strip()
    preferred_directory = input("Enter the directory where you want to save the cleaned file: ").strip()

    clean_data(input_file, output_file, output_format, preferred_directory)

# --- Format Conversion Snippet ---
def convert_file_format(input_file, output_format, output_file, preferred_directory="."):
    try:
        if input_file.endswith('.csv'):
            df = pd.read_csv(input_file)
        elif input_file.endswith('.json'):
            df = pd.read_json(input_file)
        else:
            print("Unsupported file format. Please provide a CSV or JSON file.")
            return
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        return

    output_path = os.path.join(preferred_directory, output_file)
    if output_format.lower() == "csv":
        df.to_csv(output_path, index=False)
    elif output_format.lower() == "json":
        df.to_json(output_path, orient='records', indent=4)
    else:
        print("Invalid output format. Please choose 'csv' or 'json'.")
        return

    print(f"File converted and saved to {output_path}")

# --- Example Usage for Conversion ---
# convert_file_format('your_data.csv', 'json', 'converted_data.json', '/desired/path')
