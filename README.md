# Data Cleaning Automation Script

## Overview
This Python script automates the process of cleaning and preprocessing data from CSV and JSON files. It handles missing values, text normalization, outlier detection, and duplicates, and allows conversion between CSV and JSON formats. The script is interactive, prompting users for input and output specifications.

## Features
- **Handling Missing Values**:
  - Numeric columns: Uses K-Nearest Neighbors (KNN) imputation.
  - Non-numeric columns: Fills missing values with "Unknown".
- **Text Cleaning**:
  - Lowercasing text.
  - Removing HTML tags, special characters, digits, extra whitespace, and emojis.
  - Removing stopwords and filtering for specific languages (default is English).
- **Duplicate Removal**: Automatically removes duplicate rows.
- **Data Type Conversion**:
  - Converts columns starting with "date" to datetime.
  - Converts numeric columns to appropriate numeric types.
- **Outlier Detection**: Uses Interquartile Range (IQR) to remove outliers from numeric data.
- **File Format Conversion**: Converts input files (CSV/JSON) to the desired format (CSV/JSON).

## How to Use

### Prerequisites
Ensure you have Python installed and run the following commands to install required libraries:
```bash
pip install pandas numpy nltk scikit-learn langdetect emoji
```
Download NLTK stopwords (run once):
```python
import nltk
nltk.download('stopwords')
```

### Running the Script
1. **Clone the Repository**:
```bash
git clone https://github.com/Mr-Infect/AI_data_engineering.git
cd AI_data_engineering 
```

2. **Run the Script**:
```bash
python data_cleaning.py
```

3. **Follow the Prompts**:
   - Enter the path to your input file (CSV or JSON).
   - Specify the desired output format (`csv` or `json`).
   - Provide the name for the output file.
   - Specify the directory where the cleaned data should be saved.

### Example:
```bash
Enter the path to the input file: data/raw_data.csv
Enter the desired output format (csv/json): json
Enter the name for the output file (e.g., cleaned_data.csv): cleaned_data.json
Enter the directory to save the cleaned file (default is current directory): ./cleaned_files
Cleaned data saved to ./cleaned_files/cleaned_data.json
```

## Who Will Find This Helpful?
- **Data Scientists** and **Analysts**: Simplify preprocessing before analysis or model building.
- **Researchers**: Automate repetitive data cleaning tasks in large datasets.
- **Students**: Learn best practices in data preprocessing and handling common data issues.
- **Developers**: Integrate automated data cleaning in applications or data pipelines.

## Contributing
Feel free to fork the repository and submit pull requests for any improvements or additional features!

---

For any issues or suggestions, please open an issue in the repository.

---

**Happy Data Cleaning!** 🚀

