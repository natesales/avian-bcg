from jinja2 import Template

with open("rendering/frr/template.j2") as frr_template_file:
    frr_template = Template(frr_template_file.read())


def render(config, router, sessions):
    return frr_template.render(config=config, router=router, sessions=sessions)

