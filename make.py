#!/usr/bin/env python

import jinja2
import yaml
import nbformat
from nbconvert import HTMLExporter
import os

def render_nb(path):
    notebook = nbformat.read(path, as_version=4)
    html_exporter = HTMLExporter(template_name='classic')
    html_exporter.exclude_input_prompt = True
    body, _ = html_exporter.from_notebook_node(notebook)
    return body

def main():
    for file in os.listdir("docs"):
        os.remove(os.path.join("docs", file))

    with open('conf.yaml', 'r') as f:
        ctx = yaml.safe_load(f)
    
    env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))

    for post in ctx['posts']:
        out = post['url']
        post['html'] = render_nb(post['src'])
        
        with open(f'docs/{out}', 'w') as f:
            tmpl = env.get_template('post.j2')
            f.write(tmpl.render(**{**ctx, 'post': post}))

    with open('docs/index.html', 'w') as f:
        f.write(env.get_template('index.j2').render(**ctx))

if __name__ == "__main__":
    main()