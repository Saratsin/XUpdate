"""
Routes and views for the bottle application.
"""

from bottle import route, view, get, redirect
from datetime import datetime
import  json, ssl
import urllib2

HOCKEYAPPTOKEN = 'eb31bf4e16804f768847185318d45c00'
app_id = 1


@get('/getApk')
@route('/getApk')
def getApp():
    return redirect('https://rink.hockeyapp.net/api/2/apps/5678688052d344279b4f7dc00a203d3e/app_versions/{}?format=apk&avtoken=4c7da37fdb7681457730592e61afe7f3c38275a5'.format(app_id))


def getAppInfoJson():
    newRequest = urllib2.Request('https://rink.hockeyapp.net/api/2/apps/5678688052d344279b4f7dc00a203d3e/app_versions?pages=1', headers={ 'X-HockeyAppToken': HOCKEYAPPTOKEN })
    return json.loads(urllib2.urlopen(newRequest).read())
 

@get('/checkForUpdate')
@route('/checkForUpdate')
def checkForUpdate():
    try:
        appResultJson = getAppInfoJson()
        if appResultJson is None:
            return None

        latestVersionInfo = appResultJson['app_versions'][0]
        global app_id
        app_id = int(latestVersionInfo['id'])
        resultJson = json.dumps({
            'NewVersion' : latestVersionInfo['version'],
            'UpdateMandatory' : 'true',
            'ApkSizeInBytes' : str(latestVersionInfo['appsize'])
        })
        return str(resultJson)
    except:
        return None


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