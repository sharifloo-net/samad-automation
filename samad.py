import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Samad:
	service = Service()
	TARGET_UNIVERSITY = os.getenv('TARGET_UNIVERSITY')
	CHROME_WEBDRIVER_PATH = os.getenv('CHROME_WEBDRIVER_PATH')
	USERNAME = os.getenv('SAMAD_USER')
	PASSWORD = os.getenv('SAMAD_PASS')
	
	driver = webdriver.Chrome(service=service)
	wait = WebDriverWait(driver, 5)
	
	def __init__(self):
		# Whenever want to get info from the user
		# self.username = ''
		# self.password = ''
		self.driver.get('https://samad.app/login')
	
	def login(self):
		ul = self.wait.until(
			EC.visibility_of_element_located(
				(By.TAG_NAME, 'ul')
			)
		)
		schools = ul.find_elements(By.TAG_NAME, 'li')
		for li in schools:
			if self.TARGET_UNIVERSITY in li.text.strip():
				li.click()
				break
		
		username_input = self.wait.until(
			EC.presence_of_all_elements_located(
				(By.NAME, 'username')
			)
		)
		username_input[0].send_keys(self.USERNAME)
		
		password_input = self.wait.until(
			EC.presence_of_all_elements_located(
				(By.NAME, 'password')
			)
		)
		password_input[0].send_keys(self.PASSWORD)
		login_btn = self.wait.until(
			EC.element_to_be_clickable(
				(By.CSS_SELECTOR, 'button.auth-btn')
			)
		)
		login_btn.click()
		
		modern_ui_btn = self.wait.until(
			EC.element_to_be_clickable(
				(By.XPATH, "//button[contains(., 'ورود به رابط کاربری دانشجویی')]")
			)
		)
		modern_ui_btn.click()
	
	def open_feature(self, feature_title='وضعیت رزروها'):
		features = self.wait.until(
			EC.presence_of_all_elements_located(
				(By.CLASS_NAME, 'feature-title')
			)
		)
		for feature in features:
			if feature.text == feature_title:
				feature.click()
				break
		if feature_title == 'وضعیت رزروها':
			while True:
				# is_next_page = input('Want to see next week status? (Y/N): ').lower()
				is_next_page = 'Y'.lower()
				if is_next_page == 'y' or is_next_page == 'yes':
					self.reservation_status_next_page()
					self.get_codes()
					break
				elif is_next_page == 'n' or is_next_page == 'no':
					self.get_codes()
					break
				else:
					print('Invalid key provided. Only can get "Y" or "N".')
		elif feature_title == 'رزرو غذا':
			self.driver.refresh()
	
	def reservation_status_next_page(self):
		next_page = self.wait.until(
			EC.element_to_be_clickable(
				(By.CLASS_NAME, 'flaticon-left-chevron')
			)
		)
		next_page.click()
	
	def get_codes(self):
		svgs = self.wait.until(
			EC.presence_of_all_elements_located(
				(By.CSS_SELECTOR, 'svg.text-primary, svg.text-accent')
			)
		)
		is_dinner = False
		counter = 1
		for svg in svgs:
			try:
				svg.click()
				
				dates = self.wait.until(
					EC.presence_of_all_elements_located(
						(By.CSS_SELECTOR, '.ant-modal-title')
					)
				)
				modal_card = self.wait.until(
					EC.presence_of_all_elements_located(
						(By.CLASS_NAME, 'ant-modal')
					)
				)
				
				WebDriverWait(self.driver, 1).until(
					EC.presence_of_all_elements_located(
						(By.CSS_SELECTOR, '.ant-qrcode > canvas')
					)
				)
				
				date = dates[0].text.strip().replace('جزئیات رزرو - ', '')
				modal_card[0].screenshot(f'کد_{'شام' if is_dinner else 'ناهار'}_{date}.png')
			
			except:
				pass
			finally:
				close_btn = self.wait.until(
					EC.element_to_be_clickable(
						(By.CLASS_NAME, 'ant-modal-close')
					)
				)
				close_btn.click()
				if is_dinner:
					counter += 1
				is_dinner = not is_dinner
				continue
