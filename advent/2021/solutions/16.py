from math import prod


PUZZLE_INPUT = 'A20D5080210CE4BB9BAFB001BD14A4574C014C004AE46A9B2E27297EECF0C013F00564776D7E3A825CAB8CD47B6C537DB99CD746674C1000D29BBC5AC80442966FB004C401F8771B61D8803D0B22E4682010EE7E59ACE5BC086003E3270AE4024E15C8010073B2FAD98E004333F9957BCB602E7024C01197AD452C01295CE2DC9934928B005DD258A6637F534CB3D89A944230043801A596B234B7E58509E88798029600BCF5B3BA114F5B3BA10C9E77BAF20FA4016FCDD13340118B929DD4FD54E60327C00BEB7002080AA850031400D002369400B10034400F30021400F20157D804AD400FE00034E000A6D001EB2004E5C00B9AE3AC3C300470029091ACADBFA048D656DFD126792187008635CD736B3231A51BA5EBDF42D4D299804F26B33C872E213C840022EC9C21FFB34EDE7C559C8964B43F8AD77570200FC66697AFEB6C757AC0179AB641E6AD9022006065CEA714A4D24C0179F8E795D3078026200FC118EB1B40010A8D11EA27100990200C45A83F12C401A8611D60A0803B1723542889537EFB24D6E0844004248B1980292D608D00423F49F9908049798B4452C0131006230C14868200FC668B50650043196A7F95569CF6B663341535DCFE919C464400A96DCE1C6B96D5EEFE60096006A400087C1E8610A4401887D1863AC99F9802DC00D34B5BCD72D6F36CB6E7D95EBC600013A88010A8271B6281803B12E124633006A2AC3A8AC600BCD07C9851008712DEAE83A802929DC51EE5EF5AE61BCD0648028596129C3B98129E5A9A329ADD62CCE0164DDF2F9343135CCE2137094A620E53FACF37299F0007392A0B2A7F0BA5F61B3349F3DFAEDE8C01797BD3F8BC48740140004322246A8A2200CC678651AA46F09AEB80191940029A9A9546E79764F7C9D608EA0174B63F815922999A84CE7F95C954D7FD9E0890047D2DC13B0042488259F4C0159922B0046565833828A00ACCD63D189D4983E800AFC955F211C700'
PART_1_TESTS = [
    'D2FE28',                           # Literal, version 6, value 2021
    '38006F45291200',                   # Operator, version 1, values (Literal, version 6, value 10) (Literal, version 2, value 20)
    'EE00D40C823060',                   # Operator, version 7, values (Literal, version 2, value 1) (Literal, version 4, value 2) (Literal, version 1, value 3)
    '8A004A801A8002F478',               # represents an operator packet (version 4) which contains an operator packet (version 1) which contains an operator packet (version 5) which contains a literal value (version 6); this packet has a version sum of 16.
    '620080001611562C8802118E34',       # represents an operator packet (version 3) which contains two sub-packets; each sub-packet is an operator packet that contains two literal values. This packet has a version sum of 12.
    'C0015000016115A2E0802F182340',     # has the same structure as the previous example, but the outermost packet uses a different length type ID. This packet has a version sum of 23.
    'A0016C880162017C3686B18A3D4780',   # is an operator packet that contains an operator packet that contains an operator packet that contains five literal values; it has a version sum of 31.
]

TEST_EXPECTED_VERSION_SUMS = [
    6,
    9,
    14,
    16,
    12,
    23,
    31 
]

PART_2_TESTS = [
    ('C200B40A82', 3),
    ('04005AC33890', 54),
    ('880086C3E88112', 7),
    ('CE00C43D881120', 9),
    ('D8005AC2A8F0', 1),
    ('F600BC2D8F', 0),
    ('9C005AC2F8F0', 0),
    ('9C0141080250320F1802104A08', 1),
]

def to_binary(hex):
    bin_str = []
    for hex_char in hex:
        bin_str.append(format(int(hex_char, 16), '0=4b'))
    return ''.join(bin_str)

TEST_EXPECTED_BINARY = [
    '110100101111111000101000',
    '00111000000000000110111101000101001010010001001000000000',
    '11101110000000001101010000001100100000100011000001100000',
]

def test_to_binary():
    for i in range(3):
        assert to_binary(PART_1_TESTS[i]) == TEST_EXPECTED_BINARY[i]


class Packet:
    def __init__(self, version, type_id):
        self.version = version
        self.type_id = type_id
        self.size = None

class LiteralPacket(Packet):
    def __init__(self, version, type_id, literal):
        super().__init__(version, type_id)
        self.literal = literal
        self.size = None
    
    def value(self):
        return self.literal

    def version_sum(self):
        return self.version
    
    def __str__(self):
        return f"<{self.version},{self.literal}>"

