# -*- coding: UTF-8 -*-

'''
Created on 20/05/2011

@author: ThiagoP
'''
from urllib2 import urlopen, unquote
from re import sub
from objects import ScrapeVacancy

def cut(src, pattern, include, first_last, begin_end):
    """
        Function used to cut the source string into a specified substring
        
        Parameters:
        - src : String to cut
        - pattern : Substring to search for
        - include : "yes" to include pattern into the string returned, "no" to cut it off  
        - first_last : "first" to search for the first occurrence of 'pattern', "last" to search the last occurrence
        - begin_end : "begin" to cut from the pattern to the beginning of 'src', "end" to cut from 'pattern' to the end of 'src'
    """
    
    if pattern in src:
        # first occurrence of 'pattern'
        if first_last ==  "first":
            
            # cuts from begin to end
            if begin_end == "end":
                
                # include 'pattern' into the returned string 
                if include == "yes":
                    src = src[src.find(pattern):]
                elif include == "no":
                    src = src[src.find(pattern) + len(pattern):]
                    
            # cuts from end to begin
            elif begin_end == "begin":
                
                # include 'pattern' into the returned string 
                if include == "yes":
                    src = src[:src.find(pattern) + len(pattern)]
                elif include == "no":
                    src = src[:src.find(pattern)]
                        
        # last occurrence
        elif first_last == "last":
            
            # cuts from begin to end
            if begin_end == "end":
                
                # include 'pattern' into the returned string 
                if include == "yes":
                    src = src[src.rfind(pattern):]
                elif include == "no":
                    src = src[src.rfind(pattern) + len(pattern):]
                    
            # cuts from end to begin
            elif begin_end == "begin":
                
                # include 'pattern' into the returned string 
                if include == "yes":
                    src = src[:src.rfind(pattern) + len(pattern)]
                elif include == "no":
                    src = src[:src.rfind(pattern)]
    
    src = src.strip()
    
    # returns
    return src


def get_url(url, data=None):
    """
        Function used to retrieve the html content from a given 'url'
        
        Parameters:
        - url : URL from the requested site
        - data (optional) : Content to pass as a HTML POST request.
    """
    
    if data == None:
        response = urlopen(url)
        html = response.read()
    else:
        response = urlopen(url, data)
        html = response.read()
        
    return html

def normalize(text):
    """
        Function remove htmlentities from the string
    """
    htmlCodes = (
        (' ', '&nbsp;'),         
        ('&', '&amp;'),
        ('<', '&lt;'),
        ('>', '&gt;'),
        ('"', '&quot;'),
        ("'", '&#39;'),
    )
    
    text = unquote(text)
    
    for c in htmlCodes:
        text = text.replace(c[1], c[0])

    text = text.replace("\\", "\\\\")
    text = text.replace("\"", "\\\"")
    text = text.replace('\'', '\\\'')
    
    return text 


def sanitize(html):
    """
        Function to replace BR tags for \\n and remove all the other tags from the string
    """
    html = sub('<[bB][rR]/?>', '\n', html)
    html = sub('<[^<]+?>', '', html)
    
    html = html.strip()
    
    return html


def checkScrapeVacancy(ref, script):
    sv = ScrapeVacancy.get(sv_ref = ref, sv_script = script)
    
    if len(sv) > 0:
        ret = True
    else:
        ret = False
        
    return ret

def checkExcludes(location):
    ret = False
    
    arq = open("Exclusion.txt", "r")
    excludes = arq.readlines()
    arq.close()
    
    exclusions = [ex.lower().strip() for ex in excludes]
    
    for i in exclusions:
        if i in location.lower():
            ret = True
            break
        
    return ret


def toScreen(text):
    print text
    
    
def toLog(text):
    arq = open('run.log', 'a')
    arq.write(text + '\n')
    arq.close()
    
    
def toLimbo(args):
    pass
    
    
        
        
        
        