# Retouching the initial Program xDDDD
import random

def guess(x):
    random_number = random.randint(1, x)

    guess = 0
    while guess != random_number:
        guess = int(input(f'Guess a number between 1 and {x}: '))
        if guess > random_number:
            print('Your guess is too high')
        
        if guess < random_number:
            print('Your guess is too low')

    print(f'Yay you guessed the random number : {random_number} ')

print ('Guess the random number game')
print()
x = int(input('Pick a range betwen 1 and your number, What is your number: '))
print()
guess(x)