# # main_app.py
# import streamlit as st
# import requests
# import re
# from langchain_google_genai import GoogleGenerativeAIEmbeddings
# from langchain_community.document_loaders import WebBaseLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_groq import ChatGroq
# from langchain_community.vectorstores import FAISS
# from langchain.prompts import ChatPromptTemplate
# from langchain.chains.combine_documents import create_stuff_documents_chain
# from langchain.chains import create_retrieval_chain
# import os

# # Load environment variables
# # Initialize LLM
# llm = ChatGroq(
#     groq_api_key="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",  # Replace with your actual key if needed
#     model_name="Gemma2-9b-it",  # Or other model
#     temperature=0.8,
# )

# def run():  # The run function that app.py will call
#     # Title and description for the app
#     st.title("Linqify")
#     st.write("A Centralized RAG based Link Provider")

#     # Initialize session state for vector store and links
#     if 'vector_store' not in st.session_state:
#         st.session_state.vector_store = None
#     if 'current_links' not in st.session_state:
#         st.session_state.current_links = []

#     # Input field to get user request for the dataset
#     user_input = st.text_input("Enter your request for the dataset")

#     # Function to process URLs and create vector store
#     def process_urls(urls):
#         all_docs = []
#         text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)

#         for url in urls[:5]:  # Process only top 5 URLs
#             try:
#                 loader = WebBaseLoader(url)
#                 docs = loader.load()
#                 split_docs = text_splitter.split_documents(docs)
#                 all_docs.extend(split_docs)
#             except Exception as e:
#                 st.warning(f"Error processing URL {url}: {str(e)}")

#         if all_docs:
#             embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")  # Ensure this path is correct
#             vector_store = FAISS.from_documents(all_docs, embeddings)
#             return vector_store
#         return None

#     # Button to fetch dataset and create vector store
#     if st.button("Fetch Dataset and Create RAG"):
#         if user_input.strip() != "":
#             url = "https://researcher-agent-df3x.onrender.com/process_dataset/"  # Your API endpoint
#             data = {"input": user_input}

#             try:
#                 with st.spinner("Fetching datasets and creating RAG system..."):
#                     response = requests.post(url, json=data)

#                     if response.status_code == 200:
#                         response_json = response.json()

#                         if isinstance(response_json, dict) and "result" in response_json:
#                             raw_text = str(response_json["result"])
#                             links = re.findall(r'https?://\S+', raw_text)

#                             if links:
#                                 st.session_state.current_links = links[:5] # Store in session state
#                                 st.subheader("Processing Top 5 URLs:")
#                                 for link in st.session_state.current_links:
#                                     st.markdown(f"- {link}")

#                                 st.session_state.vector_store = process_urls(links) # Store in session state
#                                 if st.session_state.vector_store:
#                                     st.success("RAG system created successfully!")
#                             else:
#                                 st.write("No links found in the response.")
#                         else:
#                             st.write("Unexpected response format.")  # Handle unexpected format

#                     else:
#                         st.error(f"Error: {response.status_code}, {response.text}")
#             except requests.exceptions.RequestException as e:  # Catch connection errors
#                 st.error(f"Connection error: {str(e)}")
#             except Exception as e: # Catch any other exception
#                 st.error(f"An error occurred: {str(e)}")
#         else:
#             st.warning("Please enter a valid request to fetch the dataset.")

#     # Always display current links if they exist in the session state
#     if st.session_state.current_links:
#         st.subheader("Current Dataset URLs:")
#         for link in st.session_state.current_links:
#             st.markdown(f"- {link}")

#     # Question answering section (only if vector store exists in session state)
#     if st.session_state.vector_store:
#         st.subheader("Ask Questions About the Dataset")

#         # Create RAG chain (same as before)
#         prompt = ChatPromptTemplate.from_template("""
#         Answer the following question based on the provided context only.
#         Please provide the most accurate response based on the question.

