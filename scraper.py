import requests
import os
from bs4 import BeautifulSoup
import nltk
import pandas as pd
    
def scrape_text(self): # This function scrape the urls of the articles present on each page from the page urls
    texts= []
    for i in range(1, self.page_numbers):
        url = f'https://kissah.org/?page={i}'
        page = requests.get(url).text
        soup = BeautifulSoup(page, 'lxml')
        articles = soup.find_all('div', class_ = 'col')
        for article in articles:
            article_title = article.find('h5', class_ ='card-title pt-3')
            article_url = article_title.a['href']
            article_page = requests.get(article_url).text
            soup2 = BeautifulSoup(article_page, 'lxml')
            about_story = soup2.find('div', class_ = 'my-5')
            if about_story:
                about_story_text = about_story.p.text.strip().replace('-', '.')
                texts.append(about_story_text.replace('....','.'))
            story_div = soup2.find('div', class_ = 'px-4 kissah-taak')
            if story_div:
                story_text = story_div.text.strip().replace('۔', '.')
                texts.append(story_text.replace('....','.'))
    return texts

class SaveFile:

    def to_csv(file_path, texts):
        tokenized_paragraph = [nltk.sent_tokenize(text) for text in texts]
        sentences = []
        for paragraph in tokenized_paragraph:
            for sent in paragraph:
                sentences.append(sent)
        df = pd.DataFrame(data=sentences, columns=['Sentences'])
        df.to_csv(file_path)

    def to_excel(file_path, texts):
        tokenized_paragraph = [nltk.sent_tokenize(text) for text in texts]
        sentences = []
        for paragraph in tokenized_paragraph:
            for sent in paragraph:
                sentences.append(sent)
        df = pd.DataFrame(data=sentences, columns=['Sentences'])
        df.to_excel(file_path,)

    def to_txt(file_path, texts):
        tokenized_paragraphs = [nltk.sent_tokenize(text) for text in texts]

        with open(file_path, 'a', encoding='utf-8') as f:
            for paragraph in tokenized_paragraphs:
                for sent in paragraph:
                    f.write(sent)


if __name__ == "__main__":
    try:
        texts = scrape_text()
        SaveFile.to_txt('Scraped_Files/BalochiText.txt', texts=texts)
        print('===========Done! Successfully completed the scraping===========')
    except:
        print("You have an internet issue")