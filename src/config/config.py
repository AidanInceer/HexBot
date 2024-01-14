import yaml


class CentralConfig(dict):
    """A dictionary that allows dot notation access to its elements."""

    def __getattr__(self, attr):
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
    """Load YAML config file and return a DotDict."""
    with open(file_path, "r") as file:
        config_dict = yaml.safe_load(file)
    return CentralConfig(config_dict)
