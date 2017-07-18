"""
Routes and views for the bottle application.
"""

from bottle import route, view, get, redirect
from datetime import datetime
import  json, ssl
import urllib2

HOCKEYAPPTOKEN = 'fcc1d505c1884c9a81953351449b4ebe'
HOCKEYAPPID = '231414e493a34ddb96a96bde60d39f2b'

# HOCKEYAPPTOKEN = 'eb31bf4e16804f768847185318d45c00'
# HOCKEYAPPID = '5678688052d344279b4f7dc00a203d3e'

app_id = 1


@get('/getApk')
@route('/getApk')
def getApp():
    return redirect('https://rink.hockeyapp.net/api/2/apps/{0}/app_versions/{1}?format=apk'.format(HOCKEYAPPID, app_id))


def getAppInfoJson():
    newRequest = urllib2.Request('https://rink.hockeyapp.net/api/2/apps/{0}/app_versions?pages=1'.format(HOCKEYAPPID), headers={ 'X-HockeyAppToken': HOCKEYAPPTOKEN })
    return json.loads(urllib2.urlopen(newRequest).read())


@get('/checkForUpdate')
@route('/checkForUpdate')
def checkForUpdate():
    try:
        appResultJson = getAppInfoJson()
        if appResultJson is None:
            return None

        latestVersionInfo = None
        for version in appResultJson['app_versions']:
            if version['status'] == 2:
                latestVersionInfo = version
                break

        if latestVersionInfo is None:
            return None

        global app_id
        app_id = int(latestVersionInfo['id'])
        resultJson = json.dumps({
            'NewVersion' : latestVersionInfo['version'],
            'UpdateMandatory' : 'false',
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