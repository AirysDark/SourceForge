def pkt_line(data: bytes) -> bytes:
    length = len(data) + 4
    return f"{length:04x}".encode() + data

def pkt_flush() -> bytes:
    return b"0000"

def decode_pkt_lines(stream: bytes):
    pos = 0
    out = []
    while pos + 4 <= len(stream):
        size = int(stream[pos:pos+4], 16)
        pos += 4
        if size == 0:
            break
        payload = stream[pos:pos+size-4]
        out.append(payload)
        pos += size - 4
    return out
