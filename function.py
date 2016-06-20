import urllib
import urllib2
import BeautifulSoup
import time

def getAllposts(nickname):
    # input : some nickname in tumblelog
    url = 'http://' + nickname + '.tumblr.com/archive'
    handle = urllib2.urlopen(url)
    data = handle.read()
    soup = BeautifulSoup.BeautifulSoup(data)
    months = ['1', '2', '3', '4', '5', '6']
    links = []
    posts = []

    for month in months:
        temp_url = url + '/2016/' + month
        links.append(temp_url)

    for link in links:
        hand = urllib2.urlopen(link)
        dat = hand.read()
        sop = BeautifulSoup.BeautifulSoup(dat)
        temp_post = sop.findAll('div', attrs={'class':'post_glass post_micro_glass_w_controls post_micro_glass'})
        for post in temp_post:
            posts.append(post.find('a')['href'])
    # output : All post list in some tumblelog
    return posts
                                                  
                                                  
def checkHarmfulinUniv(nickname):
    try:
        # input : some nickname in tumblelog
        url = 'http://' + nickname + '.tumblr.com'
        handle = urllib2.urlopen(url)
        data = handle.read()
        soup = BeautifulSoup.BeautifulSoup(data)
        link = soup.findAll('meta')[1]['content'].encode('utf-8')
        check = 'cleanweb1.uplus.co.kr' in link
        # output : harmful or not(TF)
        if check == True:
            return True
        else:
            return False
    except:
        return False
    

def checkHarmful1(nickname):
    try:
        url = 'http://' + nickname + '.tumblr.com'
        handle = urllib2.urlopen(url)
        data = handle.read()
        soup = BeautifulSoup.BeautifulSoup(data)
        source = soup.find('script').text
        link = ''
        i = 0
        start = 0
        end = 0
        while(True):
            if source[i] == '"' and start != 0:
                end = i
                link = source[start:end]
                break
            if source[i] == '"':
                start = i + 1
            i = i + 1

        if link == 'http://warning.or.kr':
            return True
        else:
            return False
    except:
        return False


def checkHarmful2(nickname):
    try:
        url = 'http://' + nickname + '.tumblr.com'
        handle = urllib2.urlopen(url)
        data = handle.read()
        soup = BeautifulSoup.BeautifulSoup(data)
        meta = str(soup.findAll('meta', attrs={'name': 'kcsc'}))
        kcsc = 'kcsc' in meta
        block = 'blocking' in meta
        if kcsc and block:
            return True
        else:
            return False
    except:
        return False
    
    
def getNotedict(posts):
    by_dict = {}
    for post in posts:
        url = urllib.quote(post.encode('utf8'), '/:')
        url = url + '#notes'
        handle = urllib2.urlopen(url)
        data = handle.read()
        soup = BeautifulSoup.BeautifulSoup(data)
        note = soup.findAll('a', attrs={'rel':'nofollow'})

        for user in note:
            temp = user.text.encode('utf-8')
            if len(temp)>0 and len(temp)<50:
                try:
                    by_dict[temp] += 1
                except:
                    by_dict.setdefault(temp, 1)
    # output : some dictionary
    return by_dict


def getReblogfrom(post):
    # input : a post url
    url = urllib.quote(post.encode('utf8'), '/:')
    url = url + '#notes'
    handle = urllib2.urlopen(url)
    data = handle.read()
    soup = BeautifulSoup.BeautifulSoup(data)
    output = soup.findAll('a', attrs={'class':'meta-item reblog-link'})
    # output : nickname in reblog source
    return output[0].text.encode('utf-8')


def checkEmpty(nickname):
    url = 'http://' + nickname + '.tumblr.com'
    try:
        url = urllib2.urlopen(url)
        return False
    except urllib2.HTTPError, e:
        # code = e.getcode()
        return True
    

def checkHarmful(nickname):
    check1 = checkHarmful1(nickname)
    check2 = checkHarmful2(nickname)
    check3 = checkHarmfulinUniv(nickname)
    return check1 or check2 or check3
