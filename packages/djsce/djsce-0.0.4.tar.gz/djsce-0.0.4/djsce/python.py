client='''
import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 12345))

while True:
    
    message = input("You: ")
    encrypted_message = message.encode()
    client_socket.send(encrypted_message)
    
    encrypted_message = client_socket.recv(1024)
    
    decrypted_message = encrypted_message
    print(f"Server: {decrypted_message.decode()}")
'''

server='''
import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1', 12345))
server_socket.listen(5)

print("Server is listening...")

client_socket, client_address = server_socket.accept()

while True:
    
    encrypted_message = client_socket.recv(1024)
    
    decrypted_message = encrypted_message
    
    print(f"Client: {decrypted_message.decode()}")

    message = input("You: ")
    encrypted_message = message.encode()
    client_socket.send(encrypted_message)
'''

toh='''
def tower_of_hanoi(n, source, auxiliary, destination):
    if n == 1:
        print(f"Move disk 1 from {source} to {destination}")
        return
    else:
        tower_of_hanoi(n - 1, source, destination, auxiliary)
        print(f"Move disk {n} from {source} to {destination}")
        tower_of_hanoi(n - 1, auxiliary, source, destination)

tower_of_hanoi(3, 'A', 'B', 'C')

'''

exception='''
class AgeBelow18Error(Exception):
    def __init__(self, message="Age must be 18 or above."):
        self.message = message
        super().__init__(self.message)

try:
    user_input = input("Enter a number: ")
    number = int(user_input)
    print("Square of the number:", number ** 2)
except ValueError:
    print("Invalid input. Please enter a valid integer.")

try:
    result = 10 / 0  
except ZeroDivisionError as e:
    print(f"Error: {type(e).__name__} - {e}")

try:
    import non_existent_module  
except ImportError as e:
    print(f"Error: {type(e).__name__} - {e}")

try:
    eval("print('Hello, world!'")
except SyntaxError as e:
    print(f"Error: {type(e).__name__} - {e}")

try:
    user_age = int(input("Enter your age: "))
    if user_age < 18:
        raise AgeBelow18Error()
    else:
        print("You are eligible.")
except AgeBelow18Error as e:
    print(f"Error: {type(e).__name__} - {e}")
except ValueError:
    print("Invalid input. Please enter a valid integer for age.")
'''

filehandling='''
def write_to_file():
    numbers = []
    for i in range(10):
        num = input(f"Enter number {i + 1}: ")
        numbers.append(int(num))

    with open("T1.txt", "w") as file:
        for num in numbers:
            file.write(str(num) + "\n")

def sort_and_write():
    with open("T1.txt", "r") as file:
        numbers = [int(line.strip()) for line in file]
    sorted_numbers = sorted(numbers)
    with open("T2.txt", "w") as file:
        for num in sorted_numbers:
            file.write(str(num) + "\n")

write_to_file()
sort_and_write()

print("Data has been written to T1.txt, sorted, and written to T2.txt.")

'''

regex='''
import re

with open('names.txt', 'r') as file:
    text = file.read()

names = re.findall(r'(?:Mr\.|Ms\.|Mrs\.)\s([A-Za-z]+)', text)
print("Names of the Users:", names)

websites = re.findall(r'(?:https?://)?(?:www\.)?([a-zA-Z0-9.-]+\.com)\b', text)
print("Website Names ending with .com:", websites)

emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
print("Identify Email IDs:", emails)

matched_numbers = re.findall(r'\b(?:\d{3}[-.\s]?)?(?:\d{2}[-.\s]?)?\d{3,}[-.\s]?\d{4}\b', text)
print("Identified Phone Numbers:", matched_numbers)
'''

database='''
import mysql.connector

myconn = mysql.connector.connect(host="localhost", user="root", passwd="Mysql@123", database="Mihir")

c = myconn.cursor()

#create
insertquery = "INSERT INTO STUDENT (name, age, marks) VALUES (%s, %s, %s)"
values = ("Dhruva", 25, 98)
c.execute(insertquery, values)
myconn.commit()
print("Record inserted successfully")

#read
selectquery = "SELECT * FROM STUDENT"
c.execute(selectquery)
result = c.fetchall()
for row in result:
    print(row)

#update
updatequery = "UPDATE STUDENT SET age = %s WHERE name = %s"
updatevalues = (30, "Dhruva")
c.execute(updatequery, updatevalues)
myconn.commit()
print("Record updated successfully")

#delete
deletequery = "DELETE FROM STUDENT WHERE name = %s"
deletevalue = ("Dhruva",)
c.execute(deletequery, deletevalue)
myconn.commit()
print("Record deleted successfully")


selectquery = "SELECT * FROM STUDENT"
c.execute(selectquery)
result = c.fetchall()
for row in result:
    print(row)
#read
selectquery = "SELECT * FROM STUDENT"
c.execute(selectquery)
result = c.fetchall()
for row in result:
    print(row)


c.close()
myconn.close()
'''

tkinter='''
import tkinter as tk

def add_numbers():
    try:
        num1 = float(entry_num1.get())
        num2 = float(entry_num2.get())
        result = num1 + num2
        label_result.config(text=f"Result: {result}")
    except ValueError:
        label_result.config(text="Please enter valid numbers.")

app = tk.Tk()
app.title("Simple Calculator")

label_num1 = tk.Label(app, text="Enter number 1:")
label_num1.grid(row=0, column=0, padx=10, pady=10)

entry_num1 = tk.Entry(app)
entry_num1.grid(row=0, column=1, padx=10, pady=10)

label_num2 = tk.Label(app, text="Enter number 2:")
label_num2.grid(row=1, column=0, padx=10, pady=10)

entry_num2 = tk.Entry(app)
entry_num2.grid(row=1, column=1, padx=10, pady=10)

btn_add = tk.Button(app, text="Add", command=add_numbers)
btn_add.grid(row=2, column=0, columnspan=2, pady=10)

label_result = tk.Label(app, text="Result:")
label_result.grid(row=3, column=0, columnspan=2, pady=10)

app.mainloop()

'''


python_exp = {
    'client.py': client,
    'server.py': server,
    'toh.py': toh,
    'exception.py': exception,
    'filehandling.py': filehandling,
    'regex.py': regex,
    'database.py': database,
    'tkinter.py': tkinter,
}

def python():
    for filename, content in python_exp.items():
        with open(filename, 'w') as file:
            file.write(content)
        print(f"File '{filename}' created successfully.")