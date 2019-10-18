import sys
import argparse
import logging
import threading
import queue

from ufv_alerts import inputs
from ufv_alerts import exceptions
from ufv_alerts.clihelpers import stderrfatal
from ufv_alerts import config as ufvaconfig
from ufv_alerts.manglers import (
    init as init_manglers,
    run_all as run_all_manglers
)
from ufv_alerts.outputs import (
    init as setup_outputs,
    dispatch as output_dispatch
)

input_threads = []
active_manglers = []
mangler_threads = []
output_threads = []
output_queues = []

logging.basicConfig(
    format='%(asctime)s %(name)s %(levelname)s %(message)s',
    level=logging.DEBUG, stream=sys.stdout)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='Relay UniFi Video notifications')
    parser.add_argument(
        '-c', '--conf', dest='conf', metavar='path', nargs='?',
        help='config file')
    args = parser.parse_args()

    try:
        config = ufvaconfig.read(args.conf)
    except FileNotFoundError:
        stderrfatal(
            'No config file. Either provide one or ' \
                'write one to /etc/ufv-alerts.rc or ~/ufv-alerts.rc')
    except exceptions.ConfigurationError:
        stderrfatal('Configuration error')

    output_queue = queue.Queue()
    input_threads.append(threading.Thread(
        target=inputs.init, args=(output_queue, {})))
    input_threads[0].start()

    manglers = init_manglers(config['manglers'])

    for handler in setup_outputs(config['outputs']):
        output_queues.append(queue.Queue())
        output_threads.append(threading.Thread(
            target=output_dispatch, args=(handler, output_queues[-1])))
        output_threads[-1].start()

    while True:
        alert = output_queue.get()
        mangled = run_all_manglers(alert, manglers)
        if not mangled:
            continue
        for q in output_queues:
            q.put(mangled)
