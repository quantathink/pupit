from flask import Flask, request, jsonify

app = Flask(__name__)

# Google Gemini
import google.generativeai as genai

genai.configure(api_key='AIzaSyCZ6Hp1HC4K13xXncG55w9TyaibrjuiOPc')
model = genai.GenerativeModel("gemini-1.5-flash")

class chatHistory:
    def __init__(self, max_length=30):
        self.history = []  # List to store chat messages
        self.max_length = max_length  # Maximum allowed length of the history
    def add_message(self, dictionary):
        self.history.append(dictionary)
        if len(self.history) > self.max_length:
            self.history.pop(0)
    def get_history(self):
        return self.history

chat = chatHistory()
## Main Functions
def chat_func(s):
    chat_history = chat.get_history()
    #print(chat_history)
    prompt = f'Your name is Alfred, Please answer {s} also this is the chat histroy for you review if needed: {chat_history}'
    response = model.generate_content(prompt)
    print(response.text)
    hist_dict = {'user':s,'Alfred':response.text}
    chat.add_message(hist_dict)
    print('My question: ', chat_history)
    return response.text

'''    
    try:
        response = model.generate_content(prompt)
        hist_dict = {'user':s,'Alfred':response.text}
        chat_history.add_message(hist_dict)

        print('My question: ', chat_history)
    except:
        print(response)
        response = {'text':'I am sorry I am getting an error from Gemnini, lete check later'}
    chat.add_message({
        "User":prompt,
        "Alfred":response
     })
    return response.text
'''

## Decoration Functions
@app.route('/gemini', methods=['POST'])
def chat_decor():
    data = request.json
    s = data.get('s')
    result = chat_func(s)
    return jsonify({'bot':result})

if __name__=='__main__':
    app.run(debug=True)