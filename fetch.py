#!/usr/bin/env python

# Script that downloads documents from indigo.openbylaws.org.za
# and stores them for use with the SAFLII content system.

import os
import requests
import errno
import codecs
import urlparse
import click


API_ENDPOINT = os.environ.get('INDIGO_API_URL', "https://indigo.africanlii.org/api")
BASE_DIR = os.getcwd()
session = requests.Session()
session.verify = False


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise e
        pass


def download_doc(doc, target):
    """ Download this document.
    """
    path = os.path.join(target, "Data")
    click.echo("Fetching: %s -> %s" % (doc['expression_frbr_uri'], path))
    mkdir_p(path)

    doc['base_filename'] = base_filename(doc)
    base_fname = os.path.join(path, doc['base_filename'])

    # add alternate forms
    for title in ['Standalone HTML']:  # PDF? ePUB?
        link = [link for link in doc['links'] if link['title'] == title]
        if link:
            link = link[0]

            resp = session.get(link['href'])
            resp.raise_for_status()

            fname = urlparse.urlsplit(link['href']).path
            _, ext = os.path.splitext(fname)

            fname = base_fname + ext
            click.echo(fname)
            with open(fname, 'wb') as f:
                f.write(resp.content)


def base_filename(doc):
    # the filename to use for this doc
    return doc['frbr_uri'][1:].replace('/', '-')


def write_registry(docs, target):
    fname = os.path.join(target, 'Registry.txt')
    click.echo("Writing registry to %s" % fname)

    with codecs.open(fname, 'w', 'utf-8') as f:
        for doc in docs:
            title = doc['title']
            title = title + " (Act %s of %s)" % (doc['number'], doc['year'])
            f.write("\"%s.html\" (%s) %s\n" % (doc['base_filename'], doc['publication_date'], title))


def get_remote_documents(url, region):
    url = url + '/' + region + '/.json'
    docs = []

    while url:
        resp = session.get(url)
        resp.raise_for_status()
        data = resp.json()
        docs.extend(data['results'])
        url = data['next']

    return docs


def fetch_region(base_url, region, target):
    click.echo("Archiving documents from %s to %s" % (base_url, target))

    docs = get_remote_documents(base_url, region)
    # filter to just acts
    docs = [d for d in docs if not d['subtype']]

    click.echo("Documents: %d" % len(docs))
    for doc in docs:
        download_doc(doc, target)

    return docs


def setup_session():
    with open("indigo-api-token", "r") as f:
        token = f.read().strip()
        session.headers.update({'Authorization': 'Token %s' % token})


@click.command()
@click.option('--target', default='.', help='Target directory')
@click.option('--url', default=API_ENDPOINT, help='Indigo API URL (%s)' % API_ENDPOINT)
@click.option('--regions', help='Comma-separated region codes (za, zm, etc.)')
def main(target, url, regions):
    regions = [r.lower() for r in regions.split(",")]
    click.echo("Regions: " + ", ".join(regions))

    setup_session()

    all_docs = []
    for region in regions:
        all_docs.extend(fetch_region(url, region, target))

    write_registry(all_docs, target)


if __name__ == '__main__':
    main()
