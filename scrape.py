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
	
	myurl = """https://www.google.com/maps/place/Murugan+Idli+Shop/@1.3087768,103.8563853,15z/data=!3m1!5s0x31da184956e15451:0x2b138430ae632476!4m7!3m6!1s0x0:0x3189a6dde2f4df90!8m2!3d1.3087768!4d103.8563853!9m1!1b1"""
	mydf = scrape(myurl);
	mydf = process(mydf)
	# mydf.to_csv('googlereviews.csv')

