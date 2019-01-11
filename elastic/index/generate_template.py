#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Generates an index template for ElasticSearch from the BuildResults document.
"""

import argparse
import json
import sys

from elasticsearch_dsl import Index
import elastic
from elastic.schema.build_results import BuildResults

def generate_template(index_name, output_file=None):
    """
    Generates the index template associated with the structure of the BuildResults
    document, allowing it to be uploaded to an ElasticSearch instance.

    Args:
        index_name: index name to generate the template with, should be the index the module will upload to
        output_file: (optional) file path to write template to
    """

    document = BuildResults(job_name=None, job_link=None, build_date_time=None, build_id=None)
    index = Index(index_name)
    index.document(document)
    index_template = index.as_template(template_name="template")

    # Unfortunately there is no possibility to add the version via the elasticsearch_dsl library.
    # We add the version of the index template as described in
    # https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-templates.html#versioning-templates
    template_dict = index_template.to_dict()
    template_dict["version"] = elastic.__version__

    if output_file:
        with open(output_file, "w") as file:
            json.dump(template_dict, file, ensure_ascii=False, indent=4, sort_keys=True)
    else:
        print(json.dumps(template_dict, ensure_ascii=False, indent=4, sort_keys=True))

def main():
    """
    CLI interface to generate the index template for BuildResults
    """
    parser = argparse.ArgumentParser(description="Script for generating an index template out of a document")
    parser.add_argument("INDEX_NAME", help="Name of index")
    parser.add_argument("--output_file", help="File to write schema to")
    args = parser.parse_args()

    generate_template(args.INDEX_NAME, args.output_file)


if __name__ == '__main__':
    sys.exit(main())
