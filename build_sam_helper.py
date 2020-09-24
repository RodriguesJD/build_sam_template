import yaml
from pprint import pprint
import shutil
import os
import json
import toml

class BuildSamTemplate:

    project_name = None
    description = None

    def _collect_variables(self):
        # TODO this would be better as a json file

        if os.path.isfile(f"{os.getcwd()}/sam_vars.json"):
            with open(f"{os.getcwd()}/sam_vars.json", "r") as read_file:
                data = json.load(read_file)
                self.project_name = data["project_name"]
                self.description = data["description"]
        else:
            self.project_name = input("Name of lambda project folder")
            self.description = input("what is the Description")
            with open(f"{os.getcwd()}/sam_vars.json",  "w") as write_file:
                data = {"project_name": f"{self.project_name}\n",
                        "description": f"{self.description}"}
                json.dump(data, write_file)

    def _lambda_function_root_folder(self):
        # Create lambda function root project folder.
        if os.path.isdir(self.project_name):
            pass
        else:
            os.mkdir(self.project_name)
        # Create __init__.py so python sees project root as a package.
        if os.path.isfile(f"{self.project_name}/__init__.py"):
            pass
        else:
            with open(f"{self.project_name}/__init__.py", 'w') as fp:
                pass

    def _create_template_file(self):
        dict_file = {'AWSTemplateFormatVersion': '2010-09-09',
                     'Transform': 'AWS::Serverless-2016-10-31',
                     'Description': self.description,
                     'Globals': {
                         'Function': {
                             'Timeout': 3}},
                     'Resources': {
                         f'{self.project_name.title().replace("_", "")}Function': {
                             'Type': 'AWS::Serverless::Function',
                             'Properties': {
                                 'CodeUri': f'{self.project_name}/',
                                 'Handler': 'app.lambda_handler',
                                 'Runtime': 'python3.7',
                                 'Events': {
                                     'HelloWorld': {
                                         'Type': 'Schedule',
                                         'Properties': {
                                             'Schedule': 'rate(5 minutes)',
                                             'Description': 'Example schedule',
                                             'Name': f'{self.project_name.replace("_", "-")}-schedule',
                                             'Enabled': True}
                                     }
                                 }
                             }
                         }
                     }
                     }

        with open(f"{self.project_name}/template.yaml", 'w') as file:
            documents = yaml.dump(dict_file, file)

    def _lambda_function_child_folder(self):
        # Create lambda function child folder.
        if os.path.isdir(f"{self.project_name}/{self.project_name}"):
            pass
        else:
            os.mkdir(f"{self.project_name}/{self.project_name}")

        # Create __init__.py so python sees child_folder as a package.
        if os.path.isfile(f"{self.project_name}/{self.project_name}/__init__.py"):
            pass
        else:
            with open(f"{self.project_name}/{self.project_name}/__init__.py", 'w') as fp:
                pass

    def _create_app_file(self):
        with open(f"{self.project_name}/{self.project_name}/app.py", 'w') as fp:
            text = '''import json


        def lambda_handler(event, context):
            """Sample pure Lambda function

            Parameters
            ----------
            event: dict, required
                API Gateway Lambda Proxy Input Format

                Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

            context: object, required
                Lambda Context runtime methods and attributes

                Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

            Returns
            ------
            API Gateway Lambda Proxy Output Format: dict

                Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
            """

            return {
                "statusCode": 200,
                "body": json.dumps({
                    "message": "hello world",
                }),
            }
        '''
            fp.writelines(text)

    def _create_requirements_file(self):
        with open(f"{self.project_name}/{self.project_name}/requirements.txt", 'w') as fp:
            dependencies = list(toml.load("pyproject.toml")['tool']['poetry']['dependencies'].keys())
            for dependency in dependencies:
                if dependency == "python":
                    pass
                elif dependency == "aws-sam-cli":
                    pass
                else:
                    fp.write(f"{dependency}\n")

    def create(self):
        self._collect_variables()

        self._lambda_function_root_folder()
        self._create_template_file()

        self._lambda_function_child_folder()
        self._create_app_file()
        self._create_requirements_file()
        # TODO test that the template file passes samcli command?
        # TODO add pull git project into child folder


if __name__ == '__main__':
    BuildSamTemplate().create()
