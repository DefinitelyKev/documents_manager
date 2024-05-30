import os


try:
    file = open("test_file.txt", 'r')
    content = file.read()
    print(content)
except FileNotFoundError as e:
    print(f"An error has occured: {e}")
