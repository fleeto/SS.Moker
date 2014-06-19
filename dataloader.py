import re
import os.path
import urllib
import json
import imp
import sys
import string

left_sign = "_|"
right_sign = "|_"
base_path = os.path.dirname(os.path.realpath(sys.argv[0]))


def get_data(method, path):
    """
    According the requesting url and http method , search in the mock_index.json, then parse the parameters in data files,
    and the last, return it to the client.
    :param method: "POST" or "GET"
    :param path: "URL"
    :return: http_status_code and message_string
    """
    f = open(os.path.join(base_path, 'mock_index.json'), 'r')
    config_str = f.read()
    f.close()
    config = json.loads(config_str)
    for service in config:
        if method in service['method']:
            path_pattern = service['path']
            if re.match(path_pattern, path):
                sys.stderr.write("opening '%s' ....\n" % os.path.join(base_path, 'data', service['datafile']))
                fi = open(os.path.join(base_path, 'data', service['datafile']), 'r')
                data = fi.read()
                data = data.decode('utf-8')
                data = parse_data(data)

                data = data.encode(service['response']['encoding'])
                if service['response']['url']:
                    data = urllib.quote_plus(data)
                return 200, data, service
    return 404, ''


def parse_data(data):
    """
    Get parameters from data file contents, then processing the parameters get its values.
    :param data: string from data file
    :return: parameters had been replaced into values.
    """
    rex = re.compile(re.escape(left_sign) + "(.*?)" + re.escape(right_sign))
    params = rex.findall(data)
    result_list = {}
    if len(params) > 0:
        for param in params:
            r_param = string.replace(param, "'", '"')
            result_list[left_sign + param + right_sign] = process_param(json.loads(r_param))
    for k, v in result_list.items():
        data = string.replace(data, k, v)
    return data


def process_param(param):
    """
    find the right plug-in to process the parameter.

    param = {}
    param['type'] = 'datafile'  //It's the parameters type, and the corresponding python file name in the plugins dir.
    param['method'] = 'random'        //each plugin can have more than one method to get values.
    param['param1'] = 'param1_value' //others is the parameter passed to the plugins.
    :param param: parameters get from the data files
    :return: parameter values
    """
    plugin_type = param['type']
    sys.stderr.write("Plug in %s is started \n" % plugin_type)
    param_mod = imp.load_source(plugin_type, os.path.join(base_path, 'plugins', plugin_type + ".py"))
    param_value = param_mod.get_value(param)
    return param_value
