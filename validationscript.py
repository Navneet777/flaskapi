import re

def User_validation(id,fname,lname,phone,email):

    fname = fname
    lname = lname
    phone = phone
    email = email
    idmatch = re.match(r'^([\s\d]+)$', id)

    if idmatch is not None:
        print('Your ID is Valid',id)
    else:
        print("ID contains only numbers you enter",id)

    if re.match('^[A-Za-z ]*$', fname):
        print("First Name is Valid",fname)
    else:
        print("First Name not Valid",fname)

    if re.match('^[A-Za-z ]*$', lname):
        print("Last Name is Valid ",lname)
    else:
        print("Last Name not Valid",lname)


    phonematch = re.search(r'[789]\d{9}$', phone, re.I)
    if phonematch is not None:
        print("Valid Phone Number",phone)
    else:
        print("please enter 10 Digit phone number you enter",phone,"This is not valid")

    emailmatch = re.search(r'\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b', email, re.I)
    if emailmatch is not None:
        print("Valid Email ID",email)
    else:
        print("please enter Correct email id you enter",email,"this is not valid")
id = input("Enter ID Number ?")
fname = input("Enter First Name ?")
lname = input("Enter Last Name ?")
phone = input("Enter Phone Number ?")
email = input("Enter Email ID ?")
User_validation(id,fname,lname,phone,email)
