#!/usr/bin/env python3
"""proclist - List and filter running processes."""
import subprocess, argparse, re, sys

def get_processes():
    out = subprocess.check_output(['ps', 'aux'], text=True)
    lines = out.strip().split('\n')
    header = lines[0]
    procs = []
    for line in lines[1:]:
        parts = line.split(None, 10)
        if len(parts) >= 11:
            procs.append({
                'user': parts[0], 'pid': int(parts[1]),
                'cpu': float(parts[2]), 'mem': float(parts[3]),
                'vsz': int(parts[4]), 'rss': int(parts[5]),
                'tty': parts[6], 'stat': parts[7],
                'start': parts[8], 'time': parts[9],
                'command': parts[10]
            })
    return procs

def fmt_mem(kb):
    if kb >= 1048576: return f"{kb/1048576:.1f}G"
    if kb >= 1024: return f"{kb/1024:.1f}M"
    return f"{kb}K"

def main():
    p = argparse.ArgumentParser(description='List and filter processes')
    p.add_argument('filter', nargs='?', help='Filter by name (regex)')
    p.add_argument('-u', '--user', help='Filter by user')
    p.add_argument('--sort', choices=['cpu','mem','pid','rss'], default='cpu', help='Sort by field')
    p.add_argument('-n', '--top', type=int, help='Show top N processes')
    p.add_argument('--min-cpu', type=float, default=0, help='Min CPU%%')
    p.add_argument('--min-mem', type=float, default=0, help='Min MEM%%')
    p.add_argument('-k', '--kill', action='store_true', help='Kill matched processes')
    args = p.parse_args()

    procs = get_processes()
    if args.filter:
        pat = re.compile(args.filter, re.I)
        procs = [p for p in procs if pat.search(p['command'])]
    if args.user:
        procs = [p for p in procs if p['user'] == args.user]
    procs = [p for p in procs if p['cpu'] >= args.min_cpu and p['mem'] >= args.min_mem]
    procs.sort(key=lambda x: x[args.sort], reverse=True)
    if args.top:
        procs = procs[:args.top]

    if args.kill:
        import signal
        for proc in procs:
            try:
                import os as _os
                _os.kill(proc['pid'], signal.SIGTERM)
                print(f"Killed PID {proc['pid']}: {proc['command'][:60]}")
            except ProcessLookupError:
                pass
        return

    print(f"{'PID':>7} {'USER':<10} {'CPU%':>5} {'MEM%':>5} {'RSS':>7} {'COMMAND'}")
    for proc in procs:
        print(f"{proc['pid']:>7} {proc['user']:<10} {proc['cpu']:>5.1f} {proc['mem']:>5.1f} {fmt_mem(proc['rss']):>7} {proc['command'][:80]}")
    print(f"\n{len(procs)} processes")

if __name__ == '__main__':
    main()