#         <context>
#         {context}
#         </context>

#         Question: {input}
#         """)

#         document_chain = create_stuff_documents_chain(llm, prompt)
#         retrieval = st.session_state.vector_store.as_retriever()  # Use vector store from session state
#         retrieval_chain = create_retrieval_chain(retrieval, document_chain)

#         question = st.text_input("Enter your question about the dataset:")

#         if st.button("Get Answer"):
#             if question.strip():
#                 with st.spinner("Generating answer..."):
#                     try:
#                         response = retrieval_chain.invoke({'input': question})
#                         st.write("Answer:", response['answer'])
#                     except Exception as e:
#                         st.error(f"Error during answer generation: {e}") # Catch and display errors
#             else:
#                 st.warning("Please enter a question.")


# main_app.py
import streamlit as st
import requests
import re
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS
from langchain.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
import asyncio
import aiohttp

class OptimizedRAG:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        self.llm = ChatGroq(
            groq_api_key="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",
            model_name="Gemma2-9b-it",
            temperature=0.8,
        )

    async def fetch_url(self, session, url):
        try:
            async with session.get(url, timeout=10) as response:
                if response.status == 200:
                    content = await response.text()
                    docs = self.text_splitter.split_text(content)
                    return docs
                return None
        except Exception:
            return None

    async def process_urls_async(self, urls):
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch_url(session, url) for url in urls[:5]]
            docs = await asyncio.gather(*tasks)
            return [doc for doc in docs if doc]

    def create_vector_store(self, docs):
        if not docs:
            return None
        return FAISS.from_texts(docs, self.embeddings)

def init_session_state():
    for key in ['vector_store', 'current_links', 'processing_complete']:
        if key not in st.session_state:
            st.session_state[key] = None

def run():
    st.title("Linqify")
    st.write("A Centralized RAG based Link Provider")
    
    init_session_state()
    rag = OptimizedRAG()
    
    user_input = st.text_input("Enter your request for the dataset")
    
    if st.button("Fetch Dataset and Create RAG"):
        if not user_input.strip():
            st.warning("Please enter a dataset request.")
            return

        try:
            with st.spinner("Processing..."):
                response = requests.post(
                    "https://researcher-agent-df3x.onrender.com/process_dataset/",
                    json={"input": user_input},
                    timeout=15
                )
                
                if response.status_code != 200:
                    st.error("Failed to fetch datasets")
                    return
                
                links = re.findall(r'https?://\S+', str(response.json().get("result", "")))
                if not links:
                    st.warning("No valid links found")
                    return
                
                st.session_state.current_links = links[:5]
                
                with st.spinner("Building RAG system..."):
                    docs = asyncio.run(rag.process_urls_async(links[:5]))
                    st.session_state.vector_store = rag.create_vector_store(docs)
                    st.session_state.processing_complete = True
                    st.success("RAG system ready!")

        except Exception as e:
            st.error(f"Error: {str(e)}")
            return

    if st.session_state.current_links:
        with st.expander("Dataset URLs"):
            for link in st.session_state.current_links:
                st.write(f"• {link}")

    if st.session_state.vector_store and st.session_state.processing_complete:
        st.subheader("Ask Questions")
        
        prompt = ChatPromptTemplate.from_template("""
        Answer based on context only: {context}
        Question: {input}
        """)
        
        document_chain = create_stuff_documents_chain(rag.llm, prompt)
        retrieval_chain = create_retrieval_chain(
            st.session_state.vector_store.as_retriever(search_kwargs={"k": 3}),
            document_chain
        )
        
        question = st.text_input("Enter your question:")
        
        if st.button("Get Answer") and question.strip():
            try:
                with st.spinner("Generating answer..."):
                    response = retrieval_chain.invoke({'input': question})
                    st.write("Answer:", response['answer'])
            except Exception as e:
                st.error(f"Error: {str(e)}")
