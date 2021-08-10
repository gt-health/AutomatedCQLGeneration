import ast
import csv
import json
import os
import re
import string
from os import path, remove, write

import requests

from entities import *

from generators import *

import argparse

def cleanup_row(r):
    # Turns a row from the csv and turns it into a dictionary
    output_row = dict()
    row = json.loads(json.dumps(r, indent=4, sort_keys=True).replace('\\u00a0', ' ').replace('\\u00ad', '-')
                     .replace('\\u2265', '>=').replace('\\u2264', '<=').replace('\\u00b3', '3').replace(
        '\\u00b0', ' degrees')
                     .replace('\\u03b3', 'gamma').replace('\\u03b1', 'alpha').replace('\\u00b5', 'u'))
    for ro in row.keys():
        new_key = ro.strip().lower()
        output_row[new_key] = row[ro].strip()
    return output_row

def cql_convert_to_concept_statement(feature_name,codes,code_sys,valueset_oid):
    concepts = []
    c_string = ""
    if not codes:
        codes = list()
    if len(codes) == 1 and codes[0] == '':
        codes = list()
    if len(codes) > 0:
        for c in codes:
            if len(c_string) > 0:
                c_string += ', \n            '
            code = c.replace('?', '').replace('"', '').replace("'", '')
            c_string += 'Code \'{}\' from "{}"'.format(code, code_sys)
        cql_concept = cql_concept_template % (feature_name, c_string)
        concepts.append(cql_concept)
    if valueset_oid and len(valueset_oid) > 0:
        valueset_oid = valueset_oid.replace('?', '').replace('"', '').replace("'", '')
        cql_header = cql_valueset_template.format(feature_name, valueset_oid)
    if len(concepts) == 0:
        return ""
    concepts = "\n\n".join(concepts)
    return concepts

def cql_convert_to_retrieval_statement(feature_name,resource,codes,valueset_oid):
    cql_result_members = []
    if not resource or len(resource) == 0:
        resource = 'Observation'
    if not codes:
        codes = list()
    if len(codes) == 1 and codes[0] == '':
        codes = list()
    if len(codes) > 0:
        cql_result_members.append(cql_result_template_cs.format(resource, feature_name))
    if valueset_oid and len(valueset_oid) > 0:
        cql_result_members.append(cql_result_template_vs.format(resource, feature_name))
    if len(cql_result_members) == 0:
        cql_result_members.append(cql_result_template_res.format(resource))
    return "".join(cql_result_members)

