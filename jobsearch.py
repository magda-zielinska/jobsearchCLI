import os
import platform
import csv
import argparse
import requests
from lxml import html

from requests.exceptions import ConnectionError
from requests.exceptions import SSLError

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver import Firefox


def _save_to_csv(links):
    links = [[link] for link in links]
    desktop_file_macos_win = os.path.expanduser("~/Desktop/job_listings.csv")
    if platform.system() == 'Darwin' or platform.system() == 'Windows':
        with open(desktop_file_macos_win, 'w') as outcsv:
            writer = csv.writer(outcsv, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL,
                                lineterminator='\n')
            for link in links:
                writer.writerow(link)
    else:
        with open('job_listings.csv', 'w') as outcsv:
            writer = csv.writer(outcsv, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL,
                                lineterminator='\n')
            for link in links:
                writer.writerow(link)


def _search_stackoverflow(job, location):
    job = job.replace(' ', '+')
    url_stackoverflow = 'https://stackoverflow.com/jobs?q={}&l={}&d=20&u=Km'.format(job, location)
    firefox_options = Options()
    firefox_options.headless = True
    try:
        browser = Firefox(options=firefox_options)
        browser.get(url_stackoverflow)
    except TimeoutException as e:
        raise e
    try:
        links = [a.get_attribute('href') for a in browser.find_elements_by_tag_name('a')]
        links_wo_nones = [x for x in links if x is not None]
        stackoverflow_links = []
        base_url = 'https://stackoverflow.com/jobs/'
        for link in links_wo_nones:
            if link.startswith(base_url + '0') or link.startswith(base_url + '1') \
                    or link.startswith(base_url + '2') or link.startswith(base_url + '3') \
                    or link.startswith(base_url + '4') or link.startswith(base_url + '5') \
                    or link.startswith(base_url + '6') or link.startswith(base_url + '7') \
                    or link.startswith(base_url + '8') or link.startswith(base_url + '9'):
                stackoverflow_links.append(link)
        return _save_to_csv(stackoverflow_links)
    except NoSuchElementException as e:
        raise e


def _search_linkedin(job, location):
    try:
        jobsearch_session = requests.session()
        url_linkedin = 'https://www.linkedin.com/jobs/search/?geoId=106967730&keywords={}' \
                       '&location={}%2C%20Berlin&redirect=false&position=1&pageNum=0'.format(job, location)
        connection = jobsearch_session.get(url_linkedin, verify=True)
        search_contents = html.fromstring(connection.content)
        links = []
        for link in search_contents.xpath('//a/@href'):
            if link.startswith('https://de.linkedin.com/jobs/view/'):
                links.append(link)
        return _save_to_csv(links)

    except requests.exceptions.SSLError as e:
        print('Encountered an SSL Error. Try again later')
        raise e


def _find_links(args):
    args['job'] = ' '.join(args['job'])
    if args['stackoverflow']:
        _search_stackoverflow(args['job'], args['location'])
    if args['linkedin']:
        _search_linkedin(args['job'], args['location'])
    else:
        _search_linkedin(args['job'], args['location'])


def jobsearch(args):
    try:
        jobs = _find_links(args)
        if not jobs:
            jobs = 'Sorry, couldn\'t find any job listings for the position you wanted!'

        return jobs

    except (ConnectionError, SSLError):
        return 'Failed to establish network connection.' \
               'Please check your internet connection'


def get_parser():
    parser = argparse.ArgumentParser(description='tool to store links to job adds')
    parser.add_argument('job', metavar='JOB', type=str, nargs='*',
                        help='the position you are looking for')
    parser.add_argument('location', metavar='LOCATION', type=str, nargs='*',
                        help='the city in which you are looking for a job')
    parser.add_argument('-s', '--stackoverflow', help='look for jobs on stackoverflow, default: linkedin',
                        action='store_true')
    parser.add_argument('-l', '--linkedin', help='look for jobs on linkedin', action='store_true')
    # @TODO: include the feature to define the number of saved listings
    parser.add_argument('-n', '--num-answers', help='number of links to be stored', default=26, type=int)

    return parser


def command_line_parser():
    parser = get_parser()
    args = vars(parser.parse_args())

    if not args['job']:
        parser.print_help()
        return

    jobsearch(args)


if __name__ == '__main__':
    command_line_parser()
