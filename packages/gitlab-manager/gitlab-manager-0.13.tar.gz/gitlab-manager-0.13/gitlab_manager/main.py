
from gitlab_manager.gitlab_api import create_variable
from gitlab_manager.utils import load_env_variables
import argparse


def main():

    parser = argparse.ArgumentParser(description='GitLab Manager')

    subparsers = parser.add_subparsers(title='subcommands', dest='subcommand', help='Subcommand to run')

    # Подкоманда create_variable
    create_variable_parser = subparsers.add_parser('create_variable', help='Create a variable')
    create_variable_parser.add_argument('--api_url', required=True, help='GitLab API URL')
    create_variable_parser.add_argument('--project_id', type=int, required=True, help='Project ID')
    create_variable_parser.add_argument('--private_token', required=True, help='Private Token')
    create_variable_parser.add_argument('--key', required=True, help='Key for the variable')
    create_variable_parser.add_argument('--value', required=True, help='Value for the variable')
    create_variable_parser.add_argument('--type', default='env_var', help='Variable Type')
    create_variable_parser.add_argument('--masked', action='store_true', help='Masked')
    create_variable_parser.add_argument('--protected', action='store_true', help='Protected')
    create_variable_parser.add_argument('--environment_scope', default='*', help='Environment Scope')
    create_variable_parser.set_defaults(func=create_variable_command)


    create_variable_from_file_parser = subparsers.add_parser('create_variable_from_file', help='Create a variable fron env file')
    create_variable_from_file_parser.add_argument('--api_url', required=True, help='GitLab API URL')
    create_variable_from_file_parser.add_argument('--project_id', type=int, required=True, help='Project ID')
    create_variable_from_file_parser.add_argument('--private_token', required=True, help='Private Token')
    create_variable_from_file_parser.add_argument('--file', required=True, help='Path to env file with the variable')
    create_variable_from_file_parser.add_argument('--type', default='env_var', help='Variable Type')
    create_variable_from_file_parser.add_argument('--masked', action='store_true', help='Masked')
    create_variable_from_file_parser.add_argument('--protected', action='store_true', help='Protected')
    create_variable_from_file_parser.add_argument('--environment_scope', default='*', help='Environment Scope')
    create_variable_from_file_parser.set_defaults(func=create_variable_from_file)

    # Парсим аргументы командной строки
    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        print("No subcommand specified")
    

def create_variable_command(args):
    # Вызываем функцию create_variable, передавая ей значения аргументов
    create_variable(
        api_url=args.api_url,
        project_id=args.project_id,
        private_token=args.private_token,
        variable_key=args.key,
        variable_value=args.value,
        variable_type=args.type,
        masked=args.masked,
        protected=args.protected,
        environment_scope=args.environment_scope
    )

def create_variable_from_file(args):

    print("created from file")
    variables = load_env_variables(args.file)

    # Создание CI/CD переменных
    for variable_key, variable_value in variables.items():
            create_variable(
                api_url=args.api_url,
                project_id=args.project_id,
                private_token=args.private_token,
                variable_key=variable_key,
                variable_value=variable_value,
                variable_type=args.type,
                masked=args.masked,
                protected=args.protected,
                environment_scope=args.environment_scope
    )

if __name__ == "__main__":
    main()
