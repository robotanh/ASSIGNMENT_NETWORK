
from client import *
from seeder import *


mode = input("Enter 1 or 2: ")

if mode == "1":
    client_mode()
elif mode == "2":
    seeder_mode()
else:
    print("Invalid input. Please enter 1 or 2.")