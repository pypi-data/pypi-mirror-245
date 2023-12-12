import os
def user_confirmation(output_message: str, default_answer='N') -> bool:
    if default_answer.lower() == 'n':
        output_message = f'{output_message} [N/y] '
    if default_answer.lower() == 'y':
        output_message = f'{output_message} [Y/n] '
    while True:
        response = input(output_message)
        if response.lower() == 'n':
            return False
        elif response.lower() == 'y':
            return True
        elif default_answer.lower() == 'n' and response == '':
            return False
        elif default_answer.lower() == 'y' and response == '':
            return True
        else:
            print(
                f"Invalid response. Enter 'y','n', or nothing to use the default response of {default_answer.lower()}")
def read_file(filename) -> str:
    package_dir = os.path.dirname(__file__)
    filepath = os.path.join(package_dir, filename)
    with open(f'{filepath}', 'r') as f:
        return f.read()