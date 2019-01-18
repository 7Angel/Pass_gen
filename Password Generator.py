import string
import secrets
import binascii

secret_questions = {
1:"What is the name of your first boyfriend or girlfriend? \n",
2:"Which phone number do you remember most from your childhood? \n",
3:"What was your favorite place to visit as a child? \n",
4:"Who is your favorite actor, musician, or artist? \n",
5:"What is the name of your favorite pet? \n",
6:"In what city were you born? \n",
7:"What high school did you attend? \n",
8:"What is the name of your first school? \n",
9:"What is your favorite movie? \n",
10:"What is your mother's maiden name? \n",
11:"What street did you grow up on? \n",
12:"What was the make of your first car? \n",
13:"When is your anniversary? \n",
14:"What is your favorite color? \n",
15:"What is your father's middle name? \n",
16:"What is the name of your first grade teacher? \n",
17:"What was your high school mascot? \n",
18:"Which is your favorite web browser? \n",
19:"what is your favorite website \n",
20:"what is your favorite forum \n",
21:"what is your favorite online platform \n",
22:"what is your favorite social media website \n"
}

remake = {"e":"3", "i":"1", "o":"0", "s":"5", "z":"2", "a":"4", "g":"9"}

def PassGen():

  AvailableChoices = ["r", "c", "e", "s", "random", "caesar", "encrypted", "secret question"]
  while True:
    choice = input("Please choose, what type of Password You want to generate: ").lower().strip()
    if choice in AvailableChoices:
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
      firstPass = input("Please enter preferred password (at least 8 characters): ").strip()
      if len(firstPass) > 7:
        break
    while True:
      offset = input("Please enter preferred password offset: ")
      if offset.isnumeric():
        break
    for char in firstPass:
      number = ord(char)
      newChar = chr(number + int(offset))
      password += newChar
      
  elif choice == "e" or choice == "encrypted":
    print("You chose Encrypted")
    while True:
      firstPass = input("Please enter preferred password (at least 8 characters): ").strip()
      if len(firstPass) > 7:
        break
    password = str(binascii.hexlify(firstPass.encode()))[2:-1]
           
  else:
    print("You chose Secret Question. Please provide your answers (at least 4 characters) to the following questions:")
    password_tmp = []
    while len(password_tmp) < 3:
      while True:
        answer = input(secret_questions[secrets.choice(list(secret_questions))]).strip()
        if len(answer) > 3:
          password_tmp.append(answer)
          break
    new_password=password_tmp[0] + password_tmp[1] + password_tmp[2]
    for i in range(len(new_password)):
      if new_password[i] in remake:
        password += remake[new_password[i]]
      else:
        password += new_password[i]

  print (f"Your new password is {password}")

PassGen()