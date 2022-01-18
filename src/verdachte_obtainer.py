import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://uitspraken.rechtspraak.nl/inziendocument?id={0}'

ecli_file = open('../txt_files/ECLI_list.txt', 'r')
ecli_lines = ecli_file.readlines()

instantie_xpath = '//*[@id="Main"]/div[2]/dl/dd[1]/span'

verdachtes_list = ['[verdachte] ,', '[verdachte]', 'verdachte', '[Verdachte] ,', '[verdachte],',
                   '[naam verdachte] ,', '[naam verdachte],', '[naam verdachte]']

# read all possible headers in a string
with open('../txt_files/header_list.txt') as f:
    all_headers_string = f.read()

# create a list of uitspraken to append every uitspraak to
list_of_verdachtes = []

# get all verdachtes
count = 0
for ecli in ecli_lines:
    # ecli = 'ECLI:NL:RBROT:2019:10756'
    # if count > 5:
    #     break
    header_text = ''
    # retrieve uitspraak
    response = requests.get(url.format(ecli_lines[count].strip()))
    # response = requests.get(url.format('ECLI:NL:RBROT:2019:10756'))
    content = response.content
    parser = BeautifulSoup(content, 'html.parser')
    body = parser.body
    uitspraak = body.find(class_="uitspraak")


    # get the headers of the uitspraak
    head = body.find(class_="dl-horizontal")

    # get the datum uitspraak
    date_raw = head.find_all('dd')[1]
    date = date_raw.get_text()

    # do some preprocessing to recognize the headers effectively, and append verdachten text
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
                if line != ',':
                    break
            if line in verdachtes_list:
                in_header = True
                continue
                # if line resides in header, append text to the string
            if in_header:
                # add a whitespace at the end of a line so that words are not literally concatenated
                if header_text != '':
                    if header_text[-1] != ' ':
                        header_text += ' '
                header_text += line

        print(ecli)
        print(header_text)
        list_of_verdachtes.append([ecli.strip(), date, header_text])
    except ValueError:
        print("something wrong with uitspraak")
    count += 1

# write to csv file
uitspraken_dataframe = pd.DataFrame(data=list_of_verdachtes)
uitspraken_dataframe.to_csv(header=['ECLI', 'Datum', 'verdachte'],
                            path_or_buf='../txt_files/verdachte_text.csv')