import string
import time

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO


def get_pdf_text(path):
    """ Reads a pdf file and returns a dict of the text where the
        index represents the page number.
        http://stackoverflow.com/a/20905381
    """
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    # change to to utf-8 if the text comes out garbled
    codec = 'ascii'
    #codec = 'utf-8'
    laparams = LAParams()
    pages = {}
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams, showpageno=True, pages=pages)
    fp = file(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching, check_extractable=True):
        interpreter.process_page(page)
    fp.close()
    device.close()
    retstr.close()
    return pages

def find_whole_word(needle, haystack, case_sensitive = False):
    """ Searches text for a whole word match. Ignores whitespace and punctuation.
        Example: find_whole_word('test', 'This is a test; This is also a tester')
        matches 'test;' but not 'tester'
        http://stackoverflow.com/a/4155029
    """
    if case_sensitive:
        index = haystack.find(needle)
    else:
        index = haystack.lower().find(needle.lower())
    if index == -1:
        return False
    if index != 0 and haystack[index-1].isalnum():
        return False
    L = index + len(needle)
    if L < len(haystack) and haystack[L].isalnum():
        return False
    return True

def create_index(pdf_path, word_list):
    """ Create a word index from pdf file
    """
    text_data = get_pdf_text(pdf_path)
    word_index = {}
    for page in text_data:
        for word in words_list:
            if find_whole_word(word, text_data[page]):
                if word in word_index:
                    word_index[word].append(page)
                else:
                    word_index[word] = [page]
    return word_index

words_list = ['this', 'This', 'foobard']
start = time.clock()
index = create_index("mature-optimization.pdf", words_list)
for word in index:
    print "%s: %s \n" % (word, index[word])
end = time.clock()

print "Finished in %f seconds" % (end - start)