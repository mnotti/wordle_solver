import site
import requests
from bs4 import BeautifulSoup
import random
import nltk
import json 
nltk.download('punkt')

from textblob import TextBlob

class WikiVisitor:
    def __init__(self, firstLink, depthLimit) -> None:
        self.letter_frequency = {}
        self.depthLimit = depthLimit
        self.checkpointIterationMod = 1000
        self.iterations = 1
        self.initFromCheckpoint()
        self.visitWikiPage(firstLink, 0)

    def initFromCheckpoint(self):
        self.wordFrequencyFile = 'word_frequency.json'
        self.sitesVisitedFile = 'sites_visited.json'

        try:
            f = open(self.wordFrequencyFile)
            wordFrequency = json.load(f)

            f2 = open(self.sitesVisitedFile)
            sitesVisited = json.load(f2)
        except: 
            print('failed to open jsons ... starting empty')
            wordFrequency = {}
            sitesVisited = {}
        
        self.words_frequency = wordFrequency
        self.visitedSites = sitesVisited
    
    def saveCheckpoint(self):
        # Serializing json  
        with open(self.wordFrequencyFile, "w") as outfile:
            json.dump(self.words_frequency, outfile)
        with open(self.sitesVisitedFile, "w") as outfile:
            json.dump(self.visitedSites, outfile)

        print(f'finished writing word_frequency w/ size: {len(self.words_frequency)}')
        print(f'finished writing visited sites w/ size: {len(self.visitedSites)}')

    # Returns total iterations so we can checkpoint after x iterations
    def visitWikiPage(self, link, depth):
        if depth > self.depthLimit:
            print("reached depth limit... backing off and starting to wind down")
            return
        
        print(f"visiting {link} w/ depth {depth}")
        self.visitedSites[link] = True

        try:
            response = requests.get(link)
        except:
            print(f'failed to get {link}')
            return
        
        soup = BeautifulSoup(response.content, 'html.parser')

        # Track the words
        try:
            for p in soup.find(id="bodyContent").find_all("p"):
                self.trackWords(p.get_text())
        except:
            print(f"failed to get track words for link {link}...")
            return
        
        # Find the next link
        if depth == self.depthLimit:
            return 
        try:
            allLinks = soup.find(id="bodyContent").find_all("a")
        except: 
            print(f"failed to find links on page {link}")
            return
        for linkElement in allLinks:
            # We are only interested in other wiki articles
            try:
                nextLink = f"https://en.wikipedia.org{linkElement['href']}"
            except:
                print(f'failed to get href of {linkElement}')
                return
            if nextLink.find(".svg") != -1 or nextLink.find(".png") != -1:
                print(f'link is image, skipping ... ({nextLink})')
            elif nextLink in self.visitedSites:
                print(f"already visited {nextLink} ... skipping")
            elif nextLink.find("/wiki/") == -1:
                print(f"{nextLink} not a wiki page ... skipping")
            else:
                self.visitWikiPage(nextLink, depth+1)
                
    def trackWords(self, blob): 
        allWords = TextBlob(blob).words
        for w in allWords:
            lowered = w.lower()
            if len(lowered) != 5:
                continue
            if not isAllLetters(lowered):
                continue
            if lowered in self.words_frequency:
                self.words_frequency[lowered] = self.words_frequency[lowered] + 1
            else:
                self.words_frequency[lowered] = 1
        self.iterations += 1
        if self.iterations % self.checkpointIterationMod == 0:
            print(f'saving checkpoint for iteration {self.iterations}') 
            self.saveCheckpoint()

def isAllLetters(value):
    for character in value:
        if not character.isalpha():
            return False
    return True

# ("https://en.wikipedia.org/wiki/Philosophy", 1)
# ("https://en.wikipedia.org/wiki/Web_scraping", 1)
# ("https://en.wikipedia.org/wiki/Astronomy", 1)
# ("https://en.wikipedia.org/wiki/Economics", 3)
# starting: 
#   finished writing word_frequency w/ size: 5120
#   finished writing visited sites w/ size: 752

wv = WikiVisitor("https://en.wikipedia.org/wiki/Economics", 3)
wv.saveCheckpoint()