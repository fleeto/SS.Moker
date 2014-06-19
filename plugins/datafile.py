import os.path
import json
import random
import linecache
import sys

base_path = os.path.dirname(os.path.realpath(sys.argv[0]))


def get_value(param):
    """
    param['type'] = 'datafile'
    param['Method'] = 'random' // or 'sequence'
    param['name'] = 'data_file_name1' //    ./param/datafile.data_file_name/content.dat will be the text file to be processed.
    :param param:
    :return: single line from datafile.
    """
    data_name = param['name']
    method = param['method']
    sys.stderr.write("Datafile is '%s' , Method is '%s'" % (data_name, method))
    data_path = os.path.join(base_path, 'param', 'datafile.' + data_name)
    info_name = os.path.join(data_path, 'info.dat')
    content_name = os.path.join(data_path, 'content.dat')
    print " %s \n %s \n" % (info_name, content_name)
    should_refresh = False
    if (os.path.getsize(info_name) > 0) and os.path.exists(info_name):
        info_m_time = os.path.getmtime(info_name)
        content_m_time = os.path.getmtime(content_name)
        # get file info if info is older than the content file.
        if content_m_time > info_m_time:
            should_refresh = True
    else:
        should_refresh = True

    info = {'lines': 0, 'current': 0}
    if not should_refresh:
        info_handle = open(info_name, 'r')
        info = json.loads(info_handle.readline())

    if method == 'random':
        random.seed()
        line_number = random.randint(1, info['lines'])
        sys.stderr.write("Reading %d \n" % line_number)
    else:
        info['current'] += 1
        line_number = info['current']

    info_handle = open(info_name, 'w')
    content_handle = open(content_name, 'r')
    info['lines'] = len(content_handle.readlines())
    info_handle.write(json.dumps(info))
    ret = linecache.getline(content_name, line_number).strip()
    return ret