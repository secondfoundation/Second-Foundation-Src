import sys
import urllib2
import urllib
import httplib
from xml.etree import ElementTree as etree
 
class wolfram(object):
    def __init__(self, appid):
        self.appid = appid
        self.base_url = 'http://api.wolframalpha.com/v2/query?'
        self.headers = {'User-Agent':None}
 
    def _get_xml(self, ip):
        url_params = {'input':ip, 'appid':self.appid}
        data = urllib.urlencode(url_params)
        req = urllib2.Request(self.base_url, data, self.headers)
        xml = urllib2.urlopen(req).read()
        return xml
 
    def _xmlparser(self, xml):
        data_dics = {}
        tree = etree.fromstring(xml)
        #retrieving every tag with label 'plaintext'
        for e in tree.findall('pod'):
            for item in [ef for ef in list(e) if ef.tag=='subpod']:
                for it in [i for i in list(item) if i.tag=='plaintext']:
                    if it.tag=='plaintext':
                        data_dics[e.get('title')] = it.text
        return data_dics
 
    def search(self, ip):
        xml = self._get_xml(ip)
        result_dics = self._xmlparser(xml)
        #return result_dics 
        #print result_dics
        print result_dics['Result']
 
if __name__ == "__main__":
    if(len(sys.argv) != 2):
        print 'incorrect call pattern, exiting'
        sys.exit(1)

    appid = sys.argv[0]
    query = sys.argv[1]
    print query
    app_id = "WK4VHQ-827PXK9QWY"
    w = wolfram(app_id)
    w.search(query)
