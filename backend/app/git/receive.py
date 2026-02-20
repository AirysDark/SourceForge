from app.git.pktline import decode_pkt_lines, pkt_line, pkt_flush
from app.git.hooks.update_engine import run_update

def parse_push(body: bytes):
    pkts = decode_pkt_lines(body)
    cmds = []
    for p in pkts:
        try:
            line = p.decode(errors="ignore").strip()
            parts = line.split()
            if len(parts) >= 3 and parts[2].startswith("refs/"):
                cmds.append((parts[0], parts[1], parts[2]))
        except:
            pass
    return cmds

def apply_push(repo: str, cmds):
    results = []
    for old_sha, new_sha, ref in cmds:
        ok, msg = run_update(repo, ref, old_sha, new_sha, user="demo")
        results.append((ref, ok, msg))
    return results

def report(results):
    out = b""
    for ref, ok, msg in results:
        if ok:
            out += pkt_line(f"ok {ref}\n".encode())
        else:
            out += pkt_line(f"ng {ref} {msg}\n".encode())
    out += pkt_flush()
    return out
