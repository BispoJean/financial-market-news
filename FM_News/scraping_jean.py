import requests
from bs4 import BeautifulSoup

class Site:
    def __init__(self, site):
        self.site = site
        self.news = []
        self.sites_todos = ["Yahoo Finance",
                            "Forbes",
                            "Financial Times",
                            "Investing.com"]
    
    def update_news(self):
        '''Lê o site e entende o que é uma notícia e o que não é.'''
        
        if self.site == self.sites_todos[0]:
            url = 'https://finance.yahoo.com/'
            browsers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \(KHTML, like Gecko) Chrome / 86.0.4240.198Safari / 537.36"}
            page = requests.get(url, headers= browsers)
            
            resposta = page.text
            soup = BeautifulSoup(resposta, 'html.parser')
            
            noticias = soup.find_all('a')
            
            tg_class1 = 'subtle-link fin-size-small titles noUnderline yf-1xqzjha'
            tg_class2 = 'subtle-link fin-size-small titles basis-without-img noUndrline yf-1xqzjha'
            
            news_dict_yfinance = {}
            for noticia in noticias:
                if noticia.h3 != None:
                    if tg_class2 or tg_class1 in noticia.h3.get("class"):
                        news_dict_yfinance[noticia.h3.text] = noticia.get('href')
            
            self.news = news_dict_yfinance
            
        if self.site == self.sites_todos[1]:
            url = "https://www.forbes.com/markets/"
            browsers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \(KHTML, like Gecko) Chrome / 86.0.4240.198Safari / 537.36"}
            page = requests.get(url, headers= browsers)
            
            resposta = page.text
            soup = BeautifulSoup(resposta, 'html.parser')
            
            noticias_a = soup.find_all("a")
            
            a_tg_class1 = "zEzPL6aA"
            
            news_dict_forbes = {}
            
            for noticia in noticias_a:
                if noticia.h2 != None:
                    if a_tg_class1 in noticia.get("class"):
                        news_dict_forbes[noticia.h2.text] = noticia.get('href')
                        
            noticias_h3 = soup.find_all("h3")

            h3_tg_class1 = "HNChVRGc"
            a_tg_class2 = "_1-FLFW4R"
            
            for noticia in noticias_h3:
                if h3_tg_class1 in noticia.get("class"):
                    if a_tg_class2 in noticia.a.get("class"):
                        news_dict_forbes[noticia.a.text] = noticia.a.get('href')

            self.news = news_dict_forbes
            
        if self.site == self.sites_todos[2]:
            url = "https://ft.com/markets"
            browsers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \(KHTML, like Gecko) Chrome / 86.0.4240.198Safari / 537.36"}
            page = requests.get(url, headers= browsers)
            
            resposta = page.text
            soup = BeautifulSoup(resposta, 'html.parser')
            
            noticias = soup.find_all("div")
            
            div_tg_class = "o-teaser__heading"
            
            news_dict_ft = {}

            for noticia in noticias:
                noticia_classes = noticia.get("class", [])
                if div_tg_class in noticia_classes:
                    news_dict_ft[noticia.get_text()] = noticia.a.get('href')
            
            links_corretos = []
            
            for link in news_dict_ft.values():
                if link.startswith("/content/"):
                    links_corretos.append("https://www.ft.com" + link)
                else:
                    links_corretos.append(link)
                    
            news_dict_ft = dict(zip(news_dict_ft.keys(), links_corretos))

            self.news = news_dict_ft
        
        if self.site == self.sites_todos[3]:
            url = "https://www.investing.com/news/stock-market-news"
            browsers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \(KHTML, like Gecko) Chrome / 86.0.4240.198Safari / 537.36"}
            page = requests.get(url, headers= browsers)
            
            resposta = page.text
            soup = BeautifulSoup(resposta, 'html.parser')
            
            noticias = soup.find_all("div")
            
            div_tg_class = "news-analysis-v2_content__z0iLP w-full text-xs sm:flex-1"
            
            news_dict_investing = {}
            
            for noticia in noticias:
                noticia_classes = noticia.get("class", [])
                # Verificar se a string inteira da classe está presente
                if div_tg_class in " ".join(noticia_classes):
                    link_element = noticia.find('a')
                    if link_element and link_element.get('href'):
                        news_dict_investing[noticia.a.get_text(strip=True)] = link_element.get('href')
            
            self.news = news_dict_investing