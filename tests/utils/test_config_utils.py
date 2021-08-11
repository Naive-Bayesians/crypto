import pytest
from omegaconf import DictConfig
from crypto.utils import config_utils


@pytest.mark.parametrize(
    argnames=(
        "cfg",
        "expected_result",
    ),
    argvalues=[
        (
            DictConfig(
                {
                    "opt1": {"apply": True, "opt1_param1": 1},
                    "opt2": {"apply": False, "opt2_param1": "text", "opt2_param2": 2},
                }
            ),
            {"opt1": {"opt1_param1": 1}},
        ),
        (
            DictConfig(
                {
                    "opt1": {"apply": False, "opt1_param1": 1},
                    "opt2": {"apply": True, "opt2_param1": "text", "opt2_param2": 2},
                }
            ),
            {"opt2": {"opt2_param1": "text", "opt2_param2": 2}},
        ),
    ],
    ids=["1", "2"],
)
def test_get_exclusive_option(cfg, expected_result):
    result = config_utils.get_exclusive_option(cfg)
    assert result == expected_result


def test_get_exclusive_option_fail(multiple_option_config):

    with pytest.raises(ValueError):
        result = config_utils.get_exclusive_option(multiple_option_config)


@pytest.fixture
def multiple_option_config() -> DictConfig:
    base = DictConfig(
        {
            "opt1": {"apply": True, "opt1_param1": 1},
            "opt2": {"apply": True, "opt2_param1": "text", "opt2_param2": 2},
        }
    )

    return base