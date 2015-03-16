"""
"============================================================================
"File:        aws_dl.py
"Description: Python aws ocumentation reader (under development).
"Author: Marcin Katulski ( marcin.katulski@gmail.com )
"
"============================================================================
"""
import re
import codecs
import urllib
from bs4 import BeautifulSoup

class DownloadDoc:
    def __init__(self, url, doc,  proxy={} ):
        self._url = url
        self._doc = doc
        self._proxy = proxy
        self._linkList = {}

    def downloadList( self, fname ):
        print("Downloading: .... {0}".format(self._url+self._doc))
        self._site = urllib.urlopen( self._url+self._doc, proxies=self._proxy )
        html = self._site.read()
        self._listSoup = BeautifulSoup( html )
        print("Searching list of types ...")
        div = self._listSoup.find_all("div",{"class":"highlights"})

        if len(div)==1:
            print("Processing types ...")
            refList = div[0].find_all("a")

            for i in refList:
                 if i.text!="AWS::CloudFormation::Init":
                    if i.attrs.has_key("href"):
                        print("{0}".format(i.text))
                    self._linkList[ i.text ]={}
                    site = urllib.urlopen( self._url+i.attrs["href"],
                            proxies=self._proxy )
                    text = site.read()
                    sp = BeautifulSoup( text )
                    dvs = sp.find_all("div",{"class":"section"})
                    p = dvs[0].findChildren("p", recursive=False)
                    self._linkList[ i.text ]["doc"] =""
                    for j in p:
                        self._linkList[ i.text ]["doc"] += re.sub("[\"']", " ",
                                j.text+"\\n")
                    hr=dvs[0].findChildren("div",{"class":"section"})
                    self._linkList[ i.text ]["properties"] = {}
                    if len(hr)==0:
                        continue
                    hr=hr[0].find_all("a")
                    for prop in hr:
                        if self._linkList[i.text]["properties"].has_key(
                                prop.text ):
                            continue
                        if re.match('\w+\s+', prop.text  )is not None:
                            continue
                        "Try to load description for parameters"
                        dvsx = dvs[0].find_all("div", {"class":"variablelist"})
                        term = ""
                        for xvsd in dvsx:
                           span= xvsd.find_all("span", {"class":"term"}, text=prop.text)
                           if len(span) !=0:
                               term=span[0].findParent().findNextSibling()
                               break
                        self._linkList[ i.text
                                ]["properties"][prop.text]=re.sub("[\"']"," ",
                                        re.sub("<.*?>","",re.sub("</p>",'\\n',"{0}".format(term))))

            with codecs.open(fname, "wb" , encoding='utf8' ) as file:
                file.write("let g:AWSTypes=")
                s=str(self._linkList)
                s=re.sub("'", '"',s)
                s=re.sub("u\"","\"",s)
                file.write(s)



if __name__ == "__main__":
    doc = DownloadDoc("http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/","aws-template-resource-type-ref.html")
    doc.downloadList( "./AWSTypes.vim" )

