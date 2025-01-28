import openai

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
