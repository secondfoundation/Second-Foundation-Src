__version__ = "$Revision: 0.9.4$"

import sys

if sys.version_info[:3] < (2,5,1):
    from elementtree import ElementTree as ET
else:
    import xml.etree.ElementTree as ET

from xml.parsers.expat import ExpatError
from urllib import urlencode
from datetime import datetime, date

from urllib2 import urlopen, URLError, HTTPError

get_attributes = lambda obj : [ attr for attr in dir(obj)\
                                if not callable(getattr(obj, attr)) ]

class NewsCred(object):
    
    @staticmethod
    def parse(module_name, access_key, xml):
        if module_name not in ['topic', 'article', 'source', 'author']:
            return
        
        load_module = lambda module_name : eval('NewsCred' + \
                                                module_name.capitalize() + '()')
        objects = []
        for parsed_node in NewsCredParser.parse(module_name, xml):
        
            module_obj = load_module(module_name)
            module_obj.access_key = access_key
            
            for attr in get_attributes(module_obj):
                
                if parsed_node.has_key(attr):
                    setattr(module_obj, attr, parsed_node[attr])
            
            objects.append(module_obj)

        return objects
    
    @staticmethod
    def parameterize(param):
        parameterize = lambda n : str(n).lower().replace(' ', '-')
        
        if str(type(param)) == "<type 'list'>":
            return (' ').join([parameterize(item) for item in param])

        return parameterize(param)
    
    @staticmethod
    def domain():
        return 'http://api.newscred.com'
    
    @staticmethod
    def get(url):
        print url
        try:
            response = ET.parse(urlopen(url))
        except HTTPError, e:
            if e.code == 401:
                raise NewsCredError(NewsCredError.AUTHENTICATION_FAILURE)
            elif e.code == 500:
                raise NewsCredError(NewsCredError.PLATFORM_RETURNED_ERROR + url)
            else:
                raise NewsCredError(NewsCredError.API_RESPONSE_GET_FAILED + url)
            return
        except URLError:
            raise NewsCredError(NewsCredError.API_RESPONSE_GET_FAILED + url)
            return
        except ExpatError:
            raise NewsCredError(NewsCredError.XML_PARSER_ERROR + url)
            return
        return response

    @staticmethod
    def parse_str_to_date(datetime_str):
            
        if sys.version_info[:3] < (2, 5, 1):
            try:
                from time import strptime
                time_struct = strptime(datetime_str, "%Y-%m-%d %H:%M:%S")                
                return datetime(*time_struct[:6])
            except Exception:
                return
        
        return datetime.strptime(datetime_str,"%Y-%m-%d %H:%M:%S")
    
    @staticmethod
    def build_request_url(options):
        
        for key in options:
            if str(type(options[key])) == "<type 'list'>":
                if (key == 'sources' or key == 'source_countries'):
                    options[key] = (' ').join(options[key])
                else:
                    options[key] = NewsCred.parameterize(options[key])
        
        return '&'+urlencode(options)

