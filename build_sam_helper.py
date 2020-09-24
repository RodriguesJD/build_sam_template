import yaml
from pprint import pprint
import shutil
import os
import pkgutil
import pip._internal.operations.freeze


class BuildSamTemplate:

    project_name = None
    description = None
    # TODO look for sam_vars.py for configuration vars

    def _collect_variables(self):
        if os.path.isfile("sam_vars.py"):
            import sam_vars
            self.project_name = sam_vars.project_name
            self.description = sam_vars.description
        else:
            self.project_name = input("Name of lambda project folder")
            self.description = input("what is the Description")
            with open('sam_vars.py', 'w') as file:
                file.writelines(f"project_name = {self.project_name}\n"
                                f"description = {self.description}")

    def lambda_function_root_folder(self):
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

    def lambda_function_child_folder(self):
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

    def template_dict(self):
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

        with open('template.yaml', 'w') as file:
            documents = yaml.dump(dict_file, file)


        with open(f"{self.project_name}/{self.project_name}/requirements.txt", 'w') as fp:
            # TODO try using .toml file to extract this data
            modules = pip._internal.operations.freeze.get_installed_distributions()
            ignore_these_packages = ["wcwidth","six", "pytest", "pyparsing", "py", "pluggy", "packaging", "more-itertools",
                                     "attrs", "setuptools", "pip"]
            for module in modules:
                if module.key in ignore_these_packages:
                    pass
                else:
                    fp.write(f"{module.key}\n")

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

        shutil.copyfile('template.yaml', f"{self.project_name}/template.yaml")

        print(f"mkdir {self.project_name}")
        print(f"cp app.py {self.project_name}/app.py")

    def create(self):
        self._collect_variables()
        self.lambda_function_root_folder()
        self.lambda_function_child_folder()
        self.template_dict()


if __name__ == '__main__':
    BuildSamTemplate().create()
