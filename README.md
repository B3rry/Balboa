# Balboa

Balboa is a Python based bot that enables subreddit administrators to define, manage, and automate the process of handling changes to a user's flair. Features include the automatic handling and construction of flair text and CSS changes, including the dynamic constructions of these values via regex and time-based restrictions.

## Getting Started

### Prerequisites
* [Python 2.7.x](https://docs.python.org/2/ "documentation")
* [pip](https://pip.pypa.io/en/stable/installing/ "installation instructions")
* [PRAW](http://praw.readthedocs.io/en/latest/# "PRAW documentation")
* [python-dotenv](https://pypi.python.org/pypi/python-dotenv)


### Installation
* Ensure your system has all requisite packages installed
* `pip install -r requirements.txt`


#### Reddit
* Obtain an `APP_ID`, and `APP_SECRET` from [reddit.com](https://www.reddit.com/prefs/apps)
> Note: you'll need to select a type of `script` from the radio options under the 'create application' prompt.