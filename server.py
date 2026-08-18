from database import Database
import json
class Server:
    def __init__(self,host,ip,os,cpu,ram,disk,loc,stat):
        self.host = host
        self.ip = ip
        self.os = os
        self.cpu = cpu
        self.ram = ram
        self.disk = disk
        self.loc = loc
        self.stat = stat
    def info(self):
        print(f"""
        {self.host} = host
        {self.ip} = ip
        {self.os} = os
        {self.cpu} = cpu
        {self.ram} = ram
        {self.disk} = disk
        {self.loc} = loc
        {self.stat} = stat
        """)
    def __str__(self):
        return f"{self.host:<16} | {self.ip:<15} | {self.os:<6} | {self.cpu:<4} | {self.ram:<5} | {self.disk:<5} | {self.loc:<16} | {self.stat}"

class Inventory:
    def __init__(self):
        self.ser =[]
        self.db = Database()
        self.copydb()
    def add(self,server):
        self.ser.append(server)
        self.db.addserver(server)
    def view(self):
        if len(self.ser) == 0:
            print("-------No servers-------")
        else:
            print(f"\n\n{'Host Name':<16} | {'IP':<15} | {'OS':<6} | {'CPU':<4} | {'RAM':<5} | {'DISK':<5} | {'Location':<16} | Status ")
            print("_"*98,'\n')
        for i in self.ser:
            print(i,'\n')
    def search(self,data):
        if self.ser:
            for i in self.ser:
                if i.host == data:
                    print("=====server found=====")
                    print(i)
                    return
            print("----Server Not Found----")
        else:
            print("------No servers------")
    def update(self,hname,data):
        for i in self.ser:
            if i.host == hname:
                i.host = data
                self.db.updateserver(hname,data)
                print(i)
                return
        print("----Given name not found----")
    def switchstats(self,hname):
        for i in self.ser:
            if i.host == hname:
                if i.stat == "Online":
                    i.stat = "Offline"
                else:
                    i.stat = "Online"
                self.db.switchstat(hname)
                print(i)
    def delete(self,data):
        for i in self.ser:
            if i.host == data:
                print(f"Deleted: {i}")
                self.ser.remove(i)
                self.db.deleteserver(data)
                return
        print("----No server name matched----")
    def report(self):
        return f"""Total Servers:{len(self.ser)}
                  Linux Servers: {len([c for c in self.ser if c.os == 'Linux'])}
                  Windows Servers: {len([c for c in self.ser if c.os == 'Windows'])}
                  Online Servers:{len([c for c in self.ser if c.stat == 'Online'])}
                  Offline Servers:{len([c for c in self.ser if c.stat == 'Offline'])}"""
    def copydb(self):
        db = self.db.getallserver()
        for i in db:
            s = Server(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7])
            self.ser.append(s)
    def checkhost(self,host):
        for i in self.ser:
            if i.host == host:
                return True
        return False
    def exportjson(self):
        data = []
        for i in self.ser:
            data.append({
                "hostname: ":i.host,
                "IP: ":i.ip,
                "OS: ":i.os,
                "CPU: ":i.cpu,
                "RAM: ":i.ram,
                "Disk: ":i.disk,
                "Location: ":i.loc,
                "Status: ":i.stat})
        with open('server.json','w') as f:
            json.dump(data,f,indent=4)
    def importjson(self):
        with open("server.json",'r') as f:
            data = json.load(f)
        for i in data:
            s = Server(i["hostname: "],i["IP: "],i["OS: "],i["CPU: "],i["RAM: "],i["Disk: "],i["Location: "],i["Status: "])
            if self.checkhost(s.host):
                print(f"{s.host} already exists")
                continue
            self.add(s)
