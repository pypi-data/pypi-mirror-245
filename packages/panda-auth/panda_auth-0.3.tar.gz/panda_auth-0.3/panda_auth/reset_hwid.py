import requests


def reset_hwid(service, key, newhwid, debug):
    url = f"https://pandadevelopment.net/serviceapi/edit/hwid?service={service}&key={key}&newhwid={newhwid}"
    response = requests.post(url)
    if debug:
        print(f"[Debug] Response : {response} , StatusCode : {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        if debug:
            print("[Debug] HWID edited successfully ✅")
        return 'Success'
      