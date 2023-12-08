# get_ua

## Overview

`get_ua` is a Python library for generating random user agents. It provides a simple interface to retrieve user agents based on different criteria such as browser, operating system, and device.

## Installation

You can install the library using pip:

```bash
pip install get-ua
```

## Usage
```python
import get_ua

# Create an instance of the user agent generator
ua = get_ua.ua()

# Generate a random user agent
random_ua = ua.random()
print("Random User Agent:", random_ua)

# Get a random user agent for a specific browser, OS, and device type
random_agent = ua.random(browser='Chrome', os='Windows', device='desktop')
print("Random User Agent (filtered):", random_agent)

# Generate a random user agent based on browser
chrome_ua = ua.by_browser('Chrome')
print("Chrome User Agent:", chrome_ua)

# Generate a random user agent based on operating system
windows_ua = ua.by_os('Windows')
print("Windows User Agent:", windows_ua)

# Generate a random user agent based on device
iphone_ua = ua.by_device('iPhone')
print("iPhone User Agent:", iphone_ua)

# Get a list of user agents for a specific browser
firefox_agents = ua.list_by_browser('Firefox')
print("Firefox User Agents:", firefox_agents)

# Get a list of user agents for a specific operating system
linux_agents = ua.list_by_os('Linux')
print("Linux User Agents:", linux_agents)

# Get a list of user agents for a specific device
tablet_agents = ua.list_by_device('Tablet')
print("Tablet User Agents:", tablet_agents)

# Get a list of all available user agents
all_agents = ua.list_all()
print("All User Agents:", all_agents)
```

## .random() Possible Filters:
### Browsers:
   * "Chrome"
   * "Edge"
   * "Firefox"
   * "Internet Explorer"
   * "Safari"

### Device Types:
   * "desktop"
   * "mobile"

### Operating Systems:
   * "Android"
   * "iOS"
   * "macOS"
   * "Windows"