def parse_questions_from_feature_csv(folder_prefix='',
                                     form_name='testcsv',
                                     file_name='test_csv.csv',
                                     output_dir=os.path.dirname(os.path.realpath(__file__)),
                                     description=None):
    # This is the main function that is run when processing a csv into CQL and NLPQL files
    # Inputs: folder_prefix = if you want to put everything in a new subfolder, you would put that value here (defaults to nothing)
    #         form_name = the name of the form you want to create using your csv (defaults to testcsv)
    #         file_name = the name of the csv that you want to process (defaults to test_csv.csv). It will take just the file name if the 
    #                     file is in the same folder or it will take the full path, but if the file is not in the same folder, you MUST provide the full path
    #         output_dir = where you want your output files to go (defaults to directory in which this file is saved)
    #         description = Description of your form (defaults to the form_name)
    # Outputs: CQL file with the generated CQL from the CSV
    #          NLPQL file that has the CQL wrapped in a CQL Execution Task in NLPQL    

    if not description:
        description = form_name
    
    # Creates output folders as needed
    output_folder_path = os.path.join(output_dir, folder_prefix)
    if not os.path.exists(output_folder_path):
        os.mkdir(output_folder_path)
    cql_folder = os.path.join(output_folder_path, 'cql')
    if not os.path.exists(cql_folder):
        os.mkdir(cql_folder)


    temp = False
    # if file name is from the web, it pulls that data into a temp csv
    if file_name.startswith('http'):
        r = requests.get(file_name)
        temp = True

        file_name = '/tmp/{}.csv'.format(folder_prefix)
        with open(file_name, 'wb') as f:
            f.write(r.content)
    
    # if file name is not a full path, it makes it into one
    if not (file_name.startswith('/') or file_name.startswith('C:\\')):
        file_name = os.path.dirname(os.path.realpath(__file__)) + '/' + file_name

    # new area of coding, using typed objects and generating an entities.json file from all entities present
    with open(file_name, 'r', encoding='utf-8', errors='ignore') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',', quotechar='"')
        retrievalLibrary = {}
        group_names = []
        for r in reader:
            row = cleanup_row(r)
            filled_fields = sum(x != '' for x in row.values())-7
            r_evidence_bundle = row.get('evidence_bundle', '')
            r_num = row.get('#', '')
            r_group = row.get('group', '')
            group_names.append(r_group)
            r_question_name = row.get('question_name', r.get('name', 'Unknown'))
            r_answers = row.get('answers', '')
            r_type = row.get('type', row.get('question_type', ''))
            r_feature_name = row.get('feature_name', '').replace(' ', '')
            r_fhir_resource_type = row.get('fhir_resource_type', '')
            r_code_system = row.get('code_system', '')
            r_codes = row.get('codes', '')
            r_codes_split = r_codes.split(':')
            r_valueset_oid = row.get('valueset_oid', '')
            r_cql_expression = row.get('cql_expression', '')
            r_nlp_task_type = row.get('nlp_task_type', '')

            r_where_clause_attribute = row.get('where_clause_attribute', '')
            r_where_clause_value = row.get('where_clause_value')
            r_where_clause_during_begin = row.get('where_clause_during_begin')
            r_where_clause_during_after = row.get('where_clause_during_after')

            # Convert date into correct format if not already
            if r_where_clause_during_begin and r_where_clause_during_begin[0]!='@':
                r_where_clause_during_begin = '@'+ parser.parse(r_where_clause_during_begin).isoformat()
            if r_where_clause_during_after and r_where_clause_during_after[0]!='@':
                r_where_clause_during_after = '@'+ parser.parse(r_where_clause_during_after).isoformat()

            r_relationship_fhir_resource_type = row.get('relationship_fhir_resource_type','')
            r_relationship_code_system = row.get('relationship_code_system')
            r_relationship_codes = row.get('relationship_codes')
            r_relationship_valueset = row.get('relationship_valueset')
            r_relationship_where_clause = row.get('relationship_where_clause')

            if (r_cql_expression):
                retrievalLibrary[r_feature_name] = FreeTextEntity(r_group, r_fhir_resource_type, r_cql_expression).__dict__
            elif (r_fhir_resource_type and r_code_system and r_codes and filled_fields==3):
                retrievalLibrary[r_feature_name] = SimpleRetrievalEntity(r_group, r_fhir_resource_type, r_code_system, r_codes_split, r_valueset_oid).__dict__
            elif (r_fhir_resource_type and r_code_system and r_codes and (r_where_clause_during_begin or r_where_clause_during_after)):
                retrievalLibrary[r_feature_name] = TemporalFilterEntity(r_group, r_fhir_resource_type, r_code_system, r_codes_split, r_valueset_oid, r_where_clause_attribute, \
                                                                        r_where_clause_during_begin, r_where_clause_during_after).__dict__
            elif (r_where_clause_attribute and r_where_clause_value):
                retrievalLibrary[r_feature_name] = ValueFilterEntity(r_group, r_fhir_resource_type, r_where_clause_attribute, r_where_clause_value).__dict__
            elif (r_relationship_fhir_resource_type and ((r_relationship_codes and r_relationship_code_system) or r_relationship_valueset)):
                retrievalLibrary[r_feature_name] = RelatedEntity(r_group, r_fhir_resource_type, r_code_system, r_codes_split, r_valueset_oid, r_relationship_fhir_resource_type, \
                                                                 r_relationship_codes, r_relationship_code_system, r_relationship_valueset, r_relationship_where_clause).__dict__
            else:
                retrievalLibrary[r_feature_name] = NonEntity(r_group, {k: v for k, v in row.items() if v != ''}).__dict__

    # creates entities_{filename}.json file
    with open(os.path.dirname(os.path.realpath(__file__))+'/entities_{}.json'.format(form_name), 'w') as f:
        f.write(json.dumps(retrievalLibrary, indent=4))
    
    # Next thing to make: use the retrievalLibrary to generate the CQL instead of the individual logic below
    group_names = list(set(group_names))
    output_cql = {k:'' for k in group_names}

    # Generates CQL for each entity that was previously created
    for name, entity in retrievalLibrary.items():
        group_name = entity['group']
        # if entity has codes, need to define concepts first before using the regular template
        if entity['entity_type'] == 'SimpleRetrievalEntity':
            simple_concepts = cql_convert_to_concept_statement(name, entity['codes'], entity['code_system'], entity['valueset_oid'])
            simple_retrieval = cql_convert_to_retrieval_statement(name, entity['fhir_resource'], entity['codes'], entity['valueset_oid'])
            simple_retrieval = cql_result_template.format(name, simple_retrieval)
            output_cql[group_name] = output_cql[group_name] + simple_concepts + simple_retrieval
        if entity['entity_type'] == 'FreeTextEntity':
            free_text = cql_result_template.format(name, entity['cql_expression'])
            output_cql[group_name] += free_text
        if entity['entity_type'] == 'TemporalFilterEntity':
            temporal_concepts = cql_convert_to_concept_statement(name, entity['codes'], entity['code_system'], entity['valueset_oid'])
            attribute = entity["where_clause_attribute"]
            if entity["where_clause_during_begin"] and entity["where_clause_during_after"]:
                begin = entity["where_clause_during_begin"]
                after = entity["where_clause_during_after"]
                temporal_result = cql_filter_where_during_clause_template.format(attribute,begin,after)
            elif entity["where_clause_during_begin"]:
                begin = entity["where_clause_during_begin"]
                temporal_result = cql_filter_where_before_clause_template.format(attribute, begin)
            elif entity["where_clause_during_after"]:
                after = entity["where_clause_during_after"]
                temporal_result = cql_filter_where_before_clause_template.format(attribute, after)
            temporal_result = '        ' + temporal_result.lstrip()
            temporal_result = cql_result_template.format(name, cql_convert_to_retrieval_statement(name, entity['fhir_resource'], entity['codes'], entity['valueset_oid'])) + temporal_result
            output_cql[group_name] += temporal_result
        if entity['entity_type'] == 'ValueFilterEntity':
            value_filter_result = cql_filter_where_in_clause_template.format(entity['where_clause_attribute'], entity['where_clause_value'])
            value_filter_result = '        ' + value_filter_result.lstrip()
            value_filter_result = cql_result_template.format(name, cql_convert_to_retrieval_statement(name, entity['fhir_resource'], '', '')) + value_filter_result
            output_cql[group_name] += value_filter_result
        if entity['entity_type'] == 'RelatedEntity':
            related_concepts = cql_convert_to_concept_statement(name, entity['codes'], entity['code_system'], entity['valueset_oid'])
            related_fhir_resource_type = entity["relationship_fhir_resource_type"]
            related_codes = entity["relationship_codes"]
            related_codesys = entity["relationship_code_system"]
            related_valueset = entity["relationship_valueset"]
            relationship_where_clause = entity["relationship_where_clause"]
            related_retrevial_statement = cql_convert_to_retrieval_statement(name+"_related",
                                                                         related_fhir_resource_type,related_codes,
                                                                         related_valueset)
            related_result = cql_with_relationship_template.format(related_retrevial_statement,relationship_where_clause)
            related_result = '        ' + related_result.lstrip()
            related_result = cql_result_template.format(name, cql_convert_to_retrieval_statement(name, entity['fhir_resource'], entity['codes'], entity['valueset_oid'])) + related_result
            output_cql[group_name] += related_concepts
            output_cql[group_name] += related_result
    
    # Writes CQL using the cql_template_header
    for item in output_cql.items():
        group_name, cql_contents  = item
        cql_contents = cql_template_header.format(form_name) + cql_contents
        filename = '{}/{}.cql'.format(output_dir+'/cql', group_name)
        with open(filename, 'w') as f:
            f.write(cql_contents)

    # Writes NLPQL file with tasks based on groups
    # nlpql_template2.format(phenotype name, termsets, data entities, operations)
    termsets = ''
    entities = ''
    operations = ''

    count = 0
    for item in output_cql.items():
        group_name, cql_contents = item
        cql_contents = cql_template_header.format(form_name) + cql_contents
        entities += cql_task_template % (group_name, str(count), cql_contents)
        count += 1

    output_nlpql = nlpql_template2.format(form_name, termsets, entities, operations)
    filename = '{}/{}/{}.nlpql'.format(output_dir, folder_prefix, form_name)
    with open(filename, 'w') as f:
            f.write(output_nlpql)

