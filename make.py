#!/usr/bin/env python

import jinja2
import yaml
import nbformat
from nbconvert import MarkdownExporter
import os
import subprocess

GITHUB_URL = "https://github.com/mr0re1/mr0re1.github.io"


def render_nb(path):
    notebook = nbformat.read(path, as_version=4)
    md_exporter = MarkdownExporter()
    md, _ = md_exporter.from_notebook_node(notebook)

    p = subprocess.Popen(
        [
            "pandoc", # pandoc 3.1.6.2
            "-f",
            "markdown",
            "-t",
            "html",
            "--mathjax",
            "--template",
            "templates/pandoc_post.html",
            # To silence misleading pandoc: [WARNING] This document format requires a nonempty <title> element.
            "--metadata", 'title="-"',
        ],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE, # stderr=subprocess.DEVNULL,
    )
    
    body, _ = p.communicate(md.encode("utf-8"))
    return body.decode("utf-8")


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
        post["html"] = render_nb(post["src"])
        post["github_link"] = f"{GITHUB_URL}/blob/master/{post['src']}"

        with open(f"docs/{out}", "w") as f:
            tmpl = env.get_template("post.j2")
            f.write(tmpl.render(**{**ctx, "post": post}))

    with open("docs/index.html", "w") as f:
        f.write(env.get_template("index.j2").render(**ctx))


if __name__ == "__main__":
    main()
