import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")  # Get API Token from environment


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
        "Authorization": f"Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjM2MjgyNTg2MDExMTNlNjU3NmE0NTMzNzM2NWZlOGI4OTczZDE2NzEiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiIzMjU1NTk0MDU1OS5hcHBzLmdvb2dsZXVzZXJjb250ZW50LmNvbSIsImF1ZCI6IjMyNTU1OTQwNTU5LmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwic3ViIjoiMTEzMzU2NjA5MzQ3NDA1Mjg4NDM2IiwiaGQiOiJ1c2VrYXNlLmFpIiwiZW1haWwiOiJ2aW5jZW50QHVzZWthc2UuYWkiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiYXRfaGFzaCI6IlhaaDFMVjRIWG1HQm9rMEd1V0xnOEEiLCJpYXQiOjE3MzI4ODI5NDQsImV4cCI6MTczMjg4NjU0NH0.l_Tl_6nYQhDCQsRld63rQo88AL9MwqyXrjHy48j4-PeiaVFYF4pvKAlLx_qXq0oL9Xxn4TwbElQ6zLDrF6XDQ8w0JSbUDWfOl2zD9wb1xSWDzmNtETWCfx4PH7a0JStwqx0SWt9K2UdxmThPW8AO9vdLz2gQRX82hZ7jzsSisyWOvDKczIP0ofMta-SWdAUi4ISqD_L9QZghgntZjvwQiUJD3KA19BH8yE9YFN6OJfJQ696MAS97nwfPQOV7LYsQWHYFZ6hnWd_POgihDN-fcpyPmQ4THEA_2oViLmCmrYQcCP7OhWeGwWXUEaHf91CZcfum6Ja0sEfhR1OQPKhn8Q",  # Use the loaded API token
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
