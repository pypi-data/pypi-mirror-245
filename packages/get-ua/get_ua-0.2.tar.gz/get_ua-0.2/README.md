# Get User Agent

Simple Python library to generate random user agents based on different criteria such as browser, operating system, and device type. It provides an easy way to retrieve user agents for testing and other purposes.

## Installation

You can install it using `pip`. Open a terminal and run:

```bash
pip install get_ua
```
## Usage
```
import get_ua

# Create an instance of the get_ua class
ua = get_ua()

# Get a random user agent for a specific browser, OS, and device type
random_ua = ua.random(browser='Chrome', os='Windows', device='desktop')
print("Random User Agent (filtered):", random_ua)

# Get a random user agent for a specific browser
random_browser_ua = ua.by_browser(browser='Firefox')
print("Random User Agent by Browser:", random_browser_ua)

# Get a random user agent for a specific operating system
random_os_ua = ua.by_os(os='iOS')
print("Random User Agent by OS:", random_os_ua)

# Get a random user agent for a specific device type
random_device_ua = ua.by_device(device='mobile')
print("Random User Agent by Device:", random_device_ua)

# Get a list of user agents for a specific browser
browser_ua = ua.list_by_browser(browser='Chrome')
print("User Agents by Browser:", browser_ua)

# Get a list of user agents for a specific operating system
os_ua = ua.list_by_os(os='Android')
print("User Agents by OS:", os_ua)

# Get a list of user agents for a specific device type
device_ua = ua.list_by_device(device='tablet')

print("User Agents by Device:", device_ua)

# Get a list of all user agents
all_ua = ua.list_all()
print("All User Agents:", all_ua)
```
