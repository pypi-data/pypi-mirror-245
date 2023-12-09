def load_env_variables(env_file_path):
    variables = {}
    with open(env_file_path, "r") as file:
        for line in file:
            # Игнорировать комментарии и пустые строки
            if not line.strip() or line.strip().startswith("#"):
                continue

            # Разделение строки на ключ и значение
            key, value = line.strip().split("=")
            variables[key] = value

    return variables
