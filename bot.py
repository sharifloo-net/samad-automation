import os
import requests
import json  # for proper JSON formatting


class Bot:
	BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
	IMAGES_PATH = "./"
	
	PROXY_USER = os.getenv('PROXY_USER')
	PROXY_PASS = os.getenv('PROXY_PASS')
	PROXY_HOST = os.getenv('PROXY_HOST')
	PROXY_PORT = os.getenv('PROXY_PORT')
	if PROXY_USER and PROXY_PASS:
		proxy_url = f'socks5h://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}'
	else:
		proxy_url = f'socks5h://{PROXY_HOST}:{PROXY_PORT}'
	
	proxies = {
		'http': proxy_url,
		'https': proxy_url
	}
	
	def __init__(self):
		self.CHAT_ID = self.get_last_chat_id()
	
	def get_local_images(self) -> list[str] | None:
		return [f for f in os.listdir(self.IMAGES_PATH) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
	
	def send_all_images_as_album(self):
		# Collect images
		images = self.get_local_images()
		
		if not images:
			print("No images found.")
			return
		
		# Build media array and files dict
		media = []
		files = {}
		for img_file in images:
			media.append({"type": "photo", "media": f"attach://{img_file}"})
			files[img_file] = open(os.path.join(self.IMAGES_PATH, img_file), "rb")
		
		# Send as media group
		url = f"https://api.telegram.org/bot{self.BOT_TOKEN}/sendMediaGroup"
		data = {
			"chat_id": self.CHAT_ID,
		    "media": json.dumps(media).encode('utf-8')
		}
		
		requests.post(url, data=data, files=files, proxies=self.proxies, timeout=30)
		print('All images have been sent successfully!')
		
		# Close all files
		for f in files.values():
			f.close()
	
	def remove_local_images(self):
		images = self.get_local_images()
		for image in images:
			os.remove(image)
		print('All local images have been deleted successfully.')
	
	def get_chat_ids(self) -> list[int]:
		url = f'https://api.telegram.org/bot{self.BOT_TOKEN}/getUpdates'
		try:
			response = requests.get(url, proxies=self.proxies, timeout=60)
			data = response.json()  # parse JSON properly
		except Exception as e:
			print("Error fetching updates:", e)
			return []
		
		chat_ids = []
		for update in data.get('result', []):
			try:
				chat_id = update['message']['chat']['id']
				chat_ids.append(chat_id)
			except KeyError:
				continue
		return chat_ids
	
	def get_last_chat_id(self) -> int | None:
		ids = self.get_chat_ids()
		if ids:
			return ids[-1]
		return None