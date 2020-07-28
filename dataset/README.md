## Instructions for building database

Visit https://immunerace.adaptivebiotech.com/data/, scroll to the bottom of the page, and click on "Download the data in a zip file here". Once you have downloaded the zip file, extract the contents, find the file named `peptide-detail.csv`, and place it in this folder. Then run the following python scripts.

```
python3 build_db_sequence.py
python3 convert_json_to_csv.py --db db_sequence.json --output db_sequence
python3 build_db_category.py
python3 convert_json_to_csv.py --db db_category.json --output db_category
```
