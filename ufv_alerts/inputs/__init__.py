from . import smtp

config = {}

def init(output_queue, config=config):
    bind_addr = config.get('bind_to', '127.0.0.1')
    port = config.get('listen_port', 7025)
    smtp.create_and_start(output_queue, bind_addr, port)
