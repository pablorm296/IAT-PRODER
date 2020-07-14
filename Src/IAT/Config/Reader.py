import logging
import json
import os
import re

# Define logger
logger = logging.getLogger(__name__)

class Reader:
    def __init__(self, path: str = ".", load: str = "all"):
        """Config Files Reader

        Create an object that automatically reads configuration files for the IAT application. By default, reader will search for configuration files in /etc/Iat. However, user can specify a custom path via the `path` argument.

        Args:
            path (str, optional): Additional paths to look for configuration files. Defaults to ".".
            load (str, optional): Which configuration file should the reader load? If "all", it'll load all configuration files (app, stimuli, and text). Defaults to "all".

        Raises:
            ValueError: If `load` argument is set to an invalid option.
            FileNotFoundError: If Reader could not find a configuration file in /etc/Iat.
            Exception: If the file name failed a regex evaluation while loading its content.
            Exception: If no configurations files could be loaded from /etc/Iat, and from the user custom path.
        """
        # Check load argument (lower it)
        load = load.lower()
        if load not in ["all", "stimuli", "app", "text"]:
            error_msg = "You can either set load to 'all' or to a config file name ('stimuli','app','text')"
            logger.error(error_msg)
            raise ValueError(error_msg)
        # Define paths
        self.__paths = ["/etc/Iat"]
        self.__names = ["app.config.json", "stimuli.config.json", "text.config.json"]
        # Define contents
        self.Config = dict()

        # Append user defined path if not None
        if path is not None:
            self.__paths.append(path)

        # Look for config files
        logger.debug("Looking for config files...")

        # Loop through each possible path
        for path in self.__paths:
            # If user wants to load all config files, then loop through all config files names.
            # Otherwise, just use the config file name defined in load argument
            if load == "all":
                for name in self.__names:
                    # Define file path
                    tmp_target = "{0}/{1}".format(path, name)
                    # Check if it exists
                    logger.debug("Checking if {0} exists...".format(tmp_target))
                    if not os.path.exists(tmp_target):
                        if len(self.__paths) == 1:
                            error_msg = "Could not find {0}. Please make sure all config files are properly installed in /etc/Iat".format(tmp_target)
                            logger.error(error_msg)
                            raise FileNotFoundError(error_msg)
                        else:
                            warning_msg = "Could not find {0}".format(tmp_target)
                            logger.warning(warning_msg)
                            continue

                    # Open file if exists
                    logger.debug("Reading {0}...".format(tmp_target))
                    with open(tmp_target) as file:
                        # Read
                        parsed = json.load(file)
                        # Get config file name
                        keyName = re.findall(r"app|stimuli|text", tmp_target)
                        # Check regex match
                        if len(keyName) != 1:
                            error_msg = "Something went wrong while evaluating the config file name"
                            logger.error(error_msg)
                            raise Exception(error_msg)
                        else:
                            keyName = keyName[0]
                        # Update config dict
                        self.Config.update(keyName = parsed)
                        logger.debug("{0} loaded successfully".format(tmp_target))

            else:
                # Define file path
                tmp_target = "{0}/{1}.config.json".format(path, load)
                # Check if it exists
                logger.debug("Checking if {0} exists...".format(tmp_target))
                if not os.path.exists(tmp_target):
                    if len(self.__paths) == 1:
                        error_msg = "Could not find {0}. Please make sure all config files are properly installed in /etc/Iat".format(tmp_target)
                        logger.error(error_msg)
                        raise FileNotFoundError(error_msg)
                    else:
                        warning_msg = "Could not find {0}".format(tmp_target)
                        logger.warning(warning_msg)
                        continue
                # Open file if exists
                logger.debug("Reading {0}...".format(tmp_target))
                with open(tmp_target) as file:
                    # Read
                    parsed = json.load(file)
                    # Update config dict
                    self.Config[load] = parsed
                    logger.debug("{0} loaded successfully".format(tmp_target))

        # Check if config files could be loaded
        if self.Config.get("app", None) is None and self.Config.get("stimuli", None) is None and self.Config.get("text", None) is None:
            error_msg = "It seems that no configuration file could be loaded. Please make sure all config files are properly installed in /etc/Iat"
            logger.error(error_msg)
            raise Exception(error_msg)

    @property
    def Mongo_Uri(self):
        # If there is not any app config loaded, return none
        if self.Config.get("app", None) is None:
            warning_msg = "It seems that there is not an app config loaded"
            logger.warning(warning_msg)
            return None
        else:
            #Make Mongo_Uri
            uri = "mongodb://{0}:{1}@{2}:{3}/{4}".format(
                self.Config["app"]["mongo_user"],
                self.Config["app"]["mongo_password"],
                self.Config["app"]["mongo_host"],
                self.Config["app"]["mongo_port"],
                self.Config["app"]["mongo_db_name"]
            )
            return uri
