import socket

formats_list = ["NATIVE", "XML", "JSON", "GOOGLE_PROTOCOL_BUFFER", "APACHE_AVRO",  "YAML", "MESSAGE_PACK"]

data_structure_to_experiment_with = {
    "bool": True,
    "int": 13052002,
    "float": 0.13052002,
    "string": "my date of birth is 13.05.2002",
    "list_of_strings": ["my ", "date ", "of ", "birth ", "is ", "13.05.2002"],
    "list_of_ints": [13, 5, 2002],
    "word_to_int": {"day": 13, "month": 5, "year": 2002}
}

def get_address_and_port_as_list(addr_port):
    address, port_as_str = addr_port.split(':')
    socket.inet_pton(socket.AF_INET, address)
    return [address, int(port_as_str)]