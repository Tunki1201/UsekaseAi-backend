import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")  # Get API Token from environment

print("API_TOKEN:", API_TOKEN)
def fetch_company_info(url: str, company_name: str, company_background: str):
    """
    Call the external API to gather company information based on the given URL.
    """
    api_url = "https://usekase-scraping-standard-347630681311.us-central1.run.app/gather_company_info"
    
    # Prepare the payload
    payload = json.dumps({
        "company_name": company_name,
        "company_url": url,  # Use the passed URL
        "company_background": company_background
    })

    # Prepare the headers
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjM2MjgyNTg2MDExMTNlNjU3NmE0NTMzNzM2NWZlOGI4OTczZDE2NzEiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiIzMjU1NTk0MDU1OS5hcHBzLmdvb2dsZXVzZXJjb250ZW50LmNvbSIsImF1ZCI6IjMyNTU1OTQwNTU5LmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwic3ViIjoiMTA5MTQ4OTM4NDcxOTU2ODcwMDU1IiwiaGQiOiJ1c2VrYXNlLmFpIiwiZW1haWwiOiJoaXJva2lAdXNla2FzZS5haSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJhdF9oYXNoIjoiV3U5MlgxakNVcmtmQWZ0SC1vazVvQSIsImlhdCI6MTczMjY5Nzc3NywiZXhwIjoxNzMyNzAxMzc3fQ.cAxMKPhKnqJKlR-a7FczGOUc5GUteq7X0jk_eqAMLT7508GT32-eRndn5oj3aJF5iLPSY1TzxZ98GpF0aC3UP5ok6vkUPzmS-CHX9ItwT9haHJdQRrhZdHBV8Ovw7u_B2VHg1Ix2kXrmwmmqeYTGBrpskYe0r7kr-kVgXFP9WCJMsd7TxJlmk9EVMpYOz4-9A9rCjZNTSWC4AOxZt68E_jfzXW_EF3Dd9GE6FlbLaS_cWJpW2AsM1qBDa2ElaAVbGhX1hmY2q2wU9o2wZ1g6iOINtJGyp4VYIj1cQ3IoJ6GW3X_wf4PRlvRtKxMOnCQOdbge7_U0XtHAOpWjUAoCMw'  # Use the loaded API token
    }

    try:
        # Make the POST request to the external API
        response = requests.post(api_url, headers=headers, data=payload)

        # Check the response
        if response.status_code == 200:
            company_data = response.json()
            return company_data  # Return the data from the external API
        else:
            print(f"Error calling external API: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"An error occurred while calling the external API: {e}")
        return None
