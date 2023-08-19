import json
import os
import streamlit as st
import pandas as pd
from langchain.llms import OpenAI
from tempfile import NamedTemporaryFile
from streamlit_chat import message
from langchain.agents import create_csv_agent
from flask import Flask, request,jsonify

app = Flask(__name__)

file = r"diabetes.csv"
open_api_key = "Enter your api key"

def get_answer(file,query):
    """Getting the answer for the user query."""
    if file is not None:
        llm = OpenAI(openai_api_key=open_api_key,temperature=0)
        agent = create_csv_agent(llm, file, verbose=True)
        if query:
            answer = agent.run(query)
    return answer

@app.route('/start', methods=['POST'])
def start():
    """processing the query."""
    request_data = request.get_json()
    query = request_data["query"]
    answer = get_answer(file,query)
    return jsonify({'query': query,'answer': answer})

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=8000)
