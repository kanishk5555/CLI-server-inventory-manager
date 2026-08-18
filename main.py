from server import Inventory , Server
import time,re
inv = Inventory()
ip = re.compile(r"\b(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\b")

while True:
    print("""
===== SERVER INVENTORY =====

1. Add Server
2. View Servers
3. Search Server
4. Update Server
5. Delete Server
6. Report
7. Export to json
8. Import json
9. Exit""")

    try:
        i = input(" Choice: ")
        if i in ['1','2','3','4','5','6','7','8','9']:
            if i == '1':
                s = Server(input("Hostname: ").strip(),input("IP: "),input("OS (Linux or Windows): ").strip().capitalize(),int(input("CPU(32 or 64): ")),int(input("RAM(only int): ")),int(input("Disk(only int): ")),input("Location: "),"Online")
                temp =[]
                if inv.checkhost(s.host):
                    temp.append(str(s.host)+" : Hostname already exist")
                if not ip.search(s.ip):
                    temp.append(str(s.ip) + " : Enter Valid IP")
                if s.os not in ["Linux","Windows"]:
                    temp.append(str(s.os) + " : Choose valid OS (Linux or Windows):")
                if s.ram <= 0 or s.disk <= 0 or s.cpu not in [32,64]:
                    if s.ram <= 0:
                        temp.append(str(s.ram) +" : RAM Should't be ZERO or Negative")
                    if s.disk <= 0:
                        temp.append(str(s.disk) +" : Disk Should't be ZERO or Negative")
                    if s.cpu not in [32,64] :
                        temp.append(str(s.cpu)+" : CPU can only be 32bit or 64bit")
                if len(temp) == 0:
                    inv.add(s)
                    print("=====Server added=====")
                    time.sleep(1)
                else:
                    print("=====ERROR=====")
                    for i in temp:
                        print(i)
                    time.sleep(2)
            elif i == '2':
                inv.view()
            elif i == '3':
                k = input("Enter hostname to search: ")
                inv.search(k)
            elif i == '4':
                print("Update Name : 1 \nUpdate Status : 2")
                choice = input("Choose (1) or (2): ")
                if choice == str(1):
                    k1 = input("Enter hostname to search: ")
                    k2 = input("Enter hostname to update: ")
                    inv.update(k1,k2)
                else:
                    hname = input("Enter hostname to switch status: ")
                    inv.switchstats(hname)
            elif i == '5':
                k = input("Enter hostname to Delete: ")
                inv.delete(k)
            elif i == '6':
                print(inv.report())
            elif i== '7':
                inv.exportjson()
                print("-----Exported to json Successfully------")
            elif i=='8':
                print("-----Imported from json------")
                inv.importjson()
            elif i == '9':
                inv.db.close()
                break
            time.sleep(2)
        else:
            print("-----Choose only from choices 1,2,3,4,5,6,7,8,9-----")
            time.sleep(2)
    except ValueError as e:
        print("Error: ",e)
        print("----Only Integers for CPU,RAM,Disk----")
        time.sleep(2)
