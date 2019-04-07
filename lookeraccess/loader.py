import glob 
import yaml 

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

def get_config_files():

	files = glob.glob('*.yml')
	files += glob.glob('*.yaml')

	files = [file for file in files if file != 'config.example.yaml']

	return files

def load_config_files():

	files = get_config_files()

	output = {}

	for file in files:
		with open(file, 'r') as stream:
			data = yaml.load(stream, Loader=Loader)

			for key in data.keys():
				if key in output:
					output[key] += data[key]
				else:
					output[key] = data[key]

	return output