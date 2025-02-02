import yaml
from pathlib import Path

config_file = Path(__file__).parent / "config.yaml" # follow config_template.yaml


def load_config():
    try:
        with open(config_file, 'r') as yaml_file:
            data = yaml.safe_load(yaml_file)
            return data
    except FileNotFoundError as e:
        print(e)