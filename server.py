from flask import Flask, jsonify, request
import pickle
import numpy as np
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 

filename = 'Back/Final_Model.sav'
load_model = pickle.load(open(filename, 'rb'))

def predict(question):
  data_1d = np.array(question)
  data_2d = data_1d.reshape(1, -1)
  y_pred = load_model.predict(data_2d)
  if(y_pred[0]==1):
     return "Churned"
  else:
    return "Not Churned"
  
sample = [63, 17, 73.36, 236, 0, 1, 0, 0, 1, 0, 0]    
sample2 = [36, 3, 97.94, 297, 1, 0, 0, 0, 0, 1, 0]   

data=predict(sample) 

@app.route('/', methods = ['GET', 'POST'])
def home():
    if(request.method == 'GET'):
      data = "hello world"
      return jsonify({'data': data})

@app.route('/api_endpoint', methods=['POST'])
def api_endpoint():
    try:
        
        data = request.get_json()
        Predict_This = []

        name = data.get('name')
        age = data.get('age')
        gender = data.get('gender')
        location = data.get('location')
        subscription = data.get('subscription')
        monthly = data.get('monthly')
        usage = data.get('usage')
        
        if(gender.lower() == "male"):
           genderCollection = [0,1]
        else:
           genderCollection = [1,0]

        Predict_This = [age, subscription,monthly,usage]+ genderCollection + [0, 0,	1,	0,	0 ]
        response = predict(Predict_This)

        response_message = response
        return jsonify({'message': response_message}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400



if __name__ == '__main__':
    app.run(debug=True)