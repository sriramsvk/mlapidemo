# Resource indicates method that can be access via http methods for performing tasks or retriving information
# Resource will be defined as Class and within the class, different task to performed by each method
# Resource will be linked to END Points or URI. Refer init file
from flask_restful import Resource,reqparse
import numpy as np
import base64 # convert Image as Base 64
import cv2

### Class for Prediction ###

def ImageClass(i):
   PageType = {
       1 : 'HCFA',
       2 : 'UB',
       3: 'DENTAL',
       4: 'HCFASUPER',
       5: 'UBSUPER',
       6: 'MEDICARE',
       7: 'COB',
       8: 'ATTACH',
       9: 'BLANK',
       10: 'EOB',
       11: 'MEOB'
   }
   return PageType.get(i)

class ImagePredictClass(Resource):
    def __init__(self):
      	# Create a request parser
        parser = reqparse.RequestParser()
        #parser.add_argument("image", type=werkzeug.datastructures.FileStorage, help="Base64 encoded image string", required=True, location='files')
        # help defined the field level defintion validation. error can be listed as dictionary
        parser.add_argument("image", type=str,help="JPEG Base64 encoded image string", required=True, location='json')
        self.req_parser = parser
    def post(self):
        img = self.req_parser.parse_args(strict=True).get("image",None)
        if img:
            # reading image received in post
            # during request base64 file is converted as utf-8 decode string.
            # this is reversed when reading file for prediction
            img = img.encode("utf-8") # encode the string to base64.
            img64_decode = base64.decodebytes(img)
            ''' 
            img64_encode = base64.encodebytes(img)
            encoded_string = img64_encode.decode("utf-8")
            
            '''
            decode_img = open('predict_decode.jpg', 'wb')  # write file
            decode_img.write(img64_decode)
            decode_img.close()
            ##### Prediction ####
            from keras.models import load_model
            #import keras.backend.tensorflow_backend as tb
            #tb._SYMBOLIC_SCOPE.value=True
            imgmodel = load_model('imageclasscnn')  # loading saved model
            imgpath = "predict_decode.jpg"
            input_img = cv2.imread(imgpath, 0)
            resize_img = cv2.resize(input_img, (100, 100))
            reshape_img = resize_img.reshape(100, 100, 1)
            predict_img = np.array(reshape_img)
            predict_img = predict_img / 255
            predict_img = predict_img.reshape(1, 100, 100, 1)
            imclass = imgmodel.predict(predict_img)
            page_type=ImageClass(np.argmax(imclass))
            predict_accuarcy=str(round(float(np.max(imclass)*100),2))+"%"
            return {'Page Type':page_type,'Prediction Accuarcy':predict_accuarcy ,'status':'success'},201
        else:
            return {'status':'Invalid Request'},400