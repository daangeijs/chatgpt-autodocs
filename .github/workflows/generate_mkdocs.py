import os

import yaml


def generate_mkdocs_settings(folder):
    pages = []
    for path, subdirs, files in os.walk(folder):
        page_list = []
        for name in files:
            page_list.append(name)
        pages.append({path: page_list})

    return {
        'site_name': 'My MkDocs Site',
        'site_url': 'https://daangeijs.github.io/chatgpt-autodocs/',
        'theme': 'readthedocs',
        'pages': pages
    }

mkdocs_settings = generate_mkdocs_settings('docs')

a = yaml.dump(mkdocs_settings)

with open('mkdocs.yml', 'w') as f:
    f.write(a)
