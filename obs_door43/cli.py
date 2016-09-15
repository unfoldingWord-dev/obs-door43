from __future__ import unicode_literals
import argparse
import sys
from obs_door43 import OBSDoor43


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
