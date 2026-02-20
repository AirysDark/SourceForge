from app.git.pktline import pkt_line, pkt_flush

def parse_wants_haves(body: bytes):
    wants, haves = [], []
    try:
        text = body.decode(errors="ignore")
        for line in text.splitlines():
            if line.startswith("want "):
                wants.append(line.split()[1])
            elif line.startswith("have "):
                haves.append(line.split()[1])
    except:
        pass
    return wants, haves

def ack():
    return pkt_line(b"NAK\n") + pkt_flush()
