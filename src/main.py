from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup
from lxml import etree

# DRIVER_PATH = r'../chromedriver.exe'
# driver = webdriver.Chrome(executable_path=DRIVER_PATH)
url = 'https://uitspraken.rechtspraak.nl/inziendocument?id={0}'

ecli_file = open('../txt_files/ECLI_list.txt', 'r')
ecli_lines = ecli_file.readlines()

# driver.get(url.format(ecli_lines[0].strip()))

# print(url.format(ecli_lines[0].strip()))

count = 0
for ecli in ecli_lines:
    if count == 1:
        break
    count += 1
    response = requests.get(url.format(ecli_lines[count].strip()))
    content = response.content
    parser = BeautifulSoup(content, 'html.parser')
    body = parser.body
    producten = body.find(class_="uitspraak")
    if producten == None:
        Exception(ValueError)
    print(producten.prettify())


# response = requests.get(url.format(ecli_lines[0].strip()))
# content = response.content
# parser = BeautifulSoup(content, 'html.parser')
# body = parser.body
# producten = body.find(class_="uitspraak")
# print(producten.prettify())
