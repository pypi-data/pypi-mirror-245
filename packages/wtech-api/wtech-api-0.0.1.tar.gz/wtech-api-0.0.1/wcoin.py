from wtech import WTech,Intents
from cryptography.fernet import Fernet

w = WTech(intents=Intents())

def pay(address : str , target : str , amout : float):
  with open("key.key","r") as f:
    key = f.read()
    fernet = Fernet(key)
    # 解密结果
    a = fernet.decrypt(address)
    b = fernet.decrypt(target)
    ad = eval(a.decode())
    bd = eval(b.decode())
    am = int(ad[1])
    bm = int(bd[1])
    tm = am - amout
    bmn = bm + amout
    am = am - tm
    print("Success to tranfer!")

def mining(address : str):
  with open("key.key","r") as f:
    key = f.read()
    fernet = Fernet(key)
    # 解密结果
    a = fernet.decrypt(address.encode())
    ad = eval(a.decode())
    am = int(ad[1])
    while True:
      tm = am + 10
      am = tm
      print("Mining result: {}".format(am))