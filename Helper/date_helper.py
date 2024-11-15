def query_date_to_string(res):
    for row in res:
        for key, value in row.items():
            if 'date' in key:
                row[key] = str(value)
    return res