from flask import Flask,render_template,url_for,request
from werkzeug.utils import secure_filename
from keras.models import load_model
from keras.preprocessing.image import image
import numpy as np
import os
from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession



app = Flask(__name__)
app.config['upimg'] = os.path.join('uploads')

model1 = load_model("my_trained.h5")

def img_predict(pat,model):
    
    load_img = image.load_img(pat,target_size=(140,140))
    imgg = image.img_to_array(load_img)
    imgg = np.expand_dims(imgg, axis = 0)
    pred = model.predict(imgg)
    pred = pred[0]
    return str(pred)
    

@app.route("/")
def home():
    return render_template('new.html')

@app.route("/predict", methods = ['POST', 'GET'] )
def predict():
    if request.method == 'POST':
        fil = request.files['file']
        bas_path = os.path.dirname(__file__)
        fil_path = os.path.join(bas_path,'uploads',secure_filename(fil.filename))
        
        if not os.path.exists('uploads'):
            os.mkdir('uploads')
        
        fil.save(fil_path)
        
       
        preds = img_predict(fil_path, model1)
        
        if preds[1] == '0':
            opp = 'Face Mask Found!'
        
        else:
           opp = 'Face Mask Not Found'
        
        
        return opp
    return None
    
    
    
    
    
    
if __name__ =='__main__':
    app.run(debug = True)
    
