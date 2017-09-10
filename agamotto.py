#! /usr/bin/python

import sys
import os
import re
import pandas as pd
import urllib2
from HTMLParser import HTMLParser
from dateutil.parser import parse as dateparse

from alexandria.dewey import HEADERS, INDICES, append_today
from util.pandas_util import condense

response = urllib2.urlopen('http://python.org/')
html = response.read()


def scan():
    parser = ComicsHTMLParser()
    data = []
    while True:
        in_str = raw_input('UPC [q to quit] >>> ')
        try:
            upc = int(in_str)
        except:
            if in_str == 'q' or in_str == 'quit':
                break
            else:
                print("I don't understand your input...\n")
        try:
            index = get_info_index(upc, parser)
        except:
            print('Could not find info for {}'.format(upc))
            continue
        confirm = raw_input('Is {} correct? [y/n] '.format(index['Issue']))
        index['Copies'] = 1
        if confirm == 'y':
            data.append(index)
        else:
            print('{} input cancelled.\n'.format(index['Issue']))
    df = pd.DataFrame(data, columns=HEADERS)
    df.set_index(INDICES, inplace=True)
    condense(df, 'Copies')
    print("I have ...\n")
    print(df.to_string())
    confirm = raw_input("Does this all look right? [y/n] ")
    if confirm == 'y':
        append_today(df)
    else:
        print('Sorry...')


def get_url(upc):
    return 'https://www.comics.org/barcode/{}/'.format(upc)


def get_info_index(upc, parser):
    url = get_url(upc)
    response = urllib2.urlopen(url)
    data = parser.feed(upc, response.read())
    return data


class ComicsHTMLParser():

    @staticmethod
    def remove_tags(s):
        return re.sub('<.*?>', '', s)

    def feed(self, upc, data):
        starting = False
        lines = data.splitlines()
        lines.reverse()
        while lines:
            line = lines.pop()
            if '<table class="listing">' in line:
                starting = True
                break
        if not starting:
            raise Exception("Found no results for {}!".format(upc))
        res = {}
        while lines:
            line = lines.pop()
            if 'listing_publisher' in line:
                res['Publisher'] = self.remove_tags(line).strip()
            elif "</table>" in line:
                break
            elif "series" in line:
                if 'Issue' in res:
                    raise Exception('Found multiple issues for {}!'.format(upc))
                res['Issue'] = self.remove_tags(line).strip()
            else:
                match = re.match('\s*<td>\s*(\w+\s*\d+)\s*</td>\s*', line)
                if match:
                    date = dateparse(match.group(1)).date()
                    res['Date'] = '{}{}01'.format(date.year, date.month)

        if len(res) != 3:
            print res
            raise Exception("Didn't find all the info for {}!".format(upc))
        res['UPC'] = upc
        return res

if __name__ == '__main__':
    scan()
