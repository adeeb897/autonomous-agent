import os

# Function to create the directory structure string

def get_directory_structure(rootdir):
    structure = []
    for dirpath, dirnames, filenames in os.walk(rootdir):
        level = dirpath.replace(rootdir, '').count(os.sep)
        indent = ' ' * 4 * (level)
        structure.append(f'{indent}{os.path.basename(dirpath)}/')
        subindent = ' ' * 4 * (level + 1)
        for f in filenames:
            structure.append(f'{subindent}{f}')
    return '\n'.join(structure)

# Read the system prompt template
with open('prompt/system_prompt.txt', 'r') as file:
    system_prompt = file.read()

# Replace the placeholder with the actual directory structure
root_directory = '.'
directory_structure = get_directory_structure(root_directory)
updated_prompt = system_prompt.replace('{{DIRECTORY_STRUCTURE}}', directory_structure)

# Save the updated system prompt
with open('prompt/system_prompt.txt', 'w') as file:
    file.write(updated_prompt)

print('System prompt updated successfully with the current directory structure.')
