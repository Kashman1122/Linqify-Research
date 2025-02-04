# import streamlit as st
# import requests
# import re
# from langchain.agents import initialize_agent, Tool, AgentType
# from langchain.agents import AgentExecutor
# from langchain.tools import DuckDuckGoSearchResults
# from langchain.chat_models import ChatOpenAI
# from langchain.prompts import PromptTemplate
# from langchain.chains import ConversationChain
# from bs4 import BeautifulSoup
# from langchain_groq import ChatGroq
#
# # Title and description for the app
# st.title("Cancer Detection Dataset Generator with RAG")
# st.write(
#     "This app fetches a healthy dataset for cancer detection based on your request, scrapes top links, and allows chatting with those links using LangChain.")
#
#
# # Function to fetch top links
# def fetch_top_links(query):
#     search_url = f"https://duckduckgo.com/html/?q={query}"
#     try:
#         response = requests.get(search_url)
#         if response.status_code == 200:
#             soup = BeautifulSoup(response.text, 'html.parser')
#             results = soup.find_all('a', class_='result__a')
#             links = [result['href'] for result in results]
#             return links[:5]  # Get top 5 links
#         else:
#             return []
#     except Exception as e:
#         st.error(f"Failed to fetch links: {str(e)}")
#         return []
#
#
# # Function to scrape content from URLs
# def scrape_content_from_urls(urls):
#     content = ""
#     for url in urls:
#         try:
#             page = requests.get(url)
#             if page.status_code == 200:
#                 soup = BeautifulSoup(page.content, "html.parser")
#                 paragraphs = soup.find_all("p")
#                 content += "\n".join([para.get_text() for para in paragraphs]) + "\n\n"
#         except Exception as e:
#             st.warning(f"Failed to scrape {url}: {str(e)}")
#     return content
#
#
# # Input field to get user request for the dataset
# user_input = st.text_input("Enter your request for the dataset", "give me healthy dataset for cancer detection")
#
# # Button to trigger the request and initiate the LangChain RAG
# if st.button("Fetch Dataset and Start Chat"):
#     if user_input.strip() != "":
#         # Fetch top 5 links based on the user input
#         st.write("Fetching top links related to your request...")
#         top_links = fetch_top_links(user_input)
#
#         if top_links:
#             # Scrape content from the top links
#             st.write("Scraping content from the top links...")
#             scraped_content = scrape_content_from_urls(top_links)
#
#             if scraped_content:
#                 st.write("Chatting with the scraped content...")
#
#                 # Initialize LangChain components
#                 model = ChatGroq(
#                     groq_api_key="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",
#                     model_name="Gemma2-9b-it",
#                     temperature=0.8,
#                 )
#                 chain = ConversationChain(llm=model)
#
#                 # Display conversation UI
#                 user_message = st.text_area("Ask something about the content:")
#
#                 if st.button("Submit"):
#                     if user_message.strip() != "":
#                         # Process the user's query based on scraped content
#                         response = chain.run(input=user_message + "\n\n" + scraped_content)
#                         st.write(f"ChatGPT's response: {response}")
#                     else:
#                         st.warning("Please enter a question to chat.")
#             else:
#                 st.write("No content found after scraping the links.")
#         else:
#             st.write("No links found based on your request.")
#     else:
#         st.warning("Please enter a valid request.")


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
# from dotenv import load_dotenv
# import os
#
# # Load environment variables
# load_dotenv()
#
# # Configure API keys
# os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY')
# google_api_key = os.getenv('GOOGLE_API_KEY')
#
# # Initialize LLM
# llm = ChatGroq(
#                     groq_api_key="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",
#                     model_name="Gemma2-9b-it",
#                     temperature=0.8,
#                 )
# # Title and description for the app
# st.title("Cancer Detection Dataset RAG System")
# st.write("This app fetches cancer detection datasets and enables question-answering using RAG.")
#
# # Initialize session state for vector store
# if 'vector_store' not in st.session_state:
#     st.session_state.vector_store = None
#
# # Input field to get user request for the dataset
# user_input = st.text_input("Enter your request for the dataset", "give me healthy dataset for cancer detection")
#
#
# # Function to process URLs and create vector store
# def process_urls(urls):
#     all_docs = []
#     text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
#
#     for url in urls[:5]:  # Process only top 5 URLs
#         try:
#             loader = WebBaseLoader(url)
#             docs = loader.load()
#             split_docs = text_splitter.split_documents(docs)
#             all_docs.extend(split_docs)
#         except Exception as e:
#             st.warning(f"Error processing URL {url}: {str(e)}")
#
#     if all_docs:
#         embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
#         vector_store = FAISS.from_documents(all_docs, embeddings)
#         return vector_store
#     return None
#
#
# # Button to fetch dataset and create vector store
# if st.button("Fetch Dataset and Create RAG"):
#     if user_input.strip() != "":
#         url = "https://researcher-agent-df3x.onrender.com/process_dataset/"
#         data = {"input": user_input}
#
#         try:
#             with st.spinner("Fetching datasets and creating RAG system..."):
#                 response = requests.post(url, json=data)
#
#                 if response.status_code == 200:
#                     response_json = response.json()
#
#                     if isinstance(response_json, dict) and "result" in response_json:
#                         raw_text = str(response_json["result"])
#                         links = re.findall(r'https?://\S+', raw_text)
#
#                         if links:
#                             st.subheader("Processing Top 5 URLs:")
#                             for link in links[:5]:
#                                 st.markdown(f"- {link}")
#
#                             # Create vector store
#                             st.session_state.vector_store = process_urls(links)
#                             if st.session_state.vector_store:
#                                 st.success("RAG system created successfully!")
#                         else:
#                             st.write("No links found in the response.")
#                 else:
#                     st.error(f"Error: {response.status_code}, {response.text}")
#         except Exception as e:
#             st.error(f"Failed to connect: {str(e)}")
#     else:
#         st.warning("Please enter a valid request to fetch the dataset.")
#
# # Question answering section
# if st.session_state.vector_store:
#     st.subheader("Ask Questions About the Dataset")
#
#     # Create RAG chain
#     prompt = ChatPromptTemplate.from_template("""
#     Answer the following question based on the provided context only.
#     Please provide the most accurate response based on the question.
#
#     <context>
#     {context}
#     </context>
#
#     Question: {input}
#     """)
#
#     document_chain = create_stuff_documents_chain(llm, prompt)
#     retrieval = st.session_state.vector_store.as_retriever()
#     retrieval_chain = create_retrieval_chain(retrieval, document_chain)
#
#     # Question input
#     question = st.text_input("Enter your question about the dataset:")
#
#     if st.button("Get Answer"):
#         if question.strip():
#             with st.spinner("Generating answer..."):
#                 response = retrieval_chain.invoke({'input': question})
#                 st.write("Answer:", response['answer'])
#         else:
#             st.warning("Please enter a question.")


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
# from dotenv import load_dotenv
# import os
#
# # Load environment variables
# load_dotenv()
#
# # Configure API keys
# os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY')
# google_api_key = os.getenv('GOOGLE_API_KEY')
#
# # Initialize LLM
# llm = ChatGroq(
#     groq_api_key="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",
#     model_name="Gemma2-9b-it",
#     temperature=0.8,
# )
#
# # Title and description for the app
# st.title("Linqify")
# st.write("A Centralized RAG based Link Provider")
#
# # Initialize session state for vector store and links
# if 'vector_store' not in st.session_state:
#     st.session_state.vector_store = None
# if 'current_links' not in st.session_state:
#     st.session_state.current_links = []
#
# # Input field to get user request for the dataset
# user_input = st.text_input("Enter your request for the dataset")
#
#
# # Function to process URLs and create vector store
# def process_urls(urls):
#     all_docs = []
#     text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
#
#     for url in urls[:5]:  # Process only top 5 URLs
#         try:
#             loader = WebBaseLoader(url)
#             docs = loader.load()
#             split_docs = text_splitter.split_documents(docs)
#             all_docs.extend(split_docs)
#         except Exception as e:
#             st.warning(f"Error processing URL {url}: {str(e)}")
#
#     if all_docs:
#         embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
#         vector_store = FAISS.from_documents(all_docs, embeddings)
#         return vector_store
#     return None
#
#
# # Button to fetch dataset and create vector store
# if st.button("Fetch Dataset and Create RAG"):
#     if user_input.strip() != "":
#         url = "https://researcher-agent-df3x.onrender.com/process_dataset/"
#         data = {"input": user_input}
#
#         try:
#             with st.spinner("Fetching datasets and creating RAG system..."):
#                 response = requests.post(url, json=data)
#
#                 if response.status_code == 200:
#                     response_json = response.json()
#
#                     if isinstance(response_json, dict) and "result" in response_json:
#                         raw_text = str(response_json["result"])
#                         links = re.findall(r'https?://\S+', raw_text)
#
#                         if links:
#                             # Store the new links in session state
#                             st.session_state.current_links = links[:5]
#
#                             st.subheader("Processing Top 5 URLs:")
#                             for link in st.session_state.current_links:
#                                 st.markdown(f"- {link}")
#
#                             # Create vector store
#                             st.session_state.vector_store = process_urls(links)
#                             if st.session_state.vector_store:
#                                 st.success("RAG system created successfully!")
#                         else:
#                             st.write("No links found in the response.")
#                 else:
#                     st.error(f"Error: {response.status_code}, {response.text}")
#         except Exception as e:
#             st.error(f"Failed to connect: {str(e)}")
#     else:
#         st.warning("Please enter a valid request to fetch the dataset.")
#
# # Always display current links if they exist
# if st.session_state.current_links:
#     st.subheader("Current Dataset URLs:")
#     for link in st.session_state.current_links:
#         st.markdown(f"- {link}")
#
# # Question answering section
# if st.session_state.vector_store:
#     st.subheader("Ask Questions About the Dataset")
#
#     # Create RAG chain
#     prompt = ChatPromptTemplate.from_template("""
#     Answer the following question based on the provided context only.
#     Please provide the most accurate response based on the question.
#
#     <context>
#     {context}
#     </context>
#
#     Question: {input}
#     """)
#
#     document_chain = create_stuff_documents_chain(llm, prompt)
#     retrieval = st.session_state.vector_store.as_retriever()
#     retrieval_chain = create_retrieval_chain(retrieval, document_chain)
#
#     # Question input
#     question = st.text_input("Enter your question about the dataset:")
#
#     if st.button("Get Answer"):
#         if question.strip():
#             with st.spinner("Generating answer..."):
#                 response = retrieval_chain.invoke({'input': question})
#                 st.write("Answer:", response['answer'])
#         else:
#             st.warning("Please enter a question.")



