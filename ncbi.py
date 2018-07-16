import argparse

import tqdm
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

class ExtractData:

    def start(self, url, ID):
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

    def findText(self, ID, page_source):
        soup = BeautifulSoup(page_source, 'html.parser')
        foundText = soup.find_all('', id=ID)
        source_pbar = tqdm.tqdm(total=len(foundText))
        for span in foundText:
            source_pbar.update(1)
            print(span.text)
        source_pbar.close()

parser = argparse.ArgumentParser()
parser.add_argument('-id', '--sample_id', help='Sample ID (example: https://www.ncbi.nlm.nih.gov/nuccore/YOUR.SAMPLE.ID)')
args = parser.parse_args()

if __name__ == '__main__':
    expression = lambda x: x and x.startswith(args.sample_id)
    ExtractData().start(args.sample_id, expression)
