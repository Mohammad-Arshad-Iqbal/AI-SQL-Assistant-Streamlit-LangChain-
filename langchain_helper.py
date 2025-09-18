from langchain_google_genai import ChatGoogleGenerativeAI
import pandas as pd
import pyodbc
from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.prompts import SemanticSimilarityExampleSelector
from langchain.prompts import PromptTemplate
from langchain.prompts import FewShotPromptTemplate
from few_shot import few_shot

def get_few_shotdb_chain():
    llm=ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        api_key="AIzaSyDcE4hTsoJFFZ0Kp5iBT-A1vrhMAmpmWjo",
        temperature=0.2)

    db_user = ""   
    db_password = ""   
    db_host = "localhost,1433"
    db_name = "Arshad_Tshirts"

    db = SQLDatabase.from_uri(
        f"mssql+pyodbc://@{db_host}/{db_name}?driver=ODBC+Driver+18+for+SQL+Server&trusted_connection=yes&TrustServerCertificate=yes"
    )
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    to_vectorize=[" ".join(example.values()) for example in few_shot]
    vectorstore=Chroma.from_texts(to_vectorize,embedding=embeddings,metadatas=few_shot)
    example_selector=SemanticSimilarityExampleSelector(
    vectorstore=vectorstore,
    k=3)
    MSSQL_PREFIX = """
    You are a Microsoft SQL Server expert. Follow this EXACT format.

    1) First write ONLY the SQL query (no commentary) after the label `SQLQuery:`. Use square brackets for identifiers.
    2) After the query is executed and the result is inserted as `SQLResult:`, write ONLY the final answer (plain English) after the label `Answer:`. DO NOT repeat the SQL, DO NOT include any SQL tokens (SELECT, FROM, [, ], etc.) in the Answer.
    3) If the SQLResult is empty, say 'No matching rows found.' and nothing else.

    Example:
    Question: How many total t shirts are left in stock?
    SQLQuery: SELECT SUM([stock_quantity]) AS [TotalStock] FROM [t_shirts];
    SQLResult: [(4451,)]
    Answer: There are 4,451 t-shirts left in stock.
    """

    MSSQL_SUFFIX = """
    Only use the following tables:
    {table_info}

    Question: {input}
    SQLQuery:
    SQLResult:
    Answer: just write result of sql query in plain english language dont write sql query here
    """

    example_prompt=PromptTemplate(
    input_variables=["Question","SQLQuery","SQLResult","Answer",],
    template="\nQuestion:{Question}\nSQLQuery:{SQLQuery}\nSQLResult: {SQLResult}\nAnswer:{Answer}",)
    few_shot_prompt=FewShotPromptTemplate(
    example_selector=example_selector,
    example_prompt=example_prompt,
    prefix=MSSQL_PREFIX,
    suffix=MSSQL_SUFFIX,
    input_variables=["input", "table_info", "top_k"],)
    chain=SQLDatabaseChain.from_llm(llm,db,verbose=True,prompt=few_shot_prompt)
    return chain

if __name__=="__main__":
    chain=get_few_shotdb_chain()
    answer = chain.invoke("which tshirt is least number in stock?")
    print(answer["result"])
    





