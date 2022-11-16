import requests
from bs4 import BeautifulSoup
import csv

links = {"NOVEL": "https://en.wikipedia.org/wiki/Hugo_Award_for_Best_Novel",
         "NOVELLA": "https://en.wikipedia.org/wiki/Hugo_Award_for_Best_Novella",
         "NOVELETTE": "https://en.wikipedia.org/wiki/Hugo_Award_for_Best_Novelette",
         "SHORT STORY": "https://en.wikipedia.org/wiki/Hugo_Award_for_Best_Short_Story"}

for key in links:
    info = requests.get(links[key])
    text = info.text

    soup = BeautifulSoup(text, 'html.parser')
    rows = soup.find_all('tr')

    names = []
    for i in rows:
        names.append(i.getText().split('\n'))

    for i in names:
        while '' in i:
            i.remove('')

    for index, item in enumerate(names):
        if len(item) == 1:
            names[index - 1].insert(2, item[0])
            names.remove(item)

        if len(item) == 4:
            item.insert(0, names[index - 1][0])

    for i in names:
        del i[-1:]

    del names[-8:]

    clean = []
    for x in names:
        year = list(i.replace('[c]', '').replace('[e]', '').replace('[f]', '').replace('[d]', '').replace('"', '')
                    .replace('[a', '').replace('[note 1]', '').replace('[note 2]', '')
                    for i in x)
        clean.append(year)

    for i in clean:
        if len(i) == 5:
            i[1] += ' & ' + i[2]
            del i[2]

    del clean[0:4]

    with open(f'HAW({key}).csv', 'w', encoding="utf-8") as doc:
        write = csv.writer(doc)
        write.writerows(clean)
