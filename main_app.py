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


# import streamlit as st
# import requests
# import re
# from langchain_community.embeddings import HuggingFaceEmbeddings
# from langchain_community.document_loaders import WebBaseLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_groq import ChatGroq
# from langchain_community.vectorstores import FAISS
# from langchain.prompts import ChatPromptTemplate
# from langchain.chains.combine_documents import create_stuff_documents_chain
# from langchain.chains import create_retrieval_chain

# llm = ChatGroq(
#     groq_api_key="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",
#     model_name="Gemma2-9b-it",
#     temperature=0.8,
# )

# def process_urls(urls):
#     all_docs = []
#     text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    
#     for url in urls[:5]:
#         try:
#             loader = WebBaseLoader(url)
#             docs = loader.load()
#             split_docs = text_splitter.split_documents(docs)
#             all_docs.extend(split_docs)
#         except Exception as e:
#             st.warning(f"Error: {str(e)}")

#     if all_docs:
#         embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
#         vector_store = FAISS.from_documents(all_docs, embeddings)
#         return vector_store
#     return None

# def run():
#     st.title("Linqify")
#     st.write("A Centralized RAG based Link Provider")

#     if 'vector_store' not in st.session_state:
#         st.session_state.vector_store = None
#     if 'current_links' not in st.session_state:
#         st.session_state.current_links = []

#     user_input = st.text_input("Enter your request for the dataset")

#     if st.button("Fetch Dataset and Create RAG"):
#         if user_input.strip():
#             try:
#                 with st.spinner("Your Agent is finding best links for you..."):
#                     response = requests.post(
#                         "https://researcher-agent-df3x.onrender.com/process_dataset/",
#                         json={"input": user_input}
#                     )
                    
#                     if response.status_code == 200:
#                         links = re.findall(r'https?://\S+', str(response.json().get("result", "")))
#                         if links:
#                             st.session_state.current_links = links[:5] # Store in session state
#                             st.subheader("Processing Top 5 URLs:")
#                             for link in st.session_state.current_links:
#                                 st.markdown(f"- {link}")

#                             st.session_state.vector_store = process_urls(links)
#                             if st.session_state.vector_store:
#                                 st.success("RAG system ready!")
#                         else:
#                             st.warning("No links found")
#                     else:
#                         st.error("API request failed")
#             except Exception as e:
#                 st.error(f"Error: {str(e)}")
#         else:
#             st.warning("Please enter a request")

#     if st.session_state.vector_store:
#         st.subheader("Ask Questions")
        
#         prompt = ChatPromptTemplate.from_template("""
#         Answer based on context: {context}
#         Question: {input}
#         """)
        
#         document_chain = create_stuff_documents_chain(llm, prompt)
#         retrieval_chain = create_retrieval_chain(
#             st.session_state.vector_store.as_retriever(search_kwargs={"k": 3}),
#             document_chain
#         )
        
#         question = st.text_input("Enter your question:")
        
#         if st.button("Get Answer") and question.strip():
#             with st.spinner("Generating answer..."):
#                 try:
#                     response = retrieval_chain.invoke({'input': question})
#                     st.write("Answer:", response['answer'])
#                 except Exception as e:
#                     st.error(f"Error: {str(e)}")


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

# Page configuration
st.set_page_config(
    page_title="Linqify - RAG Link Provider",
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
        .stButton>button {
            width: 100%;
            border-radius: 5px;
            height: 3em;
            background-color: #262730;
            border: 1px solid #464B5C;
        }
        .stButton>button:hover {
            border-color: #00ACB5;
            color: #00ACB5;
        }
        .css-1d391kg {
            padding: 2rem 1rem;
        }
        .stTextInput>div>div>input {
            background-color: #262730;
            border: 1px solid #464B5C;
        }
        .stProgress .st-bo {
            background-color: #00ACB5;
        }
        [data-testid="stMarkdownContainer"] {
            line-height: 1.6;
        }
    </style>
""", unsafe_allow_html=True)

llm = ChatGroq(
    groq_api_key="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",
    model_name="Gemma2-9b-it",
    temperature=0.8,
)

def process_urls(urls):
    all_docs = []
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    
    progress_bar = st.progress(0)
    for idx, url in enumerate(urls[:5]):
        try:
            with st.spinner(f'Processing URL {idx + 1}/5...'):
                loader = WebBaseLoader(url)
                docs = loader.load()
                split_docs = text_splitter.split_documents(docs)
                all_docs.extend(split_docs)
                progress_bar.progress((idx + 1) / 5)
        except Exception as e:
            st.error(f"Error processing {url}: {str(e)}")
    
    if all_docs:
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vector_store = FAISS.from_documents(all_docs, embeddings)
        return vector_store
    return None

def run():
    # Header section with logo and title
    col1, col2 = st.columns([1, 4])
    with col1:
        st.image("https://via.placeholder.com/150", width=100)  # Replace with your logo
    with col2:
        st.title("Linqify")
        st.markdown("*A Centralized RAG-based Link Provider*")
    
    st.divider()

    # Initialize session state
    if 'vector_store' not in st.session_state:
        st.session_state.vector_store = None
    if 'current_links' not in st.session_state:
        st.session_state.current_links = []

    # Main input section
    with st.container():
        st.subheader("📚 Dataset Request")
        user_input = st.text_input(
            "What kind of dataset are you looking for?",
            placeholder="E.g., 'Research papers on climate change impacts'"
        )

        if st.button("🔍 Find Relevant Sources"):
            if user_input.strip():
                try:
                    with st.spinner("🤖 AI Agent searching for the best sources..."):
                        response = requests.post(
                            "https://researcher-agent-df3x.onrender.com/process_dataset/",
                            json={"input": user_input}
                        )
                        
                        if response.status_code == 200:
                            links = re.findall(r'https?://\S+', str(response.json().get("result", "")))
                            if links:
                                st.session_state.current_links = links[:5]
                                with st.expander("📊 Found Sources", expanded=True):
                                    st.subheader("Processing Top 5 URLs:")
                                    for i, link in enumerate(st.session_state.current_links, 1):
                                        st.markdown(f"{i}. [{link}]({link})")
                                st.session_state.vector_store = process_urls(links)
                                if st.session_state.vector_store:
                                    st.success("✅ RAG system initialized and ready!")
                            else:
                                st.warning("⚠️ No relevant links found")
                        else:
                            st.error("❌ API request failed")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
            else:
                st.warning("⚠️ Please enter a request")

    # Q&A Section
    if st.session_state.vector_store:
        st.divider()
        st.subheader("🤔 Ask Questions About Your Sources")
        
        prompt = ChatPromptTemplate.from_template("""
        Based on the provided context: {context}
        Please answer the following question: {input}
        """)
        
        document_chain = create_stuff_documents_chain(llm, prompt)
        retrieval_chain = create_retrieval_chain(
            st.session_state.vector_store.as_retriever(search_kwargs={"k": 3}),
            document_chain
        )
        
        question = st.text_input(
            "What would you like to know?",
            placeholder="Ask a question about the content..."
        )
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🔍 Get Answer") and question.strip():
                with st.spinner("🤖 Analyzing sources..."):
                    try:
                        response = retrieval_chain.invoke({'input': question})
                        st.markdown("### 📝 Answer:")
                        st.markdown(response['answer'])
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    run()
