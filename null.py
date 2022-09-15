rows = []

with open('results1.csv') as file:
    for row in file:
        rows.append(row.replace('\\N', ''))

with open('results2.csv', 'x') as file:
    for row in rows:
        file.write(row)