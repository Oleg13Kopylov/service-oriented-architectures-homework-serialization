# https://docs.python.org/3/library/asyncio-protocol.html
# https://snyk.io/advisor/python/avro/functions/avro.schema.Parse

NUM_OF_TIMES_TO_TEST = 1000

import logging
import asyncio
from avro.io import DatumWriter, BinaryEncoder, DatumReader, BinaryDecoder
import avro.schema
import dicttoxml
import json
from io import BytesIO
import msgpack
import my_data_structure_pb2
import os
import sys
from to_include import *
import time
import xmltodict
import yaml

# Каждый из сериализаторов ниже возвращает list вида:
# [ размер сериализованной структуры,
#   время на сериализацию,
#   время на десериализацию  ]

def serialize_native(dict_arg):
    start_time = time.perf_counter_ns()
    serialized_dict = str(dict_arg)
    serialization_time_total = time.perf_counter_ns() - start_time
    start_time = time.perf_counter_ns()
    deserialized_dict = eval(serialized_dict)
    deserialization_time_total = time.perf_counter_ns() - start_time
    return [sys.getsizeof(serialized_dict), serialization_time_total, deserialization_time_total]


def serialize_xml(dict_arg):
    # logging.warning("dict_arg")
    # logging.warning(dict_arg)
    start_time = time.perf_counter_ns()
    serialized_dict = dicttoxml.dicttoxml(dict_arg)
    serialization_time_total = time.perf_counter_ns() - start_time
    start_time = time.perf_counter_ns()
    deserialized_dict = xmltodict.parse(serialized_dict)
    deserialization_time_total = time.perf_counter_ns() - start_time
    # logging.warning("deserialized_dict")
    # logging.warning(deserialized_dict)
    return [sys.getsizeof(serialized_dict), serialization_time_total, deserialization_time_total]


def serialize_yaml(dict_arg):
    start_time = time.perf_counter_ns()
    serialized_dict = yaml.dump(dict_arg)
    serialization_time_total = time.perf_counter_ns() - start_time
    start_time = time.perf_counter_ns()
    deserialized_dict = yaml.load(serialized_dict, Loader=yaml.FullLoader)
    deserialization_time_total = time.perf_counter_ns() - start_time
    return [sys.getsizeof(serialized_dict), serialization_time_total, deserialization_time_total]


def proto_get_data_structure_from_dict_arg(dict_arg):
    # logging.warning("FROM proto_get_data_structure_from_dict_arg begin")
    my_data_structure = my_data_structure_pb2.MyDataStructure()
    my_data_structure.bool = dict_arg["bool"]
    my_data_structure.int = dict_arg["int"]
    my_data_structure.float = dict_arg["float"]
    my_data_structure.string = dict_arg["string"]
    my_data_structure.list_of_strings.extend(dict_arg["list_of_strings"])
    my_data_structure.list_of_ints.extend(dict_arg["list_of_ints"])
    for key in dict_arg["word_to_int"].keys():
        my_data_structure.word_to_int[key] = dict_arg["word_to_int"][key]
    # logging.warning("FROM proto_get_data_structure_from_dict_arg end")
    return my_data_structure


def serialize_proto(dict_arg):
    # logging.warning("from serialize_proto begin")
    data_structure = proto_get_data_structure_from_dict_arg(dict_arg)
    start_time = time.perf_counter_ns()
    serialized_data_structure = data_structure.SerializeToString()
    serialization_time_total = time.perf_counter_ns() - start_time
    data_for_parsing = my_data_structure_pb2.MyDataStructure()
    start_time = time.perf_counter_ns()
    deserialized_dict = data_for_parsing.ParseFromString(serialized_data_structure)
    deserialization_time_total = time.perf_counter_ns() - start_time
    # logging.warning("from serialize_proto end")
    return [sys.getsizeof(serialized_data_structure), serialization_time_total, deserialization_time_total]


def serialize_json(dict_arg):
    start_time = time.perf_counter_ns()
    serialized_dict = json.dumps(dict_arg)
    serialization_time_total = time.perf_counter_ns() - start_time
    start_time = time.perf_counter_ns()
    deserialized_dict = json.loads(serialized_dict)
    deserialization_time_total = time.perf_counter_ns() - start_time
    return [sys.getsizeof(serialized_dict), serialization_time_total, deserialization_time_total]


