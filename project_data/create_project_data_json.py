import csv
from collections import defaultdict

project_csv_file = 'projects.csv'
projects_data_py_file = 'project_data.py'

def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')

def write_project_data():
    reader = csv.reader(utf_8_encoder(open(project_csv_file, 'rb')), delimiter=',')
    data = defaultdict(list)
    for row in reader:
        yield [unicode(cell, 'utf-8') for cell in row]
        try: type = row[0]
        except: type = ''
        try: name = row[1]
        except: name = ''
        try: service = row[2]
        except: service = ''
        try: description = row[3]
        except: description = ''
        try: skills = row[4]
        except: skills = ''
        try: picture = row[5]
        except: picture = ''
        try: my_work_url = row[6]
        except: my_work_url = ''
        try: company_url = row[7]
        except: company_url = ''
        item = {
            u'name':         unicode(name), 
            u'service':      unicode(service), 
            u'description':  unicode(description), 
            u'skills':       unicode(skills), 
            u'picture':      unicode(picture), 
            u'my_work_url':  unicode(my_work_url), 
            u'company_url':  unicode(company_url)
        }
        data[type.lower()].append(item)

    data[u'product_mantra'] = unicode("I believe the secret to great products is to continually ask 'why?' and then serve that deepest need.")
    data[u'development_mantra'] = unicode("Everyone should be able to write and understand code at a basic level.")
    data[u'data_mantra'] = unicode("Intuition is fantastic, intuition backed by robust data, even better.")
    data[u'personal_mantra'] = unicode("Life is what happens when you busy are making other plans. Spend time on things you care about.")

    del data['type']
    data_str = "data = %s" % dict(data)
    projects_data_file = open(projects_data_py_file, mode='w')
    projects_data_file.write(data_str)

if __name__ == "__main__":
    write_project_data()
