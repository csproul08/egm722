#make changes to the file name turning it blue
# import getpass module
import getpass

# Take password from the user
passwd = getpass.getpass('Password:')

# Check the password
if passwd == "python":
    print("You are verified")
else:
    print("You are not verified")
