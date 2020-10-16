from jinja2 import Environment, FileSystemLoader, select_autoescape
import pathlib

def write_homepage(chapters, index_path):
    # Jinja setup
    templates_path = str((pathlib.Path(__file__).parent.parent / "templates"))
    jinja_env = Environment(
        loader=FileSystemLoader(templates_path),
        autoescape=select_autoescape(['html', 'xml']),
        line_statement_prefix='#',
        line_comment_prefix='##',
        trim_blocks=True
    )
    template = jinja_env.get_template('index.html.jinja')

    chapter_links = {c.name: c.href for c in chapters}

    with index_path.open('w') as f:
        f.write(template.render(
            links=chapter_links
        ))

    return