def serialize_apache_avro(dict_arg):
    apache_avro_schema = avro.schema.parse('''
    {
        "type": "record",
        "name": "avro",
        "fields": [
            {"name": "bool", 
            "type": "boolean"},
            
            {"name": "int", 
            "type": "int"},
            
            {"name": "float", 
            "type": "float"},
            
            {"name": "string", 
            "type": "string"},
            
            {"name": "list_of_strings", 
            "type": {"type": "array", "items": "string"}},
            
            {"name": "list_of_ints", 
            "type": {"type": "array", "items": "int"}},
            
            {"name": "word_to_int", 
            "type": {"type": "map", "values": "int"}}
        ]
    }
    ''')
    b = BytesIO()
    datum_writer = DatumWriter(apache_avro_schema)
    binary_encoder = BinaryEncoder(b)
    start_time = time.perf_counter_ns()
    datum_writer.write(dict_arg, binary_encoder)
    serialized_dict = b.getvalue()
    serialization_time_total = time.perf_counter_ns() - start_time
    datum_reader = DatumReader(apache_avro_schema)
    start_time = time.perf_counter_ns()
    input_buffer = BytesIO(serialized_dict)
    binary_decoder = BinaryDecoder(input_buffer)
    deserialized_dict = datum_reader.read(binary_decoder)
    deserialization_time_total = time.perf_counter_ns() - start_time
    return [sys.getsizeof(serialized_dict), serialization_time_total, deserialization_time_total]


def serialize_messagepack(dict_arg):
    start_time = time.perf_counter_ns()
    serialized_dict = msgpack.packb(dict_arg)
    serialization_time_total = time.perf_counter_ns() - start_time
    start_time = time.perf_counter_ns()
    deserialized_dict = msgpack.unpackb(serialized_dict)
    deserialization_time_total = time.perf_counter_ns() - start_time
    return [sys.getsizeof(serialized_dict), serialization_time_total, deserialization_time_total]


def get_serializer_by_name(name):
    # logging.warning("FROM get_serializer_by_name")
    serializers_list = [serialize_native, serialize_xml, serialize_json,
                        serialize_proto, serialize_apache_avro, serialize_yaml,
                        serialize_messagepack,
                        ]
    # logging.warning("FROM get_serializer_by_name")
    return serializers_list[formats_list.index(name)]


def conduct_series_of_experiments(format_examined, serializer):
    sum_of_serialize_time = 0
    sum_of_deserialize_time = 0
    for i in range(NUM_OF_TIMES_TO_TEST):
        size_of_serialized, cur_serialize_time, cur_deserialize_time = serializer(data_structure_to_experiment_with)
        sum_of_serialize_time += cur_serialize_time
        sum_of_deserialize_time += cur_deserialize_time
    # nano == 10**(-9)
    # micro == 10**(-6)
    average_serialize_time_in_microseconds = sum_of_serialize_time / NUM_OF_TIMES_TO_TEST / (10 ** 3)
    average_deserialize_time_in_microseconds = sum_of_deserialize_time / NUM_OF_TIMES_TO_TEST / (10 ** 3)
    return f"{format_examined} - {size_of_serialized} - {round(average_serialize_time_in_microseconds)} microsec - " \
           f"{round(average_deserialize_time_in_microseconds)} microsec;\n"


def handle_message(transport, serializer, name_of_format, data, addr):
    decoded_data = data.decode("utf-8")
    request = json.loads(decoded_data)
    answer_to_client_str = conduct_series_of_experiments(name_of_format, serializer)
    reply_to_proxy = json.dumps({"type": "answer_to_client", "addr": request["addr"], "answer": answer_to_client_str})
    transport.sendto(reply_to_proxy.encode(), (addr[0], addr[1]))


class WorkerProtocol(asyncio.DatagramProtocol):
    def __init__(self, name_of_format):
        self.serializer = get_serializer_by_name(name_of_format)
        self.name_of_format = name_of_format
        self.transport = None

    def datagram_received(self, data, addr):
        handle_message(self.transport, self.serializer, self.name_of_format, data, addr)

    def connection_made(self, transport):
        self.transport = transport


class MulticastWorkerProtocol(asyncio.DatagramProtocol):
    def __init__(self, host, multicast_address, multicast_port, name_of_format):
        self.transport = None
        self.host = host
        self.multicast_address = multicast_address
        self.multicast_port = multicast_port
        self.name_of_format = name_of_format
        self.serializer = get_serializer_by_name(name_of_format)

    def datagram_received(self, data, addr):
        logging.warning('Worker receiver multicasted request get_result_all!')
        handle_message(self.transport, self.serializer, self.name_of_format, data, addr)

    def connection_made(self, transport):
        self.transport = transport
        sock = transport.get_extra_info('socket')
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP,
                        socket.inet_aton(self.multicast_address) + socket.inet_aton(self.host))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    FORMAT = os.getenv('FORMAT')
    HOST = os.getenv('HOST')
    UNICAST_PORT = int(os.getenv('UNICAST_PORT'))
    MULTICAST_IP = os.getenv('MULTICAST_IP')
    MULTICAST_PORT = int(os.getenv('MULTICAST_PORT'))

    t = loop.create_datagram_endpoint(lambda: WorkerProtocol(FORMAT), local_addr=(HOST, UNICAST_PORT))
    loop.run_until_complete(t)

    protocol = MulticastWorkerProtocol(HOST, MULTICAST_IP, MULTICAST_PORT, FORMAT)
    t = loop.create_datagram_endpoint(lambda: protocol, local_addr=(HOST, MULTICAST_PORT))

    loop.run_until_complete(t)
    loop.run_forever()