import streamlit as st
from chains import Chain
from portfolio import Portfolio
from utils import clean_text
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import pandas as pd

def create_streamlit_app(llm,Portfolio,clean_text):
    st.title("Cold Email Generator")
    url_input = st.text_input("Enter the URL :")
    submit_button = st.button("Submit")

    if submit_button:
        try:
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)
            Portfolio.load_portfolio()
            jobs = llm.extract_jobs(data)
            for job in jobs:
                skills = job.get('skills',[])
                links = Portfolio.query_links(skills)
                email = llm.write_mail(job,links)
                st.code(email,language = 'markdown')
        except Exception as e:
            st.error(f"An error occured : {e}")

if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout = "wide", page_title = "Cold Email Generator")
    create_streamlit_app(chain,portfolio,clean_text)

