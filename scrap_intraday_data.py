import requests 
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import pandas as pd


# Intraday Auction data

current_date = datetime.now().date()
delivery_date = current_date
trading_date = delivery_date - timedelta(days=1)

URL = 'https://www.epexspot.com/en/market-data?market_area=DE-LU&trading_date=' + str(trading_date) + '&delivery_date=' + str(delivery_date) + '&underlying_year=&modality=Auction&sub_modality=Intraday&technology=&product=15&data_mode=table&period=&production_period='
# Add headers to the request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://www.google.com/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive'
}
page = requests.get(URL, headers=headers, proxies=None)

# Check if the request was successful
if page.status_code == 200:
    print("Request successful")
else:
    print(f"Request failed with status code: {page.status_code}")

#print(page.text)

soup = BeautifulSoup(page.content, "html.parser")
table = soup.find(class_="js-table-values")

if table:
    print("Table found")
    rows = table.find_all(class_="child")
    
else:
    print("Table not found or empty")
    with open("debug_page_content.html", "w", encoding="utf-8") as f:
        f.write(soup.prettify()) 
    raise ValueError("Unable to locate the table on the webpage.")


rows = table.find_all(class_="child")

# print(page.text)



def generate_15_minute_intervals_with_date(custom_date):
    start_time = datetime.strptime("00:00", "%H:%M")
    end_time = datetime.strptime("23:59", "%H:%M")

    # Combine the custom date with the start and end times
    start_datetime = datetime.combine(custom_date, start_time.time())
    end_datetime = datetime.combine(custom_date, end_time.time())

    current_time = start_datetime
    time_intervals = []

    while current_time <= end_datetime:
        time_intervals.append(current_time.strftime("%Y-%m-%d %H:%M"))
        current_time += timedelta(minutes=15)

    return time_intervals

fifteen_minute_intervals = generate_15_minute_intervals_with_date(delivery_date)

timesteps = range(len(fifteen_minute_intervals))
df = pd.DataFrame()

for step in timesteps : 
    df.loc[step, 'datetime'] = pd.to_datetime(fifteen_minute_intervals[step])
    
    row = rows[step]
    values = row.find_all("td")
    df.loc[step, 'Buy Volume (MWh)'] = values[0].get_text()
    df.loc[step, 'Sell Volume (MWh)'] = values[1].get_text()
    df.loc[step, 'Volume (MWh)'] = values[2].get_text()
    df.loc[step, 'Price (€/MWh)'] = values[3].get_text()

import os
# Check for the output directory existence
output_dir = 'intraday_auction_data'
if not os.path.exists(output_dir):
    print(f"Directory '{output_dir}' does not exist. Creating it...")
    os.makedirs(output_dir)

# Saving CSV file
output_file = os.path.join(output_dir, 'intraday_auction_data_' + str(delivery_date) + '.csv')
print(f"Saving file to: {output_file}")
df.to_csv(output_file, sep=';')


# Intraday continuous data

current_date = datetime.now().date()
delivery_date = current_date - timedelta(days=1)

URL = 'https://www.epexspot.com/en/market-data?market_area=DE&trading_date=&delivery_date=' + str(delivery_date) + '&underlying_year=&modality=Continuous&sub_modality=&technology=&product=15&data_mode=table&period=&production_period='

 #Add headers to the request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://www.google.com/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive'
}
page = requests.get(URL, headers=headers, proxies=None)

# Check if the request was successful
if page.status_code == 200:
    print("Request is successfully verified")
else:
    print(f"Request failed with status code: {page.status_code}")

#page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
table = soup.find(class_="js-table-values")

def generate_60_minute_intervals_with_date(custom_date):
    start_time = datetime.strptime("00:00", "%H:%M")
    end_time = datetime.strptime("23:59", "%H:%M")

    # Combine the custom date with the start and end times
    start_datetime = datetime.combine(custom_date, start_time.time())
    end_datetime = datetime.combine(custom_date, end_time.time())

    current_time = start_datetime
    time_intervals = []

    while current_time <= end_datetime:
        time_intervals.append(current_time.strftime("%Y-%m-%d %H:%M"))
        current_time += timedelta(minutes=60)

    return time_intervals

