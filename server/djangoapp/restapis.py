import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth

import requests
import json
from requests.auth import HTTPBasicAuth

def get_request(url, api_key=None, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    
    headers = {'Content-Type': 'application/json'}
    
    if api_key:
        auth = HTTPBasicAuth('apikey', api_key)
    else:
        auth = None
    
    try:
        response = requests.get(url, headers=headers, params=kwargs, auth=auth)
    except:
        # If any error occurs
        print("Network exception occurred")
        return None
    
    status_code = response.status_code
    print("With status {} ".format(status_code))
    
    json_data = json.loads(response.text)
    return json_data

# Example usage
# your_api_key = "your_actual_api_key"
# json_result = get_request("your_url_here", api_key=your_api_key)


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
import requests
import json
from requests.auth import HTTPBasicAuth

import requests
import json
from requests.auth import HTTPBasicAuth

def post_request(url, json_payload, api_key=None, **kwargs):
    print(kwargs)
    print("POST to {} ".format(url))
    
    headers = {'Content-Type': 'application/json'}
    
    if api_key:
        auth = HTTPBasicAuth('apikey', api_key)
    else:
        auth = None
    
    try:
        response = requests.post(url, json=json_payload, headers=headers, params=kwargs, auth=auth)
    except:
        # If any error occurs
        print("Network exception occurred")
        return None
    
    status_code = response.status_code
    print("With status {} ".format(status_code))
    
    json_data = json.loads(response.text)
    return json_data



# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Iterate through each dealer object in the JSON result
        for dealer_item in json_result:
            # Access the "doc" dictionary within each dealer item
            dealer_doc = dealer_item["doc"]
            # Create a CarDealer object with values from the "doc" dictionary
            dealer_obj = CarDealer(
                address=dealer_doc["address"],
                city=dealer_doc["city"],
                full_name=dealer_doc["full_name"],
                id=dealer_doc["id"],
                lat=dealer_doc["lat"],
                long=dealer_doc["long"],
                short_name=dealer_doc["short_name"],
                st=dealer_doc["st"],
                zip=dealer_doc["zip"]
            )
            results.append(dealer_obj)
    return results


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
# Inside get_dealer_reviews_from_cf method
def get_dealer_reviews_from_cf(url, dealer_id):
    results = []
    # Call get_request with URL parameter and dealerId as a query parameter
    json_result = get_request(url, dealerId=dealer_id)
    if json_result:
        # Iterate through each review object in the JSON result
        for review_item in json_result:
            # Access the attributes of each review item directly
            name = review_item.get("name", "")  # Extract the 'name' attribute
            purchase = review_item.get("purchase", False)
            review = review_item.get("review", "")
            purchase_date = review_item.get("purchase_date", "")
            car_make = review_item.get("car_make", "")
            car_model = review_item.get("car_model", "")
            car_year = review_item.get("car_year", 0)
            sentiment = review_item.get("sentiment", "")  # Use a default value
            id = review_item.get("review_id", "")  # Use the correct key for the review ID

            # Create a DealerReview object with the extracted attributes
            dealer_review = DealerReview(
                dealership=dealer_id,
                name=name,
                purchase=purchase,
                review=review,
                purchase_date=purchase_date,
                car_make=car_make,
                car_model=car_model,
                car_year=car_year,
                sentiment=sentiment,
                id=id
            )
            dealer_review.sentiment = analyze_review_sentiments(
                text=dealer_review.review,
                version="2021-03-25",
                features="sentiment",
                return_analyzed_text=True
            )
            results.append(dealer_review)
    return results





# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
import requests
from requests.auth import HTTPBasicAuth
import json

def analyze_review_sentiments(**kwargs):
    url = "https://api.eu-de.natural-language-understanding.watson.cloud.ibm.com/instances/6e1922f2-2cb7-4c0b-bf7b-3b7ea3d536e3"
    
    params = dict()
    params["text"] = kwargs["text"]
    params["version"] = kwargs["version"]
    params["features"] = kwargs["features"]
    params["return_analyzed_text"] = kwargs["return_analyzed_text"]
    
    headers = {'Content-Type': 'application/json'}
    apikey = 'KrJBSL-MMQk3bo90HgDYNmrXSBDBc8ddZ4VdN4oUxBi4'
    auth = HTTPBasicAuth('apikey', apikey)
    
    try:
        response = requests.get(url, params=params, headers=headers, auth=auth)
        response_data = json.loads(response.text)
        return response_data
    except Exception as e:
        print("Error:", str(e))
        return None




