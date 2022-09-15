# https://towardsdatascience.com/finding-a-grocery-delivery-slot-the-smart-way-f4f0800c4afe

import requests
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

MY_ENV_VAR = os.getenv('MY_ENV_VAR')
from twilio.rest import Client

url = os.environ['MAIN_URL']

payload = {'csrfmiddlewaretoken': 'gwHsJhpbwvGYwMpmQPSIBAv192dIuxgq3WpakrGroKgyhrGkT7IuOIAoc5H0iqXm',
           'username': os.environ['USER'],
           'password': os.environ['PASSWORD']}

s = requests.Session()
r1 = s.post(os.environ['LOGIN_URL'], data=payload, verify=False)

start_date = datetime.today().date().strftime('%Y-%m-%dT%H:%M:%S')
end_date = (datetime.today().date() + timedelta(days=14)).strftime('%Y-%m-%dT%H:%M:%S')

count = 0

json_data = {"requestorigin": "gi",
             "data": {"customer-id": 5783385, "count": count, "next": start_date, "previous": end_date, "results": []}}

# Make POST request to API, sending required json data
#r2 = s.post(url, json=json_data)

#r2.status_code  # Inspect status code of response

# # Initialise empty dictionary for data
# slot_data = {}
#
# # Loop through json response and record slot status for each time slot
# for slot_day in r.json()['data']['slot_days']:
#
#     slot_date = slot_day['slot_date']
#
#     for slot in slot_day['slots']:
#         slot_time = slot['slot_info']['start_time']
#         slot_time = datetime.strptime(slot_time, '%Y-%m-%dT%H:%M:%SZ')
#
#         slot_status = slot['slot_info']['status']
#
#         slot_data[slot_time.strftime('%H:%M:%S %d-%m-%Y')] = slot_status
#
# # Filter for available slots
# available_list = [f'\n{key} - {value}' for (key, value) in slot_data.items() if value != 'UNAVAILABLE']
#
# # If any available slots exist, send a text notification
# if len(available_list) > 0:
#     account_sid = os.environ['TWILIO_ACT_SID']
#     auth_token = os.environ['TWILIO_AUTH_TOKEN']
#     client = Client(account_sid, auth_token)
#
#     message_txt = f'\nDelivery Slot/s Found: \n{" ".join(available_list)}'
#
#     message = client.messages \
#         .create(
#         body=message_txt,
#         from_=os.environ['TWILIO_NUMBER'],
#         to=os.environ['MY_NUMBER']
#     )
