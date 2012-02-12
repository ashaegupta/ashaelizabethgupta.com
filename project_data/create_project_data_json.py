import csv
from collections import defaultdict

project_csv_file = 'projects.csv'
projects_data_py_file = 'project_data.py'

def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')

def write_project_data():
    print "reading csv file..."
    reader = csv.reader(open(project_csv_file, 'rb'), delimiter=',')
    data = defaultdict(list)
    print "creating dict..."
    for row in reader:
        row = [unicode(cell, 'utf-8') for cell in row]
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

    print "adding other data..."
    data['projects_page'] = 1
    data[u'product_mantra'] = unicode("I believe the secret to great products is to continually ask 'why?' and then serve that deepest need.")
    data[u'development_mantra'] = unicode("Nothing like a good commit.")
    data[u'data_mantra'] = unicode("Intuition is fantastic, intuition backed by robust data, even better.")
    data[u'personal_mantra'] = unicode("'You are already naked. There is no reason not to follow your heart.' -- Steve Jobs")

    print "saving file..."
    data_str = "data = %s" % dict(data)
    print data_str
    projects_data_file = open(projects_data_py_file, mode='w')
    projects_data_file.write(data_str)

if __name__ == "__main__":
    print "running..."
    write_project_data()
    print "done."
