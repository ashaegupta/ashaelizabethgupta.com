import os
import csv
from collections import defaultdict

# input files
input_dir                       = 'project_data/inputs'
project_csv_file                = os.path.join(input_dir, 'projects.csv')
ux_csv_file                     = os.path.join(input_dir, 'ux.csv')
ux_images_directory             = 'static/images/ux'
ux_image_directory_for_static   = 'static/images/ux/'

# output files
output_dir              = 'project_data/outputs'
projects_data_py_file   = os.path.join(output_dir, 'project_data.py')
ux_data_py_file         = os.path.join(output_dir, 'ux_data.py')
ux_images_py_file       = os.path.join(output_dir, 'ux_images.py')

def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')

def write_project_data():
    print "updating project data..."
    reader = csv.reader(open(project_csv_file, 'rb'), delimiter=',')
    data = defaultdict(list)
    attrs = ['type', 'name', 'service', 'description', 
             'skills', 'picture', 'my_work_url', 'company_url']
    for row in reader:
        row = [unicode(cell, 'utf-8') for cell in row]
        item = dict()
        for index, attr in enumerate(attrs):
            try:
                item[attr] = unicode(row[index])
            except:
                pass
        data[item['type'].lower()].append(item)

    data['projects_page'] = 1
    data[u'product_mantra'] = unicode("I believe the secret to great products is to continually ask 'why?' and then serve that deepest need.")
    data[u'development_mantra'] = unicode("Nothing like a good commit.")
    data[u'data_mantra'] = unicode("Intuition is fantastic, intuition backed by robust data, even better.")
    data[u'personal_mantra'] = unicode("'You are already naked. There is no reason not to follow your heart.' -- Steve Jobs")
    data[u'ux_mantra'] = unicode("Good design stays out of the way.")

    print "saving file %s..." % projects_data_py_file
    data_str = "data = %s" % dict(data)
    projects_data_file = open(projects_data_py_file, mode='w')
    projects_data_file.write(data_str)
    projects_data_file.close()

def write_ux_data():
    print "updating ux project data..."
    reader = csv.reader(open(ux_csv_file, 'rb'), delimiter=',')
    # attributes of the csv file are in the first row
    attrs = reader.next()
    data = defaultdict(list)

    # for each row in the csv file...
    for row in reader:
        # convert the row to unicode
        row = [unicode(cell, 'utf-8') for cell in row]
        # put the attributes into a dictionary...
        item = dict()
        for index, attr in enumerate(attrs):
            try:
                val = unicode(row[index])
            except:
                val = ''
            item[attr] = val

        # and save the dictionary in the array of all ux data
        data['ux'].append(item)

    print "saving file %s..." % ux_data_py_file
    data_str = "data = %s" % dict(data)
    ux_data_file = open(ux_data_py_file, mode='w')
    ux_data_file.write(data_str)
    ux_data_file.close()

def write_ux_image_list_data():
    print "updating ux image list..."
    image_directories = os.listdir(ux_images_directory)
    image_directories_to_ignore = ['drafts', '.DS_Store']
    image_data = dict()
    for dir in image_directories:
        if dir in image_directories_to_ignore:
            continue
        try:
            files = os.listdir(os.path.join(ux_images_directory, dir))
            files = sorted(files)
            image_data[dir] = [os.path.join(ux_image_directory_for_static,
                                            dir, 
                                            file) for file in files]
        except Exception, e:
            print "Error: %s" % e

    print "saving file %s..." % ux_images_py_file
    data_str = "data = %s" % dict(image_data)
    ux_data_file = open(ux_images_py_file, mode='w')
    ux_data_file.write(data_str)
    ux_data_file.close()

if __name__ == "__main__":
    write_project_data()
    write_ux_data()
    write_ux_image_list_data()
    print "done updating project data."
