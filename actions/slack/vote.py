import os
import sys
from slack import WebClient
from slack.errors import SlackApiError

class Vote:
    if os.getenv("SLACK_SIGNING_SECRET") is None:
        from os.path import join, dirname
        from dotenv import load_dotenv

        load_dotenv()

    # Initialize a Web API client
    slack_web_client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))

    vote_prompt = [
		{
			"type": "section",
			"text": {
				"type": "plain_text",
				"text": "Time to vote.",
				"emoji": True
			}
		},
		{
			"type": "divider"
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "✅ Tony Vlachos\n\n✅ Sandra Diaz-Twine\n\n✅ Parvarti Shallow\n\n🗳 Yul Kwon\n\n🗳 Nick Wilson\n\n✅ Denise Stapley"
			}
		},
		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Cast Vote",
						"emoji": True
					},
					"value": "casting_vote"
				}
			]
		}
	]

    def __init__(self, payload):
        self.status = {
            'statusCode': 0,
            'subject': 'Make tribe action',
            'message': ''
        }

        # run through the operations here
        try:
            response = self.slack_web_client.chat_postMessage(
                channel=payload['channel'],
                blocks=self.vote_prompt
            )
            self.status['statusCode'] = 0
            self.status['subject'] = None
            print("response is")
            print(str(response))
            sys.stdout.flush()
        # pylint: disable=catching-non-exception
        except Exception as e:
        # pylint: enable=catching-non-exception
            print(e)
            sys.stdout.flush()
            self.status['statusCode'] = 200
            self.status['subject'] = str(e)

    @property
    def complete(self):
        return self.status
