import csv
import hashlib
import itertools
import time
import sys

def brute_force_solve(hash_password):
    letters = "QWERTYUIOPASDFGHJKLZXCVBNM1234567890qwertyuiopasdfghjklzxcvbnm"
    for length in range(1, 5):
        for attempt in itertools.product(letters, repeat=length):
            guess = ''.join(attempt)
            hashed_attempt = hashlib.md5(guess.encode()).hexdigest()
            if hashed_attempt==hash_password:
                return guess
    return "FAILED"

def brute_force_passwords_read(input):
    start_time = time.time()
    total_passwords = 0
    successes = 0

    with open(input, 'r') as infile, open("task1.csv", 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        for row in reader:
            username, hashed_password = row[0], row[1]
            password = brute_force_solve(hashed_password)
            writer.writerow([username, password])
            total_passwords += 1
            if password != "FAILED":
                successes += 1

        total_time = round(time.time() - start_time)
        success_rate = (successes / total_passwords) * 100.00

        writer.writerow([total_time])
        writer.writerow([f"{success_rate:.2f}"])

def main():
    input_file = sys.argv[1]
    brute_force_passwords_read(input_file)

if __name__ == "__main__":
    main()
