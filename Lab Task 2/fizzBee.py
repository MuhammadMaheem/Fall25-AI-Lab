# fizzbuzzgame
# 5th rule:
# previous number + new number

# working:
# computer -> 1
# user -> nothing
# computer -> 2 (actual numberbecomes 1+2 = 3)
# user -> fizz (right, because 1+2=3)

# computer -> 7 (actual is 2+7 = 9)
# user -> fizz (right, because 2+7 =9)


import random

print("Welcome to FizzBuzz Game!")

precount = 0
score = 0
temp_realNumber = []
def fizz(real_num):
    return real_num % 3 == 0

def buzz(real_num):
    return real_num % 5 == 0

def fizzbuzz(real_num):
    return real_num % 3 == 0 and real_num % 5 == 0

for i in range(10):
    comp_num = random.randint(1, 10)
    real_num = precount + comp_num
    temp_realNumber.append(real_num)

    guess = input(f"\nComputer number: {comp_num}\nEnter your input: ").lower()


    if fizzbuzz(real_num):
        correct_answer = "fizzbuzz"
    elif fizz(real_num):
        correct_answer = "fizz"
    elif buzz(real_num):
        correct_answer = "buzz"
    else:
        correct_answer = str(real_num)

    if guess == correct_answer:
        print("Correct!")
        score += 1
    else:
        print(f"Wrong!")

    precount = comp_num 

print(f"\nGame Over! You score: {score}")
print(f"Real numbers were: {temp_realNumber}")
