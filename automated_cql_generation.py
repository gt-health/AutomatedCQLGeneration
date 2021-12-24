import json
import re
import argparse

from entities import *
from generators import *

def cql_from_json_with_entities(data):

    # Written to support creating CQL from a pre-specified JSON file
    scriptType = data['type']
    if scriptType == 'IndexEventAndInclusion':
        script = IndexEventAndInclusionScript(data)
    else:
        return "This script type is not supported"

    return R4Generator.generate(script)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process an input json to create a CQL script.')
    parser.add_argument('--input', help='optional input json, assumes file name of input_json.json')
    parser.add_argument("--output", help="optional output file name, assumes same name as input")
    args = parser.parse_args()
    input_file = 'cql_template_definition/syphilis_medication_treatment.json'
    if args.input:
        input_file = args.input
    input_split = re.split('/|\.', input_file)
    output_file = ''.join(['cql/', input_split[-2],'.cql'])
    if args.output:
        output_file = args.output

    with open(input_file) as f:
        data = json.load(f)

    with open(output_file, 'w+') as f:
        f.write(cql_from_json_with_entities(data))















