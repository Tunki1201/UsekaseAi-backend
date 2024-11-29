import requests
import json


class ReportGenerator:
    @staticmethod
    async def generate_report(company_data: dict) -> dict:
        """
        Generate a report for the given company data by calling the external API.

        :param company_data: A dictionary containing company information.
        :return: The generated report as a dictionary.
        """
        try:
            # External API endpoint
            external_api_url = "https://9aa7-2400-8d60-4-00-1-ab45-f52b.ngrok-free.app/api/v1/generate-report"

            # Prepare the payload
            payload = {
                "company_name": company_data.get("company_name"),
                "company_url": company_data.get("company_url"),
                "company_background": company_data.get("company_background"),
            }

            # Make the POST request
            response = requests.post(
                external_api_url,
                headers={"Content-Type": "application/json"},
                data=json.dumps(payload),
            )

            print('------------------------response', response.json())
            # Check for errors
            if response.status_code != 200:
                raise Exception(
                    f"Failed to generate report. Status: {response.status_code}, Response: {response.text}"
                )

            # Return the report as a dictionary
            return response.json()

        except Exception as e:
            print(f"Error in ReportGenerator: {str(e)}")
            raise