def cql_from_json(input_json):
    
    # Written to support creating CQL from a prespecified JSON file
    cql_statements = ''
    entityLibrary = {}
    
    with open(input_json) as f:
        data = json.load(f)
        
    # Generates Concept statements
    for concept in data['concepts']:
        name = concept['name']
        codelist = concept['codeset']['codelist']
        codesystem = concept['codeset']['system']
        cql_statements += cql_convert_to_concept_statement(name, codelist, codesystem, '')
    
    # Generates Event Statement
    event_statement = cql_retrieval.format(data['event']['name'], data['event']['fhirResource'], 'myConcept')
    cql_statements += event_statement
    event_return = cql_event_return.format(data['event']['returnField'], data['event']['returnField'].lower()+data['event']['returnType'])
    cql_statements += event_return
    
    retrievalLibrary[data['event']['name']] = EventEntity(data['event']['fhirResource'], data['concept'], data['returnField'], data['returnType'])
    
    # Generates Inclusion Criteria
    for inclusion in data['Inclusion']:
        fhirResource = inclusion['fhirResource']
        concept = inclusion['concept']
        resultType = inclusion['resultType']
        resultAnswer = inclusion['resultAnswer']
        sourceValue = inclusion['sourceValue']
        filterType = inclusion['filter']
    
    filename = 'cql/{}.cql'.format(data['type'])
    cql_final = cql_template_header.format(data['type']) + cql_statements
    with open(filename, 'w') as f:
        f.write(cql_final)

def cql_from_json_with_entities(input_json):
    
    # Written to support creating CQL from a pre-specified JSON file
    
    entityLibrary = {}
    
    with open(input_json) as f:
        data = json.load(f)
        
    scriptType = data['type']
    if scriptType == 'EventAndInclusion':
        script = EventAndInclusionScript(data)
    #print(script)
    
    return STU3Generator.generate(script)

if __name__ == "__main__":
    # parse_questions_from_feature_csv(folder_prefix = '', form_name =  'testcsv', description = 'Test Definition')
    
    parser = argparse.ArgumentParser(description='Process an input json to create a CQL script.')
    parser.add_argument('--input', help='the input json')
    parser.add_argument("--output", help="optional output file name")
    args = parser.parse_args()
    input_file = 'input_json.json'
    if args.input:
        input_file = args.input
    input_split = input_file.split('.')
    output_file = ''.join([input_split[0],'.cql'])
    if args.output:
        output_file = args.output

    with open(output_file, 'w+') as f:
        f.write(cql_from_json_with_entities(input_file))

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    