import openai
import sqlparse
import os
from dotenv import load_dotenv
import pandas as pd
import re

load_dotenv()

from openai import OpenAI
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def extract_column_names(sql_query):
    select_pattern = re.compile(r"SELECT\s+(.*?)\s+FROM", re.DOTALL | re.IGNORECASE)
    
    select_match = select_pattern.search(sql_query)
    if not select_match:
        return []

    select_clause = select_match.group(1)

    columns = re.split(r",\s*(?![^()]*\))", select_clause)

    column_names = []
    for col in columns:
        col = col.strip()
        alias_match = re.search(r"(?:AS\s+)?(\w+)$", col, re.IGNORECASE)
        if alias_match:
            column_names.append(alias_match.group(1))

    print(f"Extracted column names: {column_names}")
    return column_names

def generate_column_description(column_name, sql_query):
    """
    Generate a description for a column using OpenAI.
    """
    prompt = f"""
    Generate a precise, non-repetitive description for the column "{column_name}" in the following SQL query:
    
    {sql_query}
    """
    try:
        response = client.chat.completions.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=100,
        )
        description = response["choices"][0]["text"].strip()
        print(f"Generated description for {column_name}: {description}")
        return description
    except Exception as e:
        print(f"Error generating description for {column_name}: {e}")
        return f"Description for {column_name}"

def process_sql_file(sql_file_path):
    """
    Process a SQL file and generate column descriptions.
    """
    print(f"Processing SQL file: {sql_file_path}")  
    with open(sql_file_path, "r") as file:
        sql_content = file.read()

    queries = sqlparse.split(sql_content)

    results = []
    for i, query in enumerate(queries, 1):
        query = query.strip()
        if query:
            columns = extract_column_names(query)
            for col in columns:
                description = generate_column_description(col, query)
                results.append({
                    "SQL Query ID": i,
                    "Column Name": col,
                    "Description": description
                })
    return results

def save_to_excel(results, output_file):
    """
    Save results to an Excel file.
    """
    print(f"Saving results to Excel file: {output_file}")  # Debugging
    df = pd.DataFrame(results)
    df.to_excel(output_file, index=False)

if __name__ == "__main__":
    sql_file_path = "sql_queries.sql"
    output_file = "final_SQL_Column_Descriptions.xlsx"
    results = process_sql_file(sql_file_path)
    save_to_excel(results, output_file)
    print(f"Excel file generated at: {output_file}")