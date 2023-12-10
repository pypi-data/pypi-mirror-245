import xml.sax
import xml.etree.ElementTree as ET
import io
class XmlStack(object):
    def __init__(self):
        self.elements = []
    def push(self, elem):
        self.elements.append(elem)
    def pop(self, elem):
        assert self.elements[-1] == elem
        del self.elements[-1]
    def check(self, names):
        return self.elements == list(names)
class ConvertContentHandler(xml.sax.handler.ContentHandler):
    def __init__(self):
        super(ConvertContentHandler, self).__init__()
        self.fragment = None
        self.frags = []
        self.tail = None
        self.s = io.StringIO()
    def ready(self):
        return self.fragment is not None and len(self.frags) == 0
    def startElement(self, name, attrs):
        if len(self.frags) > 0:
            elem = ET.SubElement(self.frags[-1], name, dict(attrs))
        else:
            elem = ET.Element(name, dict(attrs))
        if self.fragment is None:
            self.fragment = elem
        if len(self.frags) > 0:
            if len(self.s.getvalue()) > 0:
                if self.tail is None:
                    self.frags[-1].text = self.s.getvalue()
                else:
                    self.tail.tail = self.s.getvalue()
            #self.frags[-1].append(elem) # not needed, automatic by SubElement
        self.s = io.StringIO()
        self.frags.append(elem)
        self.tail = None
    def endElement(self, name):
        if len(self.s.getvalue()) > 0:
            if self.tail is None:
                self.frags[-1].text = self.s.getvalue()
            else:
                self.tail.tail = self.s.getvalue()
            self.s = io.StringIO()
        self.tail = self.frags[-1]
        del self.frags[-1]
    def characters(self, content):
        self.s.write(content)
class XmlFragContentHandler(xml.sax.handler.ContentHandler):
    def __init__(self):
        super(XmlFragContentHandler, self).__init__()
        self.stack = XmlStack()
        self.h = None # ConvertContentHandler
        self.startXMLElementCallActive = False
    def startDocument(self):
        pass
    def endDocument(self):
        pass
    def startElement(self, name, attrs):
        self.stack.push(name)
        if self.h == None:
            self.startXMLElementCallActive = True
            try:
                self.startXMLElement(name, attrs)
            finally:
                self.startXMLElementCallActive = False
        # Note: h may have changed here
        if self.h != None:
            self.h.startElement(name, attrs)
    def endElement(self, name):
        df = None
        if self.h != None:
            self.h.endElement(name)
            if self.h.ready():
                df = self.h.fragment
                self.h = None
        # Note: h may have changed here
        if self.h == None:
            self.endXMLElement(name, df)
        self.stack.pop(name)
    def characters(self, content):
        if self.h != None:
            self.h.characters(content)
        else:
            self.xmlCharacters(content)
    def startXMLElement(self, name, attrs):
        pass
    def endXMLElement(self, name, df):
        pass
    def xmlCharacters(self, content):
        pass
    def startFragmentCollection(self):
        if not self.startXMLElementCallActive:
            raise Exception("can be called only within startXMLElement")
        if self.h != None:
            raise Exception("fragment collection already started")
        self.h = ConvertContentHandler()
    def check(self, names):
        return self.stack.check(names)
class WholeDocumentHandler(XmlFragContentHandler):
    def __init__(self):
        super(WholeDocumentHandler, self).__init__()
        self.f_global = None
    def startXMLElement(self, name, attrs):
        self.startFragmentCollection()
    def endXMLElement(self, name, f):
        if self.f_global != None:
            raise Exception("multiple endXMLElement calls, expected only one")
        self.f_global = f
def parseWhole(fileObject):
    whole = WholeDocumentHandler()
    p = xml.sax.make_parser()
    p.setContentHandler(whole)
    p.parse(fileObject)
    return whole.f_global
