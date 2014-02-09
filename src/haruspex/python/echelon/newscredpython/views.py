from django.http import HttpResponse
from django.shortcuts import render_to_response
from newscred import *

ACCESS_KEY = 'c4bcc3f7c9bf9ec159f51da0a86ca658'

def index(request):
    return render_to_response('index.html', {})

def topic(request):
    
    data = {}
    sources =  ['e5b7feb6870f7c251d7ad10c8b9b8820',
                'f5cf0126fabbbf97a44c9252761b60dd', 
                '-a5364a204a0422bdcf23acc6c5c88af8']
    
    try:
        searched_topics = NewsCredTopic.search(access_key=ACCESS_KEY, query='obama')
        
        topic = NewsCredTopic(access_key=ACCESS_KEY, guid='1e3f343e71de57fe9cc70b90c07e196e')
        
        related_topics = topic.get_related_topics()
        related_articles = topic.get_related_articles()
        related_articles_sources = topic.get_related_articles(options={'sources': sources})
        extracted_topics = NewsCredTopic.extract(access_key=ACCESS_KEY, query=topic.name)
        
        related_images = topic.get_related_images()
        topic_sources = topic.get_related_sources()
        
        data['topic'] = topic
        data['related_topics'] = related_topics
        data['related_articles'] = related_articles
        data['related_articles_sources'] = related_articles_sources
        data['searched_topics'] = searched_topics
        data['extracted_topics'] = extracted_topics
        data['related_images'] = related_images
        data['topic_sources'] = topic_sources
    
    except (NewsCredError), e:
        data['error'] = str(e)
    
    return render_to_response('topic.html', data)

def article(request):
    data    = {}
    sources = ['a5364a204a0422bdcf23acc6c5c88af8', 'f5cf0126fabbbf97a44c9252761b60dd',
               '-f668ac1f65393e74632007ba18c56bf0']
    try:
        searched_articles = NewsCredArticle.search(access_key=ACCESS_KEY, query='obama')
        
        article = NewsCredArticle(access_key = ACCESS_KEY,
        guid='3c144aca4082da4d43dd765c03c13e25')
        
        related_articles = article.get_related_articles()
        related_topics = article.get_related_topics()
        related_article_sources = article.get_related_articles(options={'sources': sources})
        related_images = article.get_related_images()

        data['article'] = article
        data['related_topics'] = related_topics
        data['related_articles'] = related_articles
        data['related_article_sources'] = related_article_sources
        data['searched_articles'] = searched_articles
        data['related_images'] = related_images
    
    except (NewsCredError), e:
        data['error'] = str(e)
    
    return render_to_response('article.html', data)

def source(request):
    
    data = {}
    try:
        
        source = NewsCredSource(access_key=ACCESS_KEY,
        guid='a5364a204a0422bdcf23acc6c5c88af8')
        
        data['source'] = source
        data['related_topics'] = source.get_related_topics()
        data['related_articles'] = source.get_related_articles()
        data['search_sources'] = NewsCredSource.search(\
        access_key=ACCESS_KEY,query='guardian')

    except (NewsCredError), e:
        data['error'] = str(e)

    return render_to_response('source.html', data)


def author(request):
    
    data = {}
    blacklist =  ['-f668ac1f65393e74632007ba18c56bf0','-a5364a204a0422bdcf23acc6c5c88af8']
    try:
        
        author           = NewsCredAuthor(access_key=ACCESS_KEY, guid='aab86c756ac5b04ea325e6fd3f105ddc')
        related_articles = author.get_related_articles(options={'sources': blacklist})
        related_topics   = author.get_related_topics()
        search_authors   = NewsCredAuthor.search(access_key=ACCESS_KEY, query='paul')
        
        data['author']           = author
        data['related_articles'] = related_articles
        data['related_topics']   = related_topics
        data['authors']          = search_authors
    
    except (NewsCredError), e:
        data['error'] = str(e)
    
    return render_to_response('author.html', data)