class NewsCredParser(object):
    
    @staticmethod
    def parse(tag_name, xml):
        
        return [NewsCredParser.parse_node_to_dict(tag_name,element) \
                for element in xml.getiterator(tag=tag_name)]
    
    @staticmethod
    def get_clusters(xml, key):
        
        def get_cluster(cluster_node):
            cluster = [get_article_object(article_node) for article_node in cluster_node.find('article_set').findall('article')]            
            return cluster
        
        def get_article_object(article_node):
            article_dict = NewsCredParser.parse_node_to_dict('article', article_node)
            article_obj = NewsCredArticle(access_key=key)
            for attr in get_attributes(article_obj):
                if article_dict.has_key(attr):
                    setattr(article_obj, attr, article_dict[attr])
            article_obj.source = get_source_object(article_node.find('source'))
            return article_obj
        
        def get_source_object(source_node):
            source_dict = NewsCredParser.parse_node_to_dict('source', source_node)
            source_obj = NewsCredSource(access_key=key)
            for attr in get_attributes(source_obj):
                if source_dict.has_key(attr):
                    setattr(source_obj, attr, source_dict[attr])
            return source_obj
            
        return [get_cluster(cluster_node) for cluster_node in xml.findall('cluster')]
    
    @staticmethod
    def parse_node_to_dict(tag_name, node):

        def parse_topic_node(topic_node):
            topic = {}

            for child in topic_node.getchildren():
                try:
                    if child.tag == 'topic_classification':
                        if child.find('name') is not None:
                            topic['classification'] = child.find('name').text
                        else:
                            topic['classification'] = child.text
                    elif child.tag == 'topic_subclassification':
                        if child.find('name') is not None:
                            topic['subclassification'] = child.find('name').text
                        else:
                            topic['subclassification'] = child.text
                    else:
                        topic[child.tag] = child.text
                except AttributeError:
                    continue
            return topic

        def parse_article_node(article_node):
            article = {}
            for child in article_node.getchildren():
                try:
                    if child.tag == 'category':
                        article['category'] = child.find('name').text
                    elif child.tag == 'created_at' or child.tag == 'published_at':
                        article[child.tag] = NewsCred.parse_str_to_date(child.text)
                    elif child.tag == 'source':
                        article['source']         = child.find('name').text
                        article['source_guid']    = child.find('guid').text
                        article['source_website'] = child.find('website').text
                    elif child.tag == 'thumbnail':
                        article['thumbnail'] = child.find('link').text
                        article['thumbnail_original'] = child.find('original_image').text
                    elif child.tag == 'topic_set':
                        article['topics'] = [parse_topic_node(topic_node) for topic_node in child.findall('topic')]
                    else :
                        article[child.tag] = child.text
                except AttributeError:
                    continue
            return article

        def parse_source_node(source_node):
            source = {}
            for child in source_node.getchildren():
                try:
                    source[child.tag] = child.text
                except AttributeError:
                    continue
            return source
        
        def parse_author_node(author_node):
            author = {}
            for child in author_node.getchildren():
                try:
                    if child.tag == 'first_name':
                        author['first_name'] = child.text
                    elif child.tag == 'last_name':
                        author['last_name'] = child.text
                    elif child.tag == 'guid':
                        author['guid'] = child.text
                    else : continue
                except AttributeError:
                    continue
            return author

        def parse_image_node(image_node):

            image = {}
            for child in image_node.getchildren():
                try:
                    if child.tag == 'urls':
                        try:
                            for url_child in child.getchildren():
                                if url_child.tag == 'small':
                                    image['image_small'] = url_child.text
                                elif url_child.tag == 'medium':
                                    image['image_medium'] = url_child.text
                                elif url_child.tag == 'large':
                                    image['image_large'] = url_child.text
                                else: continue
                        except AttributeError:
                            continue
                    elif child.tag == 'published_at' or child.tag == 'created_at':
                        image[child.tag] = NewsCred.parse_str_to_date(child.text)
                    else :
                        image[child.tag] = child.text
                except AttributeError:
                    continue
            return image
        
        def parse_tweet_node(tweetNode):
            tweet = {}
            for child in tweetNode.getchildren():
                try:
                    if child.tag == 'created_at':
                        tweet['created_at'] = NewsCred.parse_str_to_date(child.text)
                    else:
                        tweet[child.tag] = child.text
                except AttributeError:
                    continue
            return tweet
        
        def parse_video_node(videoNode):
            video = {}
            for child in videoNode.getchildren():
                try:
                    if child.tag == 'source':
                        video['source_name'] = child.find('name').text
                    elif child.tag == 'category':
                        video['category'] = child.find('name').text
                    elif child.tag == 'published_at':
                        video['published_at'] = NewsCred.parse_str_to_date(child.text)
                    else:
                        video[child.tag] = child.text
                except AttributeError:
                    continue
            return video
        
        #Register methods for parsing specific type of node
        node_parsers =  (
                            ('topic',   parse_topic_node), 
                            ('article', parse_article_node),
                            ('source',  parse_source_node), 
                            ('author',  parse_author_node),
                            ('image',   parse_image_node),
                            ('tweet',   parse_tweet_node),
                            ('video',   parse_video_node),
                        )
        
        if tag_name not in [node_type for node_type, node_parser in node_parsers]:
            return
        
        #check the current node_type and call appropriate method to parse
        for node_type, node_parser in node_parsers:
            if tag_name == node_type:
                parsed_node = node_parser(node)
                break

        return parsed_node  

class NewsCredError(Exception):
    
    NO_ACCESS_KEY           = 'No Access Key provided.'
    XML_PARSE_ERROR         = 'Failed to parse XML response for the request: '
    AUTHENTICATION_FAILURE  = 'Authentication Failed. Please check the Access Key.'
    PLATFORM_RETURNED_ERROR = 'NewsCred Platform returned Internal Server Error for this request: '
    API_RESPONSE_GET_FAILED = 'Failed to get response from NewsCred Platform for the request: '
    
    def __init__(self, message):
        self.message = message
    
    def __str__(self):
        return self.message