sixty_minute_intervals = generate_60_minute_intervals_with_date(delivery_date)

def generate_30_minute_intervals_with_date(custom_date):
    start_time = datetime.strptime("00:00", "%H:%M")
    end_time = datetime.strptime("23:59", "%H:%M")

    # Combine the custom date with the start and end times
    start_datetime = datetime.combine(custom_date, start_time.time())
    end_datetime = datetime.combine(custom_date, end_time.time())

    current_time = start_datetime
    time_intervals = []

    while current_time <= end_datetime:
        time_intervals.append(current_time.strftime("%Y-%m-%d %H:%M"))
        current_time += timedelta(minutes=30)

    return time_intervals

thirty_minute_intervals = generate_30_minute_intervals_with_date(delivery_date)

def generate_15_minute_intervals_with_date(custom_date):
    start_time = datetime.strptime("00:00", "%H:%M")
    end_time = datetime.strptime("23:59", "%H:%M")

    # Combine the custom date with the start and end times
    start_datetime = datetime.combine(custom_date, start_time.time())
    end_datetime = datetime.combine(custom_date, end_time.time())

    current_time = start_datetime
    time_intervals = []

    while current_time <= end_datetime:
        time_intervals.append(current_time.strftime("%Y-%m-%d %H:%M"))
        current_time += timedelta(minutes=15)

    return time_intervals

fifteen_minute_intervals = generate_15_minute_intervals_with_date(delivery_date)

#Day interval data

hours = range(24)
thirty_minutes_in_hour = range(2)
fifteen_minutes_in_half_hour = range(2)

df_60 = pd.DataFrame()
df_30 = pd.DataFrame()
df_15 = pd.DataFrame()