class OpPacket(Packet):
    def __init__(self, version, type_id, subpackets):
        super().__init__(version, type_id)
        self.subpackets = subpackets

    def version_sum(self):
        return self.version + sum([subpacket.version_sum() for subpacket in self.subpackets])

    def value(self):
        subpacket_values = [subpacket.value() for subpacket in self.subpackets]
        if self.type_id == 0: #sum
            return sum(subpacket_values)
        elif self.type_id == 1: #product
            return prod(subpacket_values)
        elif self.type_id == 2: #minimum
            return min(subpacket_values) 
        elif self.type_id == 3: #maximum
            return max(subpacket_values)
        elif self.type_id == 4:
            assert False, "Op somehow has id 4"
        else:
            assert len(subpacket_values) == 2
            if self.type_id == 5: # greater than
                predicate = lambda a, b: a > b
            elif self.type_id == 6: # less than
                predicate = lambda a, b: a < b
            elif self.type_id == 7: # equal_to
                predicate = lambda a, b: a == b
            return predicate(subpacket_values[0], subpacket_values[1])
        
    def __str__(self):
        return  f"{self.version}{{" + "  ".join([str(subpacket) for subpacket in self.subpackets]) + "}"


class PacketReader:
    def __init__(self, hex_string):
        self.pointer = 0
        self.binary_string = to_binary(hex_string)
    
    def read(self, bits_to_read, value_transformer=None):
        value = self.binary_string[self.pointer:self.pointer+bits_to_read]
        self.pointer += bits_to_read
        if value_transformer is not None:
            value = value_transformer(value)
        return value
    
    def read_bit(self):
        return self.read_int(1)

    def read_int(self, bits_to_read):
        b_to_i = lambda b: int(b, 2)
        return self.read(bits_to_read, value_transformer=b_to_i)

    def read_sequence(self, *bit_sequences_to_read):
        sequence = []
        for bit_sequence_to_read in bit_sequences_to_read:
            bit_sequence = self.read(bit_sequence_to_read)
            sequence.append(bit_sequence)
        return sequence

def parse_literal(reader):
    literal = []
    should_continue = True
    while should_continue:
        should_continue_bit, literal_group = reader.read_sequence(1, 4)
        should_continue = should_continue_bit == '1'
        literal.append(literal_group)
    return int(''.join(literal), 2)

def parse_bit_length_operator_packet(reader):
    bits_to_read = reader.read_int(15)
    bits_read = 0
    subpackets = []
    while bits_read < bits_to_read:
        packet = parse_packet(reader)
        subpackets.append(packet)
        bits_read += packet.size
    return subpackets

def parse_subpacket_count_operator_packet(reader):
    subpackets_to_read = reader.read_int(11)
    subpackets_read = 0
    subpackets = []
    while subpackets_read < subpackets_to_read:
        packet = parse_packet(reader)
        subpackets.append(packet)
        subpackets_read += 1
    return subpackets

def parse_packet(reader):
    packet_pointer_start = reader.pointer
    packet_version = reader.read_int(3)
    packet_type_id = reader.read_int(3)
    
    if packet_type_id == 4:
        literal = parse_literal(reader)
        packet = LiteralPacket(packet_version, packet_type_id, literal)
    else:
        length_type_id = reader.read_bit()
        if length_type_id == 0:
            subpackets = parse_bit_length_operator_packet(reader)
        else:
            subpackets = parse_subpacket_count_operator_packet(reader)
        packet = OpPacket(packet_version, packet_type_id, subpackets)
    packet.size = reader.pointer - packet_pointer_start
    return packet

def parse_packets(hex_str):
    reader = PacketReader(hex_str)
    base_packet = parse_packet(reader)
    return base_packet

def run_tests():
    test_to_binary()
    test_packets = [parse_packets(test_str) for test_str in PART_1_TESTS]
    for i, (packet, expected_sum) in enumerate(zip(test_packets, TEST_EXPECTED_VERSION_SUMS)):
        version_sum = packet.version_sum()
        assert version_sum == expected_sum, f"#{i}: {version_sum} != {expected_sum}"
        
    for test_input, expected_result in PART_2_TESTS:
        packet = parse_packets(test_input)
        actual = packet.value()
        assert actual == expected_result, str(packet)
    print('> Tests all pass')
    

if __name__ == "__main__":
    run_tests()
    packet = parse_packets(PUZZLE_INPUT)
    print(f"Part 1: {packet.version_sum()}")
    print(f"Part 2: {packet.value()}")
