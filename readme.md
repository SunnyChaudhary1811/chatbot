Company Performance Insights with Streamlit
This Streamlit application extracts company performance information from user queries and presents it in a structured JSON format.
-------------------------------------------------------------------------------------------------------------------------------------

Features
Extracts Company Names: Identify and extract company names from user queries.
Performance Metrics: Gather and display various performance metrics.
Date Handling: Manage and interpret relative dates (e.g., "today", "one year ago") and convert them into absolute dates.
JSON Output: Display the extracted information in a structured JSON format for easy reading and integration.
---------------------------------------------------------------------------------------------------------------------------------------

Requirements
langchain_core
langchain_community
streamlit
dotenv
Ollama (for LLM access)
Installation
Install the required libraries:
---------------------------------------------------------------------------------------------------------------------------------------
pip install -r requirements.txt
---------------------------------------------------------------------------------------------------------------------------------------

Set up a .env file with your LANGCHAIN_API_KEY:
makefile

LANGCHAIN_API_KEY=your_api_key_here
---------------------------------------------------------------------------------------------------------------------------------------
Run Streamlit Application
streamlit run chatbot.py
----------------------------------------------------------------------------------------------------------------------------------------
Usage
Enter your question in the text input box.
Click "Enter" or submit the query.
View the extracted information displayed in JSON format.
Example Query
Question: What is the recent performance of Apple and Google?
-----------------------------------------------------------------------------------------------------------------------------------------
Results
Extracted Information
JSON Output
-----------------------------------------------------------------------------------------------------------------------------------------
Deployment
This application is deployed on the Streamlit cloud platform, which provides single-click deployment.
------------------------------------------------------------------------------------------------------------------------------------------
Model Performance
Using a locally installed llama2 open-source model, the application occasionally provides inaccurate results. Processing each query may take 1-2 minutes due to system specifications.
------------------------------------------------------------------------------------------------------------------------------------------
Additional Notes
The code utilizes ChatPromptTemplate to define the interaction between the user and the LLM.
StrOutputParser parses the LLM's output for relevant information.
Ollama is used to access the LLM (replace "llama2" with your desired model if needed).
Streamlit creates the interactive web app.
The script handles relative dates and converts them to absolute formats.
Context is stored in the session state to keep track of previous queries and extracted information.
Example Visualization
To give you a better understanding of the application's capabilities, here's a simple visualization:

Streamlit Application URL
Streamlit App

http://192.168.84.33:8501/ 