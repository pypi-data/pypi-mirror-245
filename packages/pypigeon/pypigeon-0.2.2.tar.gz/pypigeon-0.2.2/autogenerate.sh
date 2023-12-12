#!/bin/bash

set -e
cd "$(dirname "$0")"

if [[ ! -e venv/bin/activate ]]; then
    python3 -m venv venv
    . venv/bin/activate
    pip install -e '.[dev]'
else
    . venv/bin/activate
fi

### Update the pigeon_core low level client library

pushd pypigeon

# Preserve hand-edited files
PIGEON_CORE="$PWD/pigeon_core"
TMPF=$(mktemp)
pushd pigeon_core; tar cf $TMPF.tar .opcignore $(< .opcignore); popd
trap "cd $PIGEON_CORE; tar xf $TMPF.tar; rm $TMPF.tar" EXIT

# dereference requestBody and parameters
# this is necessary because of:
# - https://github.com/openapi-generators/openapi-python-client/issues/605
# - https://github.com/openapi-generators/openapi-python-client/issues/595

PROCESSED_API=$(mktemp)
python - $PROCESSED_API <<"EOF"
import sys, yaml, copy

doc = yaml.safe_load(open('../../../pigeon-api.yaml'))

def deref(top, path):
    assert path.startswith('#/')
    x = top
    for component in path.split('/')[1:]:
        x = x[component]
    return copy.deepcopy(x)

for path_key, path in doc['paths'].items():
    if 'parameters' in path:
        for i in range(len(path['parameters'])):
            if '$ref' not in path['parameters'][i]:
                continue
            ref = path['parameters'][i]['$ref']
            path['parameters'][i] = deref(doc, ref)

    for method_key, method in path.items():
        if method_key == 'parameters':
            continue
        if 'parameters' in method:
            for i in range(len(method['parameters'])):
                if '$ref' not in method['parameters'][i]:
                    continue
                ref = method['parameters'][i]['$ref']
                method['parameters'][i] = deref(doc, ref)

        if 'requestBody' in method and '$ref' in method['requestBody']:
            method['requestBody'] = deref(doc, method['requestBody']['$ref'])

        for k in method['responses']:
            if '$ref' in method['responses'][k]:
                method['responses'][k] = deref(doc, method['responses'][k]['$ref'])

with open(sys.argv[1], 'w') as fp:
    fp.write(yaml.dump(doc))

EOF

openapi-python-client update \
                      --path $PROCESSED_API \
                      --config ../.openapi-python-client/config.yaml \
                      --custom-template-path ../.openapi-python-client/templates \
                      --meta none

rm $PROCESSED_API

popd
