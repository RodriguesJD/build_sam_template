import yaml
from pprint import pprint

project_name = input("Name of lambda project folder")


def description():
    des = input("what is the Description")
    return des


dict_file = {'AWSTemplateFormatVersion': '2010-09-09',
             'Transform': 'AWS::Serverless-2016-10-31',
             'Description': description(),
             'Globals': {
                 'Function': {
                     'Timeout': 3}},
             'Resources': {
                 f'{project_name.title().replace("_", "")}Function': {
                     'Type': 'AWS::Serverless::Function',
                     'Properties': {
                         'CodeUri': f'{project_name}/',
                         'Handler': 'app.lambda_handler',
                         'Runtime': 'python3.7',
                         'Events': {
                             'HelloWorld': {
                                 'Type': 'Schedule',
                                 'Properties': {
                                     'Schedule': 'rate(5 minutes)',
                                     'Description': 'Example schedule',
                                     'Name': f'{project_name.replace("_", "-")}-schedule',
                                     'Enabled': True}
                             }
                         }
                     }
                 }
             }
             }


with open('template.yaml', 'w') as file:
    documents = yaml.dump(dict_file, file)

print(f"mkdir {project_name}")
print(f"cp app.py {project_name}/app.py")