import shlex
from subprocess import Popen,PIPE,STDOUT

def get_simple_cmd_output(cmd, stderr=STDOUT):
    """
    Execute a simple external command and get its output.
    """
    args = shlex.split(cmd)
    return Popen(args, stdout=PIPE, stderr=stderr).communicate()[0]


def get_ping_time(host):
    host = host.split(':')[0]
    cmd = "fping {host} -C 3 -q".format(host=host)
    # result = str(get_simple_cmd_output(cmd)).replace('\\','').split(':')[-1].split() if x != '-']
    print(str(get_simple_cmd_output(cmd)))
    result = str(get_simple_cmd_output(cmd)).replace('\\', '').split(':')[-1].replace("n'", '').replace("-",
                                                                                                        '').replace(
        "b''", '').split()
    print(result)
    res = [float(x) for x in result]
    if len(res) > 0:
        return sum(res) / len(res)
    else:
        return 999999


def main():
    # sample hard code for test
    #host = 'google.com'
    host='10.1.1.6'
    print([host, get_ping_time(host)])

    #host = 'besparapp.com'
    #print([host, get_ping_time(host)])
if __name__=='__main__':
    main()
