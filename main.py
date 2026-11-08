"""Compare printer firmware versions against minimum versions.

Usage: python3 main.py printers.csv --minimums minimums.csv
Printers CSV columns: printer,model,firmware_version.
Minimums CSV columns: model,minimum_version.
UPDATE when the installed version is below the minimum for its
model, OK when it meets it, UNKNOWN when no minimum is recorded
for that model. Updates first, lowest version first.
"""
import argparse, csv, sys

def parse_version(text):
    return tuple(int(part) for part in text.strip().split("."))

def compare_versions(installed, minimum):
    a, b = parse_version(installed), parse_version(minimum)
    return (a > b) - (a < b)

def check(rows, minimums):
    out = []
    for row in rows:
        model = row["model"].strip()
        installed = row["firmware_version"].strip()
        minimum = minimums.get(model)
        if minimum is None:
            verdict = "UNKNOWN"
        elif compare_versions(installed, minimum) < 0:
            verdict = "UPDATE"
        else:
            verdict = "OK"
        out.append((row["printer"].strip(), model, installed, minimum, verdict))
    order = {"UPDATE": 0, "UNKNOWN": 1, "OK": 2}
    return sorted(out, key=lambda r: (order[r[4]], parse_version(r[2])))

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path")
    parser.add_argument("--minimums", required=True)
    args = parser.parse_args(argv)
    with open(args.minimums, newline="", encoding="utf-8") as f:
        minimums = {r["model"].strip(): r["minimum_version"].strip() for r in csv.DictReader(f)}
    with open(args.path, newline="", encoding="utf-8") as f:
        results = check(list(csv.DictReader(f)), minimums)
    for printer, model, installed, minimum, verdict in results:
        minimum_text = f"minimum {minimum}" if minimum else "no minimum recorded"
        print(f"{printer} ({model}): {verdict} (firmware {installed}, {minimum_text})")
    print(f"{sum(1 for *_, v in results if v == 'UPDATE')} printer(s) need a firmware update.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
