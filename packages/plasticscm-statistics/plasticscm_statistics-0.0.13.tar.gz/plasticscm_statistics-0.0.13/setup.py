# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['bootloader',
 'bootloader.cli',
 'bootloader.utils',
 'bootloader.utils.plasticscm']

package_data = \
{'': ['*']}

install_requires = \
['perseus-core-library>=1.19,<2.0']

entry_points = \
{'console_scripts': ['cmstats = bootloader.cli.cmstats:run']}

setup_kwargs = {
    'name': 'plasticscm-statistics',
    'version': '0.0.13',
    'description': 'Python command line library to generate Plastic SCM activities reports',
    'long_description': '# Plastic SCM Repository Activities Reporting\nPython command line library to generate Plastic SCM repository activities reports.\n\n## Usage\n\n### Prerequisite\nOur command line utility relies on the following other utilities:\n- [`cm`](https://docs.plasticscm.com/cli/plastic-scm-version-control-cli-guide): Plastic SCM command line.\n- [`diff`](https://man.cx/diff): Unix utility that computes and displays the differences between the contents of files\n- [`diffstat`](https://man.cx/diffstat): Unix utility that provides statistics based on the output of diff.\n\nMake sure that you have configured Plastic SCM client application so that it uses the Unix command-line utility `diff` for comparing text files.  This setting needs to be written in the Plastic SCM client application\'s configuration file `$USER/.plastic4/client.conf`:\n\n```xml\n<DiffTools>\n  <DiffToolData>\n    <FileType>enTextFile</FileType>\n    <FileExtensions>*</FileExtensions>\n    <Tools>\n      <string>/usr/bin/diff -u "@sourcefile" "@destinationfile"</string>\n    </Tools>\n  </DiffToolData>\n  ...\n</DiffTools>\n```\n\n### Installation\n```shell\npip install plasticscm-statistics\n```\n\n### Execution\n\n```shell\nusage: cmstats [-h] [--end-time ISO8601] [--logging-level LEVEL] [--server NAME] [-o PATH]\n               [--start-time ISO8601]\n\nPlastic SCM repository activities reporting\n\noptions:\n  -h, --help            show this help message and exit\n  --end-time ISO8601\n                        specify the latest date of changesets to return. This date is exclusive, so changesets that\n                        were made at this date are not returned.\n  --logging-level LEVEL\n                        specify the logging level (critical, error, warning, info, debug)\n  --server NAME         specify the Plastic SCM server to connect to\n  -o PATH, --output-file PATH\n                        specify the path and name of the file to write in the activity statistics of the Plastic SCM\n                        repositories\n  --start-time ISO8601\n                        specify the earliest date of changesets to return. This date is inclusive, so changesets that\n                        were made at this date are returned.\n```',
    'author': 'Daniel CAUNE',
    'author_email': 'daniel@bootloader.studio',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/bootloader-studio/cli-plasticscm-statistics.git',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
