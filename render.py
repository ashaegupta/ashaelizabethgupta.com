# render html files for the project using jinja2 templates

import codecs
from jinja2 import Environment, FileSystemLoader
from project_data import project_data # json data for projects

templates_location = 'templates'
projects_template = 'projects_template.html'
projects_output = 'projects.html'
index_template = 'index_template.html'
index_output = 'index.html'

env = Environment(loader = FileSystemLoader(templates_location))

# render project page
template = env.get_template(projects_template)
project_html = template.render(project_data.data)
project_file = codecs.open(projects_output, encoding='utf-8', mode='w')
project_file.write(project_html)
project_file.close()

# render homepage
template = env.get_template(index_template)
index_html = template.render(index_page=1)
index_file = codecs.open(index_output, encoding='utf-8', mode='w')
index_file.write(index_html)
index_file.close()
