import datetime
import sys
import random


def get_value(param):
    """
    param['type'] = 'timedata'
    param['method'] = 'now' // or random
    param['min'] = '1999-02-01' // required if method == 'random'
    param['max'] = '2010-03-01' // required if method == 'random'
    :param param:
    :return:
    """
    method = param['method']
    pattern = param['pattern']
    if method == 'now':
        dt = datetime.datetime.now()
    if method == 'random':
        dt1 = datetime.datetime.strptime(param['min'], '%Y-%m-%d')
        dt2 = datetime.datetime.strptime(param['max'], '%Y-%m-%d')
        dt = random_date(dt1, dt2)
    result = dt.strftime(pattern)
    sys.stderr.write('time data returned: %s\n' % result)
    return result


def random_date(start, end):
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + datetime.timedelta(random_second)
