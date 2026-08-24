import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Получаем даты за последний год
end_date = datetime.now()
start_date = end_date - timedelta(days=365)
start_str = start_date.strftime('%Y-%m-%d')
end_str = end_date.strftime('%Y-%m-%d')

# Загружаем исторические данные с exchangerate.host
url = f"https://api.exchangerate.host/timeseries?start_date={start_str}&end_date={end_str}&base=USD&symbols=RUB"
response = requests.get(url)
data = response.json()["rates"]

# Преобразуем в DataFrame
df = pd.DataFrame.from_dict(data, orient='index')
df.index = pd.to_datetime(df.index)
df.sort_index(inplace=True)

# Строим график
plt.figure(figsize=(14,6))
plt.plot(df.index, df['RUB'], label='USD/RUB')
plt.title('Курс доллара к рублю за последний год')
plt.xlabel('Дата')
plt.ylabel('Курс, руб/доллар')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()