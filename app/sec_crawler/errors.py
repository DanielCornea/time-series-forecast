f = open("Errors.txt", "r")

with open("Errors.txt", "r") as f: 
    ls = f.readlines()

f.close()
ls = [x.strip() for x in ls]
ls = filter(bool, ls)
ls = list(ls)

print(len(ls))
