 # Imports
import streamlit as st
import pandas as pd
import re
import streamlit as st
from datetime import datetime

# Example stored queries
storedQueries = [['First', "Select from db where date in (2022-12-01)"], ['Second', "Select * From LPCE1V1_DB_DH.draw.bet_types limit 10"]]

conn = st.connection(
    "",
    type="snowflake",
    account="IGTGLOBALLOTTERY-IGTP1V1_LDI",
    user="MEGHAN.ANDREWS@IGT.COM",
    authenticator="externalbrowser",
)

session = conn.session()

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

# Add some space below the banner
st.write("<br>", unsafe_allow_html=True)

# Initialize session states
if 'sql_query' not in st.session_state:
    st.session_state['sql_query'] = ""
    st.session_state.disabled = False

if 'df' not in st.session_state:
    st.session_state['df'] = None

if 'show_dialog' not in st.session_state:
    st.session_state['show_dialog'] = False

#Function to clear Custom SQL text area and reset states
def clear_text():
    st.session_state['sql_query'] = ""
    st.session_state['df'] = None

@st.dialog("Add Favorite",width="large")
def addFavorite(query):
    st.write("Enter a unique name for your favorite:")
    name = st.text_input("Enter name...")
    if st.button("Submit"):
        storedQueries.append([name, query])
        st.success(f"Query '{name}' added successfully!")
        st.rerun()

@st.dialog("Select Favorite",width="large")
def loadFavorite():
    done = False
    query_names = [query[0] for query in storedQueries]
    selected_query_name = st.selectbox('Select a query:', query_names)
    selected_index = query_names.index(selected_query_name)
    selected_query = storedQueries[selected_index][1]
    
    if st.button("Load"):
        dates = validateParamQuery(selected_query)
        if dates:
            st.write('Query contains dates:', dates)
            parameterized_query = parameterize_query(selected_query, dates)
            st.write('Parameterized Query:', parameterized_query)

            # Example of how to use the parameterized query with user input
            user_date = st.text_input('Enter a date (YYYY-MM-DD):')
            if user_date:
                final_query = parameterized_query.format(date=user_date)
                st.session_state['sql_query'] = final_query
                done = True

        else:
            st.write('No dates found in the query')
            st.session_state['sql_query'] = selected_query
            done = True

        if done:
            st.rerun()

# function to validate query
def validateQuery(query):
    good = True
    formatedQuery = query.lower()

    formatedQuery = formatedQuery.replace('(',' ')
    formatedQuery = formatedQuery.replace(')',' ')

    queryArray = formatedQuery.split(" ")
    
    # illegal terms
    illegalTerms = ['delete', 'update', 'drop', 'add', 'truncate', 'insert', 'merge', 'rename', 'alter']

    for term in illegalTerms:
        if term in queryArray:
            st.toast(body="'"+term+"' not allowed to be queried", icon="❌")
            good = False
    return good


def validateParamQuery(query):
    # Regular expression to find date patterns (YYYY-MM-DD)
    date_pattern = r'\d{4}-\d{2}-\d{2}'
    matches = re.findall(date_pattern, query)
    return matches

# replace date with parameters
def parameterize_query(query, dates):
    for date in dates:
        query = query.replace(date, '{date}')
    return query

# Title
with st.container(border=True):
    st.markdown("""
        <div style="">
            <h1 style="font-family: 'Open Sans', sans-serif;font-weight: 300;font-size: 240">Custom SQL</h1>
        </div>
    """, unsafe_allow_html=True)

# Input Container   
with st.container(border=True):
        
    col1, col2= st.columns([1,.1]) 
    with col1:
        if st.button("Show Favorites"):
            st.session_state['show_dialog'] = True
            loadFavorite()
        
    with col2:
        if st.button("Add Favorite",type="primary"):
            addFavorite(st.session_state['sql_query'])

    st.text_area(
        label="Enter SQL Query", 
        value=st.session_state['sql_query'], 
        key="sql_query",
        disabled=False, 
        label_visibility="visible"
    )
        
    # Custom CSS to remove space between columns
    st.markdown("""
        <style>
        .stButton { margin: 0; }
        .stButton button { float: right; }
        .stButton {font-family:'Open Sans', sans-serif;font-weight:300;}
        </style>
    """, unsafe_allow_html=True)
    
    # Create columns layout
    col1, col2= st.columns([1,.1])

    # clear button
    with col1:
        st.button("Clear", type="secondary",on_click=clear_text)

    # search button
    with col2:
        if st.button("Search", type="primary",disabled=not st.session_state['sql_query']):
            try:
                with st.spinner("Loading data..."):
                    query = f"{st.session_state['sql_query']}"
                    if(validateQuery(query)):
                        st.session_state['df'] = session.sql(query).to_pandas()
            except Exception as e:
                st.toast(body=e, icon="❌")

# Display the data 
if st.session_state['df'] is not None:
    with st.container():
        try:
            with st.spinner("Wait for it..."):
                st.write(f"Search Results ({len(st.session_state['df'])})")
                st.dataframe(st.session_state['df'],use_container_width=True)
                st.toast(body="Successful query", icon="✅")
        except Exception as e:
            st.toast(body=e, icon="❌")
