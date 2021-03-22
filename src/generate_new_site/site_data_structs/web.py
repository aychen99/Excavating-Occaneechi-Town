from .site import SiteChapter
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path


TEMPLATES_DIRECTORY = str(Path(__file__).parent.parent / "templates")
GATEWAY_TEMPLATE_FILENAME = "electronic_dig_gateway.html.jinja"

jinja_env = Environment(
    loader=FileSystemLoader(TEMPLATES_DIRECTORY),
    autoescape=select_autoescape(['html', 'xml']),
    line_statement_prefix='#', line_comment_prefix='##',
    trim_blocks=True, lstrip_blocks=True
)
GATEWAY_TEMPLATE = jinja_env.get_template(GATEWAY_TEMPLATE_FILENAME)


class WebChapter(SiteChapter):
    """Chapter object to capture special behavior of Electronic Dig chapter."""

    def __init__(self, name, parent, path):
        super().__init__(name=name, parent=parent, path=path / "electronic_dig_gateway.html")
        self.template = GATEWAY_TEMPLATE
        self.parent.pathtable.register(
            "", self.path, self)
        self.parent.pathtable.register(
            "", self.path, self)

    def write(self):
        """
        Write the files to which this object and its children correspond.
        """
        print("Writing 'Electronic Dig Gateway' page... ", end='', flush=True)

        self.parent.update_href(self.path)

        with self.path.open('wb') as f:
            f.write(self.template.render().encode('utf-8'))

        print("Done.")
