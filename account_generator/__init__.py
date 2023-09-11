import logging
from json import dumps

import capmonster_python
import requests

from account_generator.constants import API, WEBSITE_KEY, URLS, CONFIG_URL, REGIONS, LOCALES


class GenerateAccount:
    def __init__(self, debug=False, proxy=None):

        self.CAPMONSTER_KEY = "<YOUR API>"

        self.session = requests.session()

        # Configure proxy
        if proxy:
            self.session.proxies = {'https': proxy}

        # Configure logging
        if debug:
            logging.basicConfig(filename='account_generator.log', level=logging.DEBUG,
                                format='%(asctime)s - %(levelname)s - %(message)s')
        else:
            logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def solve_hcaptcha(self, custom_data, region='EUW'):
        """
        Solves an hCaptcha challenge and returns the response.

        Args:
            custom_data (str): Custom data to be included with the task.
            region (str, optional): The region to use for solving the hCaptcha challenge. Defaults to 'EUW'.

        Returns:
            str: The response to the hCaptcha challenge.

        Raises:
            Exception: If an error occurs while solving the hCaptcha challenge.
        """
        try:
            capmonster = capmonster_python.HCaptchaTask(self.CAPMONSTER_KEY)
            capmonster.set_user_agent(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.3")
            task_id = capmonster.create_task(website_url=URLS[region], website_key=WEBSITE_KEY,
                                             custom_data=custom_data)
            result = capmonster.join_task_result(task_id)

            return result.get("gRecaptchaResponse")
        except Exception as e:
            logging.error(f"Error solving hCaptcha: {str(e)}")
            raise

    def get_rqdata_and_cookies(self):
        """
        Get the rqdata and cookies from the session.

        Returns:
            str: The rqdata value obtained from the session.

        Raises:
            Exception: If there is an error while getting the rqdata and cookies.
        """
        try:

            data = self.session.get(CONFIG_URL).json()
            captcha = data.get('captcha', {}).get('hcaptcha')
            return captcha.get('rqdata')
        except Exception as e:
            logging.error(f"Error getting rqdata and cookies: {str(e)}")
            raise

    def generate_account(self, password, username, region, date_of_birth="2001-12-06", email="xes22scboy32@gmail.com"):
        """
        Generates an account with the given parameters.

        Parameters:
            - password (str): The password for the account.
            - username (str): The username for the account.
            - region (str): The region for the account. Should be one of the valid region keys.
            - date_of_birth (str, optional): The date of birth for the account. Defaults to "2001-12-06".
            - email (str, optional): The email for the account. Defaults to "xesxyboy32@gmail.com".

        Returns:
            - response (Response): The API response.

        Raises:
            - Exception: If there is an error generating the account.
        """
        try:

            # Get the region value based on the user's chosen region
            region_value = REGIONS.get(region.upper())
            if region_value is None:
                raise ValueError("Invalid region")

            logging.info("Getting rqdata")
            rqdata = self.get_rqdata_and_cookies()

            logging.info(f"RQDATA: {rqdata}")

            logging.info("Solving captcha...")
            token = self.solve_hcaptcha(rqdata)
            logging.info(f"Captcha token = {token}")

            payload = {
                "campaign": "",
                "confirm_password": password,
                "date_of_birth": date_of_birth,
                "email": email,
                "locale": LOCALES.get(region),
                "newsletter": False,
                "password": password,
                "product_id": "league_of_legends",
                "region": region_value,
                "token": f"hcaptcha {token}",
                "tou_agree": True,
                "username": username
            }

            response = self.session.post(url=API, data=dumps(payload),
                                         headers={'Content-Type': 'application/json'})

            logging.info(f"API response: {response}")
            return response

        except Exception as e:
            logging.error(f"Error generating account: {str(e)}")
            raise

# if __name__ == "__main__":
#     try:
#         account_generator = GenerateAccount()
#         response = account_generator.generate_account("cooluysedsfs", "fdsfsfs", 'euw')
#         print(response.text)
#     except Exception as e:
#         print(f"An error occurred: {str(e)}")
