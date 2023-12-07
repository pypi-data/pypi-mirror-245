#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
"""A CLI for the ramses_rf library."""
from __future__ import annotations

import json
from io import TextIOWrapper
from pathlib import PurePath

import yaml


def load_config_as_json(config_file: TextIOWrapper) -> dict:
    """Return a json file as a config dict."""

    result = json.load(config_file)
    return result


def load_config_as_yaml(config_file: TextIOWrapper) -> dict:
    """Return a yaml file as a config dict."""

    result = yaml.load(config_file)
    return result


def load_config_file(config_file: TextIOWrapper) -> dict:
    """Return a config file (json, yaml) as a config dict."""

    if PurePath(config_file).suffix == ".json":
        return load_config_as_json(config_file)

    elif PurePath(config_file).suffix == ".yaml":
        return load_config_as_yaml(config_file)


def main() -> None:
    """Run the CLI."""

    with open("config.json") as config_file:
        config_json = load_config_file(config_file)

    with open("config.yaml") as config_file:
        config_yaml = load_config_file(config_file)


if __name__ == "__main__":
    main()
