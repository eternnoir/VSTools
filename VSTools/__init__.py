from VSTools.build import MsBuild

__author__ = 'eternnoir'
VERSION = "v0.0.1"

FrameworkVersionDic = {"v4.0.30319":  r'C:\Windows\Microsoft.NET\Framework\v4.0.30319'}


def getDefautlMsBuild(debug=False):
    return MsBuild(FrameworkVersionDic["v4.0.30319"]+r'\MSBuild.exe',debug)
