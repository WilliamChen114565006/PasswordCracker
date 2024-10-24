import csv
import hashlib
import time
import sys

def rainbow_table():
    rainbow_table = {}
    with open('common_passwords.csv', 'r') as passwords_file, open("rainbow_table_unsalted.csv", 'w', newline='') as rainbow_file:
        reader = csv.reader(passwords_file)
        writer= csv.writer(rainbow_file)

        for row in reader:
            password = row[0]
            hashed_password = hashlib.md5(password.encode()).hexdigest()
            rainbow_table[hashed_password] = password
            writer.writerow([hashed_password, password])
    return rainbow_table

def rainbow_attack_read(input):
    rain_table=rainbow_table()

    start_time = time.time()
    total_passwords = 0
    successes = 0

    with open(input,'r') as infile, open("task3.csv", 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        for row in reader:
            username, hashed_password = row[0], row[1]
            password = rain_table.get(hashed_password, "FAILED")
            writer.writerow([username, password])
            total_passwords += 1
            if password != "FAILED":
                successes += 1

        total_time=round(time.time() - start_time)
        success_rate=(successes/total_passwords)*100

        writer.writerow([total_time])
        writer.writerow([f"{success_rate:.2f}"])

def main():
    input_file = sys.argv[1]
    rainbow_attack_read(input_file)

if __name__ == "__main__":
    main()