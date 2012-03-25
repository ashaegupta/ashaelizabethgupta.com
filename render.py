# render html files for the project using jinja2 templates

import codecs
from jinja2 import Environment, FileSystemLoader
from project_data.outputs import project_data, ux_data # json data for projects

combined_project_data = dict(project_data.data.items() + ux_data.data.items())

templates_dir = 'templates'
env = Environment(loader = FileSystemLoader(templates_dir))

templates_to_render = {
    'index':{'index_page':1},
    'projects': combined_project_data,
    'pictures':{'pictures_page':1}
}

for template_root, template_data in templates_to_render.iteritems():
    template_name = "%s_template.html" % template_root
    template = env.get_template(template_name)
    html = template.render(template_data)
    file_name = "%s.html" % template_root
    f = codecs.open(file_name, encoding='utf-8', mode='w')
    f.write(html)
    f.close()
