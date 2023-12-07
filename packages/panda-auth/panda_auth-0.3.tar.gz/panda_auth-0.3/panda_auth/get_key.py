import requests
import platform
import uuid
import pyperclip
import json
import hashlib
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def copy_to_clipboard(text):
    pyperclip.copy(text)

def sha256_hash(input_string):
    sha256_hash_object = hashlib.sha256()
    sha256_hash_object.update(input_string.encode('utf-8'))
    hashed_string = sha256_hash_object.hexdigest()
    return hashed_string

def get_hardware_id():
    try:
        mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(5, -1, -1)])
        processor_info = platform.processor()
        hardware_id = f"{mac_address}-{processor_info}"
        return sha256_hash(hardware_id)
    except Exception as e:
        print(f"Error: {e}")
        return None

def get_webpage_content(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Error: Unable to fetch webpage. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None



def get_keyHWID(service_name, hardwareid, debug):
    url = f"https://pandadevelopment.net/validate?key=testkey&hwid=lol&service={service_name}"
    webpage_content = get_webpage_content(url)

    if not webpage_content:
      if debug:
        print("[Debug]: Unable to fetch webpage content.")
    generatedlink = f"https://auth.pandadevelopment.net/getkey?service={service_name}&hwid={hardwareid}"
    if debug:
      print(f"[Debug] Link generated successfully : {generatedlink} ")
    return generatedlink

def get_key(service_name, debug):
    url = f"https://pandadevelopment.net/validate?key=testkey&hwid=lol&service={service_name}"
    webpage_content = get_webpage_content(url)

    if not webpage_content:
      if debug:
        print("[Debug]: Unable to fetch webpage content.")
    generatedlink = f"https://auth.pandadevelopment.net/startkey.html?service={service_name}"
    if debug:
      print(f"[Debug] Link generated successfully : {generatedlink} ")
    return generatedlink


      



