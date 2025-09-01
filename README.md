# AI-SQL-Assistant-Streamlit-LangChain-
Transform **natural language questions** into **SQL queries** and get real-time database insights with AI!
## 📌 Overview  
This project is an AI-powered **Natural Language to SQL Query Assistant** built using **LangChain, Google Generative AI, and Streamlit**.  
It allows users to ask questions in **plain English** about the database, automatically converts them into optimized SQL queries, executes them on a **Microsoft SQL Server database**, and returns accurate results in natural language.  
Perfect for **non-technical users, business analysts, and e-commerce inventory management**.
## 🚀 Features  
✅ Convert **natural language** to **SQL queries** using LangChain  
✅ Integrates **Google Generative AI (Gemini 2.5 Flash)** for query generation  
✅ Uses **Few-Shot Prompting with Semantic Similarity** for better accuracy  
✅ Supports **Microsoft SQL Server** database with secure connection  
✅ Interactive **Streamlit dashboard** for user-friendly Q&A experience  
✅ Download **Q&A history as CSV**  
✅ Predefined sample questions + custom input  

# 🛠 Tech Stack

- **Programming Language:** Python  
- **LLM Orchestration:** LangChain (Prompt Templates, Chains)  
- **Generative AI Model:** Google Generative AI (Gemini 2.5 Flash)  
- **Frontend:** Streamlit  
- **Vector Database:** HuggingFace Embeddings + Chroma DB  
- **Database Connectivity:** PyODBC + SQLAlchemy  
- **Relational Database:** Microsoft SQL Server  

**Diagram:**

```mermaid
flowchart LR
    A[User] --> B[Streamlit UI]
    B --> C[LangChain Prompt]
    C --> D[Google Generative AI]
    D --> E[SQL Query]
    E --> F[MS SQL Database]
    F --> G[Natural Language Answer]
```
