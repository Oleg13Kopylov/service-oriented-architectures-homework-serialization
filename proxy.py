# https://docs.python.org/3/library/asyncio-protocol.html

from to_include import *
import asyncio
import json
import logging
import os
logging.basicConfig(level=logging.INFO)


class ProxyProtocol(asyncio.DatagramProtocol):
    def __init__(self, workers_port, multicast_port, multicast_ip):
        self.transport = None
        self.workers_port = workers_port
        self.multicast_ip = multicast_ip
        self.multicast_port = multicast_port

    def datagram_received(self, data, addr):
        data = data.decode("utf-8")
        logging.info("FROM datagram_received:: data is=%s", data)
        request = json.loads(data)

        # Если от worker пришел результат, отсылаем результат клиенту
        if "answer_to_client" == request["type"]:
            client_address, client_port = get_address_and_port_as_list(request["addr"])
            logging.info("FROM datagram_received::send to client at %s:%d", client_address, client_port)
            self.transport.sendto(request["answer"].encode(), (client_address, client_port))

        # Если от клиента пришел запрос для получения инф-ции обо всех форматах, то делаем мультикаст
        elif "get_result_all" == request["type"]:
            logging.info("Multicast Protocol Working!")
            logging.info("Multicast Protocol Working!")
            logging.info("Multicast Protocol Working!")
            logging.info("Multicast Protocol Working!")
            logging.info("Multicast Protocol Working!")
            logging.info("Multicast Protocol Working!")
            data_to_send = json.dumps({"type": "get_result", "addr": addr[0] + ":" + str(addr[1])})
            self.transport.sendto(data_to_send.encode(), (self.multicast_ip, self.multicast_port))

        # Если от клиента пришел запрос для получения инф-ции о каких-то конкретных форматах, то
        # отсылаем эти запросы соответствующим worker'ам
        elif "get_result" == request["type"]:
            for format in request["formats"]:
                data_to_send = json.dumps({"type": "get_result", "addr": addr[0] + ":" + str(addr[1])})
                logging.info("FROM datagram_received:: Send to %d", self.workers_port)
                self.transport.sendto(data_to_send.encode(), (format, self.workers_port))

    def connection_made(self, transport):
        self.transport = transport


if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    HOST = os.getenv('HOST')
    WORKERS_PORT = int(os.getenv('WORKERS_PORT'))
    UNICAST_PORT = int(os.getenv('UNICAST_PORT'))

    MULTICAST_IP = os.getenv('MULTICAST_IP')
    MULTICAST_PORT = int(os.getenv('MULTICAST_PORT'))

    logging.info('HELLO, I am proxy server and I just started working!!!')
    t = loop.create_datagram_endpoint(lambda: ProxyProtocol(WORKERS_PORT, MULTICAST_PORT, MULTICAST_IP),
                                      local_addr=(HOST, UNICAST_PORT))

    loop.run_until_complete(t)
    loop.run_forever()