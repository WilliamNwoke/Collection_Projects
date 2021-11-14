import random

def guess(x):
    random_number = random.randint(1,x)
    
    guess = 0
    while guess != random_number:
        guess = int(input(f'Guess the number between 1 and {x}: '))
        if guess < random_number:
            print('Sorry, guess again. Too low.')
        
        if guess > random_number:
            print('Sorry, guess again. Too high.')

    print(f'Yay, congrats. You have guessed the number {random_number}')
print('-------------------------------------')
print('\tGuessing Game')
print('-------------------------------------\n\n')
x = int(input('Pick a range between 1 and your number, what is your number: '))
print()
guess(x)