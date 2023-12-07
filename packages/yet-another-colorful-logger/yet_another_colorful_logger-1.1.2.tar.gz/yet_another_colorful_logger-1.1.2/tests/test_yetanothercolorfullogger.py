from itertools import combinations

import pytest
from yaclogger import YACLogger


# TEST CLASS CONSTRUCTOR
def test_yaclogger_constructor():
    with pytest.raises(AssertionError):
        YACLogger('TEST', log_colors='INVALID')

    with pytest.raises(KeyError):
        YACLogger('TEST', log_colors={'INVALID': 'red'})

    with pytest.raises(ValueError):
        YACLogger('TEST', log_colors={'debug': 'INVALID'})
######

###### TEST CLASS METHODS
@pytest.fixture
def default_yaclogger():
    return YACLogger("DEFAULT_COLOR")

def test_debug(default_yaclogger):
    default_yaclogger.debug("This is a debug message")

def test_info(default_yaclogger):
    default_yaclogger.info("This is an info message")

def test_warning(default_yaclogger):
    default_yaclogger.warning("This is a warning message")

def test_error(default_yaclogger):
    default_yaclogger.error("This is an error message")

def test_critical(default_yaclogger):
    with pytest.raises(SystemExit) as exception_info:
        default_yaclogger.critical("This is a critical message")
    assert exception_info.value.code == -1
######

###### TEST CLASS METHODS WITH CUSTOM COLORS
@pytest.fixture()
def generate_logs_color_dicts():
    def generate_combinations(input_dict):
        result = []
        keys = list(input_dict.keys())
        for r in range(1, len(keys) + 1):
            result.extend(list(combinations(keys, r)))
        return result

    log_colors = {'debug': 'green', 'info': 'blue', 'warning': 'light_purple', 'error': 'light_blue', 'critical': 'purple'}
    colors_combinations_list = generate_combinations(log_colors)
    list_of_colors_combination = []
    for i, combination in enumerate(colors_combinations_list, start=1):
        combined_dict = {key: log_colors[key] for key in combination}
        list_of_colors_combination.append(combined_dict)
    return list_of_colors_combination


def test_messages_colors(default_yaclogger, generate_logs_color_dicts):
    for idx,log_colors_dict in enumerate(generate_logs_color_dicts):
        custom_yaclogger = YACLogger(f"CUSTOM_COLOR_{idx}", log_colors=log_colors_dict)
        default_yaclogger.debug("This is a debug message")
        custom_yaclogger.debug("This is a debug message")
        default_yaclogger.info("This is an info message")
        custom_yaclogger.info("This is an info message")
        default_yaclogger.warning("This is a warning message")
        custom_yaclogger.warning("This is a warning message")
        default_yaclogger.error("This is an error message")
        custom_yaclogger.error("This is an error message")
        with pytest.raises(SystemExit) as exception_info:
            default_yaclogger.critical("This is a critical message")
        assert exception_info.value.code == -1
        with pytest.raises(SystemExit) as exception_info:
            custom_yaclogger.critical("This is a critical message")
        assert exception_info.value.code == -1
        del custom_yaclogger
######