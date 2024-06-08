from flask import Flask, jsonify
import requests
from collections import deque
import random
app = Flask(__name__)
WINDOW_SIZE = 10
TIMEOUT = 0.5
API_URLS = {
    'p': 'http://20.244.56.144/test/primes',
    'f': 'http://20.244.56.144/test/fibo',
    'e': 'http://20.244.56.144/test/even',
    'r': 'http://20.244.56.144/test/rand'
}
number_window = deque(maxlen=WINDOW_SIZE)
def fetch_numbers(number_type):
    try:
        response = requests.get(API_URLS[number_type], timeout=TIMEOUT)
        if response.status_code == 200:
            return response.json().get('numbers')  # Handle null case directly here
    except (requests.Timeout, requests.RequestException):
        return []  # Return None if there's an error
def calculate_average(numbers):
    return sum(numbers) / len(numbers) if numbers else 0
@app.route('/number/<string:number_id>', methods=['GET'])
def get_numbers(number_id):
    if number_id not in API_URLS:
        return jsonify({'error': 'Invalid number ID'}), 400
    prev_state = list(number_window)
    new_numbers = fetch_numbers(number_id)
    if new_numbers is not []:  
        random.shuffle(new_numbers) 
        for number in new_numbers:
            if number not in number_window:
                number_window.append(number)
                break
    curr_state = list(number_window)
    average = calculate_average(number_window)
    response = {
        "windowPrevState": prev_state,
        "windowCurrState": curr_state,
        "numbers": new_numbers if new_numbers is not None else [],
        "avg": round(average, 2)
    }
    return jsonify(response), 200
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9856)

