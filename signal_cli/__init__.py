# Python Libs (OS)
import datetime

# Logging
import logging
import subprocess

# Python Libs {Time}
import time
from typing import Any, Dict, List

# WebBowser | WebDriver (Gecko-Diver)
from selenium import webdriver
from selenium.webdriver.common.by import By


class SignalCLI_Exception(Exception):

    error_code : dict = {
        "-1" : "\nRegister invalid format ({}) Exemple: (+351 918553222)\n",
        "0"  : "\nInvalid Verification Code: {}\n",
        "1"  : "\nInvalid Captcha:\n({})\nTo get a valid Captcha Solve: https://signalcaptchas.org/registration/generate.html",
        "2"  : "\nTimeout [Wait] (To many tries)",
        "3"  : "\nThe phone number ({}) is Already Register",
        "4"  : "\nThe phone number ({}) is not Register or Link",
        "5"  : "\nYou need fust to load a number to be able to use it",
        "6"  : "\nReceiver ({}) Not Found",
        "shell": "\n{}",
    }

    def __init__(self,code,value) -> Exception:
        self.code   = code
        self.value  = value
        logging.error(self.error_code[str(self.code)].format(self.value))
        super().__init__(self.error_code[str(self.code)].format(self.value))

class DataValidator(object):

    def is_signal_capthe(self,url) -> bool:
        if "signalcaptcha://" in url and isinstance(url,str):
            return True
        return False

    def is_phone_number(self,phone) -> bool:
        if " " in phone and isinstance(phone,str):
            return True
        return False

