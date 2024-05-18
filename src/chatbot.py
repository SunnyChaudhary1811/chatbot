from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama
import streamlit as st
import os
from dotenv import load_dotenv
import datetime
import json
import re

# Load environment variables
load_dotenv()

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "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"

# Define the prompt template for extracting information
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Extract the company names, performance metrics, start date, and end date from the user query. Return the information in the following format for each company and metric: 'Company: [company], Metric: [metric], Start Date: [YYYY-MM-DD], End Date: [YYYY-MM-DD]'. If the dates are not mentioned, assume the start date as one year ago from today and the end date as today."),
        ("user", "Question: {question}")
    ]
)

# Define the function to parse extracted information
def parse_extracted_information(extracted_info):
    pattern = re.compile(r'Company: (.*?), Metric: (.*?), Start Date: (.*?), End Date: (.*?)')
    matches = pattern.findall(extracted_info)
    info_list = []
    
    for match in matches:
        info_dict = {
            "entity": match[0].strip(),
            "parameter": match[1].strip(),
            "start_date": match[2].strip(),
            "end_date": match[3].strip()
        }
        info_list.append(info_dict)
    
    return info_list

# Define the function to handle default dates and convert relative dates
def handle_default_dates(info_list):
    today = datetime.date.today()
    one_year_ago = today - datetime.timedelta(days=365)
    
    def parse_relative_date(date_str):
        if not date_str or "today" in date_str.lower():
            return today.isoformat()
        elif "yesterday" in date_str.lower():
            return (today - datetime.timedelta(days=1)).isoformat()
        elif "one year ago" in date_str.lower():
            return one_year_ago.isoformat()
        try:
            return datetime.datetime.strptime(date_str, "%Y-%m-%d").date().isoformat()
        except ValueError:
            return None
    
    for info_dict in info_list:
        start_date = parse_relative_date(info_dict['start_date'])
        end_date = parse_relative_date(info_dict['end_date'])
        
        info_dict['start_date'] = start_date if start_date else one_year_ago.isoformat()
        info_dict['end_date'] = end_date if end_date else today.isoformat()
    
    return info_list

# Define the function to extract company names from the user query
def extract_company_names(query):
    # Simple heuristic to find company names
    # Assume company names are capitalized and may appear after specific keywords
    companies = re.findall(r'\b[A-Z][a-zA-Z]*\b', query)
    return set(companies)

# Define the function to filter results for specific companies
def filter_results(info_list, companies):
    return [info for info in info_list if info['entity'].lower() in [c.lower() for c in companies]]

# Define the function to convert the information to JSON format
def convert_to_json(info_list):
    return json.dumps(info_list, indent=4)

# Initialize the Streamlit app
st.title('Company Performance Insights')
input_text = st.text_input("Ask me anything")

# Initialize the LLM (using Ollama's LLaMA2)
llm = Ollama(model="llama2")
output_parser = StrOutputParser()
chain = prompt | llm | output_parser

# Initialize context to keep track of previous queries
if "context" not in st.session_state:
    st.session_state.context = []

# Process the user query and display the JSON output
if input_text:
    try:
        extracted_info = chain.invoke({"question": input_text})
        parsed_info = parse_extracted_information(extracted_info)
        info_with_dates = handle_default_dates(parsed_info)
        
        # Extract company names from user query
        companies = extract_company_names(input_text)
        
        # Filter results for the extracted companies
        filtered_info = filter_results(info_with_dates, companies)
        
        # Update context with new information
        st.session_state.context.extend(filtered_info)
        
        json_output = convert_to_json(st.session_state.context)
        st.write(json_output)
    except Exception as e:
        st.error(f"An error occurred: {e}")

