# Resource indicates method that can be access via http methods for performing tasks or retriving information
# Resource will be defined as Class and within the class, different task to performed by each method
# Resource will be linked to END Points or URI. Refer init file
from flask_restful import Resource,reqparse
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
import re
import numpy as np
REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;:]')  # re.complie is method combine list of value you search in a string
BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')
MAX_SEQUENCE_LENGTH = 250
MAX_NB_WORDS = 50000
def clean_text(text):
    """
        text: a string
        return: modified initial string
    """
    text = text.lower()  # lowercase text
    text = REPLACE_BY_SPACE_RE.sub(' ',
                                   text)  # replace REPLACE_BY_SPACE_RE symbols by space in text. substitute the matched string in REPLACE_BY_SPACE_RE with space.
    text = BAD_SYMBOLS_RE.sub('',
                              text)  # remove symbols which are in BAD_SYMBOLS_RE from text. substitute the matched string in BAD_SYMBOLS_RE with nothing.
    text = text.replace('x', '')  # replace value with new one. in this example replace "x" with space
    #    text = re.sub(r'\W+', '', text)
    text = ' '.join(word for word in text.split() if word not in STOPWORDS)  # remove stopwors from text
    return text

class UTreviewpredict(Resource):
    def __init__(self):
      	# Create a request parser
        parser = reqparse.RequestParser()
       # help defined the field level defintion validation. error can be listed as dictionary
        parser.add_argument("Report Finding", type=str,help="Details of  Patient case history ", required=True, location='json')
        self.req_parser = parser

    def post(self):
        finding = self.req_parser.parse_args(strict=True).get("Report Finding", None)
        if finding:
            ''' pre processing '''
            x_pred = finding
            #x_pred = clean_text(x_pred)
            #print(x_pred)
            from keras.preprocessing.text import Tokenizer
            from keras.preprocessing.sequence import pad_sequences
            tokenizer = Tokenizer(num_words=MAX_NB_WORDS, filters='!"#$%&()*+,-./:;<=>?@[\]^_`{|}~',
                                  lower=True)  # assign words or text to numeric index

            x_pred = tokenizer.texts_to_sequences(x_pred)
            x_pred = pad_sequences(x_pred, maxlen=MAX_SEQUENCE_LENGTH)

            ##### Prediction ####
            from keras.models import load_model
            lstm_model = load_model('./APP/utreview-lstmmodel.h5')
            y_pred = lstm_model.predict_proba(x_pred)
            y_predclass = lstm_model.predict_classes(x_pred)
            labels = ['Overturned Decision of Health Plan', 'Upheld Decision of Health Plan']
            decision = labels[np.argmax(y_predclass)]
            print(np.max(y_pred))
            accuarcy = str(round(float(np.max(y_pred)*100),2)) + "%"

            return {'Review status':  decision, 'Prediction Accuarcy':accuarcy , 'status': 'success'}, 201
        else:
            return {'status': 'Invalid Request'}, 400
