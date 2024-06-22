from crewai import Crew
import os
import requests
import json
from google.oauth2.credentials import Credentials as OAuth2Credentials
import vertexai
from vertexai.preview.generative_models import GenerativeModel
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
from langchain_core.callbacks import BaseCallbackHandler
from typing import TYPE_CHECKING, Any, Dict
from crewai_tools import SerperDevTool
import streamlit as st
from langchain.utilities.tavily_search import TavilySearchAPIWrapper
from langchain.tools.tavily_search import TavilySearchResults       


# # set up the agent
os.environ["TAVILY_API_KEY"] = "xxxxx"
# set up the agent
tavily_tool = TavilySearchResults()

 
# Initialize the Gemini tool, here is just demo code.
gemini_llm = GeminiTool(
    model_name=os.environ["MODEL_NAME"],
    auth_url=os.environ["AUTH_URL"]
)

# UI
import streamlit as st

st.title("💬 Finance Watch")
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Finance Watch is a tool to gather the latest Finance news, risk model updates, and emerging trends for a specified Asset Class. Please provide the practice area that you are interested in."}]

# Display existing messages
for msg in st.session_state.messages:
    if msg["role"] == "assistant":
        st.markdown(f"**Assistant**: {msg['content']}")

# Setup columns for the layout: input on the left, results on the right
left_col, right_col = st.columns([1, 2])
with left_col:
    asset_class = st.text_input("Asset Class")
    market_data_feed = st.text_input("Market Data Feed")
    risk_models = st.text_input("Risk Models")
    
    submit_button = st.button("Submit")
    
    # Example user inputs
    inputs = {
        'asset_class': asset_class,
        'market_data_feed': market_data_feed,
        'risk_models': risk_models
    }

with right_col:
    # Results section
    # Handle user input
    if submit_button:
        user_message = f"Asset Class: {asset_class}, Market Data Feed: {market_data_feed}, Risk Models: {risk_models}"
        st.session_state.messages.append({"role": "user", "content": user_message})
        st.markdown(f"**User**: {user_message}")

        # Define the Research Agent
        research_agent = Agent(
            role='Finance Researcher',
            goal='Discover and compile the latest finance news, market updates, and trends for {asset_class} in {market_data_feed}, focusing on {risk_models}.',
            verbose=True,
            memory=False,
            llm=gemini_llm,  
            backstory=(
                "As a dedicated finance researcher, you excel in finding and compiling "
                "relevant finance information that keeps finance professionals informed about the latest developments in their practice area. "
                "Please pass your search result in JSON format to your co-work, ensure the content to"
                "be enclosed in curly braces and use double quotes for keys and values."
            ),
            #tools=[search_tool],
            tools=[tavily_tool],
            allow_delegation=True
        )

        # Define the Summarization Agent
        summarization_agent = Agent(
            role='Finance Summarizer',
            goal='Summarize the compiled finance information into easily digestible formats for {asset_class}.',
            verbose=True,
            memory=False,
            llm=gemini_llm,  
            backstory=(
                "As an expert in distilling complex finance information, you create concise and clear summaries "
                "that help finance professionals quickly grasp key updates and insights."
                "Please pass your search result in JSON format to your co-work, ensure the content to"
                "be enclosed in curly braces and use double quotes for keys and values."
            ),
            #tools=[search_tool],
            tools=[tavily_tool],
            allow_delegation=True
        )

        # Define the Research Task
        research_task = Task(
            description=(
                "Gather the latest finance news, market updates, and emerging trends for {asset_class} in {market_data_feed}. "
                "Focus on finding information relevant to {risk_models}. Your final report should include a comprehensive summary "
                "of key updates and trends. Include refrences to the original sources (URLs) in the summary"
            ),
            expected_output=(
                "A detailed report containing the latest updates and trends relevant to the specified practice area, market_data_feed, and risk models."
                "Please pass your search result in JSON format to your co-work, ensure the content to"
                "be enclosed in curly braces and use double quotes for keys and values."),
            #tools=[search_tool],
            tools=[tavily_tool],
            agent=research_agent
        )

        # Define the Summarization Task
        summarization_task = Task(
            description=(
                "Summarize the detailed report provided by the research task into key highlights. "
                "Ensure that the summary is concise and easy to understand, highlighting the most important developments."
            ),
            expected_output='A concise summary of the gathered information, highlighting key updates and insights. The summary must include refernces to orginal sources (URLs)',
            #tools=[search_tool],
            tools=[tavily_tool],
            agent=summarization_agent,
            async_execution=False,
            output_file='summary.txt'
        )

   
        # Form the Crew and kick it off
        crew = Crew(
            agents=[research_agent, summarization_agent],
            tasks=[research_task, summarization_task],
            process=Process.sequential
        )

        result = crew.kickoff(inputs=inputs)
        final = f"## Here is the Final Result \n\n {result}"
        st.session_state.messages.append({"role": "assistant", "content": final})
        st.chat_message("assistant").write(result)



