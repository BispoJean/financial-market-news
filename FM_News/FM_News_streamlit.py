import sys
import os
from threading import Thread
from datetime import datetime
import pickle
import webbrowser
from math import ceil
import streamlit as st
import time
from streamlit import session_state

# Para rodar: streamlit run "c:/Users/jeana/github_projects/FM_News/FM_News_streamlit.py"
# Adicionar o diretório ao sys.path
caminho_arquivo = r'C:/Users/jeana/github_projects/FM_News/'
sys.path.append(caminho_arquivo)

# Agora você pode importar o módulo
from scraping_jean import *

os.chdir("C:/Users/jeana/github_projects/FM_News")

class JeanNews:
    def __init__(self):
        self.dict_site = {}
        self.sites_todos = ["Yahoo Finance",
                            "Forbes",
                            "Financial Times",
                            "Investing.com"]
        if "page" not in st.session_state: 
            st.session_state.page = 1
        
        self.news = self._read_file("news") if "news" in os.listdir() else []
        self._update_file(self.news, 'news')
        self.sites = self._read_file("sites") if "sites" in os.listdir() else []
        self._update_file(self.sites, 'sites')
        
        for site in self.sites_todos:
            self.dict_site[site] = Site(site)
        
    def _update_file(self, lista, mode="news"):
        with open(mode, "wb") as fp:
            pickle.dump(lista, fp)
    
    def _read_file(self, mode="news"):
        try:
            with open(mode, "rb") as fp:
                n_list = pickle.load(fp)
                return n_list
        except (EOFError, pickle.UnpicklingError):
            return []
    
    def display_news(self):
        st.write(f"Last update: {datetime.now().strftime('%b %d, %Y | %I:%M:%S %p')}")
        
        self.filtered_news = [i for i in self.news if i["fonte"] in self.sites]
        self.max_page = ceil(len(self.filtered_news) / 10)
        
        if st.session_state.page > self.max_page: st.session_state.page = 1        
        
        aux_const = (st.session_state.page-1)*10
        for i, artigo in enumerate(self.filtered_news[aux_const:aux_const+10]):
            news_number = aux_const + i + 1
            st.markdown(f"[{news_number}. {artigo['data'].strftime('%b %d, %Y | %I:%M:%S %p')} - {artigo['fonte'].upper()} - {artigo['materia']}]({artigo['link']})")
            
        col1, col2, col3, col4, col5 = st.columns(5) 
        with col1:
            if st.button("First Page"):
                st.session_state.page = 1
        
        with col2:
            if st.button("Previous Page"): 
                if st.session_state.page > 1: 
                    st.session_state.page -= 1 
        
        with col3: 
            if st.button("Next Page"): 
                if st.session_state.page < self.max_page: 
                    st.session_state.page += 1

        with col4:
            if st.button("Last Page"):
                st.session_state.page = self.max_page
                
        with col5:
            st.write(f'Page {st.session_state.page}/{self.max_page}')

    def update_news(self):
        for site in self.sites_todos:
            self.dict_site[site].update_news()
            
            for key, value in self.dict_site[site].news.items():
                dict_aux = {}
                dict_aux['data'] = datetime.now()
                dict_aux['fonte'] = site
                dict_aux['materia'] = key
                dict_aux['link'] = value

                if len(self.news) == 0:
                    self.news.insert(0, dict_aux)
                    continue
                
                add_news = True
                for news in self.news:
                    if dict_aux["materia"] == news["materia"] and dict_aux["fonte"] == news["fonte"]:
                        add_news = False
                        break
                
                if add_news:
                    self.news.insert(0, dict_aux)
        
        self.news = sorted(self.news, key = lambda d: d['data'], reverse=True)
        self._update_file(self.news,'news')

    def main(self):
        st.set_page_config(layout="wide")
        image_url_all = "https://images.pexels.com/photos/7130549/pexels-photo-7130549.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
        image_sidebar = "https://images.pexels.com/photos/62693/pexels-photo-62693.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
        pg_bg_img = f"""
        <style>
        [data-testid="stAppViewContainer"] {{
            background-image: url("{image_url_all}");
            background-size: cover;
            background-position: center;
        }}
        [data-testid="stHeader"] {{
        background-color: rgba(0, 0, 0, 0);
        }}
        
        [data-testid="stSidebarContent"]{{
            background-image: url("{image_sidebar}");
            background-position:center;
        }}
        
        </style>
        """

        st.markdown(pg_bg_img, unsafe_allow_html=True)
        
        #SIDEBAR
        st.sidebar.title('News Settings')
        
        
        selected_sites = st.sidebar.multiselect("Select the news sources:", options=self.sites_todos, default=self.sites)
        
        if set(selected_sites) != set(self.sites):
            self.sites = selected_sites
            self._update_file(self.sites, 'sites')
        
        if st.sidebar.button('Update News'): 
            self.update_news()
        
        
        st.title("Financial Markets News!")
        st.write('We will show the most recent news of the Financial Markets')
        
        self.display_news()
        

if __name__ == "__main__":
    jean = JeanNews()
    jean.main()
