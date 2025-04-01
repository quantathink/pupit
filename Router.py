from flask import Flask, request, jsonify

#import google.generativeai as genai

from inference import *
app = Flask(__name__)

'''
## Decoration Functions
@app.route('/gemini', methods=['POST'])
def chat_decor():
    data = request.json
    s = data.get('s')
    result = chat_func(s)
    return jsonify({'bot':result})
'''
import re

def clean_string(s):
    s = s.lower()  # Convert to lowercase
    s = re.sub(r'\W+', '', s)  # Remove special characters (non-alphanumeric)
    s = s.strip()
    return s


@app.route('/router', methods=['POST'])
def router_decor():
    data = request.json
    s = data.get('s')
    result = clean_string(router_func(s))
    return jsonify({'bot':result})

@app.route('/simple_answer', methods=['POST'])
def simple_answer_decor():
    data = request.json
    s = data.get('s')
    result = simple_answer(s)
    return jsonify({'bot':result})

@app.route('/garbage_clean', methods=['POST'])
def garbage_clean():
    clear_folder()
    return ""

@app.route('/secretary_mind', methods=['POST'])
def secretary_mind_decor():
    data = request.json
    s = data.get('s')
    Document = data.get('Document')
    routing_dict = data.get('routing_dict')

    result = secretary_mind(s, Document, routing_dict)
    return jsonify({'bot':result})

@app.route('/accountant_mind', methods=['POST'])
def accountant_mind_decor():
    data = request.json
    s = data.get('s')
    routing_dict = data.get('routing_dict')
    result = accountant_mind(s,routing_dict)
    return jsonify({'bot':result})

@app.route('/jarvis_mind', methods=['POST'])
def jarvis_mind_decor():
    data = request.json
    s = data.get('s')
    result = jarvis_mind(s)
    return jsonify({'bot':result})

@app.route('/youtuber_mind', methods=['POST'])
def youtuber_mind_decor():
    data = request.json
    s = data.get('s')
    result = convert_text_to_url(s)
    result = download_audio_as_mp3(result[0],result[1])
    return jsonify({'bot':result})

if __name__=='__main__':
    app.run(debug=True)