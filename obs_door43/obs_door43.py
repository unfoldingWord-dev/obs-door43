from __future__ import unicode_literals, print_function
import argparse
import codecs
import os
import sys
import shutil
import tempfile
from bs4 import BeautifulSoup
from general_tools.file_utils import write_file, load_json_object
from general_tools.url_utils import join_url_parts, get_url


class OBSDoor43(object):
    def __init__(self, source_location, output_location, template, quiet):
        self.source_location = source_location
        self.output_location = output_location
        self.template = template
        self.quiet = quiet
        self.temp_dir = ''

    def __enter__(self):
            return self

    # noinspection PyUnusedLocal
    def __exit__(self, exc_type, exc_val, exc_tb):
        # delete temp files
        if os.path.isdir(self.temp_dir):
            shutil.rmtree(self.temp_dir, ignore_errors=True)

    def run(self):

        self.temp_dir = tempfile.mkdtemp()

        # get build_log.json
        build_log = self.load_json_from_url(self.source_location, 'build_log.json')

        # get the template
        try:
            if not self.quiet:
                print('Downloading {0}...'.format(self.template), end=' ')
            template_html = get_url(self.template)

        finally:
            if not self.quiet:
                print('finished.')

        # get the source files
        obs_files = []
        for i in range(1, 51):
            obs_files.append(self.download_obs_file(self.source_location, str(i).zfill(2) + '.html'))

        self.apply_the_template(template_html, obs_files)

    def apply_the_template(self, template_html, obs_files):

        language_code = ''
        title = ''
        canonical = ''

        # apply the template
        template = BeautifulSoup(template_html, 'html.parser')

        # find the target div in the template
        template_div = template.body.find('div', {'id': 'obs-content'})
        if not template_div:
            raise Exception('No div tag with id "obs-content" was found in the template')

        # loop through the downloaded files
        for file_name in obs_files:

            if not self.quiet:
                print('Applying template to {0}.'.format(file_name))

            # read the downloaded file into a dom abject
            with codecs.open(file_name, 'r', 'utf-8-sig') as obs_file:
                soup = BeautifulSoup(obs_file, 'html.parser')

            # get the language code, if we haven't yet
            if not language_code:
                language_code = soup.html['lang']

            # get the title, if we haven't
            if not title:
                title = soup.head.title.text

            # get the canonical UTL, if we haven't
            if not canonical:
                links = template.head.select('link[rel="canonical"]')
                if len(links) == 1:
                    canonical = links[0]['href']

            # get the OBS content from the temp file
            div = soup.body.find_all('div', class_='obs-content')
            if len(div) != 1:
                raise Exception('No div tag with class "obs-content" was found in {0}'.format(file_name))

            # insert new HTML into the template
            template_div.clear()
            template_div.append(div[0])
            template.html['lang'] = language_code
            template.head.title.clear()
            template.head.title.append(title)
            for a_tag in template.body.select('a[rel="dct:source"]'):
                a_tag.clear()
                a_tag.append(title)

            # get the html
            html = unicode(template)

            # update the canonical URL - it is in several different locations
            html = html.replace(canonical, canonical.replace('/templates/', '/{0}/'.format(language_code)))

            # write to output directory
            out_file = os.path.join(self.output_location, os.path.basename(file_name))

            if not self.quiet:
                print('Writing {0}.'.format(out_file))

            write_file(out_file, html.encode('ascii', 'xmlcharrefreplace'))

    def download_obs_file(self, base_url, file_to_download):

        download_url = join_url_parts(base_url, file_to_download)
        return self.download_file_to_temp(download_url)

    def download_file_to_temp(self, url_to_download):

        try:
            if not self.quiet:
                print('Downloading {0}...'.format(url_to_download), end=' ')
            file_text = get_url(url_to_download)

        finally:
            if not self.quiet:
                print('finished.')

        file_name = url_to_download.rpartition('/')[2]
        save_as = os.path.join(self.temp_dir, file_name)

        if not self.quiet:
            print('Saving {0}...'.format(save_as), end=' ')
        write_file(save_as, file_text)
        if not self.quiet:
            print('finished.')

        return save_as

    def load_json_from_url(self, base_url, file_name):

        self.download_obs_file(base_url, file_name)
        return load_json_object(os.path.join(self.temp_dir, file_name))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-s', '--source', dest='source_location', default=False, required=True,
                        help='The URL of the directory containing the OBS 01.html - 50.html source files.')

    parser.add_argument('-o', '--output', dest='output_location', default=False, required=True,
                        help='The directory for the generated HTML files.')

    parser.add_argument('-t', '--template', dest='template', default=False, required=True,
                        help='The URL of the HTML template.')

    parser.add_argument('-q', '--quiet', dest='quiet', action='store_true', help='Do not write to console.')

    args = parser.parse_args(sys.argv[1:])

    with OBSDoor43(args.source_location, args.output_location, args.template, args.quiet) as obs:
        obs.run()
