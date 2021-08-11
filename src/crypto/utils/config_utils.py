from typing import Dict, Any
from omegaconf import DictConfig


def get_exclusive_option(sub_cfg: DictConfig) -> Dict[str, Dict[str, Any]]:
    """Returns the chosen option from the config

    Args:
        sub_cfg (DictConfig): Config parameters with options

    Raises:
        ValueError: If more than one option is selected
    Returns:
        Dict[str, Dict[str, Any]]: Option name as the key and values are option parameters
    """

    selected_option = {opt: args for opt, args in sub_cfg.items() if args["apply"]}

    if len(selected_option.keys()) > 1:

        raise ValueError(
            f"Config error. Only one option is allowed to be set to apply: True."
            f"Current setting is {selected_option}."
        )

    else:

        option_name = list(selected_option.keys())[0]

        params = list(selected_option.values())[0]

        params_without_apply = {
            arg: val for arg, val in params.items() if arg != "apply"
        }

        selected_option_with_kwargs_only = {option_name: params_without_apply}

        return selected_option_with_kwargs_only