# main_app.py
import streamlit as st
import requests
import re
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS
from langchain.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure API keys
os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY')
google_api_key = os.getenv('GOOGLE_API_KEY')

# Initialize LLM
llm = ChatGroq(
    groq_api_key="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",  # Replace with your actual key if needed
    model_name="Gemma2-9b-it",  # Or other model
    temperature=0.8,
)

def run():  # The run function that app.py will call
    # Title and description for the app
    st.title("Linqify")
    st.write("A Centralized RAG based Link Provider")

    # Initialize session state for vector store and links
    if 'vector_store' not in st.session_state:
        st.session_state.vector_store = None
    if 'current_links' not in st.session_state:
        st.session_state.current_links = []

    # Input field to get user request for the dataset
    user_input = st.text_input("Enter your request for the dataset")

    # Function to process URLs and create vector store
    def process_urls(urls):
        all_docs = []
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)

        for url in urls[:5]:  # Process only top 5 URLs
            try:
                loader = WebBaseLoader(url)
                docs = loader.load()
                split_docs = text_splitter.split_documents(docs)
                all_docs.extend(split_docs)
            except Exception as e:
                st.warning(f"Error processing URL {url}: {str(e)}")

        if all_docs:
            embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")  # Ensure this path is correct
            vector_store = FAISS.from_documents(all_docs, embeddings)
            return vector_store
        return None

    # Button to fetch dataset and create vector store
    if st.button("Fetch Dataset and Create RAG"):
        if user_input.strip() != "":
            url = "https://researcher-agent-df3x.onrender.com/process_dataset/"  # Your API endpoint
            data = {"input": user_input}

            try:
                with st.spinner("Fetching datasets and creating RAG system..."):
                    response = requests.post(url, json=data)

                    if response.status_code == 200:
                        response_json = response.json()

                        if isinstance(response_json, dict) and "result" in response_json:
                            raw_text = str(response_json["result"])
                            links = re.findall(r'https?://\S+', raw_text)

                            if links:
                                st.session_state.current_links = links[:5] # Store in session state
                                st.subheader("Processing Top 5 URLs:")
                                for link in st.session_state.current_links:
                                    st.markdown(f"- {link}")

                                st.session_state.vector_store = process_urls(links) # Store in session state
                                if st.session_state.vector_store:
                                    st.success("RAG system created successfully!")
                            else:
                                st.write("No links found in the response.")
                        else:
                            st.write("Unexpected response format.")  # Handle unexpected format

                    else:
                        st.error(f"Error: {response.status_code}, {response.text}")
            except requests.exceptions.RequestException as e:  # Catch connection errors
                st.error(f"Connection error: {str(e)}")
            except Exception as e: # Catch any other exception
                st.error(f"An error occurred: {str(e)}")
        else:
            st.warning("Please enter a valid request to fetch the dataset.")

    # Always display current links if they exist in the session state
    if st.session_state.current_links:
        st.subheader("Current Dataset URLs:")
        for link in st.session_state.current_links:
            st.markdown(f"- {link}")

    # Question answering section (only if vector store exists in session state)
    if st.session_state.vector_store:
        st.subheader("Ask Questions About the Dataset")

        # Create RAG chain (same as before)
        prompt = ChatPromptTemplate.from_template("""
        Answer the following question based on the provided context only.
        Please provide the most accurate response based on the question.

        <context>
        {context}
        </context>

        Question: {input}
        """)

        document_chain = create_stuff_documents_chain(llm, prompt)
        retrieval = st.session_state.vector_store.as_retriever()  # Use vector store from session state
        retrieval_chain = create_retrieval_chain(retrieval, document_chain)

        question = st.text_input("Enter your question about the dataset:")

        if st.button("Get Answer"):
            if question.strip():
                with st.spinner("Generating answer..."):
                    try:
                        response = retrieval_chain.invoke({'input': question})
                        st.write("Answer:", response['answer'])
                    except Exception as e:
                        st.error(f"Error during answer generation: {e}") # Catch and display errors
            else:
                st.warning("Please enter a question.")