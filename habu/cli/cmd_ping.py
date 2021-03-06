import click
from scapy.all import ICMP, IP, conf, sr1
from time import sleep

@click.command()
@click.argument('ip')
@click.option('-c', 'count', default=0, help='How many packets send (default: infinit)')
@click.option('-t', 'timeout', default=2, help='Timeout in seconds (default: 2)')
@click.option('-w', 'wait', default=1, help='How many seconds between packets (default: 1)')
@click.option('-v', 'verbose', is_flag=True, default=False, help='Verbose')
def cmd_ping(ip, count, timeout, wait, verbose):

    conf.verb = False

    layer3 = IP()
    layer3.dst = ip
    layer3.tos = 0
    layer3.id = 1
    layer3.flags = 0
    layer3.frag = 0
    layer3.ttl = 64
    layer3.proto = 1 # icmp

    layer4 = ICMP()
    layer4.type = 8 # echo-request
    layer4.code = 0
    layer4.id = 0
    layer4.seq = 0

    pkt = layer3 / layer4

    counter = 0

    while True:
        ans = sr1(pkt, timeout=timeout)
        if ans:
            if verbose:
                ans.show()
            else:
                print(ans.summary())
            del(ans)
        else:
            print('Timeout')

        counter += 1

        if count != 0 and counter == count:
            break

        sleep(wait)

    return True

if __name__ == '__main__':
    cmd_ping()
