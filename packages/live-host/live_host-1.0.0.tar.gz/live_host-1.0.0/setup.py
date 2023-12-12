#!/usr/bin/env python
from setuptools import setup

setup(
    name="live_host",
    version="1.0.0",
    author="Tanaka Chinengundu",
    author_email="tanakah30@gmail.com",
    long_description="""
### Live-Host
### Live-Host a robust module for checking is a host is live

- This module checks if a target host is alive by sending a get request to the host.

- ## Installation 
- You can install this module using `pip`. Just run `pip install live-host`.

- ## Usage 
- To check if a host is alive, you can use the `is_live()` function. This function takes a hostname or IP address as an argument. For example:

```
from live_host.check_host import is_live

if is_live('www.google.com'):
	print('Host is alive!')
else:
	print('Host is down')
```
## Why Live-Host 
- Well its a easy and fast way of checking if a target host is available
could be a website, cloud database, API or any resource your application 
needs to communicate with. so your application can take appropriate
action depending on the results from live-host

- ## Supported platforms 
- This module is supported on Python 3 or later, and is tested on Windows, Linux, and macOS.

- ## Dependencies 
- This module requires requests module

- ## Source code 
- The source code for this module is available at [https://github.com/TaqsBlaze/Live-Host](https://github.com/TaqsBlaze/Live-Host).

- ## License 
- This module is licensed under the Apache 2.0 License. See the LICENSE file for more information.

- ## Note
- Live-Host is still under development any contributions are welcomed
- Feel free to report bugs if any found and also suggest features or changes

- ## Author 
- Author: Tanaka Chinengundu
- Email: tanakah30@mail.com
""",
    license="Apache 2.0",
    url="https://github.com/taqsblaze/Live-Host",
    install_requires=["pip", "requests"],
    classifiers=[
    	"Development Status :: 3 - Alpha",
		"Intended Audience :: Developers",
		"Topic :: Software Development",
		"License :: OSI Approved :: MIT License",
		],
	long_description_content_type="text/markdown",
	python_requires=">=3.8"
)

