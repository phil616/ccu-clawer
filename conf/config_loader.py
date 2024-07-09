
import json
from typing import Dict,Optional
from pathlib import Path
from loguru import logger
def load_config(config_path:Optional[str] = None) -> Dict[str, str]:
    """
    this function loads the config file and returns a dictionary of key value pairs
    :param config_path: path to the config file
    :return: dictionary of key value pairs
    """
    if config_path is None:
        config_path = Path(__file__).parent / "config.json"
    with open(config_path,"r") as f:
        return json.load(f)
    
class ConfigLoader:
    """
    this class loads the config file and returns a dictionary of key value pairs
    """
    def __init__(self,config_path:Optional[str] = None) -> None:
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config.json"
        with open(config_path,"r") as f:
            self._config = json.load(f)
    @property
    def config(self):
        return self._config
    def get(self,key:str) -> str:
        try:
            self._config[key]
        except KeyError:
            raise KeyError(f"key {key} not found in config")
        res = self._config[key]
        logger.info(f"key {key} found in config: {res}")
        return res