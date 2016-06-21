#Content management portal for the dashboard.
def Content():
    TOPIC_DICT = {"Slack Settings": [["Team Name", "/slack-settings/"], ["OAuth Token","/slack-settings"],["Channel", "/slack-settings"]], 
                  "Github Settings": [["User Name", "/github-settings/"], ["OAuth Token","/github-settings"],["Project Name", "/github-settings"]],
                  "Twitter Settings": [["Handle", "/twitter-settings/"], ["OAuth Token","/twitter-settings"],["Hashtags", "/twitter-settings"]]        
                 }
    return TOPIC_DICT