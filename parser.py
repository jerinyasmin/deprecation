#!/usr/bin/env python3
# coding=utf-8

# MIT License
#
# Copyright 2017 Niels Lohmann <http://nlohmann.me>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of
# the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
# OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT
# OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import json
import sys
import csv
from typing import List, Optional, Any, Set

import pickle

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


def resolve_ref(ref):
    return ref.split('/')[-1]


class Property:
    def __init__(self, name, type, required, example=None, description=None, default=None, enum=None, format=None,
                 items=None, maximum=None, exclusive_maximum=False, minimum=None, exclusive_minimum=False,
                 multiple_of=None, max_length=None, min_length=0, pattern=None, max_items=None, min_items=0,
                 unique_items=False, ref_type=None, deprecated=False):
        # type
        self.type = type  # type: str
        self.format = format  # type: Optional[str]
        self.ref_type = ref_type  # type: Optional[str]

        # constraints
        self.required = required  # type: bool
        self.enum = enum  # type: Optional[List[Any]]
        self.deprecated = deprecated  # type: Optional[List[Any]]

        # documentation
        self.name = name  # type: str
        self.example = example  # type: Optional[Any]
        self.description = description  # type: Optional[str]
        self.default = default  # type: Optional[Any]

        # numbers
        self.maximum = maximum  # type: Optional[float,int]
        self.exclusive_maximum = exclusive_maximum  # type: bool
        self.minimum = minimum  # type: Optional[float,int]
        self.exclusive_minimum = exclusive_minimum  # type: bool
        self.multiple_of = multiple_of  # type: Optional[float,int]

        # strings
        self.max_length = max_length  # type: Optional[int]
        self.min_length = min_length  # type: int
        self.pattern = pattern  # type: Optional[str]

        # arrays
        self.max_items = max_items  # type: Optional[int]
        self.min_items = min_items  # type: int
        self.unique_items = unique_items  # type: bool
        self.items = items  # type: Optional[str]

    @staticmethod
    def from_dict(property_name, d, required):
        # whether the type was resolved
        ref_type = None

        # We use the Parameter class for parameters inside the swagger specification, but also for parameters. There,
        # type information is given in a "schema" property.
        if 'type' in d or '$ref' in d:
            type_dict = d
        elif 'schema' in d:
            type_dict = d['schema']
        elif 'allOf' in d and len(d['allOf']) > 0:
            type_dict = d['allOf'][0]
        else:
            type_dict = {}

        # type is given or must be resolved from $ref
        if 'type' in type_dict:
            type_str = type_dict['type']
        elif '$ref' in type_dict:
            type_str = resolve_ref(type_dict['$ref'])
            ref_type = type_str
        else:
            type_str = '<i>not specified</i>'

        # join multiple types to string
        if isinstance(type_str, list):
            type_str = '/'.join(type_str)

        # items type is given or must be resolved from $ref
        if 'items' in type_dict:
            if 'type' in type_dict['items']:
                items = type_dict['items']['type']
            else:
                items = resolve_ref(type_dict['items']['$ref'])
                ref_type = items

        else:
            items = None

        return Property(
            name=property_name,
            type=type_str,
            required=required,
            example=d.get('example'),
            description=d.get('description'),
            default=d.get('default'),
            enum=d.get('enum'),
            format=d.get('format'),
            items=items,
            maximum=d.get('maximum'),
            exclusive_maximum=d.get('exclusiveMaximum', False),
            minimum=d.get('minimum'),
            exclusive_minimum=d.get('exclusiveMinimum', False),
            multiple_of=d.get('multipleOf'),
            max_length=d.get('maxLength'),
            min_length=d.get('minLength', 0),
            pattern=d.get('pattern'),
            max_items=d.get('maxItems', 0),
            min_items=d.get('minItems'),
            unique_items=d.get('uniqueItems', False),
            ref_type=ref_type
        )


class Definition:
    def __init__(self, name, type, properties, relationships):
        self.name = name  # type: str
        self.type = type  # type: str
        self.properties = properties  # type: List[Property]
        self.relationships = relationships  # type: Set[str]

    @staticmethod
    def from_dict(name, d):
        properties = []  # type: List[Property]
        for property_name, property in d.get('properties', {}).items():
            properties.append(Property.from_dict(
                property_name=property_name,
                d=property,
                required=property_name in d.get('required', [])
            ))
        type=''
        if not 'type' in d:
            print('required key "type" not found in dictionary ' + json.dumps(d), file=sys.stderr)
        else:
            type = d['type']

        return Definition(name=name,
                          type=type,
                          properties=properties,
                          relationships={property.ref_type for property in properties if property.ref_type})


class Parameter:
    def __init__(self, name, location, description, required, property):
        self.name = name  # type: str
        self.location = location  # type: str
        self.description = description  # type: Optional[str]
        self.required = required  # type: bool
        self.property = property  # type: Property

    @staticmethod
    def from_dict(whole, d):
        ref = d.get('$ref')
        if ref != None:
            d = whole['parameters'][resolve_ref(ref)]
        return Parameter(
            name=d['name'],
            location=d['in'],
            description=d.get('description'),
            required=d.get('required', False),
            property=Property.from_dict(d['name'], d, d.get('required', False))
        )


