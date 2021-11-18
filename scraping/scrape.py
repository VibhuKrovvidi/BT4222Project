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
		if reviewCount >= 75:
			break

	reviews = driver.find_elements_by_class_name("""ODSEW-ShBeI-text""")
	review_date = driver.find_elements_by_class_name("""ODSEW-ShBeI-RgZmSc-date""")
	review_stars = driver.find_elements_by_class_name("""ODSEW-ShBeI-H1e3jb""")



	rev = [i.text for i in reviews]
	redate = [i.text for i in review_date]
	revstar = [i.get_attribute("aria-label") for i in review_stars]
	retdf = pd.DataFrame(list(zip(rev, redate, revstar)),columns =['Review', 'Date', "Stars"])
	driver.close()
	return retdf



if __name__ == '__main__':

	restaurants = dict()
	restaurants["Gravy_Restaurant"] = """https://www.google.com/maps/place/Gravy+Restaurant+%26+Bar+(Tanjong+Katong)/@1.3039038,103.8988077,15.25z/data=!4m12!1m3!2m2!1srestaurants!6e5!3m7!1s0x31da193257f33767:0x42996ddf16c716d7!8m2!3d1.3063739!4d103.8956192!9m1!1b1!15sCgtyZXN0YXVyYW50c1oNIgtyZXN0YXVyYW50c5IBCnJlc3RhdXJhbnQ"""
	restaurants["Volare"] = """https://www.google.com/maps/place/Volare/@1.3039398,103.8988077,15z/data=!4m12!1m3!2m2!1srestaurants!6e5!3m7!1s0x31da194d7e086cdb:0xe1acb2e426af4fa4!8m2!3d1.3043697!4d103.9021355!9m1!1b1!15sCgtyZXN0YXVyYW50c1oNIgtyZXN0YXVyYW50c5IBEml0YWxpYW5fcmVzdGF1cmFudA"""
	restaurants["La_Bonne_Table"] = """https://www.google.com/maps/place/la+bonne+table/@1.3039398,103.8988077,15z/data=!4m12!1m3!2m2!1srestaurants!6e5!3m7!1s0x31da19abe60e2c1f:0x159a2d5b905c3349!8m2!3d1.3073601!4d103.9072264!9m1!1b1!15sCgtyZXN0YXVyYW50c1oNIgtyZXN0YXVyYW50c5IBEWZyZW5jaF9yZXN0YXVyYW50"""
	restaurants["Danji_KBBQ"] = """https://www.google.com/maps/place/Danji+Korean+BBQ+Buffet/@1.3039398,103.8988077,15z/data=!4m12!1m3!2m2!1srestaurants!6e5!3m7!1s0x31da1814ddba393b:0xd3f2557c12654744!8m2!3d1.3085505!4d103.8945949!9m1!1b1!15sCgtyZXN0YXVyYW50c1oNIgtyZXN0YXVyYW50c5IBGmtvcmVhbl9iYXJiZWN1ZV9yZXN0YXVyYW50"""
	restaurants["Comida_Mexicana"] = """https://www.google.com/maps/place/Comida+Mexicana+Singapore/@1.3039398,103.8988077,15z/data=!4m12!1m3!2m2!1srestaurants!6e5!3m7!1s0x31da180ae6487617:0x777c2fa714016c!8m2!3d1.3087498!4d103.9120937!9m1!1b1!15sCgtyZXN0YXVyYW50c1oNIgtyZXN0YXVyYW50c5IBCnJlc3RhdXJhbnQ"""
	restaurants["Adda"] = """https://www.google.com/maps/place/ADDA/@1.2982514,103.8796023,15z/data=!4m7!3m6!1s0x31da19a537d5f015:0xcc8940ea7024154b!8m2!3d1.2997048!4d103.8599014!9m1!1b1"""
	restaurants["Poulet"] = """https://www.google.com/maps/place/Poulet/@1.3030972,103.8732638,15z/data=!3m1!5s0x31da18494cf47473:0xb825fcec56243f30!4m11!1m2!2m1!1sRestaurants!3m7!1s0x31da1849669a11e3:0x2bc845b400f37b01!8m2!3d1.3028821!4d103.8728563!9m1!1b1!15sCgtSZXN0YXVyYW50c1oNIgtyZXN0YXVyYW50c5IBEWZyZW5jaF9yZXN0YXVyYW50"""
	restaurants["ThaiVillage"] = """https://www.google.com/maps/place/Thai+Village+Restaurant/@1.3030972,103.8732638,15z/data=!4m11!1m2!2m1!1sRestaurants!3m7!1s0x31da184efe220581:0x321e166118cf1ac9!8m2!3d1.3001894!4d103.8747734!9m1!1b1!15sCgtSZXN0YXVyYW50c1oNIgtyZXN0YXVyYW50c5IBEmNoaW5lc2VfcmVzdGF1cmFudA"""
	restaurants["Joyden"] = """https://www.google.com/maps/place/Joyden+Seafood/@1.3030972,103.8732638,15z/data=!4m11!1m2!2m1!1sRestaurants!3m7!1s0x31da1a8d608e7479:0xc753fcdd433ed20d!8m2!3d1.3022164!4d103.8764421!9m1!1b1!15sCgtSZXN0YXVyYW50c1oNIgtyZXN0YXVyYW50c5IBEmNoaW5lc2VfcmVzdGF1cmFudA"""
	restaurants["LittleItaly"] = """https://www.google.com/maps/place/Little+Italy/@1.3030972,103.8732638,15z/data=!4m10!1m2!2m1!1sRestaurants!3m6!1s0x31da19ce3194573f:0x4aee6ce168247594!8m2!3d1.3168839!4d103.9023014!9m1!1b1"""
	restaurants["GracePot"] = """https://www.google.com/maps/place/Grace's+Pot+Indian+Restaurant/@1.4166094,103.8265544,14.5z/data=!4m12!1m3!2m2!1sRestaurants!6e5!3m7!1s0x31da147739b8013f:0x47eaa0851953c1c!8m2!3d1.428435!4d103.826622!9m1!1b1!15sCgtSZXN0YXVyYW50c1oNIgtyZXN0YXVyYW50c5IBCnJlc3RhdXJhbnQ"""
	restaurants["Tashas"] = """https://www.google.com/maps/place/Tasha's+Restaurant/@1.4044678,103.8068962,14z/data=!4m12!1m3!2m2!1sRestaurants!6e5!3m7!1s0x31da13ffeef195e1:0x9803ab68255afd7!8m2!3d1.4044684!4d103.819277!9m1!1b1!15sCgtSZXN0YXVyYW50c1oNIgtyZXN0YXVyYW50c5IBCnJlc3RhdXJhbnQ"""
	restaurants["WilderMann"] = """https://www.google.com/maps/place/Wilder+Mann/@1.4044678,103.8068962,14z/data=!4m12!1m3!2m2!1sRestaurants!6e5!3m7!1s0x31da11547d379e93:0xf592e6f8f27f51fa!8m2!3d1.3979628!4d103.8184532!9m1!1b1!15sCgtSZXN0YXVyYW50c1oNIgtyZXN0YXVyYW50c5IBEWdlcm1hbl9yZXN0YXVyYW50"""
	restaurants["Summerhouse"] = """https://www.google.com/maps/place/The+Summerhouse/@1.4044678,103.8068962,14z/data=!4m12!1m3!2m2!1sRestaurants!6e5!3m7!1s0x31da15d32c2cbafb:0x439659cc6b10a1c3!8m2!3d1.4079871!4d103.8683134!9m1!1b1!15sCgtSZXN0YXVyYW50c1oNIgtyZXN0YXVyYW50c5IBCnJlc3RhdXJhbnQ"""
	restaurants["MyHome"] = """https://www.google.com/maps/place/My+Home+Cafe,+Indonesian+Food/@1.4331801,103.8241321,14z/data=!4m17!1m9!3m8!1s0x31da15d32c2cbafb:0x439659cc6b10a1c3!2sThe+Summerhouse!8m2!3d1.4079871!4d103.8683134!9m1!1b1!15sCgtSZXN0YXVyYW50c1oNIgtyZXN0YXVyYW50c5IBCnJlc3RhdXJhbnQ!3m6!1s0x31da15552f14eb57:0x2a1e8218b5b9cc4!8m2!3d1.4331801!4d103.8416415!9m1!1b1"""
	restaurants["Brio"] = """https://www.google.com/maps/place/Brio/@1.3382098,103.6835069,14z/data=!4m11!1m2!2m1!1sRestaurants!3m7!1s0x31da0f932d4ab9c5:0x203757fc4d74d48f!8m2!3d1.3399361!4d103.7071702!9m1!1b1!15sCgtSZXN0YXVyYW50c1oNIgtyZXN0YXVyYW50c5IBCnJlc3RhdXJhbnQ"""
	restaurants["DTF"] = """https://www.google.com/maps/place/Din+Tai+Fung/@1.3393229,103.7048641,18.25z/data=!3m1!5s0x31da0feccd9a4093:0xd320a963d0ae2e88!4m11!1m2!2m1!1sRestaurants!3m7!1s0x31da0fecc42faecb:0xb1854616569aa862!8m2!3d1.3390568!4d103.7057767!9m1!1b1!15sCgtSZXN0YXVyYW50c1oNIgtyZXN0YXVyYW50c5IBFHRhaXdhbmVzZV9yZXN0YXVyYW50"""
	restaurants["Legendary"] = """https://www.google.com/maps/place/Legendary+Hong+Kong+Restaurant+%E6%B8%AF%E9%A3%B2%E6%B8%AF%E9%A3%9F%E9%A4%90%E5%BB%B3/@1.3397987,103.7060933,19.25z/data=!4m11!1m2!2m1!1sRestaurants!3m7!1s0x31da0f932e98c61d:0xe9ef409f45cc108e!8m2!3d1.3397443!4d103.7067297!9m1!1b1!15sCgtSZXN0YXVyYW50c1oNIgtyZXN0YXVyYW50c5IBJGhvbmdfa29uZ19zdHlsZV9mYXN0X2Zvb2RfcmVzdGF1cmFudA"""
	restaurants["Kotobuki"] = """https://www.google.com/maps/place/Kotobuki/@1.3255659,103.7245164,19z/data=!4m11!1m2!2m1!1sRestaurants!3m7!1s0x31da055595d5eb69:0xbb9a88abad2baa81!8m2!3d1.3256557!4d103.7249543!9m1!1b1!15sCgtSZXN0YXVyYW50c1oNIgtyZXN0YXVyYW50c5IBE2phcGFuZXNlX3Jlc3RhdXJhbnQ"""
	restaurants["VegetarianVillas"] = """https://www.google.com/maps/place/Vegetarian+Villas/@1.3471065,103.7239914,19z/data=!4m11!1m2!2m1!1sRestaurants!3m7!1s0x31da0fde31bf613f:0xcf36f3c18da7d98b!8m2!3d1.3471065!4d103.7245386!9m1!1b1!15sCgtSZXN0YXVyYW50c1oNIgtyZXN0YXVyYW50c5IBFXZlZ2V0YXJpYW5fcmVzdGF1cmFudA"""
	restaurants["WaCow"] = """https://www.google.com/maps/place/Waa+Cow!+NUS+U+Town/@1.3042642,103.7717364,17z/data=!4m12!1m3!2m2!1sRestaurants!6e5!3m7!1s0x31da1aff322c6f33:0x1daed4a590fe216c!8m2!3d1.3047299!4d103.7725536!9m1!1b1!15sCgtSZXN0YXVyYW50c1oNIgtyZXN0YXVyYW50c5IBCnJlc3RhdXJhbnQ"""
	restaurants["UdonDon"] = """https://www.google.com/maps/place/Waa+Cow!+NUS+U+Town/@1.3042642,103.7717364,17z/data=!4m12!1m3!2m2!1sRestaurants!6e5!3m7!1s0x31da1aff322c6f33:0x1daed4a590fe216c!8m2!3d1.3047299!4d103.7725536!9m1!1b1!15sCgtSZXN0YXVyYW50c1oNIgtyZXN0YXVyYW50c5IBCnJlc3RhdXJhbnQ"""
	restaurants["Sapore"] = """https://www.google.com/maps/place/Sapore+Italian+Restaurant/@1.3042642,103.7717364,17z/data=!4m12!1m3!2m2!1sRestaurants!6e5!3m7!1s0x31da1af5e92ec7ad:0xf8fb5e3cd94b8eb4!8m2!3d1.3042724!4d103.773897!9m1!1b1!15sCgtSZXN0YXVyYW50c1oNIgtyZXN0YXVyYW50c5IBEml0YWxpYW5fcmVzdGF1cmFudA"""
	restaurants["ReoyalsBistro"] = """https://www.google.com/maps/place/The+Royals+Cafe+(NUS)/@1.3042642,103.7717364,17z/data=!4m12!1m3!2m2!1sRestaurants!6e5!3m7!1s0x31da1af5e69f25e7:0x40eab761b3da1445!8m2!3d1.3039101!4d103.7738303!9m1!1b1!15sCgtSZXN0YXVyYW50c1oNIgtyZXN0YXVyYW50c5IBEGhhbGFsX3Jlc3RhdXJhbnQ"""
	restaurants["AlAmeen"] = """https://www.google.com/maps/place/Al+Aleem+Eating+Corner/@1.2924132,103.7683981,20.96z/data=!4m12!1m3!2m2!1sRestaurants!6e5!3m7!1s0x31da1afc37554c7b:0xed7ac30b37672f13!8m2!3d1.2924032!4d103.7683609!9m1!1b1!15sCgtSZXN0YXVyYW50c1oNIgtyZXN0YXVyYW50c5IBCnJlc3RhdXJhbnQ"""
	restaurants["Igokochi"] = """https://www.google.com/maps/place/Igokochi+Dining+Bar/@1.3101191,103.7534525,15.58z/data=!4m12!1m3!2m2!1sRestaurants!6e5!3m7!1s0x31da1b3d0f4ed0b3:0xabd21d8b2dd8cd20!8m2!3d1.3158284!4d103.7575711!9m1!1b1!15sCgtSZXN0YXVyYW50c1oNIgtyZXN0YXVyYW50c5IBCnJlc3RhdXJhbnQ"""
	restaurants["Rangooli"] = """https://www.google.com/maps/place/Rangooli+Restaurant/@1.3023122,103.7583872,15z/data=!4m12!1m3!2m2!1sRestaurants!6e5!3m7!1s0x31da1ba543665e57:0xdfac451f887a50be!8m2!3d1.3023124!4d103.7642302!9m1!1b1!15sCgtSZXN0YXVyYW50c1oNIgtyZXN0YXVyYW50c5IBEWluZGlhbl9yZXN0YXVyYW50"""
	restaurants["McD"] = """https://www.google.com/maps/place/McDonald's+West+Coast+Park/@1.2963971,103.7634395,16.54z/data=!4m11!1m3!2m2!1sRestaurants!6e5!3m6!1s0x31da1afc6e15924b:0x1282116999f0130f!8m2!3d1.2976211!4d103.7633918!9m1!1b1"""
	restaurants["Pietrasanta"] = """https://www.google.com/maps/place/Pietrasanta+The+Italian+Restaurant/@1.2973189,103.7847256,16.29z/data=!4m12!1m3!2m2!1sRestaurants!6e5!3m7!1s0x31da1a498159cea7:0x536fd14711fcb2!8m2!3d1.2986242!4d103.7879068!9m1!1b1!15sCgtSZXN0YXVyYW50c1oNIgtyZXN0YXVyYW50c5IBEml0YWxpYW5fcmVzdGF1cmFudA"""
	restaurants["roots"] = """https://www.google.com/maps/place/roots@onenorth+restaurant/@1.2995797,103.7867942,17.29z/data=!3m1!5s0x31da1a4549b75f71:0x3333a570ffc4dabc!4m12!1m3!2m2!1sRestaurants!6e5!3m7!1s0x31da1a45480d25e7:0x48b71c87cdcb56c0!8m2!3d1.2996794!4d103.78726!9m1!1b1!15sCgtSZXN0YXVyYW50c1oNIgtyZXN0YXVyYW50c5IBEndlc3Rlcm5fcmVzdGF1cmFudA"""



	output_df = pd.DataFrame();

	for i in restaurants.keys():
		print(i)
		retdf = scrape(restaurants[i])
		# retdf = process(retdf)
		retdf["Restaurant"] = str(i)
		output_df = output_df.append(retdf)

	output_df.to_csv("reg_scraped_output.csv", index=False)

	print(len(output_df))
	# driver.quit()

