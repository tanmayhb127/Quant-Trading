import pandas as pd

df = pd.read_csv('bloomberg_nifty50.csv')
df['Date'] = pd.to_datetime(df['Date'])

saturdays = (df['Date'].dt.dayofweek == 5).sum()
sundays = (df['Date'].dt.dayofweek == 6).sum()

print('Verification - bloomberg_nifty50.csv (3-year):')
print(f'  Total records: {len(df)}')
print(f'  Saturdays: {saturdays}')
print(f'  Sundays: {sundays}')
print(f'  Date range: {df["Date"].min().date()} to {df["Date"].max().date()}')
print(f'  Sample dates:')
for idx in [0, 1, 2, 3, 4, 100, 200, 749]:
    date_obj = df['Date'].iloc[idx]
    day_name = date_obj.strftime('%A')
    print(f'    {date_obj.date()} ({day_name})')
