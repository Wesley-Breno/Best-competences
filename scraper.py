from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome

from bs4 import BeautifulSoup
from random import randint
from time import sleep


class Scraper:
    def __init__(self):
        self._mail = 'rorakel890@vikinoko.com'
        self._pass = 'senha123'
        self.competences = []
        self.session = self._prepare_session()

    def _prepare_session(self) -> WebDriver:
        """
        Login in the account of Linkedin
        :return: Session of Selenium Webdriver
        """
        session = Chrome()
        session.get('https://www.linkedin.com/')
        sleep(2)
        session.refresh()
        sleep(randint(6, 12))
        session.find_element(By.NAME, 'session_key').send_keys(self._mail)
        sleep(randint(6, 12))
        session.find_element(By.NAME, 'session_password').send_keys(self._pass)
        sleep(randint(6, 12))
        session.find_element(By.XPATH, '/html/body/main/section[1]/div/div/form/div[2]/button').click()
        sleep(60)

        return session

    def get_urls_jobs(self, job: str, total_pages: int) -> list:
        """
        Searches for a specific type of vacancy, accesses pages containing that type of vacancy and returns the links of
        each vacancy found.
        :param job: Type of job waited
        :param total_pages: Total pages to be scraped
        :return: List contains urls of vacancys
        """
        nonduplicate_urls = set()
        unformated_url = 'https://www.linkedin.com/jobs/search/?currentJobId=3694278070&keywords=$&refresh=true&start='
        formated_url = unformated_url.replace('$', job)
        formated_url = formated_url.replace(' ', '%20')

        self.session.get(formated_url)

        for page in range(0, total_pages):
            self.session.get(formated_url + str(page * 25))
            sleep(randint(6, 12))
            html = BeautifulSoup(self.session.page_source, 'html.parser')

            scraped_urls = html.find_all('a')
            for link in scraped_urls:
                if str(link.get('href')).startswith('/jobs/view/'):
                    nonduplicate_urls.add('https://www.linkedin.com' + link.get('href'))

        return list(nonduplicate_urls)

    def get_competences(self, url_job: str):
        """
        Acessing vacancy and getting the competences.
        :param url_job: Url of vacancy
        :return: None
        """
        self.session.get(url_job)
        sleep(randint(6, 12))
        try:
            self.session.find_element(By.CSS_SELECTOR, 'body > div.application-outlet > div.authentication-outlet > div > div.job-view-layout.jobs-details > div.grid > div > div:nth-child(1) > div > div > div.p5 > div.mt5.mb2 > ul > li:nth-child(4) > button').click()
        except StaleElementReferenceException:
            ...
        else:
            sleep(randint(6, 12))
            html = BeautifulSoup(self.session.page_source, 'html.parser')
            for competencia in html.select('.job-details-skill-match-status-list__unmatched-skill.text-body-small'):
                self.competences.append(competencia.text.strip().replace('Adicionar', '').replace('\n', ''))


__all__ = ['Scraper']
