import dns.resolver

def dns_lookup(domain):
    records = {}
    try:
        for rtype in ["A", "MX", "NS"]:
            answers = dns.resolver.resolve(domain, rtype)
            records[rtype] = [str(r) for r in answers]
    except Exception as e:
        records["error"] = str(e)
    return records