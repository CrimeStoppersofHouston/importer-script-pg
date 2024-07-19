from datetime import date

array = ["2024-07-17 CrimFilingsMonthly_withHeadings.txt", "2024-07-20 CrimFilingsMonthly_withHeadings.txt", "2024-07-15 CrimFilingsMonthly_withHeadings.txt", "2024-07-01 CrimFilingsMonthly_withHeadings.txt"]

print (max(array))

day = int(f'{date.today().day:02d}')

print (day -1)
string = "2024-07-17 CrimFilingsMonthly_withHeadings.txt"

print (string.find(f'{date.year}-{date.month:02d}-*[0-9]'))