from scraper import Scraper
from selenium.common.exceptions import NoSuchElementException
from collections import Counter

if __name__ == '__main__':
    scrapzin = Scraper()
    for url in scrapzin.get_urls_jobs('Python', 12):  # Put the type of vacancy and the number of pages that will be analyzed here
        try:
            scrapzin.get_competences(url)
        except NoSuchElementException:
            continue

    contagem = dict(Counter(scrapzin.competences))
    contagem = sorted(contagem.items(), key=lambda item: item[1], reverse=True)

    for competence in contagem:
        print(f'{competence[1]}x -> {competence[0]}')