def category(request):
    
    data = {}
    sources   = ['a5364a204a0422bdcf23acc6c5c88af8','-f668ac1f65393e74632007ba18c56bf0','f5cf0126fabbbf97a44c9252761b60dd']
    
    try:
        category                = NewsCredCategory(access_key=ACCESS_KEY, name='technology')
        related_topics          = category.get_related_topics(options={'topic_classifications': ['product']})
        related_articles        = category.get_related_articles()
        related_article_sources = category.get_related_articles(options={'sources': sources})
        related_sources         = category.get_related_sources()

        data['category']                = category
        data['related_topics']          = related_topics
        data['related_sources']         = related_sources
        data['related_articles']        = related_articles
        data['related_article_sources'] = related_article_sources

    except (NewsCredError), e:
        data['error'] = str(e)
    
    return render_to_response('category.html', data)

def topicpage(request):
    
    data = {}
    
    try:
        topics = NewsCredTopic.search(access_key = 'c4bcc3f7c9bf9ec159f51da0a86ca658', query = 'barack obama')
    
        data['topic']           = topics[0]
        data['related_topics']  = topics[0].get_related_topics(
                                    options={'pagesize': 5, 'topic_classifications': ['Person'], 
                                             'topic_subclassifications': ['Politician', 'Lawyer']})
        
        data['related_articles'] = topics[0].get_related_articles(
                                    options={'media_types': ['Newspaper']})
        data['related_images']   = topics[0].get_related_images()
        data['related_videos']   = topics[0].get_related_videos({'pagesize' : 3})
        data['related_tweets']   = topics[0].get_related_tweets({'pagesize' : 5})
    
    except (NewsCredError), e:
        data['error'] = str(e)
    
    return render_to_response('topicpage.html', data)

def articlepage(request):
    
    data = {}
    
    try:
        articles         = NewsCredArticle.search(access_key=ACCESS_KEY, query='obama')
        related_articles = NewsCredArticle.search(access_key=ACCESS_KEY, query=articles[0].title)
        related_topics   = NewsCredTopic.extract(access_key=ACCESS_KEY, query=articles[0].title, options={'topic_filter_mode': 'blacklist'} )
        related_images   = articles[0].get_related_images()

        data['article']          = articles[0]
        data['related_topics']   = related_topics
        data['related_articles'] = related_articles
        data['related_images']   = articles[0].get_related_images()
        
    except (NewsCredError), e:
        data['error'] = str(e)

    return render_to_response('articlepage.html', data)

def extract(request):
    text = "'Whitewash' could slow global warming."+\
            " A Peruvian scientist has called on his country to help slow the melting of Andean glaciers by daubing white paint on the rock and earth left behind by receding ice so they will"+\
            " absorb less heat. Eduardo Gold, president of non-governmental organisation Glaciers of Peru, made the suggestion in a presentation Tuesday to the country's parliamentary commission"+\
            " on climate change. His idea has already attracted interest from the World Bank, and is among a series of projects to counter climate change that the organisation is considering,"+\
            " Gold told AFP."    
    query = request.GET.get('text', text)
    topics_mentioned = NewsCredTopic.extract(ACCESS_KEY, query, {'exact': True})
    topics_related   = NewsCredTopic.extract(ACCESS_KEY, query)
    
    return render_to_response('extract_topics.html', {'text': query, 'topics_mentioned': topics_mentioned, 'topics_related': topics_related})

def stories(request):
    data = {}
    data['haiti_stories'] = NewsCredArticle.search_stories(access_key=ACCESS_KEY, query='haiti', options={'cluster_size': 2})
    data['sport_stories'] = NewsCredCategory(access_key=ACCESS_KEY, name='sports').get_related_stories(options={'cluster_size': 2})
    data['federar_stories'] = NewsCredTopic(access_key=ACCESS_KEY, guid='49a8d8523c7d5b0c86504d37031ceea3').get_related_stories(options={'cluster_size': 2})
    
    return render_to_response('stories.html', data)