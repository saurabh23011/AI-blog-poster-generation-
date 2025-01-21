
from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from openai import OpenAI  # Updated import for latest OpenAI

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize OpenAI client with API key from environment variable
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    topic = data.get('topic')
    
    if not client.api_key:
        return jsonify({'error': 'API key not found in environment variables'}), 500
    
    try:
        prompt = f"""
        As an experienced startup and venture capital writer, 
        generate a 400-word blog post about '{topic}'
        
        Your response should be in this format:
        First, print the blog post.
        Then, sum the total number of words in it and print the result like this: This post has X words.
        """
        
        # Using the latest OpenAI API syntax
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=2048,
            temperature=0.7
        )
        
        # Extract the generated text
        generated_text = response.choices[0].message.content
        
        return jsonify({'response': generated_text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)