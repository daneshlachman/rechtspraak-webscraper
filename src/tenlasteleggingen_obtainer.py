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
                        'vrijspraak van het primair ten laste gelegde', 'tenlasteleggingen', 'De tenlastelegging.',]

list_of_not_valuable_string = 'Aan de verdachte is ten laste gelegd dat: De verdachte is ten laste gelegd dat: ' \
                              'De tenlastelegging is als bijlage aan dit vonnis gehecht. De gewijzigde tenlastelegging' \
                              ' is als bijlage aan dit vonnis gehecht. Aan verdachte is ten laste gelegd dat: Aan verdachte' \
                              ' is, na wijziging van de tenlastelegging, ten laste gelegd dat: Aan verdachte is tenlastegelegd dat: De ' \
                              'verdenking komt er, kort en feitelijk weergegeven, op neer dat de verdachte:'

bijlage_list = ['bijlage', 'Bijlage']

list_of_not_valuable_string = list_of_not_valuable_string.lower()

# read all possible headers in a string
with open('../txt_files/header_list.txt') as f:
    all_headers_string = f.read()

# create a list of uitspraken to append every uitspraak to
list_of_uitspraken = []

# get all tenlasteleggingen
count = 0
for ecli in ecli_lines:
    # ecli = 'ECLI:NL:RBGEL:2020:6212'
    # if count > 1:
    #     break
    header_text = ''
    # retrieve uitspraak
    response = requests.get(url.format(ecli_lines[count].strip()))
    # response = requests.get(url.format('ECLI:NL:RBGEL:2020:6212'))
    content = response.content
    parser = BeautifulSoup(content, 'html.parser')
    body = parser.body
    uitspraak = body.find(class_="uitspraak")

    # do some preprocessing to recognize the headers effectively, and append tenlastelegging text
    # to a string until a header is encountered
    try:
        spraaktest = [line for line in uitspraak.text.split('\n') if line.strip() != '']
        in_header = False
        for line in spraaktest:
            line = line.strip().lstrip("1234567890 .\t")
            # pdb.set_trace()
            if line == '':
                continue
            if line in all_headers_string and in_header:
                break
            if line.lower() in tenlastelegging_list:
                in_header = True
                continue
            if in_header:
                if line.lower() not in list_of_not_valuable_string:
                    header_text += line

        # if tenlastelegging text refers to the bijlage, then the text
        # should be retrieved somewhere else or partially ignored
        # if 'bijlage' in header_text or 'Bijlage' in header_text:
        #     header_text = ''

        print(ecli)
        print(header_text)
        list_of_uitspraken.append([ecli.strip(), header_text])
    except ValueError:
        print("something wrong with uitspraak")
    count += 1

# write list of ecli and uitspraken to csv file
uitspraken_dataframe = pd.DataFrame(data=list_of_uitspraken)
uitspraken_dataframe.to_csv(header=['ecli', 'uitspraak'], path_or_buf='../txt_files/uitspraken.csv')