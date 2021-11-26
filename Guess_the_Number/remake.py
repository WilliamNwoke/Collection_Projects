import random

def guess(x):
    random_number = random.randint(1, x)

    while True:
        guess = int(input(f'Guess the number between 1 and {x}: '))
        if guess < random_number:
            print('Sorry, guess again. Too low.')
        
        if guess > random_number:
            print('Sorry, guess again. Too high.')
            
        if guess == random_number:
            print(f'Yay, congrats. You have guessed the number {random_number}')
            break

        
print('-------------------------------------')
print('\tGuessing Game')
print('-------------------------------------\n\n')
x = int(input('Pick a range between 1 and your number, what is your number: '))
print()
guess(x)