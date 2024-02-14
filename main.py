from flask import Flask, request, jsonify 
from  data.validation import is_valid_ticker

app = Flask(__name__)


@app.route("/sampleAPI/analysis", methods=['GET'])
def sampleAPI():
    #tickers parameter
    try:
        tickers = request.args.get('tickers')
        print(tickers)
        tickers_list = list(map(lambda x: x.upper() , tickers.split(",")))
        
    except: 
        return jsonify({'error': 'No tickers provided'}), 400

    #range parameter 
    try:
        date_range = request.args.get('range') 
    except:
        return jsonify({'error': 'No range provided'}), 400

    #Validating all stock ticker
    invalid_tickers = list(filter(lambda x: not is_valid_ticker(x), tickers_list))
    if len(invalid_tickers): 
        return jsonify({'error': 'Please Correct Invalid Tickers - ' + str(invalid_tickers) }), 400


    #Todo: display top 5 day over day percent moves by absolute value for specified stocks

    
    return jsonify({'tickers': tickers_list, 'range': date_range})



if __name__ == "__main__":
    app.run(debug=True)