import toml

app_info = toml.load("pyproject.toml")["tool"]["poetry"]

__version__ = app_info["version"]
__description__ = app_info["description"]
__api_title__ = app_info["name"]
