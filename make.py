#!/usr/bin/env python

import jinja2
import yaml
import json
import nbformat
import tempfile
from nbconvert import HTMLExporter, TemplateExporter
import os

GITHUB_URL = "https://github.com/mr0re1/mr0re1.github.io"


def render_something(path):
    ext = os.path.splitext(path)[1]
    if ext == ".ipynb":
        return render_nb(path)
    elif ext == ".md":
        return render_md(path)
    raise ValueError(f"Can't handle {ext} files: {path}")

def render_nb(path):
    notebook = nbformat.read(path, as_version=4)
    TemplateExporter.extra_template_basedirs = ["templates"]
    html_exporter = HTMLExporter(template_name="nbconvert_post")

    html_exporter.exclude_input_prompt = True
    body, _ = html_exporter.from_notebook_node(notebook)
    return body


def render_md(path):
    with open(path) as f:
        md = f.read()

    js = {
        "cells": [{"cell_type": "markdown", "metadata": {}, "source": [md]}],
        "metadata": {"language_info": {"name": "python"}},
        "nbformat": 4,
        "nbformat_minor": 2,
    }
    tmp = tempfile.NamedTemporaryFile(mode="w")
    json.dump(js, tmp)
    tmp.flush()
    html = render_nb(tmp.name)
    tmp.close()
    return html


def main():
    for file in os.listdir("docs"):
        if file in ["CNAME", "static"]:
            continue
        os.remove(os.path.join("docs", file))

    with open("conf.yaml", "r") as f:
        ctx = yaml.safe_load(f)

    env = jinja2.Environment(loader=jinja2.FileSystemLoader("templates"))

    for post in ctx["posts"]:
        out = post["url"]
        post["html"] = render_something(post["src"])
        post["github_link"] = f"{GITHUB_URL}/blob/master/{post['src']}"

        with open(f"docs/{out}", "w") as f:
            tmpl = env.get_template("post.j2")
            f.write(tmpl.render(**{**ctx, "post": post}))

    for p in ["index"]:
        with open(f"docs/{p}.html", "w") as f:
            f.write(env.get_template(f"{p}.j2").render(**ctx))


if __name__ == "__main__":
    main()
