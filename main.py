#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import requests
from lxml import etree
import json

def scrape_pubmed(pmid):
    base_url = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = "db=pubmed&retmode=xml&tool=PMA&id=" + pmid
    response = requests.get(base_url + "?" + params)
    content = response.content
    return content

def get_xml_attrib(content, attrib):
    tree = etree.fromstring(content)
    for i in tree.iter(attrib):
        return i.text

def reach_api(text, format):
    base_url = "http://agathon.sista.arizona.edu:8080/odinweb/api/text"
    params = {"text":text, "output":format}
    response = requests.post(base_url, params=params)
    return response.json()

def event_stats(content):
    event_frames = reach_output['events']['frames']
    print("Number of events extracted - ",len(event_frames))
    print("Event types are -")
    for event_frame in event_frames:
        print(event_frame['type'])

def json_save_file(data, filename):
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pmid", help="PubMed Article ID", required="True")
    args = parser.parse_args()
    pmid = args.pmid

    pubmed_content = scrape_pubmed(pmid)
    abstract = get_xml_attrib(pubmed_content, 'AbstractText')
    reach_output = reach_api(abstract, 'fries')
    json_save_file(reach_output, pmid + '.json')
    event_stats(reach_output['events']['frames'])