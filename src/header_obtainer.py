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

ecli_file = open(r'../txt_files/ECLI_list.txt', 'r')
ecli_lines = ecli_file.readlines()

number_of_results = 2600
header_set = set()


def header_processor(header):
    pre_processed_header = header.text.strip().lstrip("1234567890 .")
    if not len(pre_processed_header) > 45 and not len(pre_processed_header) < 6:
        if "[" not in pre_processed_header and "]" not in pre_processed_header:
            if pre_processed_header:
                if "[…]" not in pre_processed_header:
                    if any(char.isalpha() for char in pre_processed_header):
                        header_set.add(pre_processed_header)


count = 0
for ecli in ecli_lines:
    print(ecli + " " + str(count))
    if count == 2600:
        break
    count += 1
    response = requests.get(url.format(ecli_lines[count].strip()))
    content = response.content
    parser = BeautifulSoup(content, 'html.parser')
    body = parser.body
    h2_element = body.find_all('h2')
    for raw_header in h2_element[2:]:
        header_processor(raw_header)


# read ECLI codes, and write them to ECLI_list.txt
text_file = open(r"../txt_files/header_list.txt", "w")
for element in list(header_set):
    text_file.write(element + "\n")
text_file.close()

print(header_set)