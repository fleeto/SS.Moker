import os.path
import sys

left_sign = "_|"
right_sign = "|_"
base_path = os.path.dirname(os.path.realpath(sys.argv[0]))


def get_value(param):
    """
    param['type'] = 'sequence'
    param['pattern'] = 'sequence[%s]' //
    param['name'] = 'sequence_id' //    ./param/sequence.sequence_id/content.dat will be the storage of this param.
    :param param: see above
    :return: an integer.
    """
    pattern = param['pattern']
    file_name = os.path.join(base_path, 'param', 'sequence.' + param['name'], 'content.dat')
    if os.path.exists(file_name):
        fh = open(file_name, 'r')
        seed = fh.readline().strip()
        fh.close()
    else:
        seed = ''
    if len(seed) == 0:
        seed = '0'
    seed = int(seed)
    fh = open(file_name, 'w')
    new_seed = seed + 1
    fh.write(str(new_seed))
    fh.close()
    result = pattern % new_seed
    sys.stderr.write("sequence returned: %s \n" % result)
    return result