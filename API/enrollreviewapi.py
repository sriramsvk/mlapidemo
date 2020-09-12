# Resource indicates method that can be access via http methods for performing tasks or retriving information
# Resource will be defined as Class and within the class, different task to performed by each method
# Resource will be linked to END Points or URI. Refer init file
from flask_restful import Resource, reqparse
import numpy as np
import pandas as pd
import sklearn

class enrollstatus(Resource):
    def __init__(self):
        # Create a request parser
        parser = reqparse.RequestParser()
        # parser.add_argument("image", type=werkzeug.datastructures.FileStorage, help="Base64 encoded image string", required=True, location='files')
        # help defined the field level defintion validation. error can be listed as dictionary
        parser.add_argument("Applicant Name", type=str, help="string", required=True, location='json')
        parser.add_argument("Applicant MartialStatus", type=str, help="S - single , M- Married , P - Partnership", required=True,
                            location='json')
        parser.add_argument("Reside of State", type=bool, help="Y / N",
                            required=True,
                            location='json')
        parser.add_argument("Applicant Prior Coverage", type=bool, help="Y if enrolled with same plan previous else N",
                            required=True,
                            location='json')
        parser.add_argument("Applicant Medicare Eligible", type=bool, help="Y if eligible for Medicare coverage else N",
                            required=True,
                            location='json')
        parser.add_argument("Applicant Domestic Partner", type=bool,
                            help="Y with Domestic Partner  else N",
                            required=True,
                            location='json')
        parser.add_argument("Spouse", type=bool,
                            help="Y with Spouse  else N",
                            required=True,
                            location='json')
        parser.add_argument("Applicant Age", type=int,
                            help="Y with Spouse  else N",
                            required=True,
                            location='json')
        self.req_parser = parser

    def post(self):
        applicant_name = self.req_parser.parse_args(strict=True).get("Applicant Name", None)
        print(applicant_name)
        applicant_martialstatus = self.req_parser.parse_args(strict=True).get("Applicant MartialStatus", None)
        print( applicant_martialstatus)
        state_resident = self.req_parser.parse_args(strict=True).get("Reside of State", None)
        print(state_resident)
        prior_coverage = self.req_parser.parse_args(strict=True).get("Applicant Prior Coverage", None)
        print(prior_coverage)
        medicare_eligible = self.req_parser.parse_args(strict=True).get("Applicant Medicare Eligible", None)
        print(medicare_eligible)
        partner = self.req_parser.parse_args(strict=True).get("Applicant Domestic Partner", None)
        print(partner)
        spouse = self.req_parser.parse_args(strict=True).get("Spouse", None)
        print(spouse)
        applicant_age = self.req_parser.parse_args(strict=True).get("Applicant Age",None)
        print(str(applicant_age))
        if (applicant_name and applicant_martialstatus and state_resident and prior_coverage and medicare_eligible
        and partner and spouse and applicant_age) :
            # preprocessing the data
            applicant_martialstatus =  0 if applicant_martialstatus=='M' else (1 if applicant_martialstatus=='P' else 2)
            print(applicant_martialstatus)
            state_resident = 1 if state_resident == True else 0
            print(state_resident)
            prior_coverage = 1 if prior_coverage == True else 0
            print(prior_coverage)
            medicare_eligible = 1 if medicare_eligible == True else 0
            print(medicare_eligible)
            partner= 1 if partner == True else 0
            print(partner)
            spouse =  1 if spouse == True else 0
            print(spouse)
            #applicant_age = int(applicant_age)
            #### convert to data Frame ####
            x_pred = pd.DataFrame ({'AppliMartialStatus':applicant_martialstatus,
                                      'AppliResideCA':state_resident,
                                     'AppliPriorBSCCoverage':prior_coverage,
                                     'AppliMedicareEligible':medicare_eligible,
                                     'AppliDomesticPartner':partner,
                                     'Applicant Age':str(applicant_age),
                                      'Spouse?':spouse},index=[0])
            print(x_pred)
            ##### Prediction ####
            import pickle
            modelname = 'enroll_reviews.sav'
            reviewlogmodel = pickle.load(open(modelname, 'rb'))
            y_pred = reviewlogmodel.predict(x_pred)
            y_pred_prob = reviewlogmodel.predict_proba(x_pred)
            enroll_status = 'Approved' if y_pred == 0 else 'Not approved'
            predict_accuarcy = str(round(float(np.max(y_pred_prob) * 100), 2)) + "%"
                
            return {'Enrollment Status': enroll_status, 'Prediction Accuarcy': predict_accuarcy, 'status': 'success'}, 201
        else:
            return {'status': 'Invalid Request'}, 400