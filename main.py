from flask import Flask, request, jsonify 
from data.yahoo_finance import top_five_day_over_day
from user.properties import authenticate_user

app = Flask(__name__)


@app.route("/sampleAPI/analysis", methods=['GET'])
def sampleAPI():

    #authenticate users
    #Todo


 
    #tickers parameter
    try:
        tickers = request.args.get('tickers')
        print(tickers)
        tickers_list = list(map(lambda x: x.upper() , tickers.split(",")))
        
    except: 
        return jsonify({'error': 'No tickers provided'}), 400

    #range parameter 
    try:
        date_range = request.args.get('range') #Todo: Add validation for the range so it is between 1 month and 2 years
        print(type(date_range))
    except:
        return jsonify({'error': 'No range provided'}), 400

    valid_ranges = ["1mo", "3mo", "6mo", "1y", "2y"]
    if date_range not in valid_ranges:
        return jsonify({'error': 'provide a valid range between 1 month and 2 years'}), 400



    #Todo: display top 5 day over day percent moves by absolute value for specified stocks
    res = list(map(lambda x: top_five_day_over_day(x, date_range), tickers))
    
    #Todo: Finish looping through and running function on all tickers and then debug


    return top_five_day_over_day(tickers_list[0], date_range)




if __name__ == "__main__":
    app.run(debug=True)