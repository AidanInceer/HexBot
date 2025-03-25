import yaml


class CentralConfig(dict):
    def __getattr__(self, attr):
        """
        Retrieve the value of the attribute from the configuration dictionary.

        If the attribute exists in the configuration dictionary, it returns the value.
        If the value is a dictionary, it returns a new instance of CentralConfig with
        the value as the configuration dictionary.
        If the value is a list, it returns a new list with each item converted to
        CentralConfig if it is a dictionary, otherwise it returns the item as is.

        Args:
            attr (str): The name of the attribute to retrieve.

        Returns:
            The value of the attribute.

        Raises:
            AttributeError: If the attribute does not exist in the configuration dictionary.
        """
        if attr in self:
            value = self[attr]
            if isinstance(value, dict):
                return CentralConfig(value)
            elif isinstance(value, list):
                return [
                    CentralConfig(item) if isinstance(item, dict) else item
                    for item in value
                ]
            return value
        raise AttributeError(
            f"'{type(self).__name__}' object has no attribute '{attr}'"
        )

    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def load_config(file_path):
    """
    Load YAML config file and return a CentralConfig.

    Args:
        file_path (str): The path to the YAML config file.

    Returns:
        CentralConfig: The loaded config as a CentralConfig object.
    """
    with open(file_path, "r") as file:
        config_dict = yaml.safe_load(file)
    return CentralConfig(config_dict)
