#!/usr/bin/env python3
#
# TakeOver - Subdomain TakeOver Finder
# Coded by Momo Outaadi (m4ll0k)

from __future__ import print_function

import re
import os
import sys
import time
import getopt
import urllib3
import urllib.parse
import requests
import json
# -- common services
# -- Add new services
# -- {'NAME SERVICE' : {'code':'[300-499]','error':'ERROR HERE'}}
# -- https://github.com/EdOverflow/can-i-take-over-xyz

services = {
        'AWS/S3'          : {'code':'[300-499]','error':r'The specified bucket does not exit'},
        'BitBucket'       : {'code':'[300-499]','error':r'Repository not found'},
        'Github'          : {'code':'[300-499]','error':r'There isn\'t a Github Pages site here\.'},
        'Shopify'         : {'code':'[300-499]','error':r'Sorry\, this shop is currently unavailable\.'},
        'Fastly'          : {'code':'[300-499]','error':r'Fastly error\: unknown domain\:'},

        'FeedPress'       : {'code':'[300-499]','error':r'The feed has not been found\.'},
        'Ghost'           : {'code':'[300-499]','error':r'The thing you were looking for is no longer here\, or never was'},
        'Heroku'          : {'code':'[300-499]','error':r'no-such-app.html|<title>no such app</title>|herokucdn.com/error-pages/no-such-app.html'},
        'Pantheon'        : {'code':'[300-499]','error':r'The gods are wise, but do not know of the site which you seek.'},
        'Tumbler'         : {'code':'[300-499]','error':r'Whatever you were looking for doesn\'t currently exist at this address.'},
        'Wordpress'       : {'code':'[300-499]','error':r'Do you want to register'},

        'TeamWork'        : {'code':'[300-499]','error':r'Oops - We didn\'t find your site.'},
        'Helpjuice'       : {'code':'[300-499]','error':r'We could not find what you\'re looking for.'},
        'Helpscout'       : {'code':'[300-499]','error':r'No settings were found for this company:'},
        'Cargo'           : {'code':'[300-499]','error':r'<title>404 &mdash; File not found</title>'},
        'StatusPage'      : {'code':'[300-499]','error':r'You are being <a href=\"https://www.statuspage.io\">redirected'},
        'Uservoice'       : {'code':'[300-499]','error':r'This UserVoice subdomain is currently available!'},
        'Surge'           : {'code':'[300-499]','error':r'project not found'},
        'Intercom'        : {'code':'[300-499]','error':r'This page is reserved for artistic dogs\.|Uh oh\. That page doesn\'t exist</h1>'},

        'Webflow'         : {'code':'[300-499]','error':r'<p class=\"description\">The page you are looking for doesn\'t exist or has been moved.</p>'},
        'Kajabi'          : {'code':'[300-499]','error':r'<h1>The page you were looking for doesn\'t exist.</h1>'},
        'Thinkific'       : {'code':'[300-499]','error':r'You may have mistyped the address or the page may have moved.'},
        'Tave'            : {'code':'[300-499]','error':r'<h1>Error 404: Page Not Found</h1>'},

        'Wishpond'        : {'code':'[300-499]','error':r'<h1>https://www.wishpond.com/404?campaign=true'},
        'Aftership'       : {'code':'[300-499]','error':r'Oops.</h2><p class=\"text-muted text-tight\">The page you\'re looking for doesn\'t exist.'},
        'Aha'             : {'code':'[300-499]','error':r'There is no portal here \.\.\. sending you back to Aha!'},
        'Tictail'         : {'code':'[300-499]','error':r'to target URL: <a href=\"https://tictail.com|Start selling on Tictail.'},
        'Brightcove'      : {'code':'[300-499]','error':r'<p class=\"bc-gallery-error-code\">Error Code: 404</p>'},
        'Bigcartel'       : {'code':'[300-499]','error':r'<h1>Oops! We couldn&#8217;t find that page.</h1>'},
        'ActiveCampaign'  : {'code':'[300-499]','error':r'alt=\"LIGHTTPD - fly light.\"'},

        'Campaignmonitor' : {'code':'[300-499]','error':r'Double check the URL or <a href=\"mailto:help@createsend.com'},
        'Acquia'          : {'code':'[300-499]','error':r'The site you are looking for could not be found.|If you are an Acquia Cloud customer and expect to see your site at this address'},
        'Proposify'       : {'code':'[300-499]','error':r'If you need immediate assistance, please contact <a href=\"mailto:support@proposify.biz'},
        'Simplebooklet'   : {'code':'[300-499]','error':r'We can\'t find this <a href=\"https://simplebooklet.com'},
        'GetResponse'     : {'code':'[300-499]','error':r'With GetResponse Landing Pages, lead generation has never been easier'},
        'Vend'            : {'code':'[300-499]','error':r'Looks like you\'ve traveled too far into cyberspace.'},
        'Jetbrains'       : {'code':'[300-499]','error':r'is not a registered InCloud YouTrack.'},

        'Smartling'       : {'code':'[300-499]','error':r'Domain is not configured'},
        'Pingdom'         : {'code':'[300-499]','error':r'pingdom'},
        'Tilda'           : {'code':'[300-499]','error':r'Domain has been assigned'},
        'Surveygizmo'     : {'code':'[300-499]','error':r'data-html-name'},
        'Mashery'         : {'code':'[300-499]','error':r'Unrecognized domain <strong>'},

}


def request(url,proxy,timeout):
        headers = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0'}
        try:
                req = requests.packages.urllib3.disable_warnings(
                        urllib3.exceptions.InsecureRequestWarning
                        )
                if proxy:
                        req = requests.get(url=url,headers=headers,proxies=proxy,timeout=timeout)
                else:
                        req = requests.get(url=url,headers=headers,timeout=timeout)
                return req.status_code,req.content
        except Exception as e:
                pass
        return None,None


def checker(status,content):
        code = ""
        error = ""
        # --
        for service in services:
                values = services[service]
                for value in values:
                        opt = services[service][value]
                        if value == 'error':
                                error = opt
                        if value == 'code':
                                code = opt
                # ---
                if re.search(code,str(status),re.I) and re.search(error,content.decode(),re.I):
                        return service,error
        return None,None

if __name__ =="__main__":
    fn = sys.argv[1]
    with open(fn+'/online.txt') as fp:
        for line in fp:
            if '. CNAME ' in line:
                dict = {}
                domain = line.split()[0][:-1]
                cname = line.split()[2][:-1]
                url = 'http://'+ cname
                status,content = request(url,None,3)
                service,error = checker(status,content)
                if service and error:
                    dict[domain] = {"cname" :cname,"service": service, "message" : 'True' }
                else:
                    dict[domain] = {"cname" : cname}

                with open(fn+'/takeover.txt','a') as file:
                    print(json.dumps(dict),file=file)                        
'''
                status,content = request(sub_domain,set_proxy,set_timeout)
                service,error = checker(status,content)
                if service and error:
                        plus(f'Found service: {service}')
                        plus('A potential TAKEOVER vulnerability found!')
'''