class NewsCredModule:
    
    def __init__(self):
        self.access_key = ''
        self.guid       = ''
        self.url        = ''
        
    def get_related_topics(self, options={}):
        if not self.access_key:
            raise NewsCredError(NewsCredError.NO_ACCESS_KEY) 
        
        self.url = NewsCred.domain() + '/' + self.module + '/'
                
        self.url += (self.module == 'category') and self.name or self.guid
        
        self.url += '/topics?' + urlencode({'access_key': self.access_key})
        
        if options:
            self.url += NewsCred.build_request_url(options)
        
        xml = NewsCred.get(self.url)
        
        return NewsCred.parse('topic', self.access_key, xml)

    def get_related_articles(self, options={}):
        if not self.access_key:
            raise NewsCredError(NewsCredError.NO_ACCESS_KEY)
        
        self.url = NewsCred.domain() + '/' + self.module + '/'
        
        if self.module == 'category':
            self.url += self.name
        else:
            self.url += self.guid
        
        self.url += '/articles?' + urlencode({'access_key': self.access_key})
        
        if options:
            self.url += NewsCred.build_request_url(options)
        
        xml = NewsCred.get(self.url)
        
        return NewsCred.parse('article', self.access_key, xml)
    
class NewsCredTopic(NewsCredModule):

    def __init__(self, access_key = '', guid = ''):
        self.module = 'topic'
        NewsCredModule.__init__(self)
        self.name              = ''
        self.image_url         = ''
        self.classification    = ''
        self.subclassification = ''
        self.description       = ''
        self.dashed_name       = ''
        self.link              = ''
        self.access_key        = access_key
        self.guid              = guid

        if access_key and guid:
            self.url = NewsCred.domain() + '/topic/' + guid + '?access_key=' \
                                                            + access_key
            xml = NewsCred.get(self.url)
            topic = NewsCredParser.parse('topic', xml)[0]
            
            for attr in get_attributes(self):
                if topic.has_key(attr):
                    setattr(self, attr, topic[attr])
        return
    
    def get_related_images(self, options={}):
        
        if not self.access_key:
            raise NewsCredError(NewsCredError.NO_ACCESS_KEY)
            
        self.url = NewsCred.domain() + '/topic/' + self.guid + '/images?' \
                                     + urlencode({'access_key': self.access_key})
        
        if options:
            self.url += NewsCred.build_request_url(options)
        
        xml = NewsCred.get(self.url)

        return NewsCredParser.parse('image', xml)
    
    def get_related_sources(self, options={}):
        if not self.access_key:
            raise NewsCredError(NewsCredError.NO_ACCESS_KEY) 
        
        self.url = NewsCred.domain() + '/' + self.module + '/' + self.guid \
                                     + '/sources?' + \
                                     urlencode({'access_key': self.access_key})
        if options:
            self.url += NewsCred.build_request_url(options)
        
        xml = NewsCred.get(self.url)
        
        return NewsCred.parse('source', self.access_key, xml)

    def get_related_tweets(self, options={}):
        if not self.access_key:
            raise NewsCredError(NewsCredError.NO_ACCESS_KEY)
        
        self.url = NewsCred.domain() + '/topic/' + self.guid + '/tweets?'\
                                     + urlencode({'access_key': self.access_key})
        
        if options:
            self.url += NewsCred.build_request_url(options)

        xml = NewsCred.get(self.url)

        return NewsCredParser.parse('tweet', xml)
    
    def get_related_videos(self, options={}):
        if not self.access_key:
            raise NewsCredError(NewsCredError.NO_ACCESS_KEY)
        
        self.url = NewsCred.domain() + '/topic/' + self.guid + '/videos?'\
                                     + urlencode({'access_key': self.access_key})
           
        if options:
            self.url += NewsCred.build_request_url(options)
        
        xml = NewsCred.get(self.url)

        return NewsCredParser.parse('video', xml)
    
    def get_related_stories(self, options={}):
        if not self.access_key:
            raise NewsCredError(NewsCredError.NO_ACCESS_KEY)
        
        self.url = NewsCred.domain() + '/topic/' + self.guid + '/stories?'\
                                     + urlencode({'access_key': self.access_key})
           
        if options:
            self.url += NewsCred.build_request_url(options)
        
        xml = NewsCred.get(self.url)
        
        return NewsCredParser.get_clusters(xml, self.access_key)
    
    @staticmethod
    def extract(access_key, query, options={}):
        if not access_key:
            raise NewsCredError(NewsCredError.NO_ACCESS_KEY)
        
        api_method_name = (options.has_key('exact') and options['exact'] == True)\
                          and 'extract' or 'related'
        
        url = NewsCred.domain() + '/topics/'+api_method_name+'?'\
                                + urlencode({'access_key': access_key,\
                                             'query': query.encode('utf-8')})
        if options:
            url += NewsCred.build_request_url(options)
        
        xml = NewsCred.get(url)
        
        return NewsCred.parse('topic', access_key, xml)

    @staticmethod
    def search(access_key, query, options={}):
        if not access_key:
            raise NewsCredError(NewsCredError.NO_ACCESS_KEY)
        
        url = NewsCred.domain() + '/topics?'\
                                + urlencode({'access_key': access_key,\
                                             'query': query.encode('utf-8')})
        
        if options:
            url += NewsCred.build_request_url(options)
        
        xml = NewsCred.get(url)
        return NewsCred.parse('topic', access_key, xml)


