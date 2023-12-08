# Plastic SCM Repository Activities Reporting
Python command line library to generate Plastic SCM repository activities reports.

## Usage

### Prerequisite
Our command line utility relies on the following other utilities:
- [`cm`](https://docs.plasticscm.com/cli/plastic-scm-version-control-cli-guide): Plastic SCM command line.
- [`diff`](https://man.cx/diff): Unix utility that computes and displays the differences between the contents of files
- [`diffstat`](https://man.cx/diffstat): Unix utility that provides statistics based on the output of diff.

Make sure that you have configured Plastic SCM client application so that it uses the Unix command-line utility `diff` for comparing text files.  This setting needs to be written in the Plastic SCM client application's configuration file `$USER/.plastic4/client.conf`:

```xml
<DiffTools>
  <DiffToolData>
    <FileType>enTextFile</FileType>
    <FileExtensions>*</FileExtensions>
    <Tools>
      <string>/usr/bin/diff -u "@sourcefile" "@destinationfile"</string>
    </Tools>
  </DiffToolData>
  ...
</DiffTools>
```

### Installation
```shell
pip install plasticscm-statistics
```

### Execution

```shell
usage: cmstats [-h] [--end-time ISO8601] [--logging-level LEVEL] [--server NAME] [-o PATH]
               [--start-time ISO8601]

Plastic SCM repository activities reporting

options:
  -h, --help            show this help message and exit
  --end-time ISO8601
                        specify the latest date of changesets to return. This date is exclusive, so changesets that
                        were made at this date are not returned.
  --logging-level LEVEL
                        specify the logging level (critical, error, warning, info, debug)
  --server NAME         specify the Plastic SCM server to connect to
  -o PATH, --output-file PATH
                        specify the path and name of the file to write in the activity statistics of the Plastic SCM
                        repositories
  --start-time ISO8601
                        specify the earliest date of changesets to return. This date is inclusive, so changesets that
                        were made at this date are returned.
```