# if __name__ == '__main__':

# 	restaurants = dict()
# 	# restaurants["TFDB"] = """https://www.google.com/maps/place/25+Degrees+Burger,+Wine+%26+Liquor+Bar/@1.3007261,103.8516291,17z/data=!4m7!3m6!1s0x31da19bb7807cba3:0x76563778a023572a!8m2!3d1.3007127!4d103.8516181!9m1!1b1"""
# 	# restaurants["TR"] = """https://www.google.com/maps/place/Tiga+Roti/@1.4433247,103.8158846,17z/data=!4m7!3m6!1s0x31da136c330fbc5b:0xf56c97db1899a57e!8m2!3d1.4433247!4d103.8158846!9m1!1b1"""
# 	# restaurants["TMG"] = """https://www.google.com/maps/place/The+Market+Grill/@1.2799855,103.8471047,17z/data=!4m7!3m6!1s0x31da190d7b80291f:0x826105028950285c!8m2!3d1.2799757!4d103.8471269!9m1!1b1"""

	

# 	output_df = pd.DataFrame();

# 	for i in restaurants.keys():
# 		print(i)
# 		retdf = scrape(restaurants[i])
# 		retdf = process(retdf)
# 		retdf["Restaurant"] = str(i)
# 		output_df = output_df.append(retdf)

# 	output_df.to_csv("testing_scraped_output.csv")

# 	print(len(output_df))

