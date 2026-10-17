"""Conservative consumer compatibility check: additions must be optional."""
def breaking_changes(old, new):
    failures = []
    for name, definition in old['fields'].items():
        if name not in new['fields']:
            failures.append(f'{name}: removed')
        elif definition['type'] != new['fields'][name]['type']:
            failures.append(f'{name}: type changed')
        elif not definition['required'] and new['fields'][name]['required']:
            failures.append(f'{name}: now required')
    for name, definition in new['fields'].items():
        if name not in old['fields'] and definition['required']:
            failures.append(f'{name}: new required field')
    return failures

def main():
    import argparse
    import json
    from pathlib import Path
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('old'); parser.add_argument('new'); args = parser.parse_args()
    failures = breaking_changes(json.loads(Path(args.old).read_text()), json.loads(Path(args.new).read_text()))
    if failures:
        raise SystemExit('\n'.join(failures))
    print('No structural breaking changes')

if __name__ == '__main__':
    main()
