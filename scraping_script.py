def script():
    from bs4 import BeautifulSoup
    import requests
    import pandas as pd
    import csv

    page = requests.get('https://en.wikipedia.org/wiki/List_of_most-viewed_YouTube_videos')

    page_text = page.text

    soup = BeautifulSoup(page_text,'html.parser')

    # First remove None if present
    table_soup = soup.find_all('table')
    filtered_table_soup = [table for table in table_soup if table.caption is not None]

    required_table = None

    for table in filtered_table_soup:
        if str(table.caption.string).strip() == 'Top 30 most-viewed YouTube videos':
            required_table = table
            break  

    headers = [header.text.strip() for header in required_table.find_all('th')]

    rows = []

    # Find all `tr` tags
    data_rows = required_table.find_all('tr')

    for row in data_rows:
        value = row.find_all('td')
        beautified_value = [ele.text.strip() for ele in value]
        # Remove data arrays that are empty
        if len(beautified_value) == 0:
            continue
        rows.append(beautified_value)

    import csv

    with open(r'C:\Users\nseka\Desktop\desktop\Wikipedia Scrap\script_top_videos.csv', 'w', newline="") as output:
        writer = csv.writer(output)
        writer.writerow(headers)
        writer.writerows(rows)
    df = pd.read_csv(r'C:\Users\nseka\Desktop\desktop\Wikipedia Scrap\script_top_videos.csv',encoding= 'unicode_escape')
    df = df.iloc[:,1:5] #keeping only relevent columns
    df.to_csv(r'C:\Users\nseka\Desktop\desktop\Wikipedia Scrap\final_script_top_videos.csv', index = False, header = True)
    return df
script()
