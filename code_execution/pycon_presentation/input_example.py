#! python2
import subprocess

print("What is your id?")
user_id = input()
print("Hello " + user_id + ", here's what's in your home directory:")
subprocess.call(["ls", "/home/" + user_id])
