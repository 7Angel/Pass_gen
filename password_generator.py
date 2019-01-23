import string
import secrets
import binascii
import sys
import os
import ast

with open(os.path.join(sys.path[0], "secret_questions.txt"), "r") as f:
  secret_questions = f.readlines()
  secret_questions = [x.strip() for x in secret_questions]

with open(os.path.join(sys.path[0], "logins_db.txt"), "r") as f:
  my_logins = str(f.read())
  if my_logins == "": 
    my_logins = {}
  else:
    my_logins = ast.literal_eval(my_logins)

class Login:
  def __init__(self, url, login_name, password):
    self.url = url
    self.login_name = login_name
    self.password = password

  def remind(self):
    return f"Your credentials for {self.url} are: \n Login name: {self.login_name} \n Password: {self.password}"
  
  def export(self):
    return [self.url, self.login_name, self.password]

for key, value in my_logins.items():
    my_logins[key] = Login(value[0], value[1], value[2])

def generate_password():

  available_choices = ["r", "c", "e", "s", "random", "caesar", "encrypted", "secret question"]
  while True:
    choice = input("Please choose, what type of Password You want to generate: ").lower().strip()
    if choice in available_choices:
      break
#  print (choice)
  password = ''
  
  if choice == "r" or choice == "random":
    print("You chose Random")
    while True:
      size = input("Please enter preferred password length (can't be less than 8): ")
      if size.isnumeric() and int(size) > 7:
        break
    password = password.join(secrets.choice(string.ascii_letters + string.digits + string.punctuation) for i in range(int(size)))
    
  elif choice == "c" or choice == "caesar":
    print("You chose Caesar")
    while True:
      first_pass = input("Please enter preferred password (at least 8 characters): ").strip()
      if len(first_pass) > 7:
        break
    while True:
      offset = input("Please enter preferred password offset: ")
      if offset.isnumeric():
        break
    for char in first_pass:
      number = ord(char)
      new_char = chr(number + int(offset))
      password += new_char
      
  elif choice == "e" or choice == "encrypted":
    print("You chose Encrypted")
    while True:
      first_pass = input("Please enter preferred password (at least 8 characters): ").strip()
      if len(first_pass) > 7:
        break
    password = str(binascii.hexlify(first_pass.encode()))[2:-1]
           
  else:
    remake = {"e":"3", "i":"1", "o":"0", "s":"5", "z":"2", "a":"4", "g":"9"}
    print("You chose Secret Question. Please provide your answers (at least 4 characters) to the following questions:")
    password_tmp = []
    while len(password_tmp) < 3:
      while True:
        answer = input(secrets.choice(secret_questions)).strip()
        if len(answer) > 3:
          password_tmp.append(answer)
          break
    new_password=password_tmp[0] + password_tmp[1] + password_tmp[2]
    for i in range(len(new_password)):
      if new_password[i] in remake:
        password += remake[new_password[i]]
      else:
        password += new_password[i]

  return password

def create_record():
  while True:
    service = input("Please enter the preferred name of the service(at least 4 characters): ").strip()
    if service in my_logins:
      while True:
        overwrite = input("This service already exists in the database. Do You want to update its information (Y/N)? ").lower().strip()
        if overwrite == "y":
          break
        elif overwrite == "n":
          return
      break
    elif len(service) > 3: 
      break
  while True:
    url = input("Please enter the service url: ").strip()
    if len(url) > 4 and "." in url: break
  while True:
    login_name = input("Please enter your login name (at least 4 characters): ").strip()
    if len(login_name) > 3: break
  password = generate_password()
  
  return [service, url, login_name, password]

while True:
  print("What would You like to do?")
  print("If you would like your credentials REMINDED, etner 'R'")
  print("If you would like to CREATE new Login, etner 'C'")
  print("If you would like to EXIT, etner 'E'")
  choice = input("What is your choice: ").lower().strip()
  if choice == "r":
    reminder = input("Enter the name of the service: ")
    if reminder in my_logins:
      print(my_logins[reminder].remind())
    else:
      print("There is no such record in the database")
  elif choice == "c":
    my_login = create_record()
    try: 
      my_logins[my_login[0]] = Login(my_login[1], my_login[2], my_login[3])
    except:
      pass
  elif choice == "e":
    for key, value in my_logins.items():
      my_logins[key] = my_logins[key].export()
    with open(os.path.join(sys.path[0], "logins_db.txt"), "w") as f:
      f.write(str(my_logins))
    break
  else:
    print("invalid input")
