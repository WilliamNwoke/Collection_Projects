"""
This is free and unencumbered software released into the public domain.
:Authors: Uchena
"""

import subprocess

# Will store the profiles data
data = subprocess.check_output(['netsh', 'wlan','show','profiles']).decode('utf-8').split('\n')
profiles = [i.split(':')[1][1:-1] for i in data if 'All User Profile' in i]

# We wil check and print the passwords if they are available
for i in profiles:
    # Command to check for passwords
    results= subprocess.check_output(['netsh', 'wlan','show','profiles', i, 'key=clear']).decode('utf-8').split('\n')
    # Storing passwords after converting to list
    results = [b.split(':')[1][1:-1] for b in results if 'Key Content' in b]
    # printing the wifi-names and passwords
    try:
        print ("{:<30}|   {:<}".format(i, results[0]))
    except IndexError:
        print ("{:<30}|   {:<}".format(i, ""))