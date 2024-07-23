import requests
from bs4 import BeautifulSoup

mi_doc = requests.get("https://python.beispiel.programmierenlernen.io/index.php")

doc_final=BeautifulSoup(mi_doc.text,"html.parser")

for cuerpoTexto in doc_final.select (".card-text"):
    print (cuerpoTexto.text)
    print ("")


for imagen in doc_final.select (".card-block img"):
    print (imagen.attrs["src"])
    print ("")