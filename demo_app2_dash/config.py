
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path='demo_app2_dash/.env')


class Configuration:

    def __init__(self, api_key=os.getenv('api_key')):

        self.api_key = api_key
        