class Response:
    def __init__(self, status, description, property):
        self.status = status  # type: str
        self.description = description  # type: Optional[str]
        self.property = property  # type: Property

    @staticmethod
    def from_dict(whole, status, d):
        return Response(
            status=status,
            description=d.get('description'),
            property=Property.from_dict('', d, False)
        )


class Operation:
    def __init__(self, path, type, summary, description, responses, tags, parameters, deprecated):
        self.path = path  # type: str
        self.type = type  # type: str
        self.summary = summary  # type: Optional[str]
        self.description = description  # type: Optional[str]
        self.responses = responses  # type: List[Response]
        self.tags = tags  # type: List[str]
        self.parameters = parameters  # type: List[Parameter]
        self.deprecated = deprecated

    def __lt__(self, other):
        return self.type < other.type

    @staticmethod
    def from_dict(whole, path, type, d, path_parameters):
        # print(d)
        return Operation(
            path=path,
            type=type,
            summary=d.get('summary'),
            description=d.get('description'),
            tags=d.get('tags'),
            deprecated=d.get('deprecated'),
            responses=[Response.from_dict(whole, status, response) for status, response in d['responses'].items()],
            parameters=path_parameters + [Parameter.from_dict(whole, param) for param in d.get('parameters', [])]
        )

    @property
    def name(self):
        return '{type} {path}'.format(
            type=self.type.upper(),
            path=self.path
        )


class Path:
    def __init__(self, path, operations):
        self.path = path  # type: str
        self.operations = operations  # type: List[Operation]

    @staticmethod
    def from_dict(whole, path_name, d):
        parameters = [Parameter.from_dict(whole, param) for param in d.get('parameters', [])]
        # print(d.items())

        return Path(
            path=path_name,
            operations=[Operation.from_dict(whole, path_name, t, op, parameters) for t, op in d.items()
                        if t not in ['parameters', 'summary', 'description', 'deprecated']]
        )


class Swagger:
    def __init__(self, definitions, paths):
        self.definitions = definitions  # type: List[Definition]
        self.paths = paths  # type: List[Path]

    @staticmethod
    def from_dict(d):
        definitions = [Definition.from_dict(name, definition) for name, definition in d.get('definitions', {}).items()]
        paths = [Path.from_dict(d, path_name, path) for path_name, path in d['paths'].items()]
        return Swagger(definitions=definitions, paths=paths)

    @staticmethod
    def from_file(filename):
        loader = json.load
        if filename.endswith('.yml') or filename.endswith('.yaml'):
            import yaml
            loader = yaml.load
        with open(filename, 'r', encoding='utf-8') as fd:
            return Swagger.from_dict(loader(fd))


def read(filename):
    with open(filename, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        apis = []
        for row in csv_reader:
                api = row[0].replace("\\", "/")
                apis.append(api)
                line_count += 1
    return list(set(apis))


if __name__ == '__main__':

    apis = read("result/deprecated_file.csv")
    result_operations_api = {}

    # apis = ['APIs/kubernetes.io/v1.17.0/swagger.yaml']
    apis = ['swagger1.yaml']

    for api in apis:
        if api.endswith("swagger1.yaml"):
            print(api)
            input_file_name = api
            sw = Swagger.from_file(input_file_name)
            paths = sw.paths

            result_operations = []
            for path in paths:
                endpoint = path.path
                operations = path.operations

                for operation in operations:
                    operation_path = operation.path
                    operation_type = operation.type
                    operation_description = operation.description
                    operation_summary = operation.summary

                    operation_name = operation_path + "_" + operation_type

                    # print(operation_name)

                    # operation
                    value_description = ""
                    value_summary = ""
                    if operation_description:
                        value_description = operation_description.lower()
                    if operation_summary:
                        value_summary = operation_summary.lower()
                    operation_deprecated = operation.deprecated
                    if "deprecate" in value_description or "deprecate" in value_summary or operation_deprecated:
                        result_operations.append(operation_name)


                    #operation response
                    responses = operation.responses

                    for response in responses:
                        # response.description
                        prop = response.property.ref_type
                        # print(prop)


                        # print(response.property)



            result_operations_api[api] = len(list(set(result_operations)))


            definitions = sw.definitions


            for definition in definitions:
                print(definition.name)
                def_properties = definition.properties
                # print(definition.from_dict("ref", def_properties))
                def_relations = definition.relationships

                print(def_relations)

                # for prop in def_properties:
                #     print(prop.name)
                #     print(prop.items)

                for relation in def_relations:
                    print('relation')
                    print(relation)

    print(result_operations_api)

            # parameters = operation.parameters




#cyclic references

#will be deprecated

# version pre(adobe)

#check extensions of files YAML, YML JSON