import requests
import json
import constants
import apihelper
import datetime
import slackhelper

now = datetime.datetime.now()

todayDateString = str(now.year) + '-' + str(now.month) + '-' + str(now.day)

params = {
    'from': todayDateString,
    'to': todayDateString,
}

response = apihelper.queryAPI('get_events', params)

if response.status_code == requests.codes.ok :
    allMatches = response.json()
    if allMatches :
        attachments = []
        liveMatches = [match for match in allMatches if match['match_status'] == 'FT']
        for match in liveMatches :
            goalScorers = [];
            if match['goalscorer'] :
                homeScore = {
                    "title": match['match_hometeam_name'],
                    "value": "",
                    "short": 'true'
                }
                awayScore = {
                    "title": match['match_awayteam_name'],
                    "value": "",
                    "short": 'true'
                }
                for scorer in match['goalscorer'] :
                    if not scorer['away_scorer'] :
                        homeScore['value'] += scorer['home_scorer'] + " " + scorer['time'] + "\n"
                    elif not scorer['home_scorer'] :
                        awayScore['value'] += scorer['away_scorer'] + " " + scorer['time'] + "\n"
                goalScorers = [homeScore, awayScore]
            message = {
                "fallback": "Match Scoreline",
                "color": "#36a64f",
                "author_name": match['country_name'] + " " + match['league_name'],
                "title": match['match_hometeam_name'] + " vs " + match['match_awayteam_name'],
                "text": match['match_hometeam_score'] + " - " + match['match_awayteam_score'] + " (" + match['match_time'] + "')",
                "fields": goalScorers
            }
            print message
            attachments.append(message)
        slackhelper.sendToSlack({"attachments": attachments})
