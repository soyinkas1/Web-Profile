
from dotenv import load_dotenv
import os

load_dotenv()


class Configuration:

    def __init__(self, api_key=os.getenv('api_key')):

        self.api_key = api_key
        

