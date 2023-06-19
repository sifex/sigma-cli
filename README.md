<a href="https://github.com/SigmaHQ/">
<p align="center">
<br />
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://cdn.jsdelivr.net/gh/sifex/sifex@master/images/sigma_logo_dark.png#gh-dark-mode-only">
  <img height="124" alt="Sigma Logo" src="https://cdn.jsdelivr.net/gh/sifex/sifex@master/images/sigma_logo_light.png#gh-light-mode-only">
</picture>
</p>
</a>

<p align="center">
<br />
<img src="https://cdn.jsdelivr.net/gh/sifex/sifex@master/images/Sigma%20Official%20Badge.svg" alt="Sigma Official" />
<img src="https://github.com/SigmaHQ/sigma-cli/actions/workflows/test.yml/badge.svg" alt="Tests" />
<img src="https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/thomaspatzke/0c868df261d4a5d5a1dafe71b1557d69/raw/SigmaHQ-sigma-cli.json" alt="Coverage Badge" />
<img src="https://img.shields.io/badge/Status-pre--release-orange" alt="Status" />
</p>


<p align="center">
This is the Sigma command line interface using the <a href="https://github.com/SigmaHQ/pySigma">pySigma</a> library
<br />
to manage, list   and convert Sigma rules into query languages.
</p>

## Getting Started

### Installation

The easiest way to install the `sigma-cli` is via *pip*. 

```bash
pip3 install sigma-cli    # Install sigma-cli
```

#### From Source

If you want to download and install `sigma-cli` from source, first install [Poetry](https://python-poetry.org/docs/basic-usage/), then run the following:

```bash
git clone https://github.com/SigmaHQ/sigma-cli.git && cd sigma-cli
poetry install && poetry shell
```

### Usage

We'll use the `sigma convert` command to start converting Sigma rules from their `.yml` file, into our desired SIEM format.

The CLI is available as `sigma` command.

```bash
sigma convert -t <backend> \
    -p <processing pipeline 1> \
    -p <processing pipeline X> \
    <directory or file of Sigma rules>
```

For example, to use `sigma-cli` to convert "process creation" Sigma rules into Splunk queries for Sysmon logs, we can run:

```bash
sigma convert -t splunk -p sysmon sigma/rules/windows/process_creation
```

Required backends must be installed using the following command prior to conducting conversions.

To list all available plugins run the following command:
```
sigma plugin list
```
Install a plugin of your choice with:
```
sigma plugin install <backend>
```
E.g. to install the splunk backend run:
```
sigma plugin install splunk
```

Available conversion backends and processing pipelines can be listed with `sigma list`. 
Use `-O` or `--backend-option` for passing options to the backend as key=value pairs (`-O testparam=123`) .
This backend option parameter can be used multiple times (`-O first=123 -O second=456`).

Backends can support different output formats, e.g. plain queries and a file that can be imported into the target
system. These formats can be listed with `sigma list formats <backend>` and specified for conversion with the `-f`
option.

In addition, an output file can be specified with `-o`.

Example for output formats and files:

```bash
sigma convert -t splunk -f savedsearches -p sysmon -o savedsearches.conf sigma/rules/windows/process_creation
```

Outputs a Splunk savedsearches.conf containing the converted searches.

### Integration of Backends and Pipelines

Backends and pipelines can be integrated by adding the corresponding packages as dependency with:

```bash
poetry add <package name>
```

A backend has to be added to the `backends` dict in `sigma/cli/backends.py` by creation of a `Backend` named tuple with
the following parameters:

* The backend class.
* A display name shown to the user in the targets list (`sigma list targets`).
* A dict that maps output format names (used in `-f` parameter) to descriptions of the formats that are shown in the
  format list (`sigma list formats <backend>`). The formats must be supported by the backend!

The dict key is the name used in the `-t` parameter.

A processing pipeline is defined in the `pipelines` variable dict in `sigma/cli/pipelines.py`. The variable contains a
`ProcessingPipelineResolver` that is instantiated with a dict that maps identifiers that can
be used in the `-p` parameter to functions that return `ProcessingPipeline` objects. The descriptive text shown in the
pipeline list (`sigma list pipelines`) is provided from
the `name` attribute of the `ProcessingPipeline` object.

## Maintainers

The project is currently maintained by:

- Thomas Patzke <thomas@patzke.org>
