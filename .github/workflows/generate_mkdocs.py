import os

import yaml

class MyDumper(yaml.Dumper):

    def increase_indent(self, flow=False, indentless=False):
        return super(MyDumper, self).increase_indent(flow, False)

def generate_mkdocs_settings(folder):
    pages = []
    for path, subdirs, files in os.walk(folder):
        page_list = []
        for name in files:
            page_list.append(path+'/'+name)
        pages.append({path: page_list})

    return {
        'site_name': 'My MkDocs Site',
        'site_url': 'https://daangeijs.github.io/chatgpt-autodocs/',
        'theme': 'readthedocs',
        'pages': pages
    }

mkdocs_settings = generate_mkdocs_settings('docs')

a = yaml.dump(mkdocs_settings, Dumper=MyDumper, default_flow_style=False)

with open('mkdocs.yml', 'w') as f:
    f.write(a)
