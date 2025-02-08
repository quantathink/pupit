from flask import Flask, request, jsonify

#import google.generativeai as genai

from inference import *
app = Flask(__name__)


## Decoration Functions
@app.route('/gemini', methods=['POST'])
def chat_decor():
    data = request.json
    s = data.get('s')
    result = chat_func(s)
    return jsonify({'bot':result})

@app.route('/router', methods=['POST'])
def router_decor():
    data = request.json
    s = data.get('s')
    result = router_func(s)
    print('from router_decor...: ', result)
    if result.strip() == 'YOUTUBER':
        print('it is youtuber')
        result = convert_text_to_url(s)
        result = download_audio_as_mp3(result[0],result[1])
        print(result)
    elif result.strip() == 'NORMAL CHAT':
        result = chat_func(s)
    return jsonify({'bot':result})


if __name__=='__main__':
    app.run(debug=True)