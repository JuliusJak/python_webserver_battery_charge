import requests

# Define the base URL for the simulated charging station
base_url = "http://localhost:5000"


#Baseload
def get_baseload():
    response = requests.get(f"{base_url}/baseload")
    return response.json()

def get_all_info():
    response = requests.get(f"{base_url}/info")
    return response.json()

#Price per hour
def get_price_per_hour():
    response = requests.get(f"{base_url}/priceperhour")
    return response.json()

#Battery
def start_charging():
    payload = {"charging": "on"}
    response = requests.post(f"{base_url}/charge", json=payload)
    return response.json()

def stop_charging():
    payload = {"charging": "off"}
    response = requests.post(f"{base_url}/charge", json=payload)
    return response.json()

def get_battery_charge():
    response = requests.get(f"{base_url}/charge")
    return response.json()

def reset_battery():
    payload = {"discharging": "on"}
    response = requests.post(f"{base_url}/discharge", json=payload)
    return response.json()