"""
Routes and views for the bottle application.
"""

from bottle import route, view, redirect
from datetime import datetime
import json
import ssl
from urllib import request

app_id= 77
TOKEN = '387238739:AAHHtOlnJ2zL_BQ_KsbnlnX4NWqOXlzyFDA'
APPNAME='cefitbot'
HOCKEYAPPTOKEN = 'eb31bf4e16804f768847185318d45c00'

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

# @route('/getApk')
# def getApp():
#     return redirect('https://rink.hockeyapp.net/api/2/apps/5678688052d344279b4f7dc00a203d3e/app_versions/{}?format=apk&avtoken=4c7da37fdb7681457730592e61afe7f3c38275a5'.format(app_id))
#
#
# def getAppInfoJson():
#     newRequest = request.Request('https://rink.hockeyapp.net/api/2/apps/5678688052d344279b4f7dc00a203d3e/app_versions?pages=1', headers={ 'X-HockeyAppToken': HOCKEYAPPTOKEN })
#     gcontext = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
#     return json.loads(request.urlopen(newRequest, context=gcontext).read())
#
#
# def checkForUpdateLocal():
#     try:
#         appResultJson = getAppInfoJson()
#         if appResultJson is None:
#             return "Empty response from hockeyapp"
#
#         latestVersionInfo = appResultJson['app_versions'][0]
#         global app_id
#         app_id = int(latestVersionInfo['id'])
#         resultJson = json.dumps({
#             'NewVersion' : latestVersionInfo['version'],
#             'UpdateMandatory' : 'true',
#             'ApkSizeInBytes' : str(latestVersionInfo['appsize'])
#         })
#         return str(resultJson)
#     except Exception as inst:
#         return repr(inst)
#
#
# @route('/checkForUpdate')
# def checkForUpdate():
#     return checkForUpdateLocal()


