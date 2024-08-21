import slack_sdk

class slackAPI:
    def __init__(self, api_key):
        self._channel = None
        self._client = slack_sdk.WebClient(token=api_key)
    def setChannel(self, channel):
        self._channel = channel
    def sendMessage(self, message):
        self._client.chat_postMessage(channel=self._channel, text=message)
    

if __name__ == "__main__":
    file = open("hidden.key","r")
    lines = file.readlines()
    file.close()
    token = lines[0].strip()
    channel = lines[2].strip()
    slack = slackAPI(token)
    slack.setChannel(channel)
    slack.sendMessage("Hello, world!")

    

    
        

        