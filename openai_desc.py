import openai
import re
import os

import dotenv

dotenv.load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_columns(sql_query):
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
    prompt = f"""
    Generate a precise, non-repetitive description for the column "{column_name}" in the following SQL query:
    
    {sql_query}
    """
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100,
    )
    return response["choices"][0]["text"].strip()

def process_sql_file(sql_file_path):
    with open(sql_file_path, "r") as file:
        sql_queries = file.read().split(";")

    results = []
    for i, query in enumerate(sql_queries, 1):
        query = query.strip()
        if query:
            columns = extract_columns(query)
            for col in columns:
                description = generate_column_description(col, query)
                results.append({
                    "SQL Query ID": i,
                    "Column Name": col,
                    "Description": description
                })
    return results
