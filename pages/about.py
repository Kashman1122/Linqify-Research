# pages/1_About.py

import streamlit as st

# Page configuration
st.set_page_config(
    page_title="About Linqify",
    page_icon="ℹ️",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .about-section {
        background-color: #020213;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .feature-card {
        background-color: #020213;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border: 1px solid #e0e0e0;
    }
    </style>
    """, unsafe_allow_html=True)

# Header
st.title("🔍 About Linqify")

# Main content
st.markdown("""
<div class='about-section'>
    <h2>Our Mission</h2>
    <p>Linqify is designed to revolutionize how researchers, academics, and professionals access and interact with scientific information. 
    Our platform combines advanced RAG (Retrieval Augmented Generation) technology with an intuitive interface to make research more efficient and accessible.</p>
</div>
""", unsafe_allow_html=True)

# Features section
st.header("🎯 Key Features")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class='feature-card'>
        <h3>📚 Comprehensive Search</h3>
        <ul>
            <li>Access to research papers and academic publications</li>
            <li>Extensive dataset repositories</li>
            <li>Patent databases</li>
            <li>Real-time data processing</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='feature-card'>
        <h3>🤖 AI-Powered Analysis</h3>
        <ul>
            <li>Advanced RAG technology</li>
            <li>Context-aware responses</li>
            <li>Intelligent document processing</li>
            <li>Natural language understanding</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='feature-card'>
        <h3>💡 Interactive Features</h3>
        <ul>
            <li>Chat-based document exploration</li>
            <li>Custom query processing</li>
            <li>Real-time responses</li>
            <li>Dynamic content analysis</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='feature-card'>
        <h3>🔒 Research Integrity</h3>
        <ul>
            <li>Source verification</li>
            <li>Academic integrity checks</li>
            <li>Citation tracking</li>
            <li>Quality assurance</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# How it works section
st.header("⚙️ How It Works")

st.markdown("""
<div class='about-section'>
    <ol>
        <li><strong>Input Your Query:</strong> Enter your research topic or specific question</li>
        <li><strong>Smart Search:</strong> Our system searches through multiple databases and sources</li>
        <li><strong>RAG Processing:</strong> Documents are processed using advanced RAG technology</li>
        <li><strong>Interactive Analysis:</strong> Chat with the system to explore and understand the content</li>
        <li><strong>Get Results:</strong> Receive comprehensive, context-aware responses</li>
    </ol>
</div>
""", unsafe_allow_html=True)

# Contact section
st.header("📬 Contact Us")

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("""
    <div class='feature-card' style='text-align: center; background-color:#020213;'>
        <p>Have questions or suggestions? We'd love to hear from you!</p>
        <p>Email: contact@linqify.com</p>
        <p>Twitter: @linqify</p>
        <p>GitHub: github.com/linqify</p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div style='text-align: center; margin-top: 2rem; padding: 1rem; background-color: #020213; border-radius: 10px;'>
    <p>Linqify - Making Research Smarter</p>
    <p style='font-size: 0.8rem;'>© 2024 Linqify. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)