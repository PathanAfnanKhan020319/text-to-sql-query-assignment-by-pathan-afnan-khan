import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_community.utilities import SQLDatabase
import os
from dotenv import load_dotenv
import json
import re

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Text-to-SQL Data Query Assistant",
    page_icon="🔍",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        background-color: #0a0e27;
    }
    .stTextArea textarea {
        background-color: #1e2139;
        color: white;
    }
    h1 {
        color: white;
    }
    .subtitle {
        color: #a0a0a0;
        font-size: 18px;
        margin-bottom: 30px;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'history' not in st.session_state:
    st.session_state.history = []

class TextToSQLAgent:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = sqlite3.connect(db_path, check_same_thread=False)

        # 🔥 OPENAI MODEL (FINAL FIX)
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
            api_key=os.getenv("OPENAI_API_KEY")
        )

        self.db = SQLDatabase.from_uri(f"sqlite:///{db_path}")
        
    def get_schema_info(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        schema_info = []
        for table in tables:
            table_name = table[0]
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            schema_info.append({
                "table": table_name,
                "columns": [col[1] for col in columns]
            })
        return schema_info
    
    def generate_sql_query(self, user_query):
        schema = self.get_schema_info()
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a SQL expert. Convert the user's natural language query into a valid SQLite query.

Database Schema:
{schema}

Rules:
1. Generate ONLY the SQL query, no explanations
2. Use proper SQLite syntax
3. Return only SELECT statements
4. Use appropriate JOINs when needed
5. Include LIMIT clause if not specified (default LIMIT 100)
6. Use meaningful aliases for readability

Return ONLY the SQL query without any formatting or backticks."""),
            ("human", "{query}")
        ])
        
        chain = prompt | self.llm
        response = chain.invoke({
            "schema": json.dumps(schema, indent=2),
            "query": user_query
        })
        
        sql_query = response.content.strip()
        sql_query = re.sub(r'^```sql\s*|\s*```$', '', sql_query, flags=re.MULTILINE).strip()
        
        return sql_query
    
    def execute_query(self, sql_query):
        try:
            df = pd.read_sql_query(sql_query, self.connection)
            return df, None
        except Exception as e:
            return None, str(e)
    
    def should_generate_chart(self, user_query, df):
        if df is None or len(df) == 0:
            return False, None, None, None
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a data visualization expert. Analyze if the user's query and data require a chart.

Data columns: {columns}
Data shape: {shape}
First few rows: {sample_data}

Response format (JSON only):
{{
    "should_plot": true/false,
    "chart_type": "bar/line/pie" or null,
    "x_axis": "column_name" or null,
    "y_axis": "column_name" or null
}}"""),
            ("human", "Query: {query}")
        ])
        
        chain = prompt | self.llm
        response = chain.invoke({
            "columns": list(df.columns),
            "shape": df.shape,
            "sample_data": df.head(3).to_dict(),
            "query": user_query
        })
        
        try:
            content = response.content.strip()
            content = re.sub(r'^```json\s*|\s*```$', '', content, flags=re.MULTILINE)
            result = json.loads(content)
            return (
                result.get("should_plot", False),
                result.get("chart_type"),
                result.get("x_axis"),
                result.get("y_axis")
            )
        except:
            return False, None, None, None
    
    def create_chart(self, df, chart_type, x_col, y_col):
        try:
            if chart_type == "bar":
                fig = px.bar(df, x=x_col, y=y_col)
            elif chart_type == "line":
                fig = px.line(df, x=x_col, y=y_col)
            elif chart_type == "pie":
                fig = px.pie(df, names=x_col, values=y_col)
            else:
                fig = px.bar(df, x=x_col, y=y_col)
            
            fig.update_layout(template="plotly_dark", height=400)
            return fig
        except:
            return None

# Main UI
st.title("🔍 Text-to-SQL Data Query Assistant")
st.markdown('<p class="subtitle">Ask questions about your data in natural language</p>', unsafe_allow_html=True)

@st.cache_resource
def get_agent():
    db_path = "data/chinook.db"
    if not os.path.exists(db_path):
        st.error("Database file not found! Place chinook.db in /data folder.")
        st.stop()
    return TextToSQLAgent(db_path)

agent = get_agent()

st.subheader("User Query")
user_query = st.text_area("", placeholder="e.g., Show me the top 10 best-selling tracks", height=100, label_visibility="collapsed")

col1, col2, col3 = st.columns([1, 1, 4])
with col1:
    submit_button = st.button("Submit Query", type="primary", use_container_width=True)
with col2:
    clear_button = st.button("Clear", use_container_width=True)

if clear_button:
    st.rerun()

if submit_button and user_query:
    with st.spinner("Processing your query..."):
        sql_query = agent.generate_sql_query(user_query)
        st.subheader("Generated SQL Query")
        st.code(sql_query, language="sql")
        
        df, error = agent.execute_query(sql_query)
        
        if error:
            st.error(f"Error executing query: {error}")
        else:
            st.subheader("Query Results")
            st.dataframe(df, use_container_width=True, height=300)

            should_plot, chart_type, x_col, y_col = agent.should_generate_chart(user_query, df)
            
            if should_plot and chart_type and x_col and y_col:
                if x_col in df.columns and y_col in df.columns:
                    plot_df = df.head(50) if len(df) > 50 else df
                    fig = agent.create_chart(plot_df, chart_type, x_col, y_col)
                    if fig:
                        st.subheader("Visualization")
                        st.plotly_chart(fig, use_container_width=True)

with st.sidebar:
    st.header("📝 Example Queries")
    examples = [
        "How many customers are in each country?",
        "Show me the top 10 best-selling tracks",
        "What is the total sales by genre?",
        "Which customers spent the most?",
        "Show revenue by year"
    ]
    for example in examples:
        if st.button(example, key=example, use_container_width=True):
            st.session_state.user = example
            st.rerun()
