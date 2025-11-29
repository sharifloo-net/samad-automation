def main():
	from samad import Samad
	from bot import Bot
	
	try:
		samad = Samad()
		samad.login()
		# feature_title = input('What feature do you want to open? ')
		samad.open_feature()
		
		# Send images to Samad Plus bot as album
		bot = Bot()
		bot.send_all_images_as_album()
		bot.remove_local_images()
		
	
	except Exception as e:
		print('Oops!')
		print(e)
		print('Please try again.')


if __name__ == '__main__':
	main()
# ====================================
# time.sleep(5)
