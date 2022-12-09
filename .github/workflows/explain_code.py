from pathlib import Path

import click
import subprocess
from chatgpt import Conversation


def get_changed_files(sha):
    # Use the `git diff` command to compare the provided SHA with the previous commit
    diff_output = subprocess.run(['git', 'diff-tree', '--no-commit-id', '--name-only', '-r', sha],
                                 stdout=subprocess.PIPE)
    diff_output = diff_output.stdout.decode('utf-8')

    # Parse the output of the `git diff` command to get a list of changed files
    changed_files = []
    for line in diff_output.split('\n')[:-1]:
        changed_files.append(line)

    # Return the list of changed files
    return list(dict.fromkeys(changed_files))


@click.command()
@click.option("--sha", type=str, required=True)
@click.option("--username", type=str, required=True)
@click.option("--password", type=str, required=True)
def main(sha, username, password):
    # Initialize the ChatGPT model
    model = Conversation()
    model._config_path = 'config.json'
    model.login(username, password)
    # Get the list of changed files
    changed_files = get_changed_files(sha)
    # Explain the contents of each changed file
    for file in changed_files:
        # Read the contents of the file
        print(file)
        with open(file, 'r') as f:
            contents = f.read()

        # Use ChatGPT to generate an explanation of the file's contents
        question_phrase = "Markdown string explaining in very extensively what this code does and end with a summary in bullets: \n \n"
        input = question_phrase + contents
        explanation = model.chat(input)

        # Generate paths for .md file output
        file_str = Path(file).stem
        document_path = Path('docs').absolute() / Path(file).parent
        document_path.mkdir(exist_ok=True, parents=True)
        # Change stuff
        # Write the contents to the file
        print(f'{str(document_path)}/{file_str}.md')
        with open(f'{str(document_path)}/{file_str}.md', 'w') as f:
            f.write(explanation)


if __name__ == "__main__":
    main()
