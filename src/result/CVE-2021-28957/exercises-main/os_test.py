import os
# C:\Users\ibrahi
os.chdir("C:\\Users\\ibrahim\\Desktop")

for i in os.listdir():
    if i.endswith((".png","PNG","jpg")):
        print(i)
    
