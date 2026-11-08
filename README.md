# printer-firmware-version-tracker

Compare printer firmware versions against minimum versions per model: UPDATE when below the minimum, OK when it meets it, UNKNOWN when no minimum is recorded — updates first.

## How to run

```sh
python3 main.py printers.csv --minimums minimums.csv
```

## Example output

```
HP-Office (LaserJet): UPDATE (firmware 1.9, minimum 2.0)
Canon-Lab (LBP): OK (firmware 3.1, minimum 3.0)
1 printer(s) need a firmware update.
```

Standard library only. Run the tests with `python3 -m unittest discover`.
