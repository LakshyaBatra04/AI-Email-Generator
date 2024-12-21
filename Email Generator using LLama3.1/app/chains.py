from langchain_groq import ChatGroq
import chromadb
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import pandas as pd
import os
import uuid
from dotenv import load_dotenv

load_dotenv()

class Chain :
    def __init__(self):
        self.llm = ChatGroq(
                        temperature=0,
                        groq_api_key = os.getenv("GROQ_API_KEY"),
                        model = "llama-3.1-70b-versatile"
                    )

    def extract_jobs(self, cleaned_text):

        prompt_template = PromptTemplate.from_template(
            '''###SCRAPPED TEXTS FROM WEBSITES:
            {page_data}
            ###INSTRUCTION:
            The scrapped text is from a career's page of a website.
            Your job is to extract the job postings and return them in JSON format containing the following keys :
            'role','experience','skills' and 'description'
            Only return the valid JSON.
            ###VALID JSON (NO PREAMBLE):
            '''
        )
        chain = prompt_template|self.llm
        res = chain.invoke(input= {'page_data':cleaned_text})
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)        

        except Exception :
            raise Exception("Process Failed")
        
        return res if isinstance(res,list) else [res]
    
    def write_mail(self,job,links):
        prompt_email = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}
            
            ### INSTRUCTION:
            You are Lakshya Batra, a third year undergraduate at IIT Delhi. You have good knowledge in ML topics like neural networks,
            LSTMs, Transformers,etc. You are proficient in languages like C++, Python and Java. You have also made several projects
            on these topics and now want to contibute to real world projects
            Your job is to write a cold email to the client regarding the job mentioned above describing the capability of Lakshya 
            in fulfilling their needs. 
            Also add the most relevant ones from the following links to showcase Lakshya's CV: {link_list}
            Remember you are Lakshya. 
            Do not provide a preamble.
            ### EMAIL (NO PREAMBLE):
            
            """
        )

        chain_email = prompt_email | self.llm
        res = chain_email.invoke({"job_description": str(job), "link_list": links})
        return res.content

if __name__ == "__main__": 
    print(os.getenv("GROQ_API_KEY"))
