# render html files for the project using jinja2 templates

from jinja2 import Environment, FileSystemLoader
import project_data # json data for projects

templates_location = 'templates'
projects_template = 'projects_template.html'
projects_output = 'projects.html'
index_template = 'index_template.html'
index_output = 'index.html'

env = Environment(loader = FileSystemLoader(templates_location))

# render project page
template = env.get_template(projects_template)
project_html = template.render(project_data.data)
project_file = open(projects_output, 'w')
project_file.write(project_html)

# render homepage
template = env.get_template(index_template)
index_html = template.render(index_page=1)
index_file = open(index_output, 'w')
index_file.write(index_html)
