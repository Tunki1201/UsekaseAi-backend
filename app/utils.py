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
    payload = json.dumps(
        {
            "company_name": company_name,
            "company_url": url,  # Use the passed URL
            "company_background": company_background,
        }
    )

    # Prepare the headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_TOKEN}",  # Use the loaded API token
    }

    try:
        # Make the POST request to the external API
        response = requests.post(api_url, headers=headers, data=payload)

        # Check the response
        if response.status_code == 200:
            company_data = response.json()
            return company_data  # Return the data from the external API
        else:
            print(
                f"Error calling external API: {response.status_code} - {response.text}"
            )
            return None
    except Exception as e:
        print(f"An error occurred while calling the external API: {e}")
        return None
