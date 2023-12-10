from datetime import datetime
import logging, os, requests, csv
from requests.auth import HTTPBasicAuth
from cashctrl.limiter import Limiter
from .constants import VALID_LANGUAGES

logging.debug=print #todo: remove
logging.info=print #todo: remove

class Client:
    """
    Client is the main class to interact with the CashCtrl API. It sends all the requests and enables limiting, logging and so on.
    It also provides a convenient way to access all the resources via cc.account, cc.person, etc.
    """
    def __init__(self, api_key=None, organization=None, language=None, limit=True):
        if api_key is None or organization is None or language is None:
            from dotenv import load_dotenv
            if api_key is None:
                try:
                    load_dotenv()
                    api_key = os.getenv("API_KEY")
                    assert api_key is not None
                except:
                    raise ValueError(f"No Api key provided neither as parameter or in a  .env file.")
            if organization is None:
                try:
                    load_dotenv()
                    organization = os.getenv("ORGANIZATION")
                    assert organization is not None
                except:
                    raise ValueError(f"No organization neither as parameter or in a .env file.")
            if language is None:
                try:
                    load_dotenv()
                    language = os.getenv("LANGUAGE")
                except:
                    language="en"
        language = language.lower()
        if language not in VALID_LANGUAGES:
            raise ValueError(f"Invalid language '{language}'. Valid options are {', '.join(self.VALID_LANGUAGES)}.")
        from .resource import account
        from .resource import person #,common,file,inventory,journal,meta,order,person,report,setting
        self.api_key = api_key
        self.organization = organization
        self.default_language = language
        self.base_url = f"https://{organization}.cashctrl.com/api/v1/"
        self.account = account.Account(self)
        self.person = person.Person(self)
        self.limit = limit
        if self.limit:
            self.limiter = Limiter(self)



    def _make_request(self, method, endpoint, params=None):
        print(params)
        url = f"{self.base_url}{endpoint}"
        params = params or {}
        params['lang'] = self.default_language
        req = requests.Request(method, url, auth=HTTPBasicAuth(self.api_key, None), params=params)
        prepared_req = req.prepare()
        # Log the complete URL with parameters
        logging.info(f"Making {method} request to {prepared_req.url}")
        try:
            with requests.Session() as s:
                response = s.send(prepared_req)
            response.raise_for_status()
            json_response = response.json()
            if not json_response.get('success', True):
                raise Exception(f"Validation errors: {json_response.get('errors')}")
            if self.limit: self.limiter.lazy_log_request(endpoint)
            return json_response

        except requests.RequestException as e:
            raise Exception(f"An error occurred: {str(e)}")