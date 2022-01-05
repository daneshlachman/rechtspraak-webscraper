import requests
from bs4 import BeautifulSoup
import io
import jellyfish
import pdb
import time
import pandas as pd

# DRIVER_PATH = r'../chromedriver.exe'
# driver = webdriver.Chrome(executable_path=DRIVER_PATH)
url = 'https://uitspraken.rechtspraak.nl/inziendocument?id={0}'

ecli_file = open('../txt_files/ECLI_list.txt', 'r')
ecli_lines = ecli_file.readlines()

tenlastelegging_list = ['inleiding en tenlastelegging', 'vrijspraak primair ten laste gelegde',
                        'ten aanzien van de tenlastelegging', 'tekst tenlastelegging',
                        'tekst gewijzigde tenlastelegging', 'tenlastelegging', 'tenlasteleggingen',
                        'de tenlastelegging', 'inhoud van de tenlastelegging', 'tekst tenlasteleggingen',
                        'de inhoud van de tenlastelegging', 'de tenlasteleggingen',
                        'vrijspraak van het primair ten laste gelegde', 'tenlasteleggingen']


# read all possible headers in a string
with open('../txt_files/header_list.txt') as f:
    all_headers_string = f.read()

# create a list of uitspraken to append every uitspraak to
list_of_uitspraken = []

# get all tenlasteleggingen
count = 0
for ecli in ecli_lines:
    header_text = ''
    # retrieve uitspraak
    response = requests.get(url.format(ecli_lines[count].strip()))
    # response = requests.get(url.format('ECLI:NL:RBNNE:2013:1780'))
    content = response.content
    parser = BeautifulSoup(content, 'html.parser')
    body = parser.body
    uitspraak = body.find(class_="uitspraak")
    try:
        spraaktest = [line for line in uitspraak.text.split('\n') if line.strip() != '']
        in_header = False
        for line in spraaktest:
            line = line.strip().lstrip("1234567890 .")
            if line == '':
                continue
            if line in all_headers_string and in_header:
                break
            if line.lower() in tenlastelegging_list:
                in_header = True
                continue
            if in_header:
                header_text += line
        # print(ecli)
        # print(header_text)
        list_of_uitspraken.append([ecli.strip(), header_text])
    except ValueError:
        print("something wrong with uitspraak")
    count += 1

# write list of ecli and uitspraken to csv file
uitspraken_dataframe = pd.DataFrame(data=list_of_uitspraken)
uitspraken_dataframe.to_csv(header=['ecli', 'uitspraak'], path_or_buf='../txt_files/uitspraken.csv')