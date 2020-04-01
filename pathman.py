import argparse
from reg import get_reg, set_reg
from subprocess import call

parser = argparse.ArgumentParser(description="Manipulate PATH varibables.",)
parser.add_argument('--add', "-a", action='append', help = "Add directory to path.", metavar = "Path", dest = "add")
parser.add_argument('--remove', "-r", action='append', help = "Remove directory from path.", metavar = "Path", dest = "remove")
parser.add_argument('--list', "-l", action='store_true', help = "List PATH directories.", dest = "list")
parser.add_argument('--in', "-i", action='store', help = "See if directory is in the PATH.", metavar = "Path", dest = "in")

args = parser.parse_args()

def update():
    call("setx /M USERNAME %USERNAME%")

def add(i):
    path = get_reg("HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment", "Path")
    path += ";"
    path += ";".join(i)
    if set_reg("HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment", "Path", path):
        print("Successful.")
        update()
    else:
        print("Failed.")

def remove(i):
    path = get_reg("HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment", "Path")
    path = path.split(";")
    o = []
    for j in path:
        if j not in i:
            o.append(j)
    path = ";".join(o)
    if set_reg("HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment", "Path", path):
        print("Successful.")
        update()
    else:
        print("Failed.")

def list_path():
    return get_reg("HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment", "Path")

def in_path(p):
##    print(list_path().split(";"))
    return p.replace(r"\\", "\\").replace("/", "\\") in [i if i[-1] != "\\" else i[:-1] for i in list_path().split(";") if i]

##print(args)
v = vars(args)
if v["list"]:
    print(*list_path().split(";"), sep = "\n")
elif s := v["in"]:
    t = in_path(s)
    if t:
        print(f"'{s}'", "is in the PATH.")
    else:
        print(f"'{s}'", "is NOT in the PATH.")
else:
    if a := v["add"]:
        add(a)
    if r := v["remove"]:
        remove(r)

