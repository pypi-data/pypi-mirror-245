import logging
import os
import json

from docopt import ParsedOptions

from config_constants import CONFIG_TEMPLATE, CLI_INPUTS_TEMPLATE
from constants import CONFIG_PATH, SUPPORTED_COMMANDS
from services.validators import is_config_file_valid, is_cluster_id


class ConfigObject:
    def __init__(self, parsed_inputs: ParsedOptions, config_file_path=CONFIG_PATH):
        self.config_file_path = config_file_path
        self._logger = logging.getLogger(__name__)
        self.app_config = None
        self._setup_config()
        self.app_inputs = CLI_INPUTS_TEMPLATE
        self._populate_parsed_inputs_data(parsed_inputs)
        self.custom_cid = None

    def create_empty_template(self):
        self._logger.info(f"Creating empty {CONFIG_PATH} file")
        with open(self.config_file_path, "w") as config_file:
            json.dump(CONFIG_TEMPLATE, config_file)

    def _populate_parsed_inputs_data(self, parsed_inputs: ParsedOptions):
        self.app_inputs["demo"] = parsed_inputs["demo"]
        self.app_inputs["demo_subcommand"] = parsed_inputs["<on | off>"]
        self.app_inputs["cluster_id"] = parsed_inputs["--cluster_id"]
        self.app_inputs["help"] = parsed_inputs["--help"]
        self.app_inputs["debug"] = parsed_inputs["--debug"]

        if self.app_inputs["cluster_id"]:
            if is_cluster_id(self.app_inputs["cluster_id"]):
                self._logger.info(f"Custom cluster id={self.app_inputs['cluster_id']} will be used")
                self.custom_cid = self.app_inputs["cluster_id"]
            else:
                raise RuntimeError("--cluster_id did not match expected format")

        for command, value in parsed_inputs.items():
            if command in SUPPORTED_COMMANDS and value:
                self.app_inputs["command"] = command

    def _setup_config(self):
        if not os.path.exists(self.config_file_path):
            self.create_empty_template()
            self._logger.critical("config.json was missing. Created an empty template.")
            raise RuntimeError("config.json was missing. Created an empty template.")

        with open(self.config_file_path, "r") as config_file:
            configuration_data = json.load(config_file)
            if not is_config_file_valid(configuration_data):
                self._logger.critical("Invalid configuration file structure")
                raise RuntimeError("Invalid configuration file structure")
            self.app_config = configuration_data
