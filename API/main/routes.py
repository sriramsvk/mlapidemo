from flask import render_template,Blueprint

main = Blueprint('main',__name__) # create instance

'''
instead of registering as posts, we will register the route in name of blue print. 
this blue print name will be registered with APP 
'''

''' both / or /home to root page '''
'''additional routing pages'''
@main.route("/")
@main.route("/about")
def about():
    return render_template('about.html',title='About')

@main.route("/AboutImageClass")
def aboutImageclass():
    samplerequest = {
        'Image': 'base64 string of the image'}
    return render_template('Imagepredict.html',samplerequest=samplerequest)

@main.route("/AboutEnrollreview")
def aboutEnrollreview():
    samplerequest = {
        "Applicant Name": "String",
        "Applicant MartialStatus": "S - Single M - Married, P - Parternship",
        "Applicant Reside of State": "Y or N ",
        "Applicant Prior Coverage": "Y or N",
        "Applicant Medicare Eligible": " Y or N",
        "Applicant DomesticPartner": "Y or N",
        "Applicant Age": "INT",
        "Spouse": "Y or N"
    }
    return render_template('enrollpredict.html',samplerequest=samplerequest)

@main.route("/AboutUTreview")
def aboutUTreview():
    samplerequest = {
    "Report Finding": "String"
    }
    return render_template('utreview.html',samplerequest=samplerequest)