for hour in hours:
    df_60.loc[hour, 'datetime'] = pd.to_datetime(sixty_minute_intervals[hour])

    row = table.find_all(class_='child-' + str(hour))
    if row:
        print(f"Data found")
        continue
    
    values_60 = row[0].find_all("td")
    df_60.loc[hour, 'Low (€/MWh)'] = values_60[0].get_text()
    df_60.loc[hour, 'High (€/MWh)'] = values_60[1].get_text()
    df_60.loc[hour, 'Last (€/MWh)'] = values_60[2].get_text()
    df_60.loc[hour, 'Weight Avg. (€/MWh)'] = values_60[3].get_text()
    df_60.loc[hour, 'ID Full (€/MWh)'] = values_60[4].get_text()
    df_60.loc[hour, 'ID 1 (€/MWh)'] = values_60[5].get_text()
    df_60.loc[hour, 'ID 3 (€/MWh)'] = values_60[6].get_text()
    df_60.loc[hour, 'Buy Volume (MWh)'] = values_60[7].get_text()
    df_60.loc[hour, 'Sell Volume (MWh)'] = values_60[8].get_text()
    df_60.loc[hour, 'Volume (MWh)'] = values_60[9].get_text()





    for thirty_minutes in thirty_minutes_in_hour:
        df_30.loc[hour * 2 + thirty_minutes, 'datetime'] = pd.to_datetime(thirty_minute_intervals[hour * 2 + thirty_minutes])

        values_30 = row[1 + (3 * thirty_minutes)].find_all("td")
        df_30.loc[hour * 2 + thirty_minutes, 'Low (€/MWh)'] = values_30[0].get_text()
        df_30.loc[hour * 2 + thirty_minutes, 'High (€/MWh)'] = values_30[1].get_text()
        df_30.loc[hour * 2 + thirty_minutes, 'Last (€/MWh)'] = values_30[2].get_text()
        df_30.loc[hour * 2 + thirty_minutes, 'Weight Avg. (€/MWh)'] = values_30[3].get_text()
        df_30.loc[hour * 2 + thirty_minutes, 'ID Full (€/MWh)'] = values_30[4].get_text()
        df_30.loc[hour * 2 + thirty_minutes, 'ID 1 (€/MWh)'] = values_30[5].get_text()
        df_30.loc[hour * 2 + thirty_minutes, 'ID 3 (€/MWh)'] = values_30[6].get_text()
        df_30.loc[hour * 2 + thirty_minutes, 'Buy Volume (MWh)'] = values_30[7].get_text()
        df_30.loc[hour * 2 + thirty_minutes, 'Sell Volume (MWh)'] = values_30[8].get_text()
        df_30.loc[hour * 2 + thirty_minutes, 'Volume (MWh)'] = values_30[9].get_text()

        for fifteen_minutes in fifteen_minutes_in_half_hour:
            df_15.loc[hour * 4 + thirty_minutes * 2  + fifteen_minutes, 'datetime'] = pd.to_datetime(fifteen_minute_intervals[hour * 4 + thirty_minutes * 2  + fifteen_minutes])
            
            values_15 = row[2 + thirty_minutes * 3 + fifteen_minutes].find_all("td")
            df_15.loc[hour * 4 + thirty_minutes * 2  + fifteen_minutes, 'Low (€/MWh)'] = values_15[0].get_text()
            df_15.loc[hour * 4 + thirty_minutes * 2  + fifteen_minutes, 'High (€/MWh)'] = values_15[1].get_text()
            df_15.loc[hour * 4 + thirty_minutes * 2  + fifteen_minutes, 'Last (€/MWh)'] = values_15[2].get_text()
            df_15.loc[hour * 4 + thirty_minutes * 2  + fifteen_minutes, 'Weight Avg. (€/MWh)'] = values_15[3].get_text()
            df_15.loc[hour * 4 + thirty_minutes * 2  + fifteen_minutes, 'ID Full (€/MWh)'] = values_15[4].get_text()
            df_15.loc[hour * 4 + thirty_minutes * 2  + fifteen_minutes, 'ID 1 (€/MWh)'] = values_15[5].get_text()
            df_15.loc[hour * 4 + thirty_minutes * 2  + fifteen_minutes, 'ID 3 (€/MWh)'] = values_15[6].get_text()
            df_15.loc[hour * 4 + thirty_minutes * 2  + fifteen_minutes, 'Buy Volume (MWh)'] = values_15[7].get_text()
            df_15.loc[hour * 4 + thirty_minutes * 2  + fifteen_minutes, 'Sell Volume (MWh)'] = values_15[8].get_text()
            df_15.loc[hour * 4 + thirty_minutes * 2  + fifteen_minutes, 'Volume (MWh)'] = values_15[9].get_text()
            
import os

# Function to ensure a directory exists or creation
def ensure_directory_exists(dir_path):
    if not os.path.exists(dir_path):
        print(f"Directory '{dir_path}' does not exist. Creating it...")
        os.makedirs(dir_path)

# Check 'intraday_auction_data' directory exists
ensure_directory_exists('intraday_auction_data')

# Saving auction data
df_30.to_csv('intraday_auction_data/intraday_auction_data_' + str(delivery_date) + '.csv', sep=';')

# Check 'intraday_continuous_data_1h' directory exists
ensure_directory_exists('intraday_continuous_data_1h')

# Saving 1-hour data
df_60.to_csv('intraday_continuous_data_1h/intraday_continuous_data_1h_' + str(delivery_date) + '.csv', sep=';')

# Check 'intraday_continuous_data_30min' directory exists
ensure_directory_exists('intraday_continuous_data_30min')

# Saving 30-minute data
df_30.to_csv('intraday_continuous_data_30min/intraday_continuous_data_30min_' + str(delivery_date) + '.csv', sep=';')

# Check 'intraday_continuous_data_15min' directory exists
ensure_directory_exists('intraday_continuous_data_15min')

# Saving 15-minute data
df_15.to_csv('intraday_continuous_data_15min/intraday_continuous_data_15min_' + str(delivery_date) + '.csv', sep=';')
