from flask import Flask, request, jsonify 
from data.yahoo_finance import top_five_day_over_day
from user.properties import authenticate_user
import base64

app = Flask(__name__)


@app.route("/sampleAPI/analysis", methods=['GET'])
def sampleAPI():
    #Usage: Returns top five day over day values for the tickers and range value passed in as a parameter 

    #Step 1: Authenticate users using basic authentication. Hashed usernames and passwords are stored in a dictionary in user.properties
    auth = request.headers.get('Authorization')
    if auth and auth.startswith('Basic '):
        auth = auth.replace('Basic ', '')
        try:
            auth = base64.b64decode(auth).decode('utf-8')
            username, password = auth.split(':') 
            if not authenticate_user(username, password)["authenticated"]:
                return jsonify({'error': 'Unauthorized'}), 401
        except:
            return jsonify({'error': 'Invalid authentication credentials'}), 401
    else:
        return jsonify({'error': 'Basic authorization header missing'}), 401

    #Step 2: Read in tickers parameter
    try:
        tickers = request.args.get('tickers')
        tickers_list = list(map(lambda x: x.upper() , tickers.split(","))) #get individual tickers and make them all caps  
    except: 
        return jsonify({'error': 'No tickers provided'}), 400


    #Step 3: Read in range parameter 
    try:
        date_range = request.args.get('range')
    except:
        return jsonify({'error': 'No range provided'}), 400
    valid_ranges = ["1mo", "3mo", "6mo", "1y", "2y"]
    if date_range not in valid_ranges:
        return jsonify({'error': 'provide a valid range between 1 month and 2 years'}), 400


    #Step 4: Calculate the top five day over day values for each ticker
    results = list(map(lambda x: top_five_day_over_day(x, date_range)["top_five_changes"], tickers_list))
    res_map = {}
    for i in range(len(results)):
        res_map[tickers_list[i]] = results[i]

    return res_map



if __name__ == "__main__":
    app.run(debug=True)