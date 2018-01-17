"""
Routes and views for the bottle application.
"""

from bottle import route, view, get, redirect, request
from datetime import datetime
import  json
import urllib2

#QA LOGIC

# QAAPITOKEN = 'fcc1d505c1884c9a81953351449b4ebe'
#
# QAAPPID = '231414e493a34ddb96a96bde60d39f2b'
#
#
# def getApiToken(companyId):
#     return QAAPITOKEN
#
# def getAppId(companyId):
#     return QAAPPID

#END


#Release LOGIC

MARAPITOKEN = 'ea53c4d267fe45a2a5525cdc0781f550'
NCSAPITOKEN = 'eb31bf4e16804f768847185318d45c00'
PROAPITOKEN = 'ec51d0fba71a4cce83ae6744c5211ba7'
FRORUSAPITOKEN = 'f565ccb84bbb43c4aa23b98c9ddc438f'

MARAPPID = '3e8c3c11679d41158dc15d5088929eae'
NCSAPPID = '5678688052d344279b4f7dc00a203d3e'
PROAPPID = '1c7acaf01ddf4db3aa8fffa84464927d'
FRORUSAPPID = '3f80246ce01f4489971a6c9925a27a5f'

def getApiToken(companyId):
    return {
        'FRORUS': FRORUSAPITOKEN,
        'MAR': MARAPITOKEN,
        'NCS': NCSAPITOKEN
        #'PRO': PROAPITOKEN
    }[companyId]


def getAppId(companyId):
    return {
        'FRORUS': FRORUSAPPID,
        'MAR': MARAPPID,
        'NCS': NCSAPPID,
        #'PRO': PROAPPID
    }[companyId]

#END


@get('/getApk')
@route('/getApk')
def getApp():
    parameters = request.query.getlist('company')
    companyId = 'NCS'
    if len(parameters) > 0:
        companyId = parameters[0]
    appId = getAppId(companyId)
    redirect('https://rink.hockeyapp.net/api/2/apps/{0}?format=apk'.format(appId), 302)


def getAppInfoJson():
    parameters = request.query.getlist('company')
    companyId = 'NCS'
    if len(parameters) > 0:
        companyId = parameters[0]
    newRequest = urllib2.Request('https://rink.hockeyapp.net/api/2/apps/{0}/app_versions?pages=1'.format(getAppId(companyId)), headers={ 'X-HockeyAppToken': getApiToken(companyId) })
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
