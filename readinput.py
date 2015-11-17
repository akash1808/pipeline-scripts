import yaml
with open('test.yaml', 'r') as f:
    doc = yaml.load(f)
print doc['stable_snapshot_uuid']
