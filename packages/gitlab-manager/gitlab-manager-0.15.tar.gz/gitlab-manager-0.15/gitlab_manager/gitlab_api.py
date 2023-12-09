import requests
import gitlab

def create_variable(api_url, project_id, private_token, variable_key, variable_value,
                           variable_type="env_var", masked=False, protected=False, environment_scope=None):
    """
    Создает переменную в GitLab CI/CD проекта с дополнительными параметрами.

    :param api_url: Адрес GitLab API, например, 'https://gitlab.com/api/v4'
    :param project_id: ID проекта GitLab
    :param private_token: Ваш персональный токен GitLab
    :param variable_key: Ключ переменной
    :param variable_value: Значение переменной
    :param variable_type: Тип переменной, по умолчанию 'variable'
    :param masked: Скрыть переменную (masked), по умолчанию False
    :param protected: Защищенная переменная (protected), по умолчанию False
    :param environment_scope: Область окружения (environment_scope), по умолчанию None
    """
    # Инициализация объекта GitLab
    gl = gitlab.Gitlab(api_url, private_token=private_token)

    try:
        # Получение проекта по ID
        project = gl.projects.get(project_id)

        # Получение списка переменных проекта
        variables = project.variables.list()

        existing_variable = next((var for var in variables if var.key == variable_key), None)

        if existing_variable:
            # Если переменная существует, обновляем её значения и параметры
            existing_variable.value = variable_value
            existing_variable.variable_type = variable_type
            existing_variable.masked = masked
            existing_variable.protected = protected
            existing_variable.environment_scope = environment_scope
            existing_variable.save()
            print(f"Updated existing variable: {variable_key}")
        else:
            # Если переменной с указанным ключом нет, создаем новую переменную
            project.variables.create({
                'key': variable_key,
                'value': variable_value,
                'variable_type': variable_type,
                'masked': masked,
                'protected': protected,
                'environment_scope': environment_scope
            })
            print(f"Created new variable: {variable_key}")

    except gitlab.exceptions.GitlabGetError as e:
        print(f"Error getting project: {e}")
    except gitlab.exceptions.GitlabCreateError as e:
        print(f"Error creating variable: {e}")
