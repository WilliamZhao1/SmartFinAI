# Finance Watch

Finance Watch is a tool that leverages the power of AI to gather the latest finance news, risk model updates, and emerging trends for a specified Asset Class. This README file will guide you through the setup and usage of the Finance Watch application.

![image (1)](https://github.com/WilliamZhao1/SmartFinAI/assets/71152785/abf4fa87-e239-4aaf-a739-e25b503876e2)


## Setup

1. **Environment Variables**
   - Set up your environment variables. You will need an API key for Tavily Search. 
   os.environ["TAVILY_API_KEY"] = "xxxxx"
   
2. Dependencies
Install the necessary dependencies using pip:
pip install streamlit crewai vertexai langchain tavily-search

3.Gemini Tool
Initialize the Gemini tool with your model name and auth URL. This is just demo code, replace it with your actual Gemini tool initialization.
     gemini_llm = GeminiTool(
         model_name=os.environ["MODEL_NAME"],
         auth_url=os.environ["AUTH_URL"]
     )

## Usage

1. **User Input**
   - Enter the Asset Class, Market Data Feed, and Risk Models you are interested in.

2. **Submit**
   - Click the 'Submit' button to initiate the research and summarization process.

3. **Results**
   - The AI will gather and summarize the latest finance news, market updates, and trends based on your input. The results will be displayed in the 'Results' section.

## Architecture

The application uses two main AI agents:

1. **Finance Researcher**
   - This agent is responsible for discovering and compiling the latest finance news, market updates, and trends based on the user's input.

2. **Finance Summarizer**
   - This agent summarizes the compiled finance information into easily digestible formats.

The two agents work sequentially in a 'Crew' to provide the user with the latest and most relevant finance information.

## Note

Please ensure that all your inputs are accurate and relevant. The quality of the output depends largely on the quality of the input.

For any issues or suggestions, please open an issue in this repository.

Happy finance watching!
