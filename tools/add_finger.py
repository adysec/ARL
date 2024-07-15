import requests
import yaml
import re
requests.packages.urllib3.disable_warnings()

def update_data(token):
	push_config = yaml.safe_load(open("tools/指纹数据.json", "r", encoding="utf-8").read())
	for i in push_config:
		name = i['name']
		rule = i['rule']
		payload = {
			"name": name,
			"human_rule": rule
		}
		headers = {
			"Content-Type": "application/json; charset=UTF-8",
			"Token": token,
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.160 Safari/537.36"
		}
		response = requests.post("https://127.0.0.1:5003/api/fingerprint/", json=payload, headers=headers,timeout=20, verify=False)
		if response.status_code==200:
			print(f"[+] 指纹:'{name}'\t规则:{rule}")
		else:
			print(f"[-] 指纹:'{name}'\t上传失败")

def do_login():
	burp0_url = "https://127.0.0.1:5003/api/user/login"
	burp0_headers = {"Sec-Ch-Ua": "\"Chromium\";v=\"121\", \"Not A(Brand\";v=\"99\"", "Accept": "application/json, text/plain, */*", "Content-Type": "application/json; charset=UTF-8", "Sec-Ch-Ua-Mobile": "?0", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.160 Safari/537.36", "Sec-Ch-Ua-Platform": "\"Windows\"", "Origin": "https://127.0.0.1:5003", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty", "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "zh-CN,zh;q=0.9", "Priority": "u=1, i"}
	burp0_json={"password": "arlpass", "username": "admin"}
	res = requests.post(burp0_url, headers=burp0_headers, json=burp0_json,timeout=20, verify=False)
	if res.json()['code']==200:
		print("[+] login Success! ")
		token = res.json()['data']['token']
		update_data(token)
	elif code==401:
		print("[-] login Failure! ")
	else:
		print("[-] login Error! ")
do_login()
