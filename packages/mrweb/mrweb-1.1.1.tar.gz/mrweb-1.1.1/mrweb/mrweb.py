import warnings
warnings.filterwarnings("ignore")

__author__ = 'mr moorgh'
__version__ = 1.1.1

from sys import version_info
if version_info[0] == 2: # Python 2.x
    from mrweb import *
elif version_info[0] == 3: # Python 3.x
    from mrweb.mrweb import *


import os
##############################################
def installlib():
    try:
        os.system("pip install requests")
    except:
        try:
            os.system("pip3 install requests")
        except:
            try:
                os.system("python3 -m pip install requests")
            except:
                os.system("python -m pip install requests")
    return True


##############################################
try:
    import requests
except:
    installlib()
    import requests
import json


version="1.1.1"
key=""




def getlatest():
    api=requests.get("https://mrapiweb.ir/mrapi/update.php?version={version}").text
    js=json.loads(api)
    if js["update"] == False:
        try:
            os.system("pip install mrweb --upgrade")
        except:
            try:
                os.system("pip3 install mrweb --upgrade")
            except:
                try:
                    os.system("python3 -m pip install mrweb --upgrade")
                except:
                    os.system("python -m pip install mrweb --upgrade")
    else:
        return True




class AIError(Exception):
    pass

class TranslateError(Exception):
    pass

class NoInternet(Exception):
    pass

class JsonError(Exception):
    pass

class NoCoin(Exception):
    pass

def getlatest():
    global version
    try:
        latest=requests.get(f"https://mrapiweb.ir/pyapi.php?ver={version}")
        ver=json.loads(latest)
        if ver["updated"] == False:
            file=open("pyai.py","w")
            file.write(requests.get(ver["get_update_from"]))
            file.close()
            return "Updated PyAPI To Latest"
    except:
        return "No Need"

class ai():
    def bard(query):
        api=requests.get(f"https://mrapiweb.ir/api/apitest/gbard.php?question={query}").text
        try:
            return api
        except Exception as er:
            raise NoInternet("Please Connect To Internet To Use This AI")
    def gpt(query):
        global key
        query=query.replace(" ","-")
        api=requests.get(f"https://mrapiweb.ir/api/chatbot.php?key={key}&question={query}").text
        result=json.loads(api)
        try:
            return result["javab"]
        except KeyError:
            raise NoCoin("Please Charge Your Key From @mrwebapi_bot")
        except Exception as er:
            raise AIError("Failed To Get Answer Make Sure That You Are Connected To Internet & vpn is off")
        

    def evilgpt(query):
        global key
        api=requests.get(f"https://mrapiweb.ir/api/evilgpt.php?key={key}&emoji=🗿&soal={query}").text
        result=json.loads(api)
        try:
            return result["javab"]
        except KeyError:
            raise NoCoin("Please Charge Your Key From @mrwebapi_bot")
            
        except Exception as er:
            raise AIError("Failed To Get Answer Make Sure That You Are Connected To Internet & vpn is off")

class api():
    def translate(to,text):
        api=requests.get(f"https://mrapiweb.ir/api/translate.php?to={to}&text={text}").text
        result=json.loads(api)
        try:
            return result["translate"]
        except KeyError:
            raise TranslateError("Translate Error For Lang {to}")
        
    def ocr(to,url):
        api=requests.get(f"https://mrapiweb.ir/api/ocr.php?url={url}&lang={to}").text
        result=json.loads(api)
        try:
            return result["result"]
        except KeyError:
            raise AIError("Error In OCR Lang {to}")
    def isbadword(text):
        text=text.replace(" ","+")
        api=requests.get(f"https://mrapiweb.ir/api/badword.php?text={text}").text
        result=json.loads(api)
        if result["isbadword"] == True:
            return True
        else:
            return False
    def randbio():
        return requests.get(f"https://mrapiweb.ir/api/bio.php").text

    def isaitext(text):
        text=text.replace(" ","-")
        api=requests.get(f"https://mrapiweb.ir/api/aitext.php?text={text}").text
        result=json.loads(api)
        if result["aipercent"] == "0%":
            return False
        else:
            return True

    def notebook(filename,text):
        text=text.replace(" ","-")
        api=requests.get(f"https://mrapiweb.ir/api/notebook.php?text={text}")
        with open(filename,"wb") as mr:
            mr.write(api.content)
            mr.close()
        return True
    def email(to,subject,text):
        text=text.replace(" ","+")
        subject=subject.replace(" ","+")
        requests.get(f"https://mrapiweb.ir/api/email.php?to={to}&subject={subject}&message={text}")
        #print(f"https://mrapiweb.ir/api/email.php?to={to}&subject={subject}&message={text}")
        return f"Email Sent To {to}"
    def ipinfo(ip):
        api=requests.get(f"https://mrapiweb.ir/api/ipinfo.php?ipaddr={ip}").text
        ip=json.loads(api)
        try:
            return ip
        except:
            raise JsonError(f"Unknown Json Key : {ip}")
    def arz():
        api=requests.get(f"https://mrapiweb.ir/api/arz.php").text
        arz=json.loads(api)
        try:
            return arz
        except:
            raise JsonError(f"Unknown Json Key : {ip}")

    def insta(link):
        global key
        text=text.replace(" ","-")
        api=requests.get(f"https://mrapiweb.ir/api/ig.php?key={key}&url={link}").text
        ins=json.loads(api)
        try:
            return ins["link"]
        except KeyError:
            raise NoCoin("Please Charge Your Key From @mrwebapi_bot")
        except Exception:
            raise TypeError("Failed Please Try Again")
    def voicemaker(sayas,text,filename):
        text=text.replace(" ","-")
        api=requests.get(f"https://mrapiweb.ir/api/voice.php?sayas={sayas}&text={text}")
        with open(filename,"wb") as mr:
            mr.write(api.content)
            mr.close()
        return True
    def walletgen():
        return requests.get(f"https://mrapiweb.ir/api/walletgen.php").text
    def imagegen(text):
        text=text.replace(" ","-")
        return requests.get(f"https://mrapiweb.ir/api/imagegen.php?imgtext={text}").text
    def proxy():
        #text=text.replace(" ","-")
        api=requests.get(f"https://mrapiweb.ir/api/telproxy.php").text
        proxy=json.loads(api)
        return proxy["connect"]

    def fal(filename):
        api=requests.get(f"https://mrapiweb.ir/api/fal.php")
        with open(filename,"wb") as mr:
            mr.write(api.content)
            mr.close()
        return True
    def worldclock():
        return requests.get(f"https://mrapiweb.ir/api/zone.php").text

    def youtube(vid):
        global key
        return requests.get(f"https://mrapiweb.ir/api/yt.php?key={key}&id={vid}").text
    def sendweb3(privatekey,address,amount,rpc,chainid):
        return requests.get(f"https://mrapiweb.ir/api/wallet.php?key={privatekey}&address={address}&amount={amount}&rpc={rpc}&chainid={chainid}").text

def help():
    return "Join @mrapilib in telegram"
