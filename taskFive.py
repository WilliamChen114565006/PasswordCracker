import csv
import hashlib
import itertools
import time
import sys
import string

def add_digits(password_table, salt, hashed_password):
    for password in password_table:
        for length in range(1, 5):
            for digits in itertools.product(string.digits, repeat=length):
                guess=password+''.join(digits)
                salted_password=guess+salt
                hashed_salted_password=hashlib.md5(salted_password.encode()).hexdigest()

                if hashed_salted_password==hashed_password:
                    return guess
    return "FAILED"

def case_change(password_table):
    new_passwords = []
    for password in password_table:
        for case_variation in map(''.join, itertools.product(*([char.lower(), char.upper()] for char in password))):
            new_passwords.append(case_variation)
    return password_table+new_passwords

def replace_chars(password_table):
    change_chars = {'e': '3', 'o': '0', 't': '7', 'E': '3', 'O': '0', 'T': '7'} 
    new_passwords = []

    for password in password_table:
        indices=[i for i, char in enumerate(password) if char in change_chars]
        combinations=itertools.product([0, 1], repeat=len(indices))

        for combo in combinations:
            new_password=list(password)
            for j, index in enumerate(indices):
                if combo[j]==1:
                    new_password[index]=change_chars[password[index]]
            new_passwords.append(''.join(new_password))

    return password_table+new_passwords

def hybrid_password_read(input):
    start_time=time.time()
    total_passwords=0
    successes=0

    with open(input, 'r') as infile, open("common_passwords.csv", 'r') as passwords_file, open("task5.csv", 'w', newline='') as outfile:
        reader=csv.reader(infile)
        writer=csv.writer(outfile)
        readerTwo=csv.reader(passwords_file)
        common_passwords=[row[0] for row in readerTwo] 

        for row in reader:
            username, hashed_password, salt=row[0], row[1], row[2]
            password="FAILED"

            # First, check common passwords
            for test_password in common_passwords:
                salted_password=test_password + salt
                hashed_salted_password=hashlib.md5(salted_password.encode()).hexdigest()
                
                if hashed_salted_password==hashed_password:
                    password=test_password
                    break

            # If not found, try replacing characters
            if password == "FAILED":
                updated_pw_list=replace_chars(common_passwords)
                for check_pw in updated_pw_list:
                    salted_password=check_pw+salt
                    hashed_salted_password = hashlib.md5(salted_password.encode()).hexdigest()

                    if hashed_salted_password == hashed_password:
                        password=check_pw
                        break

            # Next, try changing cases
            if password == "FAILED":
                updated_pw_list = case_change(updated_pw_list)
                for check_pw in updated_pw_list:
                    salted_password=check_pw+salt
                    hashed_salted_password=hashlib.md5(salted_password.encode()).hexdigest()

                    if hashed_salted_password == hashed_password:
                        password=check_pw
                        break

            # Finally, add digits to the end
            if password == "FAILED":
                password=add_digits(updated_pw_list, salt, hashed_password)

            writer.writerow([username, password])
            total_passwords+=1
            if password!="FAILED":
                successes+=1

        total_time=round(time.time() - start_time)
        success_rate=(successes / total_passwords) * 100

        writer.writerow([total_time])
        writer.writerow([f"{success_rate:.2f}"])

def main():
    input_file=sys.argv[1]
    hybrid_password_read(input_file)

if __name__ == "__main__":
    main()
