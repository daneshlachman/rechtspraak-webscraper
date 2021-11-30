import pdb

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup
from lxml import etree

# DRIVER_PATH = r'C:\Users\danes\PycharmProjects\web_scraper\chromedriver.exe'
# driver = webdriver.Chrome(executable_path=DRIVER_PATH)
url = 'https://uitspraken.rechtspraak.nl/inziendocument?id={0}'

ecli_file = open(r'C:\Users\danes\PycharmProjects\web_scraper\ECLI_list.txt', 'r')
ecli_lines = ecli_file.readlines()


header_set = set()
count = 0
for ecli in ecli_lines:
    if count > 2640:
        break
    count += 1
    response = requests.get(url.format(ecli_lines[count].strip()))
    content = response.content
    parser = BeautifulSoup(content, 'html.parser')
    body = parser.body
    h2_element = body.find_all('h2')
    for header in h2_element[2:]:
        processces_header = header.text.strip().lstrip("1234567890 ")
        header_set.add(processces_header)


# read ECLI codes, and write them to ECLI_list.txt
text_file = open(r"C:\Users\danes\PycharmProjects\web_scraper\header_list.txt", "w")
for element in list(header_set):
    text_file.write(element + "\n")
text_file.close()

print(header_set)





# response = requests.get(url.format(ecli_lines[0].strip()))
# content = response.content
# parser = BeautifulSoup(content, 'html.parser')
# body = parser.body
# producten = body.find(class_="uitspraak")
# print(producten.prettify())
