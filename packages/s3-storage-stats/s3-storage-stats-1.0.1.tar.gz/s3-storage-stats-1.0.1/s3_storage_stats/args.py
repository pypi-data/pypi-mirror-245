import argparse
import sys

def parse_args(args):
    """
    create the argument parser
    """
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers()
    
    add_checksums_subparser(subparser)
    add_reports_subparser(subparser)
    
    if len(args) == 0:
        parser.print_help(sys.stderr)
        sys.exit(1)
    
    return parser.parse_args(args)


def add_checksums_subparser(subparser):
    """
    create the checksums subparser
    """
    parser = subparser.add_parser(
        'checksums',
        help="obtain and output object/file checksums"
    )
    subparser = parser.add_subparsers()
    parser.set_defaults(cmd='checksums')
    
    add_checksums_get_subparser(subparser)
    add_checksums_put_subparser(subparser)

    
def add_checksums_get_subparser(subparser):
    """
    create the checksums get subparser
    """
    parser = subparser.add_parser(
        'get', 
        help="Get object/file checksums"
    )
    parser.set_defaults(sub_cmd='get')

    add_checksum_options(parser)

    
def add_checksums_put_subparser(subparser):
    """
    create the checksums put subparser
    """
    parser = subparser.add_parser(
        'put',
        help="Set object/file checksums.."
    )

    parser.set_defaults(sub_cmd='put')
    
    group_checksum = add_checksum_options(parser)

    group_checksum.add_argument(
        '--checksum',
        action='store',
        default=False,
        required=True,
        dest='checksum',
        type=str.lower,
        help="String with checksum to set. ['adler32', md5] "
            "Required"
    )


def add_reports_subparser(subparser):
    """
    create the reports subparser
    """
    parser = subparser.add_parser(
        'reports',
        help="obtain and output storage reports"
    )
    subparser = parser.add_subparsers()
    parser.set_defaults(cmd='reports')

    add_general_options(parser)
    add_logging_options(parser)

    
def add_checksum_options(parser):
    """
    create the common checksum options
    """
    add_general_options(parser)
    add_logging_options(parser)
    
    group_checksum = parser.add_argument_group("Checksum required options")

    group_checksum.add_argument(
        '-t', '--hash_type',
        action='store',
        default=False,
        required=True,
        dest='hash_type',
        type=str.lower,
        help="Type of checksum hash. ['adler32', md5] "
                "Required."
    )

    group_checksum.add_argument(
        '-f', '--file',
        action='store',
        default=False,
        required=True,
        dest='file',
        help="URL of object/file to request checksum of. "
                "Required."
    )
    
    return group_checksum

    
def add_general_options(parser):
    """
    create the common options for both
    checksums and reports
    """
    parser.add_argument(
        '-c', '--config',
        action='store',
        default='/etc/xrootd/s3cfg',
        dest='config_path',
        type=str.lower,
        help="Path to s3 endpoint .conf file or directory. "
            "Accepts one argument. "
            "Default: '/etc/xrootd/s3cfg'."
    )
    
    parser.add_argument(
        '--force',
        action='store_true',
        default=False,
        dest='force',
        help="Force command execution."
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        default=False,
        dest='verbose',
        help="Show on stderr events according to loglevel."
    )
    
def add_logging_options(parser):
    """Add logging optional arguments.

    Arguments:
    parser -- Object form argparse.ArgumentParser()

    """

    group_logging = parser.add_argument_group("Logging options")
    group_logging.add_argument(
        '--logfile',
        action='store',
        default='/var/log/xrootd/s3_proxy/storage_stats.log',
        dest='logfile',
        help="Set logfiles path. "
             "Default: /var/log/xrootd/s3_proxy/storage_stats.log"
    )
    group_logging.add_argument(
        '--logid',
        action='store',
        default=False,
        dest='logid',
        help='Add this log id to every log line.'
    )
    group_logging.add_argument(
        '--loglevel',
        action='store',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        default='WARNING',
        dest='loglevel',
        help="Set log output level. "
        "Default: WARNING."
    )
