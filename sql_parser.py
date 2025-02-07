import os
import re
import sqlparse
import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

LM_STUDIO_API_URL = "http://127.0.0.1:1234/v1/chat/completions"
MODEL_NAME = "llama-3.2-1b-instruct"

def extract_column_names(sql_query):
    """
    Extract column names from a SQL SELECT statement.
    """
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

def generate_column_descriptions(columns, sql_query):
    """
    Generate descriptions for multiple columns using LM Studio locally.
    """
    prompt = f"""
    Provide precise and non-repetitive descriptions for the following columns in the SQL query:

    {sql_query}

    Columns: {', '.join(columns)}

    For each column, provide a short description. provide only the description. and no other content in response.
    """

    request_payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": "You are an expert SQL analyst."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2,
        "max_tokens": 500
    }

    try:
        response = requests.post(LM_STUDIO_API_URL, json=request_payload)
        response.raise_for_status()
        result = response.json()
        
        descriptions = result["choices"][0]["message"]["content"].strip().split("\n")
        print(f"Descriptions generated: {descriptions}")

        if len(descriptions) != len(columns):
            print("Warning: Number of descriptions returned doesn't match the number of columns!")
            return [f"Description for {col} (Error)" for col in columns]
        return descriptions
    except Exception as e:
        print(f"Error generating descriptions: {str(e)}")
        return [f"Description for {col} (Error)" for col in columns]

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
            if columns:
                descriptions = generate_column_descriptions(columns, query)
                for col, description in zip(columns, descriptions):
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
    print(f"Saving results to Excel file: {output_file}")
    df = pd.DataFrame(results)
    df.to_excel(output_file, index=False)

if __name__ == "__main__":
    sql_file_path = "sql_queries.sql"
    output_file = "final_SQL_Column_Descriptions.xlsx"
    results = process_sql_file(sql_file_path)
    save_to_excel(results, output_file)
    print(f"Excel file generated at: {output_file}")
