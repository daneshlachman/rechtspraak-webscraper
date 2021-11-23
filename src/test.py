import requests
from bs4 import BeautifulSoup

producten_alle_paginas = []

for i in range(1, 15):
    response = requests.get(f"https://www.bol.com/nl/s/?page={i}&searchtext=hand+sanitizer&view=list")
    content = response.content
    parser = BeautifulSoup(content, 'html.parser')
    body = parser.body
    producten = body.find_all(class_="product-item--row js_item_root")
    producten_alle_paginas.extend(producten)

len(producten_alle_paginas)