class NewsCredArticle(NewsCredModule):

    def __init__(self, access_key='', guid=''):
        self.module = 'article'
        NewsCredModule.__init__(self)
        self.source             = ''
        self.title              = ''
        self.created_at         = ''
        self.published_at       = ''
        self.description        = ''
        self.category           = ''
        self.link               = ''
        self.source_guid        = ''
        self.source_website     = ''
        self.thumbnail          = ''
        self.thumbnail_original = ''
        self.topics             = ''
        self.access_key         = access_key
        self.guid               = guid
        
        if access_key and guid:
            self.url = NewsCred.domain() + '/article/' + self.guid \
                                         + '?access_key=' + self.access_key
            xml = NewsCred.get(self.url)
            article  = NewsCredParser.parse('article', xml)[0]

            for attr in get_attributes(self):
                if article.has_key(attr):
                    setattr(self,attr,article[attr])
        return

    def get_related_images(self, options={}):
        if not self.access_key:
            raise NewsCredError(NewsCredError.NO_ACCESS_KEY)
        
        self.url = NewsCred.domain() + '/article/' + self.guid + '/images?'\
                                     + urlencode({'access_key': self.access_key})
        if options:
            self.url += NewsCred.build_request_url(options)
        
        xml = NewsCred.get(self.url)
        
        return NewsCredParser.parse('image', xml)

    @staticmethod
    def search(access_key, query, options={}):
        if not access_key:
            raise NewsCredError(NewsCredError.NO_ACCESS_KEY)
            
        url = NewsCred.domain() + '/articles?' \
                                + urlencode({'access_key': access_key,\
                                             'query': query.encode('utf-8')})        
        if options:
            url += NewsCred.build_request_url(options)

        xml = NewsCred.get(url)
        
        return NewsCred.parse('article', access_key, xml)

    @staticmethod
    def search_stories(access_key, query, options={}):
        if not access_key:
            raise NewsCredError(NewsCredError.NO_ACCESS_KEY)
            
        url = NewsCred.domain() + '/stories?' \
                                + urlencode({'access_key': access_key,\
                                             'query': query.encode('utf-8')})        
        if options:
            url += NewsCred.build_request_url(options)
        
        xml = NewsCred.get(url)
        
        return NewsCredParser.get_clusters(xml, access_key)

class NewsCredSource(NewsCredModule):

    def __init__(self, access_key='', guid=''):
        self.module = 'source'
        NewsCredModule.__init__(self)
        self.name        = ''
        self.website     = ''
        self.country     = ''
        self.frequency   = ''
        self.media_type  = ''
        self.is_blog     = ''
        self.description = ''
        self.circulation = ''
        self.thumbnail   = ''
        self.access_key  = access_key
        self.guid        = guid
        
        if access_key and guid :
            
            self.url = NewsCred.domain() + '/source/' + self.guid\
                                         + '?access_key=' + self.access_key
            
            xml = NewsCred.get(self.url)
            source   = NewsCredParser.parse('source', xml)[0]
            
            for attr in get_attributes(self):
                if source.has_key(attr):
                    setattr(self,attr,source[attr])
        return

    @staticmethod
    def search(access_key, query, options={}):
        
        if not access_key:
            raise NewsCredError(NewsCredError.NO_ACCESS_KEY)
        
        url = NewsCred.domain() + '/sources?'\
                                + urlencode({'access_key': access_key,\
                                             'query': query.encode('utf-8')})        
        if options:
            url += NewsCred.build_request_url(options)
        
        xml = NewsCred.get(url)
        
        return NewsCred.parse('source', access_key, xml)

