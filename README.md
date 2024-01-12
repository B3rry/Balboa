<img align="right" height="180" src="./balboa_emblem.png">

# Balboa

Balboa is a Python based bot that enables reddit.com's subreddit administrators to define, manage, and automate the process of handling changes to a user's flair. Features include the automatic handling and construction of flair text and CSS changes, including the dynamic constructions of these values via regex and time-based restrictions.

Balboa was initially created for [/r/survivor](https://www.reddit.com/r/survivor) by [/u/gariond](https://www.reddit.com/user/Gariond) on behalf of [/u/aksurvivorfan](https://www.reddit.com/user/aksurvivorfan). Special thanks to GitHub user [gavin19](https://github.com/gavin19) for his work on [`gavin19/reddit-flair-bot`](https://github.com/gavin19/reddit-flair-bot), whose work this is bot is based upon.

## Getting Started

### Prerequisites
* [Python 3.7.x](https://docs.python.org/3/ "documentation")
* [pip](https://pip.pypa.io/en/stable/installing/ "installation instructions")


### Installation
* Ensure your system has all requisite packages installed `pip install -r requirements.txt`
    * [PRAW](http://praw.readthedocs.io/en/latest/# "PRAW documentation")
    * [configparser](https://docs.python.org/2/library/configparser.html "configparser documentation")
    * [python-dotenv](https://pypi.python.org/pypi/python-dotenv "dotenv documentation")
* Generate a `./.env` (or provide environmental variables)
> Note: You can use `./env.template` as a guide. Various service integrations will require additiona configration
* Provide the following .env variables:
    * `LOGGING` (`boolean`): Determines if logging will be written out to `log.txt`
    * `REFRESH_INTERVAL` (`int`, milliseconds): If you need to slow your bot down (i.e. if you're recieving errors related to reddit API rate limiting, )
    
### Reddit Configuration
1. [Create a reddit account](https://www.reddit.com/register/) that the bot will use to sign in
> Note: This bot's reddit account **_must_** be given `wiki` and `flair` moderation permissions on the subreddit you intend to have the bot manage.
2. [Register your bot](https://www.reddit.com/prefs/apps) on Reddit's Application Preferences management page. Obtain an `APP_ID`, and `APP_SECRET`
    * Click `create another app…` on the bottom of the page to begin the registration process
    > Note: You'll need to select a type of `script` from the radio options under the 'create application' prompt  
    * The `about url` field should contain a link to a wiki page on your subreddit about the bot you've created
    * The `redirect uri` needs to be a valid url, it's suggested to use the url of your subreddit
    > Note: By registering an application you are agreeing to reddit's [API Usage Guidelines](https://www.reddit.com/wiki/api)
    * Once you register successfully register your application, you'll see the `APP_ID` listed as a string below the text "personal use script", under the name you provided. **Treat this information like you would a password!**
    * To view your `APP_SECRET`, click `edit` in the bottom left corner of your registered application. Once expanded, the secret will be listed in the field labeled `secret`. **Treat this information like you would a password!**
    * You _may_ elect to register your bot on your personal account, however if you choose to you must add your bot as an application developer. You can do this by adding the bot's username to the list of developers under `Developed Applications` > application name > `edit` > `add developer`
* Provide the following .env variables:
    * `APP_ID` (`string`): Generated during the Reddit application registration process
    * `APP_SECRET` (`string`): Also generated during the Reddit application registration process
    * `USERNAME` (`string`): The reddit username of the account that will act as the bot
    * `SUBREDDIT` (`string`): The name of the subreddit where the bot will act

#### Configuring Flair
You can configure Balboa to manage the reciept, and assignemnt of flair to users on your subreddit.
<!-- TODO: JRB Subreddit Flair Configuration Description -->
