"""
Routes and views for the bottle application.
"""

from bottle import route, view, redirect, request
from datetime import datetime
import telegram
import json
import urllib
import ssl
import time

TOKEN = '387238739:AAHHtOlnJ2zL_BQ_KsbnlnX4NWqOXlzyFDA'
APPNAME='cefitbot'
HOCKEYAPPTOKEN = 'eb31bf4e16804f768847185318d45c00'
app_version = 77
app_info = None

@route('/getApk')
def getApp():
    return redirect('https://rink.hockeyapp.net/api/2/apps/5678688052d344279b4f7dc00a203d3e/app_versions/{}?format=apk&avtoken=4c7da37fdb7681457730592e61afe7f3c38275a5'.format(app_version))

@route('/checkForUpdate')
def checkForUpdate():
    return app_info

def checkForUpdateLocal():
    try:
        appResultJson = getAppInfoJson()
        if appResultJson is None:
            return None

        latestVersionInfo = appResultJson['app_versions'][0]
        global  app_version
        app_version = int(latestVersionInfo['version'])
        resultJson = json.dumps({
            'NewVersion' : latestVersionInfo['version'],
            'UpdateMandatory' : 'true',
            'ApkSizeInBytes' : str(latestVersionInfo['appsize'])
        })
        return str(resultJson)
    except:
        return None

while True:
    app_info = checkForUpdateLocal()
    time.sleep(10)

def getAppInfoJson():
    request = urllib.request.Request('https://rink.hockeyapp.net/api/2/apps/5678688052d344279b4f7dc00a203d3e/app_versions?pages=1', headers={ 'X-HockeyAppToken': HOCKEYAPPTOKEN })
    gcontext = ssl._create_unverified_context()
    return json.loads(urllib.request.urlopen(request, context=gcontext).read())

@route('/setWebhook')
def setWebhook():
    bot = telegram.Bot(TOKEN)
    botWebhookResult = bot.setWebhook(webhook_url='https://{}.azurewebsites.net/bothook'.format(APPNAME))
    return str(botWebhookResult)


@route('/bothook', method='POST')
def botHook():
    bot = telegram.Bot(TOKEN)
    update = telegram.update.Update.de_json(request.json, bot)
    bot.sendMessage(chat_id=update.message.chat_it, text=getSum(update.message.text, update.message.from_user.username))
    return 'OK'

def getSum(query, userName):
    try:
        splittedBySum = query.split('+')
        if len(splittedBySum) != 2:
            raise ValueError('Too complicated stuff')
        return str(int(splittedBySum[0]) + int(splittedBySum[1]))
    except:
        return 'I\'m sorry, {}. I\'m afraid I can\'t do that'.format(userName)


@route('/')
@route('/home')
@view('index')
def home():
    """Renders the home page."""
    return dict(
        year=datetime.now().year
    )

@route('/contact')
@view('contact')
def contact():
    """Renders the contact page."""
    return dict(
        title='Contact',
        message='Your contact page.',
        year=datetime.now().year
    )

@route('/about')
@view('about')
def about():
    """Renders the about page."""
    return dict(
        title='About',
        message='Your application description page.',
        year=datetime.now().year
    )
