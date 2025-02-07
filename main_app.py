##ABHI TK YE CHL RAHA THA
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
#     groq_api_key="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",#Add your API key here
#     model_name="Gemma2-9b-it",
#     temperature=0.8,
# )

# def process_urls(urls):
#     all_docs = []
#     text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    
#     for url in urls[:50]:
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


# def run():  # The run function that app.py will call
#     # Title and description for the app
#     st.title("Linqify")
#     st.write("A Centralized RAG based Research Agent")

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

#         for url in urls[:50]:  # Process only top 5 URLs
#             try:
#                 loader = WebBaseLoader(url)
#                 docs = loader.load()
#                 split_docs = text_splitter.split_documents(docs)
#                 all_docs.extend(split_docs)
#             except Exception as e:
#                 st.warning(f"Error processing URL {url}: {str(e)}")

#         if all_docs:
#             embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
#             vector_store = FAISS.from_documents(all_docs, embeddings)
#             return vector_store
#         return None

#     # Button to fetch dataset and create vector store
#     if st.button("Fetch Links and Create RAG"):
#         if user_input.strip() != "":
#             url = "https://researcher-agent-df3x.onrender.com/process_dataset/"  # Your API endpoint
#             data = {"input": user_input}

#             try:
#                 with st.spinner("Your AI Agent is working for you..."):
#                     response = requests.post(url, json=data)

#                     if response.status_code == 200:
#                         response_json = response.json()

#                         if isinstance(response_json, dict) and "result" in response_json:
#                             raw_text = str(response_json["result"])
#                             links = re.findall(r'https?://\S+', raw_text)

#                             if links:
#                                 st.session_state.current_links = links[:50] # Store in session state
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
#                             st.session_state.current_links = links[:50] # Store in session state
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
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import WebBaseLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS
from langchain.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from dotenv import load_dotenv
import os
import tempfile

st.markdown("""
<style>
.link-box {
    border: 1px solid #ddd;
    border-radius: 5px;
    padding: 10px;
    margin: 5px 0;
    background-color: #f8f9fa;
}
.link-box a {
    color: #0366d6;
    text-decoration: none;
}
.link-box a:hover {
    text-decoration: underline;
}
.pdf-box {
    border: 1px solid #ddd;
    border-radius: 5px;
    padding: 10px;
    margin: 5px 0;
    background-color: #fff3f3;
}
</style>
""", unsafe_allow_html=True)

load_dotenv()
google_api_key = os.getenv('GOOGLE_API_KEY')

llm = ChatGroq(
    groq_api_key="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",
    model_name="Gemma2-9b-it",
    temperature=0.8,
)


def run():
    st.title("Linqify")
    st.write("A Centralized RAG based Link Provider")

    if 'vector_store' not in st.session_state:
        st.session_state.vector_store = None
    if 'current_links' not in st.session_state:
        st.session_state.current_links = []
    if 'selected_links' not in st.session_state:
        st.session_state.selected_links = []

    user_input = st.text_input("Enter your request for the dataset")

    def process_sources(urls=None, pdfs=None):
        all_docs = []
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)

        if urls:
            for url in urls:
                try:
                    loader = WebBaseLoader(url)
                    docs = loader.load()
                    split_docs = text_splitter.split_documents(docs)
                    all_docs.extend(split_docs)
                except Exception as e:
                    st.warning(f"Error processing URL {url}: {str(e)}")

        if pdfs:
            for pdf in pdfs:
                try:
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                        tmp_file.write(pdf.getvalue())
                        loader = PyPDFLoader(tmp_file.name)
                        docs = loader.load()
                        all_docs.extend(text_splitter.split_documents(docs))
                    os.unlink(tmp_file.name)
                except Exception as e:
                    st.warning(f"Error processing PDF {pdf.name}: {str(e)}")

        if all_docs:
            embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
            return FAISS.from_documents(all_docs, embeddings)
        return None

    if st.button("Fetch Dataset"):
        if user_input.strip():
            url = "https://researcher-agent-df3x.onrender.com/process_dataset/"
            data = {"input": user_input}

            try:
                with st.spinner("Fetching datasets..."):
                    response = requests.post(url, json=data)
                    if response.status_code == 200:
                        response_json = response.json()
                        if isinstance(response_json, dict) and "result" in response_json:
                            raw_text = str(response_json["result"])
                            links = re.findall(r'https?://\S+', raw_text)
                            if links:
                                st.session_state.current_links = links[:50]
                            else:
                                st.write("No links found in the response.")
                    else:
                        st.error(f"Error: {response.status_code}, {response.text}")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
        else:
            st.warning("Please enter a valid request to fetch the dataset.")

    selected_links = []
    if st.session_state.current_links:
        st.subheader("Select Links for RAG Processing")
        select_all = st.checkbox("Select All Links")

        for i, link in enumerate(st.session_state.current_links):
            col1, col2 = st.columns([1, 8])
            with col1:
                if st.checkbox("", value=select_all, key=f"link_{i}"):
                    selected_links.append(link)
            with col2:
                st.markdown(f'<div class="link-box"><a href="{link}" target="_blank">Link {i + 1}: {link}</a></div>',
                            unsafe_allow_html=True)

    # Add PDF uploader after link selection
    st.subheader("Add PDFs (Optional)")
    uploaded_pdfs = st.file_uploader("Drop your PDFs here", type=['pdf'], accept_multiple_files=True)

    if uploaded_pdfs:
        st.markdown("### Selected PDFs:")
        for pdf in uploaded_pdfs:
            st.markdown(f'<div class="pdf-box">📄 {pdf.name}</div>', unsafe_allow_html=True)

    if st.button("Create RAG from Selected Sources"):
        if selected_links or uploaded_pdfs:
            with st.spinner("Creating RAG system..."):
                st.session_state.vector_store = process_sources(urls=selected_links, pdfs=uploaded_pdfs)
            if st.session_state.vector_store:
                st.success("RAG system created successfully!")
        else:
            st.warning("Please select at least one source (link or PDF).")

    if st.session_state.vector_store:
        st.subheader("Ask Questions About the Dataset")
        prompt = ChatPromptTemplate.from_template("""
        Answer the following question based on the provided context only.
        Please provide the most accurate response based on the question.

        <context>
        {context}
        </context>

        Question: {input}
        """)

        document_chain = create_stuff_documents_chain(llm, prompt)
        retrieval = st.session_state.vector_store.as_retriever()
        retrieval_chain = create_retrieval_chain(retrieval, document_chain)

        question = st.text_input("Enter your question about the dataset:")

        if st.button("Get Answer"):
            if question.strip():
                with st.spinner("Generating answer..."):
                    try:
                        response = retrieval_chain.invoke({'input': question})
                        st.write("Answer:", response['answer'])
                    except Exception as e:
                        st.error(f"Error during answer generation: {e}")
            else:
                st.warning("Please enter a question.")

