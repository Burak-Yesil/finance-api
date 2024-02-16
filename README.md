# Stock Analysis API - Yahoo Finance API Wrapper

## Overview
This Flask application provides a REST/JSON API that analyzes stock price movements. It focuses on displaying the top 5 day-over-day percent changes by absolute value for specified stocks over a given time range.

## Features
- **Endpoint for Analysis**: Users can request an analysis through the `/sampleAPI/analysis` endpoint by providing stock tickers and a time range.
- **Secure Access**: The API is secured with Basic Authentication, ensuring that only authorized users can access the endpoint.

## Usage
To use the API, provide a comma-delimited list of stock tickers and a time range (from 1 month up to 2 years). You also need to include an Authorization header with your HTTP request containing one of the valid username and password combinations.

For testing the API with Postman:

1. Open Postman and start a new request.
2. Set the request type to `GET`.
3. Enter the request URL: `http://<host>:<port>/sampleAPI/analysis?tickers=MSFT,C,F&range=3mo`
4. Go to the Authorization tab, select "Basic Auth", and enter one of the valid username and password combinations.
5. Hit Send to make the request and receive the response.

Replace `name1:password1` with one of the valid username and password combinations:

- `name1:password1`
- `name2:password2`
- `name3:password3`

Make sure to replace `<host>` and `<port>` with your API's actual host and port details.


## Installation
To set up the Stock Analysis API on your local machine, follow these steps:

1. Clone the repository to your local machine.
2. Navigate to the root directory of the project.
3. Create a virtual environment:
    ```sh
    python -m venv venv
    ```
4. Activate the virtual environment:
    - On Windows:
        ```sh
        .\venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```sh
        source venv/bin/activate
        ```
5. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```
6. Start the Flask API by running the `main.py` file:
    ```sh
    python main.py
    ```

## Development
Unit tests have been created, using the unittest library, to validate the functionality, including:
- Accessing the Yahoo Finance API
- Parsing JSON from a file
- Calculating day-over-day percent moves
