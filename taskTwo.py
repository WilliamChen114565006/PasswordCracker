import csv
import hashlib
import time
import sys

def dictionary_attack(hash_password, common_passwords):
    for password in common_passwords:
        guess=hashlib.md5(password.encode()).hexdigest()
        if guess == hash_password:
            return password
    return "FAILED"

def dictionary_attack_read(input):
    start_time = time.time()
    total_passwords = 0
    successes = 0

    with open(input,'r') as infile, open("common_passwords.csv", 'r') as passwords_file, open("task2.csv", 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        readerTwo = csv.reader(passwords_file)
        common_passwords = [row[0] for row in readerTwo] 

        for row in reader:
            username, hashed_password= row[0], row[1]
            password = dictionary_attack(hashed_password, common_passwords)
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
    dictionary_attack_read(input_file)

if __name__ == "__main__":
    main()