class NewsCredCategory(NewsCredModule):

    def __init__(self, access_key, name):
        self.module = 'category'
        NewsCredModule.__init__(self)
        self.url = ''
        xml = ''
        
        self.name       = name
        self.access_key = access_key
        
        return
    
    def get_related_sources(self, options={}):
        if not self.access_key:
            raise NewsCredError(NewsCredError.NO_ACCESS_KEY) 

        self.url = NewsCred.domain() + '/' + self.module + '/' + self.name\
                                     + '/sources?' + urlencode({'access_key':
                                                                 self.access_key})
        if options:
            self.url += NewsCred.build_request_url(options)
        
        xml = NewsCred.get(self.url)

        return NewsCred.parse('source', self.access_key, xml)
    

    def get_related_images(self, options={}):
        if not self.access_key:
            raise NewsCredError(NewsCredError.NO_ACCESS_KEY)

        self.url = NewsCred.domain() + '/' + self.module + '/' + self.name\
                                     + '/images?' + urlencode({'access_key':
                                                                self.access_key})

        if options:
            self.url += NewsCred.build_request_url(options)

        xml = NewsCred.get(self.url)

        return NewsCredParser.parse('image', xml)
    
    def get_related_stories(self, options={}):
        if not self.access_key:
            raise NewsCredError(NewsCredError.NO_ACCESS_KEY)
        
        self.url = NewsCred.domain() + '/category/' + self.name + '/stories?'\
                                     + urlencode({'access_key': self.access_key})
           
        if options:
            self.url += NewsCred.build_request_url(options)
        
        xml = NewsCred.get(self.url)
        
        return NewsCredParser.get_clusters(xml, self.access_key)

class NewsCredAuthor(NewsCredModule):
    
    def __init__(self, access_key='', guid=''):
        self.module = 'author'
        NewsCredModule.__init__(self)
        self.first_name = ''
        self.last_name  = ''
        self.access_key = access_key
        self.guid       = guid
        
        if access_key and guid:
            self.url = NewsCred.domain() + '/author/' + self.guid\
                                         + '?access_key=' + self.access_key
            
            xml = NewsCred.get(self.url)
            author   = NewsCredParser.parse('author', xml)[0]
            
            for attr in get_attributes(self):
                if author.has_key(attr):
                    setattr(self, attr, author[attr])
        return
        
    @staticmethod
    def search(access_key, query, options={}):
        url = NewsCred.domain() + '/authors?'\
                                + urlencode({'access_key':access_key,\
                                             'query':query.encode('utf-8')})
        
        if options:
            url += NewsCred.build_request_url(options)
        
        xml = NewsCred.get(url)

        return NewsCred.parse('author', access_key, xml)
        
class NewsCredTwitter(NewsCredModule):
    
    @staticmethod
    def search(access_key, query, options={}):
        if not access_key:
            raise NewsCredError(NewsCredError.NO_ACCESS_KEY)
        
        url = NewsCred.domain() + '/tweets?'\
                                + urlencode({'access_key': access_key,\
                                             'query': query.encode('utf-8')})        
        if options:
            url += NewsCred.build_request_url(options)
        
        xml = NewsCred.get(url)
        
        return NewsCredParser.parse('tweet', xml)

class NewsCredImage(NewsCredModule):

    @staticmethod
    def search(access_key, query, options={}):
        if not access_key:
            raise NewsCredError(NewsCredError.NO_ACCESS_KEY)

        url = NewsCred.domain() + '/images?'\
                                + urlencode({'access_key': access_key,\
                                             'query': query.encode('utf-8')})        
        if options:
            url += NewsCred.build_request_url(options)

        xml = NewsCred.get(url)

        return NewsCredParser.parse('image', xml)

class NewsCredVideo(NewsCredModule):

    @staticmethod
    def search(access_key, query, options={}):
        if not access_key:
            raise NewsCredError(NewsCredError.NO_ACCESS_KEY)

        url = NewsCred.domain() + '/videos?'\
                                + urlencode({'access_key': access_key,\
                                             'query': query.encode('utf-8')})        
        if options:
            url += NewsCred.build_request_url(options)

        xml = NewsCred.get(url)

        return NewsCredParser.parse('video', xml)                