from .config_loader import ConfigLoader

_config_dict = ConfigLoader()

BASEURL = _config_dict.get("target")
