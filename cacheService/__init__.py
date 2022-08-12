import yaml

with open('./application.yml', 'r') as config_file:
    config = yaml.load(config_file, Loader=yaml.FullLoader)
