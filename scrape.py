from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd
import requests
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import time
from selenium.webdriver.common.keys import Keys

def scrape(myurl1):
	chrome = webdriver.Chrome()
	driver = chrome
	driver.get(myurl1)

	delay = 3# seconds
	try:
		myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'content-container')))
		print("Page is ready!")
	except TimeoutException:
		print("Loading took too much time!")


	time.sleep(10)

	sortbtn = driver.find_element_by_xpath("""/html/body/div[3]/div[9]/div[8]/div/div[1]/div/div/div[2]/div[7]/div[2]/button/span""")
	sortbtn.click()

	newest = driver.find_element_by_xpath("""/html/body/div[3]/div[3]/div[1]/ul/li[2]""")
	newest.click()


	reviewCount = len(driver.find_elements_by_class_name("""ODSEW-ShBeI-text"""))
	print(reviewCount)

	totalReviews = driver.find_elements_by_xpath("""//*[@id="pane"]/div/div[1]/div/div/div[2]/div[2]/div/div[2]/div[2]""")
	totalReviews = [i for i in totalReviews][0].text
	totalReviews = totalReviews.replace(",", "")
	totalReviews = totalReviews.split(" ")[0]
	totalReviews = int(totalReviews)

	print(str(totalReviews) + " reviews found")

	elem = driver.find_elements_by_xpath("""//*[@id="pane"]/div/div[1]/div/div/div[2]/div[2]/div/div[2]/div[2]""")[0]
	elem.click()
	start = time.time()
	while reviewCount < totalReviews:
		actions = ActionChains(driver)
		actions.send_keys(Keys.END)
		actions.perform()
		time.sleep(2)
		reviewCount = len(driver.find_elements_by_class_name("""ODSEW-ShBeI-text"""))
		print(reviewCount)
		curr = time.time()
		if reviewCount == 930:
			break

	reviews = driver.find_elements_by_class_name("""ODSEW-ShBeI-text""")

	rev = [i.text for i in reviews]
	print(rev)
	return rev

def process(li):
	df = pd.DataFrame(li)
	df.columns = ["Reviews"]
	return df

if __name__ == '__main__':

	restaurants = dict()
	# restaurants["TFDB"] = """https://www.google.com/maps/place/25+Degrees+Burger,+Wine+%26+Liquor+Bar/@1.3007261,103.8516291,17z/data=!4m7!3m6!1s0x31da19bb7807cba3:0x76563778a023572a!8m2!3d1.3007127!4d103.8516181!9m1!1b1"""
	# restaurants["TR"] = """https://www.google.com/maps/place/Tiga+Roti/@1.4433247,103.8158846,17z/data=!4m7!3m6!1s0x31da136c330fbc5b:0xf56c97db1899a57e!8m2!3d1.4433247!4d103.8158846!9m1!1b1"""
	# restaurants["TMG"] = """https://www.google.com/maps/place/The+Market+Grill/@1.2799855,103.8471047,17z/data=!4m7!3m6!1s0x31da190d7b80291f:0x826105028950285c!8m2!3d1.2799757!4d103.8471269!9m1!1b1"""

	restaurants["Gravy_Restaurant"] = """https://www.google.com/maps/place/Gravy+Restaurant+%26+Bar+(Tanjong+Katong)/@1.3039038,103.8988077,15.25z/data=!4m12!1m3!2m2!1srestaurants!6e5!3m7!1s0x31da193257f33767:0x42996ddf16c716d7!8m2!3d1.3063739!4d103.8956192!9m1!1b1!15sCgtyZXN0YXVyYW50c1oNIgtyZXN0YXVyYW50c5IBCnJlc3RhdXJhbnQ"""
	restaurants["Volare"] = """https://www.google.com/maps/place/Volare/@1.3039398,103.8988077,15z/data=!4m12!1m3!2m2!1srestaurants!6e5!3m7!1s0x31da194d7e086cdb:0xe1acb2e426af4fa4!8m2!3d1.3043697!4d103.9021355!9m1!1b1!15sCgtyZXN0YXVyYW50c1oNIgtyZXN0YXVyYW50c5IBEml0YWxpYW5fcmVzdGF1cmFudA"""
	restaurants["La_Bonne_Table"] = """https://www.google.com/maps/place/la+bonne+table/@1.3039398,103.8988077,15z/data=!4m12!1m3!2m2!1srestaurants!6e5!3m7!1s0x31da19abe60e2c1f:0x159a2d5b905c3349!8m2!3d1.3073601!4d103.9072264!9m1!1b1!15sCgtyZXN0YXVyYW50c1oNIgtyZXN0YXVyYW50c5IBEWZyZW5jaF9yZXN0YXVyYW50"""
	restaurants["Danji_KBBQ"] = """https://www.google.com/maps/place/Danji+Korean+BBQ+Buffet/@1.3039398,103.8988077,15z/data=!4m12!1m3!2m2!1srestaurants!6e5!3m7!1s0x31da1814ddba393b:0xd3f2557c12654744!8m2!3d1.3085505!4d103.8945949!9m1!1b1!15sCgtyZXN0YXVyYW50c1oNIgtyZXN0YXVyYW50c5IBGmtvcmVhbl9iYXJiZWN1ZV9yZXN0YXVyYW50"""
	restaurants["Comida_Mexicana"] = """https://www.google.com/maps/place/Comida+Mexicana+Singapore/@1.3039398,103.8988077,15z/data=!4m12!1m3!2m2!1srestaurants!6e5!3m7!1s0x31da180ae6487617:0x777c2fa714016c!8m2!3d1.3087498!4d103.9120937!9m1!1b1!15sCgtyZXN0YXVyYW50c1oNIgtyZXN0YXVyYW50c5IBCnJlc3RhdXJhbnQ"""


	output_df = pd.DataFrame();

	for i in restaurants.keys():
		print(i)
		retdf = scrape(restaurants[i])
		retdf = process(retdf)
		retdf["Restaurant"] = str(i)
		output_df = output_df.append(retdf)

	output_df.to_csv("testing_scraped_output.csv")

	print(len(output_df))

