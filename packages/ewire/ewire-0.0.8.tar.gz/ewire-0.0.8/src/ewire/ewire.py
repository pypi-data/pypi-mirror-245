import getpass

def hello():
    username = getpass.getuser()
    print("Hello ", username)