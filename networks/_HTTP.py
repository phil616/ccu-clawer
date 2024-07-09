
from requests import post,get
from loguru import logger
from conf import BASEURL
from pathlib import Path
class _HTTP:
    def __init__(self,baseurl=BASEURL):
        self.headers = {}
        self.base = baseurl
        anti_clawer_header_text = Path(__file__).parent.parent / "anticlawer.txt"
        with open(anti_clawer_header_text) as f: 
            self.headers.update(parse_headers(f.read()))
            
    def json_post(self,url,data):
        try:
            logger.info(f"Posting to {url} with data: {data}")
            p = post(self.base+url,json=data,headers=self.headers)
            logger.info(f"Posting to {url} with data: {data} RAW:{p.request.body}")
            logger.info(f"Posting response: {p.text}")
            return p
        except Exception as e:
            logger.error(f"Error posting to {url} with data: {data}, {e}")

    def data_post(self,url,data):
        try:
            logger.info(f"Posting to {url} with data: {data}")
            p = post(self.base+url,data=data,headers=self.headers)
            logger.info(f"Posting response: {p.text}")
            return p
        except Exception as e:
            logger.error(f"Error posting to {url} with data: {data}, {e}")

    def get(self,url):
 
        logger.info(f"Getting from {url}")
        p = get(self.base + url,headers=self.headers,verify=True)
        return p

    def update_headers(self,headers:dict):
        logger.info(f"Updating headers to {headers}")
        self.headers.update(headers)

def _reverse_dict(original_dict):
    reversed_dict = {value: key for key, value in original_dict.items()}
    return reversed_dict

def parse_headers(header_str:str):
    headers = {}
    lines = header_str.strip().split('\n')
    
    for line in lines:
        if ':' in line:
            key, value = line.split(':', 1)
            headers[key.strip()] = value.strip()
    logger.debug(f"Parsed headers: {headers}")
    return headers