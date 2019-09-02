from selenium import webdriver
import csv
from time import sleep

options = webdriver.ChromeOptions()
prefs = {'profile.managed_default_content_settings.images': 2}
options.add_experimental_option("prefs", prefs)
options.add_argument("--window-size=1920,1080")
options.add_argument("--start-maximized")
options.add_argument("--headless")
options.add_argument("--log-level=3")
driver = webdriver.Chrome(chrome_options=options)

outputList = []

file = open('input.csv', 'r+')
readFile = csv.reader(file)
for row in readFile:
    if readFile.line_num == 1:
        continue 
    dit = row[3].replace(' ', '-')
    link = f'https://fastpeoplesearch.com/name/{row[0].lower()}-{row[2].lower()}_{dit.lower()}-{row[4].lower()}'
    mid_link = f'https://fastpeoplesearch.com/name/{row[0].lower()}-{row[1].lower()}-{row[2].lower()}_{dit.lower()}-{row[4].lower()}'

    driver.get(link if row[1] == "" else mid_link)
    driver.find_elements_by_xpath("//span[@class='larger']")[0].click()
    sleep(0.5)
    addresses = driver.find_elements_by_xpath("//a[@title='Search other people associated with this address']")   
    de = [add.text for add in addresses]
    newRow = [row[0], row[1], row[2], row[3], row[4], " ".join(de)]
    outputList.append(newRow)
file.close()
# Final file
file2 = open("output.csv", 'w+', newline="")
writer = csv.writer(file2)
writer.writerow(['first name','MiddleName','Last Name','City','State','Addresses'])
writer.writerows(outputList)
file2.close()
driver.quit()