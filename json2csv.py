import csv, json


def main():
    
    fieldnames = ["qualifyId", "raceId", "driverId", "constructorId", "number", "position", "q1", "q2", "q3"]

    with open('Datasets/Qualifying/qualifying_split_2.json') as json_file:
        data = json.load(json_file)
    

    with open('test.csv', 'a') as csv_file:
        csv_writer = csv.writer(csv_file)
        #csv_writer.writerow(data[0].keys())
        #writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        for i in range(len(data)):
            csv_writer.writerow(data[i].values())


if __name__ == "__main__":
    main()