from flask import Flask, request, jsonify

app = Flask(__name__)


## Main Functions
def lower_case(s):
    print('loweringCase...')
    return s.lower()

def add_numbers(a,b):
    print('Addition...')
    return a+b

def mult_numbers(a,b):
    print('Multiplying...')
    return a*b


## Decoration Functions
@app.route('/add', methods=['POST'])
def add():
    data = request.json
    a = data.get('a')
    b = data.get('b')
    result = add_numbers(a,b)
    return jsonify({'sum':result})
@app.route('/mult', methods=['POST'])
def mult():
    data = request.json
    a = data.get('a')
    b = data.get('b')
    result = mult_numbers(a,b)
    return jsonify({'mult':result})
@app.route('/lower', methods=['POST'])
def lower():
    data = request.json
    s = data.get('s')
    result = lower_case(s)
    return jsonify({'lower':result})

if __name__=='__main__':
    app.run(debug=True)