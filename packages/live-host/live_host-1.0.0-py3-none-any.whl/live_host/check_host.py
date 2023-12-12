import requests
import random

UserAgents = [
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1.2 Safari/605.1.15",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107"
]

headers = {}



def is_alive(target_host):
	
	headers["User-Agent"] = UserAgents[random.randrange(0,UserAgents - 1)]
	if target_host.startswith("https://"):
		status = requests.get(url = target_host, headers = headers)
	
		if status.status_code == 200:
		
			return True
		
		else:
		
			return False
			
	else:
		
		status = requests.get(url = f"https://{target_host}", headers = headers)
		if status.status_code == 200:
			
			return True
			
		else:
			
			return False
		

