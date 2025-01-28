import sqlparse
import pandas as pd

sql_file_path = "sql_queries.sql"

def extract_columns(sql_query):
    parsed_query = sqlparse.parse(sql_query)[0]
    tokens = parsed_query.tokens
    columns = []
    
    for token in tokens:
        if token.ttype is None and token.is_group:
            for subtoken in token.tokens:
                if "AS" in subtoken.value:
                    col_name = subtoken.value.split("AS")[-1].strip()
                    columns.append(col_name)
                elif "." in subtoken.value and not subtoken.value.startswith("("):
                    col_name = subtoken.value.strip()
                    columns.append(col_name)
    return columns

def process_sql_file(sql_file_path):
    with open(sql_file_path, "r") as file:
        sql_queries = file.read().split(";")

    results = []
    for i, query in enumerate(sql_queries, 1):
        query = query.strip()
        if query:
            columns = extract_columns(query)
            for col in columns:
                results.append({
                    "SQL Query ID": i,
                    "Column Name": col,
                    "Description": f"Description for {col}"
                })
    return results

def generate_excel(sql_file_path, output_path):
    results = process_sql_file(sql_file_path)
    df = pd.DataFrame(results)
    df.to_excel(output_path, index=False)
    print(f"Excel file generated at: {output_path}")

output_file_path = "final_SQL_Column_Descriptions.xlsx"

generate_excel(sql_file_path, output_file_path)
