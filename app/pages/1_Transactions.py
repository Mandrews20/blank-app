import streamlit as st
st.set_page_config(layout="wide")

# Load the CSS file
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Define the HTML for the banner
banner_html = """
<div class="full-width-banner">
    <img src="https://zeroheight.com/uploads/DAKqHhnDoTprAFJDxyKYEg.jpg">
    <h2>Data Examiner</h2>
</div>
"""

# Embed the HTML in Streamlit
st.markdown(banner_html, unsafe_allow_html=True)

st.title("Transactions")
st.write("Welcome to the Transactions page!")
