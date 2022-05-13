import datetime
import re
from flask import Flask
from flask import request, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

def cleansed_email(email):
    """Gets email and apply some process to clean and check its validation

    Parameters
    ----------
    email : str
        The email to be checked

    Returns
    -------
    email_address: str
        variable just with username without some special characters
    domain_part: str
        variable with domain part after '@'
    email_valid: bool
        variable with a previous check about the email validation based at 2 rule
    """
    email_valid = True

    # remove comments from anyplace and white spaces
    email = re.sub('<.*?>|\(.*?\)', '', email.replace(" ", ""))
    domain, email_address, domain_part = '', '', ''

    # separed email address and domain with check about '@'
    if '@' in email:
        email_address, domain_part =  email.split('@')
    else:
        email_address, domain_part = email, False

    if domain_part:
        domain = domain_part.split('.')[0]
        if ('+' in email_address and not domain in ['outlook','gmail']) or ('.' in email_address and domain != 'gmail'):
            email_valid = False
        else:
            # remove dots and anything after +
            email_address = re.sub('\+.*?$', '', email_address.replace(".", ""))

    else:
        email_valid = False

    
    return email_address, domain_part, email_valid

def validation_domain(domain_part):
    """Gets domain part (string after '@') cleaned and check if follow 5 rule

    Parameters
    ----------
    domain_part : str
        domain part to be checked

    Returns
    -------
    domain_valid: bool
        variable with check response
    """

    domain_valid = True
    last_past = domain_part.split('.')[-1]
    print(last_past)

    if last_past.isalpha() and len(last_past) >= 2:
    
        # remove just allowed speciall characters and apply alphaumeric verification
        temp_domain = domain_part.replace("-","").replace(".", "")
        domain_valid = temp_domain.isalnum()
    else:
        domain_valid = False
    
    return domain_valid

def validation_username(email_address):
    """Gets user name cleaned and check if follow 6 rule

    Parameters
    ----------
    email_address : str
        user name addres to be checked

    Returns
    -------
    value bool
        return values True or False according with the rule check
    """

    # check character after special symbols
    symbols = ['.','_','-']
    for symb in symbols:
        if symb in email_address and email_address.index(symb) < len(email_address) - 1:
            pos = email_address.index(symb)+1
            if not email_address[pos].isalnum():
                return False
    
    # remove just allowed speciall characters and apply alphaumeric verification
    temp_email = re.sub('\.|_|-', '', email_address)
    return temp_email.isalnum()

def validation_process(email):
    """Gets email from router and start the validation process

    Parameters
    ----------
    email : str
        email row received by router

    Returns
    -------
    resp: dict
        Dictionary with parameters check and informations from API
    """
    resp = {}
    email_address, domain_part, email_valid = cleansed_email(email)
    domain_check = validation_domain(domain_part) if email_valid else False
    username_check = validation_username(email_address)
    timestamp = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    domain = domain_part.split('.')[0]

    resp['raw_email'] = email 
    resp['domain'] = domain
    resp['validation_timestamp'] = timestamp
    resp['domain_valid_indicator"'] = domain_check
    resp['username_valid_indicator"'] = username_check
    resp['cleansed_email'] = email_address+ ('@' + domain if email_valid else '')

    return resp

@app.route('/validationemail', methods=['POST'])
@cross_origin()
def validation_email():
    """API router with POST method

    Parameters
    ----------
    input : str
        email row sent from API consuming user

    Returns
    -------
    resp: json
        Json with informations and checks applieds from API
    """

    content = request.json
    resp = "Bad input argments, send the field 'input!'"

    if 'input' in content.keys():
        resp = validation_process(content['input'])
    
    return jsonify(resp)

if __name__ == '__main__':
    app.run(host= '0.0.0.0',debug=True)








