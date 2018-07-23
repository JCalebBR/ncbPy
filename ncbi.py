import argparse

import tqdm
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys

class ExtractData:

    def start(self, url):
        ID = lambda x: x and x.startswith(url)

        browser_pbar = tqdm.tqdm(total=100)

        Ooptions = Options()
        Ooptions.add_argument('-headless')
        browser_pbar.update(25)

        browser = webdriver.Firefox(executable_path='geckodriver', firefox_options=Ooptions)
        browser_pbar.update(25)

        browser.get('https://www.ncbi.nlm.nih.gov/nuccore/' + url)
        source = browser.page_source
        browser_pbar.update(25)
        browser.close()
        browser_pbar.update(25)
        browser_pbar.close()
        return self.findText(ID, source)

    def search(self, search):
        browser_pbar = tqdm.tqdm(total=100)

        Ooptions = Options()
        Ooptions.add_argument('-headless')
        browser_pbar.update(25)

        browser = webdriver.Firefox(executable_path='geckodriver', firefox_options=Ooptions)
        browser_pbar.update(25)

        browser.get('https://www.ncbi.nlm.nih.gov/nuccore/?term=' + search)
        source = browser.page_source
        browser_pbar.update(25)
        browser.close()
        browser_pbar.update(25)
        browser_pbar.close()
        return self.findSearch(source)

    def findText(self, ID, page_source):
        soup = BeautifulSoup(page_source, 'html.parser')
        foundText = soup.find_all('', id=ID)
        source_pbar = tqdm.tqdm(total=len(foundText))
        for span in foundText:
            source_pbar.update(1)

            print(span.text)
        source_pbar.close()

    def findSearch(self, page_source):
        soup = BeautifulSoup(page_source, 'html.parser')
        foundText = soup.find_all('div', class_='rslt')
        source_pbar = tqdm.tqdm(total=len(foundText))
        num = 1
        for div in foundText:
            source_pbar.update(1)
            print("{0}. ".format(num) + div.text)
            num+=1
        source_pbar.close()
        result = int(input("Choose your result: "))
        foundResult = foundText[result-1]
        return self.findLinkInResult(foundResult)

    def findLinkInResult(self, result):
        soup = result
        foundLink = soup.find('a')['href']
        foundLink = foundLink.replace('/nuccore/', '')
        return self.start(foundLink)


parser = argparse.ArgumentParser()
parser.add_argument('-s', '--search', help='Insert search parameter')
args = parser.parse_args()

if __name__ == '__main__':
    ExtractData().search(args.search)
