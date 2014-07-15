#!/usr/bin/env python
'''
Provides a vector for storing and accessing various configuration options
within a running program. Particularly useful when multiple files require
access to the same, changeable values, e.g. filepaths.
'''

__version__ = "1.0"
__date__ = "01-31-2014"
__author__ = "Cameron Pelkey"

import ast


class Config:
    """Establishes a dictionary of configuration options to be used throughout
    a program."""

    def parse_config(self, config_file):
        """Read a configuration file, populating a dictionary with options."""
        temp_dict = {}
        try:
            with open(config_file, 'r') as f:
                raw_data = f.read().strip()
                temp_dict = ast.literal_eval(raw_data)
            return temp_dict
        except Exception, e:
            print "ERROR: Problem parsing configuration file."
            raise e

    def get_config(self, option):
        """Access a configuration option"""
        if option in self.config_vars:
            return self.config_vars[option]
        else:
            print "Option \"" + option + "\" not available."
            return None

    def set_config(self, option, value):
        """Set a configuration option"""
        self.config_vars[option] = value

    def check_param(self, param):
        """Check if param has been set for runtime."""
        return param in self.config_params

    def set_param(self, param):
        """Set a parameter for runtime"""
        self.config_params.append(param)

    def __init__(self, config_file):
        self.config_file = config_file
        self.config_params = []
        self.config_vars = self.parse_config(config_file)
