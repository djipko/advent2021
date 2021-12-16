#!/usr/bin/env python3

import operator
from functools import reduce
from enum import Enum, auto, IntEnum
from more_itertools import chunked, take, peekable, spy


class PacketType(Enum):
    LITERAL = auto()
    OP = auto()
    EOF = auto()


class OpType(IntEnum):
    SUM = 0
    PROD = 1
    MIN = 2
    MAX = 3
    GT = 5
    LT = 6
    EQ = 7


class Packet:
    def __init__(self, payload, parse_single=False):
        self.value = None
        self.op = None
        self.sub_packets = []
        self.next = None
        self._parse(payload, parse_single)

    def _parse(self, pload, parse_single):
        if pload.peek(None) is None:
            self.type = PacketType.EOF
            return
        head, pload = spy(pload, 6)
        if len(head) < 6:
            self.type = PacketType.EOF
            return
        pload = peekable(pload)

        self.version = int("".join(take(3, pload)), 2)
        self.type_id = int("".join(take(3, pload)), 2)

        if self.type_id == 4:
            self.type = PacketType.LITERAL
            self._parse_literal(pload)
        else:
            self.type = PacketType.OP
            self.op = OpType(self.type_id)
            self._parse_op(pload)

        if not parse_single:
            self.next = Packet(pload)

    def __iter__(self):
        return self.sequence()

    def _parse_literal(self, pload):
        parts = []
        for part in chunked(pload, 5):
            parts.append(part)
            if part[0] == "0":
                break

        num = "".join("".join(part[1:]) for part in parts)
        self.value = int(num, 2)

    def _parse_op(self, pload):
        mode = next(pload)
        if mode == "0":
            sub_p_len = int("".join(take(15, pload)), 2)
            sub_pload = peekable(take(sub_p_len, pload))
            while True:
                p = Packet(sub_pload, parse_single=True)
                if p.type == PacketType.EOF:
                    break
                self.sub_packets.append(p)
        else:  # mode == "1"
            sub_p_n = int("".join(take(11, pload)), 2)
            for _ in range(sub_p_n):
                self.sub_packets.append(Packet(pload, parse_single=True))

    def sequence(self):
        if self.type != PacketType.EOF:
            yield self
            for sub in self.sub_packets:
                yield from sub
            if self.next:
                yield from self.next

    def eval(self):
        if self.type == PacketType.LITERAL:
            return self.value
        match self.op:
            case OpType.SUM:
                return sum(p.eval() for p in self.sub_packets)
            case OpType.PROD:
                return reduce(operator.mul, (p.eval() for p in self.sub_packets), 1)
            case OpType.MIN:
                return min(p.eval() for p in self.sub_packets)
            case OpType.MAX:
                return max(p.eval() for p in self.sub_packets)
            case OpType.GT:
                assert len(self.sub_packets) == 2
                fst, snd = self.sub_packets
                return 1 if fst.eval() > snd.eval() else 0
            case OpType.LT:
                assert len(self.sub_packets) == 2
                fst, snd = self.sub_packets
                return 1 if fst.eval() < snd.eval() else 0
            case OpType.EQ:
                assert len(self.sub_packets) == 2
                fst, snd = self.sub_packets
                return 1 if fst.eval() == snd.eval() else 0
            case _:
                raise RuntimeError("Invalid op {self.op}")

    def __repr__(self):
        val = ""
        if self.value:
            val = f", val: {self.value}"
        return f"Packet<{self.type}, v: {self.version}, tid: {self.type_id}{val}>"


if __name__ == "__main__":
    with open("input") as f:
        data = f.read()
    lines = [line.strip() for line in data.split("\n")]
    # do stuff withline[0] data
    hex_pload = lines[0]
    # hex_pload = "D2FE28"
    # hex_pload = "38006F45291200"
    # hex_pload = "EE00D40C823060"
    # hex_pload = "8A004A801A8002F478"
    # hex_pload = "620080001611562C8802118E34"
    # hex_pload = "C0015000016115A2E0802F182340"
    # hex_pload = "A0016C880162017C3686B18A3D4780"
    # hex_pload = "C200B40A82"
    # hex_pload = "04005AC33890"
    # hex_pload = "880086C3E88112"
    # hex_pload = "CE00C43D881120"
    # hex_pload = "D8005AC2A8F0"
    # hex_pload = "F600BC2D8F"
    # hex_pload = "9C005AC2F8F0"
    # hex_pload = "9C0141080250320F1802104A08"

    packet_b = "".join(f"{int(d, 16):04b}" for d in hex_pload)
    pload = peekable(packet_b)
    packet = Packet(pload)

    print(sum(p.version for p in iter(packet)))
    print(packet.eval())
