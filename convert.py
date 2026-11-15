#!/usr/bin/env python3
"""Конвертирует списки Re:Filter (и community-список) в формат RULE-SET для Shadowrocket."""
import ipaddress, urllib.request, pathlib

BASE = "https://github.com/1andrevich/Re-filter-lists/releases/latest/download/"
SOURCES = {
    "domains": BASE + "domains_all.lst",
    "ips": BASE + "ipsum.lst",
    "community": "https://community.antifilter.download/list/domains.lst",
}
OUT = pathlib.Path(__file__).parent / "lists"

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "list-converter"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return [l.strip().lower() for l in r.read().decode("utf-8", "ignore").splitlines()]

def clean_domains(lines):
    doms = {l.lstrip(".") for l in lines if l and not l.startswith("#") and "." in l}
    # выкидываем поддомены, если родитель уже есть (DOMAIN-SUFFIX их покроет)
    keep = []
    for d in doms:
        parts = d.split(".")
        if not any(".".join(parts[i:]) in doms for i in range(1, len(parts) - 1)):
            keep.append(d)
    return sorted(keep)

def write(name, header, rules):
    (OUT / name).write_text(f"# {header}\n# rules: {len(rules)}\n" + "\n".join(rules) + "\n")
    print(name, len(rules))

def main():
    OUT.mkdir(exist_ok=True)
    write("refilter_domains.list", "Re:Filter domains_all",
          [f"DOMAIN-SUFFIX,{d}" for d in clean_domains(fetch(SOURCES["domains"]))])
    nets = []
    for l in fetch(SOURCES["ips"]):
        try:
            nets.append(ipaddress.ip_network(l, strict=False))
        except ValueError:
            pass
    v4 = ipaddress.collapse_addresses(n for n in nets if n.version == 4)
    v6 = ipaddress.collapse_addresses(n for n in nets if n.version == 6)
    write("refilter_ip.list", "Re:Filter ipsum",
          [f"IP-CIDR,{n},no-resolve" for n in v4] + [f"IP-CIDR6,{n},no-resolve" for n in v6])
    write("community.list", "antifilter community",
          [f"DOMAIN-SUFFIX,{d}" for d in clean_domains(fetch(SOURCES["community"]))])

if __name__ == "__main__":
    main()
