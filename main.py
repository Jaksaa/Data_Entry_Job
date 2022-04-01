import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

TO_SEARCH = "San Francisco"
PRICE = "3000"

chrome_driver_path = "C:\Development\chromedriver.exe"
driver = webdriver.Chrome(executable_path=chrome_driver_path)

driver.get("https://www.zillow.com/")
driver.implicitly_wait(3)

time.sleep(3)
search_bar = driver.find_element(by=By.ID, value="search-box-input").send_keys(TO_SEARCH, Keys.ENTER)

#### APPLY FILTERS ######

rent_filter = driver.find_element(by=By.ID, value=("listing-type")).click()
time.sleep(2)
is_for_rent = driver.find_element(by=By.ID, value=("isForRent")).click()
time.sleep(2)
done_button = driver.find_element(by=By.XPATH, value=("/html/body/div[1]/div[5]/div/section/div[2]/div/div[1]/div/div/div/button")).click()
time.sleep(2)

price_filter = driver.find_element(by=By.ID, value=("price")).click()
time.sleep(2)
price_max = driver.find_element(by=By.ID, value=("price-exposed-max")).click()
time.sleep(2)
input_price_max = driver.find_element(by=By.ID, value=("price-exposed-max")).send_keys(PRICE)
time.sleep(2)
done_button_1 = driver.find_element(by=By.XPATH, value=("/html/body/div[1]/div[5]/div/section/div[2]/div/div[2]/div/div/div/button")).click()
time.sleep(2)

beds_filter = driver.find_element(by=By.ID, value=("beds")).click()
time.sleep(2)
num_beds = driver.find_element(by=By.XPATH, value=("/html/body/div[1]/div[5]/div/section/div[2]/div/div[3]/div/div/form/fieldset[1]/div[1]/button[2]")).click()
time.sleep(2)
done_button_2 = driver.find_element(by=By.XPATH, value=("/html/body/div[1]/div[5]/div/section/div[2]/div/div[3]/div/div/div/button")).click()
time.sleep(2)

element = driver.find_element(by=By.XPATH, value=('/html/body/div[1]/div[5]/div/div/div[1]/div[1]/div[3]/nav/ul/li[2]/a'))
driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth'});", element)

#### SCRAP FIRST PAGE #######

website = driver.page_source

soup = BeautifulSoup(website, 'lxml')

apartments_info = soup.find_all("div", class_="list-card-info")

links = []
addresses = []
prices = []

for info in apartments_info:
    link = info.find_all("a", href=True)
    address = info.find_all("address", class_="list-card-addr")
    price = info.find_all("div", class_="list-card-price")
    for a in link:
        links.append(a['href'])
    for addr in address:
        addresses.append(addr.text)
    for cost in price:
        prices.append(cost.text)
driver.close()

####### OPEN PAGE WITH PREDEFINE FORM ######

driver.get("https://docs.google.com/forms/d/e/1FAIpQLScJK0UCCjhghSbGMvacURsJa9RnCFblDY4t5Az9Brjf6DGgHQ/viewform?usp=sf_link")

if len(links) == len(addresses) == len(prices):
    for i in range(len(links)):
        addr_input = driver.find_element(by=By.XPATH, value=("/html/body/div/div[3]/form/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input")).send_keys(addresses[i])
        rent_input = driver.find_element(by=By.XPATH, value=("/html/body/div/div[3]/form/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input")).send_keys(prices[i])
        link_input = driver.find_element(by=By.XPATH, value=("/html/body/div/div[3]/form/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input")).send_keys(prices[i])
        send = driver.find_element(by=By.XPATH, value=("/html/body/div/div[3]/form/div[2]/div/div[3]/div[1]/div[1]/div")).click()
        time.sleep(3)
        send_another = driver.find_element(by=By.XPATH, value=("/html/body/div[1]/div[2]/div[1]/div/div[4]/a")).click()
driver.close()

driver.get("https://docs.google.com/forms/d/1uK6fate025YX3e5R5WuWOBihsHjWWExcSXs7AvEkpUk/edit#responses")
create_sheet = driver.find_element(by=By.XPATH, value=("/html/body/div[2]/div[2]/div[1]/div[2]/div/div[1]/div[1]/div[2]/div[1]/div/div")).click()
time.sleep(60)

driver.quit()