# Yet Another Colorful Logger

[![RELEASE NEW VERSION](https://github.com/wagnercotta/yet_another_colorful_logger/actions/workflows/main.yml/badge.svg)](https://github.com/wagnercotta/yet_another_colorful_logger/actions/workflows/main.yml) [![GitHub version](https://badge.fury.io/gh/wagnercotta%2Fyet_another_colorful_logger.svg)](https://badge.fury.io/gh/wagnercotta%2Fyet_another_colorful_logger) [![PyPI version](https://badge.fury.io/py/yet-another-colorful-logger.svg)](https://badge.fury.io/py/yet-another-colorful-logger)

## Description

Yet Another Colorful Logger is just another Python logging utility that adds color to your console log messages. This module is already configured, not requiring any setup. Simply install it and integrate into your Python projects. However, if you want to customize it, you can do it as well.

For customizing the logger, you can change the colors, the format, and the log level. For more details, check the [Customization](#customization) section.

This module was created for personal use, but feel free to use it in your projects as well. 
Also, feel free to customize it according to your needs.

Any issues, suggestions, or questions, please feel free to reach out.

## Installation

To install Yet Another Colorful Logger, use `pip`:

```bash
pip install yet-another-colorful-logger
```

## Usage

To start using the logger is pretty forward. Just import it and create a logger instance:

```python
from yaclogger import YACLogger

# Create a logger instance
logger = YACLogger(name="my_logger")

# Log messages with different severity levels
logger.debug("This is a debug message !!!")
logger.info("This is an info message !!!")
logger.warning("This is a warning message !!!")
logger.error("This is an error message !!!")
logger.critical("This is a critical message !!!")
```

![Yet Another Colorful Logger Example](/docs/images/example.png "Yet Another Colorful Logger Example")

## Customization

For customizing the colors, you can pass a `dictionary` as the log_colors parameter to the `YACLogger` constructor. The dictionary must contain the log level as the key and the color as value, both in strings. In case you want to use a background color, you can pass the color name with the prefix `bg_`, separated by a comma. 

### Example 1:

If you want to change the background only for the `ERROR` log level, you can pass the following dictionary:

```python
my_custom_log_colors = {
    "ERROR": "black,bg_red"
}

yaclogger = YACLogger(name="my_logger", log_colors=my_custom_log_colors)
```

### Example 2:

If you want to change the background only for `DEBUG` and `CRITICAL` log level, you can pass the following dictionary:

```python
my_custom_log_colors = {
    "DEBUG": "green,bg_white",
    "CRITICAL": "red"
}

yaclogger = YACLogger(name="my_logger", log_colors=my_custom_log_colors)
```

### Example 3:
If you want to change the color for all log levels, you can pass the following dictionary:

```python
my_custom_log_colors = {
    "DEBUG": "light_blue",
    "INFO": "green",
    "WARNING": "cyan",
    "ERROR": "purple",
    "CRITICAL": "black,bg_white"
}
yaclogger = YACLogger(name="my_logger", log_colors=my_custom_log_colors)
```

### Available Colors

<table>
    <tbody>
        <tr>
            <td>black</td>
            <td>blue</td>
            <td>purple</td>
            <td>cyan</td>
        </tr>
        <tr>
            <td>red</td>
            <td>white</td>
            <td>light_black</td>
            <td>light_red</td>
        </tr>
        <tr>
            <td>green</td>
            <td>light_green</td>
            <td>light_yellow</td>
            <td>light_blue</td>
        </tr>
        <tr>
            <td>yellow</td>
            <td>light_purple</td>
            <td>light_cyan</td>
            <td>light_white</td>
        </tr>
    </tbody>
</table>

*Note: In some terminals, the foreground colors can have the same representation as the background colors, even both codes being different on the code. So, if you use the same color for both foreground and background in the same log level, you may not be able to see the message.*

![Colors Example](/docs/images/example2.png "Colors Example")

## Contact

For any questions, suggestions, or issues, feel free to reach out:

- GitHub: [Wagner Cotta](https://github.com/wagnercotta)

## License

This project is licensed under the GNU License - see the [LICENSE](LICENSE) file for details.
