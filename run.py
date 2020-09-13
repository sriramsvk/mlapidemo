import sys
import os
from API import create_app
app = create_app()

'''running from Python'''
''' __name__ is default function that python when executing a code 
__main__ is default that will called. 
Below condition is to check program is called directly instead of import 
import numpy will execute numpy from another code'''

''' pip install flask-restful install the api required 
for buliting Flask REST API'''

if __name__ == '__main__':
    ## setting directory to current script directory ##
    #abspath = os.path.abspath(sys.argv[0])  # script path
    #dname = os.path.dirname(abspath)  # get directory name
    os.chdir('/APP')  # change path to script directory
    app.run(debug=True)
