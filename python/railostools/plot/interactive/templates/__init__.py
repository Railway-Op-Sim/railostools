import jinja2
import os.path


def load_html_template(template_name: str) -> jinja2.Template:
    _template_file = os.path.join(os.path.dirname(__file__), f"{template_name}.jinja")
    return jinja2.Template(open(_template_file).read())
