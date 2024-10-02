from flask import Flask, render_template, request
import cohere
import re
import os  # Import os to handle environment variables
from urllib.parse import quote 
app = Flask(__name__)

# Use environment variable for the API key for better security
cohere_api_key = os.getenv('iHuAKEAXeX9kbpntvNA3x0BICUiBHtINYU5rho93')
co = cohere.Client(cohere_api_key)

# Initialize conversation history
conversation_history = []

@app.route('/')
def index():
    global conversation_history
    conversation_history = []  # Clear the history on app start
    return render_template('index.html', conversation=conversation_history)

@app.route('/submit', methods=['POST'])
def submit():
    query = request.form['query']
    response = co.generate(model='command-r-08-2024', prompt=query, max_tokens=300)
    result = response.generations[0].text.strip()

    # Add to conversation history
    conversation_history.append({"query": query, "result": format_code_blocks(result)})

    return render_template('index.html', conversation=conversation_history)

def format_code_blocks(text):
    code_pattern = r'```(.*?)```'
    formatted_text = re.sub(code_pattern, r'<pre><code>\1</code><button class="copy-button">Copy</button></pre>', text, flags=re.DOTALL)
    return formatted_text

if __name__ == '__main__':
    app.run(debug=True)
