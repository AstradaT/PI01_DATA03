import csv, json


def main():
    
    data = []
    fieldnames = ['resultId', 'raceId', 'driverId', 'constructorId', 'number', 'grid', 'position', 
    'positionText', 'positionOrder', 'points', 'laps', 'time', 'milliseconds', 'fastestLap', 'rank',
    'fastestLapTime', 'fastestLapSpeed', 'statusId']

    with open('Datasets/results.json') as json_file:
        for row in json_file:
            data.append(json.loads(row))
    
    with open('test.csv', 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(len(data)):
            writer.writerow(data[i])


if __name__ == "__main__":
    main()