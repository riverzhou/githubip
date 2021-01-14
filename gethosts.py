#!/usr/bin/env python3

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from html2text import *
import re

listDomain = [
    'rawgit.com',
    'github-cloud.s3.amazonaws.com',
    'gist.github.com',
    'api.github.com',
    'assets-cdn.github.com',
    'github.githubassets.com',
    'raw.githubusercontent.com',
    'favicons.githubusercontent.com',
    'gist.githubusercontent.com',
    'cloud.githubusercontent.com',
    'avatars0.githubusercontent.com',
    'avatars2.githubusercontent.com',
    'avatars1.githubusercontent.com',
    'avatars3.githubusercontent.com',
    'camo.githubusercontent.com',
    'user-images.githubusercontent.com',
]

#listDomain = ['raw.githubusercontent.com',]

resultFilename = 'hosts'

urlPrefix = 'https://ip.sb/domain/'
resultTag = 'https://ip.sb/whois/'
resultHead = 'Address'
waitTime = 5
maxRetry = 2

listUrl = []
dictUrlRetry = {}
for domain in listDomain:
    _url = urlPrefix+domain
    listUrl.append(_url)
    dictUrlRetry[_url] = maxRetry
listUrl.reverse()

currentUrl = ''
listResult = []


def isIP(testStr):
    p = re.compile(
        '^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    if p.match(testStr):
        return True
    else:
        return False


def loadFinished():
    bgTimer.singleShot(waitTime*1000, getHTML)


def getHTML():
    webview.page().toHtml(procHTML)


def procHTML(rawhtml):
    ip = ''
    mdText = html2text(rawhtml)
    for line in mdText.split('\n'):
        line = line.strip()
        if line.startswith(resultHead) and resultTag in line:
            ip = line.split(resultTag)[1].rstrip(')')
            if isIP(ip):
                print(line, currentUrl)
                break
    if not isIP(ip):
        if dictUrlRetry[currentUrl] > 0:
            dictUrlRetry[currentUrl] -= 1
            listUrl.insert(0, currentUrl)
            print(mdText)
    else:
        listResult.append((ip, currentUrl.split(urlPrefix)[1]))
    loadUrl()


def procResult():
    print('-'*50)
    for record in listResult:
        print(record)
    with open(resultFilename, 'w', encoding='utf-8') as wf:
        for recored in listResult:
            wf.write('{}    {} \n'.format(*recored))


def loadUrl():
    global currentUrl
    if len(listUrl) == 0:
        procResult()
        a.exit()
        return
    currentUrl = listUrl.pop()
    #currentUrl = 'https://www.baidu.com'
    print(currentUrl)
    webview.load(QUrl(currentUrl))


if __name__ == '__main__':
    a = QApplication([])
    bgTimer = QTimer()
    webview = QWebEngineView()
    webview.loadFinished.connect(loadFinished)
    loadUrl()
    a.exec_()