class SignalCLI(object):

    # Json Vars
    options     : Dict
    agent_json  : Dict = {}
    # Shell Command
    base_commnad : str = "signal-cli"
    # Local Validator
    valid : DataValidator = DataValidator()

    def __init__(self) -> None:
        self.options = {
            "new_message"   : "-a {} -o json receive",
            "getstatus"     : "-a {} -o getUserStatus {}",
            "send"          : '-a {} -o json send {} -m "{}"',
            "register"      : "-a {} register",
            "verify"        : "-a {} verify {}",
            "receipt"       : "-a {} -o json sendReceipt {} -t {} --type {}",
            "typing"        : "-a {} -o json sendTyping {}",
            "list"          : "listAccounts",
        }
        self.message = {
            "main":"Picked up _JAVA_OPTIONS: -Dawt.useSystemAAFontSettings=on -Dswing.aatext=true",
        }

    def exceute(self,command : str) -> Any:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process.wait()
        # Get Shell Output
        stdout, stderr = process.communicate()
        # Decode Bytes to String
        stdout, stderr = stdout.decode(), stderr.decode()
        # Generate Vector Data
        if "\n" in stdout:
            stdout = stdout.split("\n")
            stdout.pop(stdout.index(""))
        if "\n" in stderr:
            stderr = stderr.split("\n")
            stderr.pop(stderr.index(""))
        # Message Error
        if self.message["main"] in stderr and len(stderr) >= 1:
            stderr.pop(stderr.index(self.message["main"]))
        return stdout,stderr

    def register(self,number :str,capch : str = "") -> Any:
        # Check Number Fromat
        if f"Number: {number.replace(' ','')}" in self.listaccounts:
            raise SignalCLI_Exception("3",number)
        if not self.valid.is_phone_number(number):
            raise SignalCLI_Exception("-1",number)
        if not self.valid.is_signal_capthe(capch) and capch != "":
            raise SignalCLI_Exception("1", capch)

        # Prepare Phone Number
        number_ = number.split(" ")
        code, phone = number_[0],number_[1]
        # Generate Shell Command Block
        command = f"{self.base_commnad} {self.options['register'].format(f'{code}{phone}')} "
        if capch != "":
            command += "--captcha {}".format(capch)
        else:
            capch = self.captche
            command += "--captcha {}".format(capch)
        # Debuge Shell Command
        logging.debug("Capth_Url: {}".format(capch))
        # Execute Shell Command
        stdout, stderr = self.exceute(command)
        # Logging
        logging.debug("Command: {}".format(command))
        logging.debug("Stdout: {} | Stderr {}".format(stdout, stderr))
        # Message Error
        if len(stderr) >= 1:
            if "Failed to register: [429] Rate limit exceeded: 429" in stderr:
                raise SignalCLI_Exception("2",capch)
            if "Invalid captcha given." in stderr:
                raise SignalCLI_Exception("1",capch)
            raise SignalCLI_Exception("shell",stderr)
        # Set Account Ditals
        self.agent_json["phone_code"] = code
        self.agent_json["phone"] = phone
        return self.verify

    def verify(self,sms_message :str) -> None:
        command = f"{self.base_commnad} {self.options['verify'].format(self.phone_number,sms_message)}"
        stdout, stderr = self.exceute(command)
        logging.debug("Command: {}".format(command))
        logging.debug("Stdout: {} | Stderr {}".format(stdout, stderr))

    @property
    def listaccounts(self) -> List:
        command = f"{self.base_commnad} {self.options['list']}"
        stdout, stderr = self.exceute(command)
        accounts = []
        logging.debug("Command: {}".format(command))
        logging.debug("Stdout: {} | Stderr {}".format(stdout,stderr))
        for i in range(0,len(stdout)):
            accounts.append(stdout[i])
        logging.info("Command: {}\nOutput: {}".format(command,accounts))
        return accounts

    def sendrecipe(self,from_,type_="read") -> List:
        command = f"{self.base_commnad} {self.options['receipt'].format(self.phone_number,from_,int(datetime.datetime.now().timestamp()),type_)}"
        stdout, stderr = self.exceute(command)
        output = []
        logging.debug("Command: {}".format(command))
        logging.debug("Stdout: {} | Stderr {}".format(stdout,stderr))
        for i in range(0,len(stdout)):
            output.append(stdout[i])
        logging.info("Command: {}\nOutput: {}".format(command,output))
        return output
    
    def typing_message(self,from_):
        command = f"{self.base_commnad} {self.options['typing'].format(self.phone_number,from_)}"
        stdout, stderr = self.exceute(command)
        output = []
        logging.debug("Command: {}".format(command))
        logging.debug("Stdout: {} | Stderr {}".format(stdout,stderr))
        for i in range(0,len(stdout)):
            output.append(stdout[i])
        logging.info("Command: {}\nOutput: {}".format(command,output))
        return output
    @property
    def new_messages(self) -> List:
        run_time = time.time()
        command = f"{self.base_commnad} {self.options['new_message'].format(self.phone_number)}"
        stdout, stderr = self.exceute(command)
        logging.debug("Command: {}".format(command))
        logging.debug("Stdout: {} | Stderr {}".format(stdout,stderr))
        run_time = time.time() - run_time
        logging.debug("New Message Function have take {}".format(run_time))
        return stdout

    @property
    def captche(self) -> str:
        profile = webdriver.FirefoxProfile()
        user_agent = "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0"
        profile.set_preference("general.useragent.override", user_agent)
        browser = webdriver.Firefox(profile)
        browser.get("https://signalcaptchas.org/registration/generate.html")
        while True:
            try:
                captch_code = browser.find_elements(By.XPATH, "/html/body/div[1]/a")
                return_ = str(captch_code[0].get_attribute("href"))
                browser.close()
                return return_.replace("\n","")
            except Exception:
                pass
    @property
    def load(self) -> str:
        return self.phone_number

    @load.setter
    def load(self,number : str) -> None:
        #if f"Number: {number.replace(" ", "")}" not in self.listaccounts:
        #    raise SignalCLI_Exception("4", number)
        if not self.valid.is_phone_number(number):
            raise SignalCLI_Exception("-1", number)
        self.agent_json["phone_code"] = number.split(" ")[0]
        self.agent_json["phone"] = number.split(" ")[1]

    @property
    def phone_number(self) -> str:
        number = f"{self.agent_json['phone_code']}{self.agent_json['phone']}"
        if number != "":
            return f"{self.agent_json['phone_code']}{self.agent_json['phone']}"
        else:
            raise SignalCLI_Exception("5","")

    def getUserStatus(self,number : str) -> List:
        if not self.valid.is_phone_number(number):
            raise SignalCLI_Exception("-1",number)
        command = f"{self.base_commnad} {self.options['getstatus'].format(number,number.replace(' ', ''))}"
        stdout, stderr = self.exceute(command)
        status = []
        logging.debug("Command: {}".format(command))
        logging.debug("Stdout: {} | Stderr {}".format(stdout,stderr))
        for i in range(0, len(stdout)):
            status.append(stdout[i])
        logging.info("Command: {}\nOutput: {}".format(command,status))
        return status

    def send(self,to : str,message : str) -> List:
        
        command = f"{self.base_commnad} {self.options['send'].format(self.phone_number,to.replace(' ',''),message)}"
        stdout, stderr = self.exceute(command)
        output = []
        logging.debug("Command: {}".format(command))
        logging.debug("Stdout: {} | Stderr {}".format(stdout,stderr))
        for i in range(0, len(stdout)):
            output.append(stdout[i])
        logging.info("Command: {}\nOutput: {}".format(command,output))
        return output
