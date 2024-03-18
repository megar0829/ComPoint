from datetime import datetime, date

date1 = "2023.10.19 17:06"
date2 = "2023-03-16"
date1_t = datetime.strptime(date1, '%Y.%m.%d %H:%M')
print(date1_t)
date2_t = date.strptime(date2, '%Y-%m-%d')
print(date2_t)