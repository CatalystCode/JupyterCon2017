###########################################################################################
# Keyphrase extractor example for experimentation
# Supports algoriths: RAKE, topic rank, single rank, TFIDF and KPMINER
# For more info about RAKE algorithm and implmentation, see https://github.com/aneesha/RAKE
# Note: A copy of rake.py and SmartStoplist.txt stopwords list is included with this script
# For more info about the PKE implementations, see https://github.com/boudinfl/pke
# Note: Install PKE from the GitHub repo https://github.com/boudinfl/pke
###########################################################################################

# Import base packages
from bs4 import BeautifulSoup
import os, glob, sys, re
from rake import *
import pke


# Strip non-ascii characters that break the overlap check
def strip_non_ascii(s):
    s = (c for c in s if 0 < ord(c) < 255)
    s = ''.join(s)
    return s

# Clean text: remove newlines, compact spaces, strip non_ascii, etc.
def clean_text(text, lowercase=False, nopunct=False):
    # Convert to lowercase
    if lowercase:
        text = text.lower()

    # Remove punctuation
    if nopunct:
        puncts = string.punctuation
        for c in puncts:
            text = text.replace(c, ' ')

    # Strip non-ascii characters
    text = strip_non_ascii(text)
    
    # Remove newlines - Compact and strip whitespaces
    text = re.sub('[\r\n]+', ' ', text)
    text = re.sub('\s+', ' ', text)
    return text.strip()

# Extract keyphrases using RAKE algorithm. Limit results by minimum score.
def get_keyphrases_rake(infile, stoplist_path=None, min_score=0):
    if stoplist_path == None:
        stoplist_path = 'SmartStoplist.txt'

    rake = Rake(stoplist_path)
    text = open(infile, 'r').read()
    keywords = rake.run(text)
    phrases = []
    for keyword in keywords:
        score = keyword[1]
        if score >= min_score:
            phrases.append(keyword)

    return phrases

def get_keyphrases_pke(infile, mode='topic', stoplist_path=None, postags=None, ntop=100):
    if stoplist_path == None:
        stoplist_path = 'SmartStoplist.txt'
    stoplist = [open(stoplist_path, 'r').read()]

    if postags == None:
        postags = ['NN', 'NNS', 'NNP', 'NNPS', 'JJ', 'JJR', 'JJS', 'VBN', 'VBD']

    # Run keyphrase extractor - Topic_Rank unsupervised method
    if mode == 'topic':
        try:
            extractor = pke.TopicRank(input_file=infile, language='english')
            extractor.read_document(format='raw', stemmer=None)
            extractor.candidate_selection(stoplist=stoplist, pos=postags)
            extractor.candidate_weighting(threshold=0.25, method='average')
            phrases = extractor.get_n_best(300, redundancy_removal=True)
        except:
            phrases = []

    # Run keyphrase extractor - Single_Rank unsupervised method
    elif mode == 'single':
        try:
            extractor = pke.SingleRank(input_file=infile, language='english')
            extractor.read_document(format='raw', stemmer=None)
            extractor.candidate_selection(stoplist=stoplist)
            extractor.candidate_weighting(normalized=True)
        except:
            phrases = []

    # Run keyphrase extractor - TfIdf unsupervised method
    elif mode == 'tfidf':
        try:
            extractor= pke.TfIdf(input_file=infile, language='english')
            extractor.read_document(format='raw', stemmer=None)
            extractor.candidate_selection(stoplist=stoplist)
            extractor.candidate_weighting()
        except:
            phrases = []

    # Run keyphrase extractor - KP_Miner unsupervised method
    elif mode == 'kpminer':
        try:
            extractor = pke.KPMiner(input_file=infile, language='english')
            extractor.read_document(format='raw', stemmer=None)
            extractor.candidate_selection(stoplist=stoplist)
            extractor.candidate_weighting()
        except:
            phrases = []

    else:   # invalid mode
        print "Invalid keyphrase extraction algorithm: %s" % mode
        print "Valid PKE algorithms: [topic, single, kpminer, tfidf]"
        exit(1)

    phrases = extractor.get_n_best(ntop, redundancy_removal=True)
    return phrases

def usage():
    print('Usage %s filename [algo]' % os.path.basename(sys.argv[0]))
    print('Algo options: rake, topic, single, tfidf, kpminer')


##############################
# Main processing
##############################

if len(sys.argv) < 2:
    print('Missing content file name')
    usage()
    exit(1)

infile = sys.argv[1]
if len(sys.argv) >= 3:
    algo = sys.argv[2]
    if algo not in ['rake', 'topic', 'single', 'tfidf', 'kpminer']:
        print "Invalid keyphrase extraction algorithm: %s" % algo
        usage()
        exit(1)
else:
    algo = 'rake'

# Read custom stopwords list from file - Applies to all algos
# If no stopwords file is supplied, default uses SmartStoplist.txt
stoplist_file = 'SmartStoplist_extended.txt'

# Select POS tags to use for PKE candidate selection, use default if None
postags = ['NN', 'NNS', 'NNP', 'NNPS', 'JJ', 'JJR', 'JJS', 'VBN', 'VBD']

# Run keyphrase extraction
if algo == 'rake':
    min_score = 1
    phrases = get_keyphrases_rake(infile, stoplist_path=stoplist_file, min_score=min_score)
else:
    ntop = 200
    phrases = get_keyphrases_pke(infile, mode=algo, stoplist_path=stoplist_file, postags=postags, ntop=ntop)

# Report all keyphrases and their scores
print 'Number of extracted keyphrases = %d' % len(phrases)
for phrase in phrases:
    print phrase

# Combined list of keyphrases (no scores)
all_phrases = ', '.join(p[0] for p in phrases)
print('\nKeyphrases list: %s' % all_phrases)
