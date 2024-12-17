import sys
import subprocess

import dns.resolver

google = dns.resolver.Resolver()

google.nameservers = ["8.8.8.8"]

fasit = sorted(["x.nic.no.", "y.nic.no.", "z.nic.no."])

command = "./list-all"

result = subprocess.check_output(command, shell=False, text=True).split("\n")
with open("cats.list", "w") as f:
    for cat in result:
        f.flush()
        cat = cat.strip().encode("idna").decode()
        if not cat:
            continue
        try:
            answers = google.resolve(f"{cat}.no", "NS")
            names = sorted(map(str, answers))

            if names == fasit:
                print(f"{cat} OK", file=f)
            else:
                print(f"{cat} NOT OK: {', '.join(names)} ({cat.encode().decode('idna')})", file=f)
        except Exception as e:
            print(f"{cat} NOT OK: {e} ({cat.encode().decode('idna')})", file=f)
