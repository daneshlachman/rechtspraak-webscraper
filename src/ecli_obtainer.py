from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pdb

DRIVER_PATH = r'chromedriver.exe'
driver = webdriver.Chrome(executable_path=DRIVER_PATH)
driver.get('https://uitspraken.rechtspraak.nl/#zoekverfijn/zt[0][zt]=winkeldiefstal&zt[0]'
           '[fi]=&zt[0][ft]=Alle+velden&idx=1&so=Relevance')

list_of_ECLI = []


# parse ecli-code from the string in the webelement
def ecli_parser(ECLI_string):
    parsed_string = ''
    for character in ECLI_string:
        if character == ' ':
            break
        else:
            parsed_string += character
    return parsed_string


number_of_results = driver.find_element(By.XPATH,'//*[@id="content"]/div/div[2]/div[1]/h2/span/span').text

i = 1
counter = 1

# loop through all of the cases, and append the ECLI-codes to a list
for x in range(int(number_of_results)):
    if counter % 10 == 0:
        driver.find_element(By.XPATH, '//*[@id="laadmeer"]').click()
    search_result_element = driver.find_element(By.XPATH,'//*[@id="zoekresultaatregion"]/div/div[{0}]/div[1]/h3/a'.format(i))
    list_of_ECLI.append(ecli_parser(search_result_element.text))
    driver.implicitly_wait(3)
    i += 1
    counter += 1

pdb.set_trace()

# read ECLI codes, and write them to ECLI_list.txt
text_file = open("./ECLI_list.txt", "w")
for element in list_of_ECLI:
    text_file.write(element + "\n")
text_file.close()
driver.quit()
