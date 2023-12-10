import xml.sax
import io

class Customer(object):
    def __init__(self, customerId = None, name = None, accountCount = None, totalBalance = None):
        if customerId is not None:
            self.customerId = int(customerId)
        else:
            self.customerId = None
        self.name = name
        if accountCount is not None:
            self.accountCount = int(accountCount)
        else:
            self.accountCount = None
        if totalBalance is not None:
            self.totalBalance = float(totalBalance)
        else:
            self.totalBalance = None

all_customers = {}

class SaxExample(xml.sax.handler.ContentHandler):
    def __init__(self):
        super(SaxExample, self).__init__()
        self.txt = io.StringIO()
        self.customer = None
    def startElement(self, name, attrs):
        attrs = dict(attrs)
        self.txt = io.StringIO()
        if name == "customer":
            self.customer = Customer(customerId = int(attrs["id"]))
            all_customers[self.customer.customerId] = self.customer
    def characters(self, content):
        self.txt.write(content)
    def endElement(self, name):
        if name == "name":
            self.customer.name = self.txt.getvalue()
        if name == "accountCount":
            self.customer.accountCount = int(self.txt.getvalue())
        if name == "totalBalance":
            self.customer.totalBalance = float(self.txt.getvalue())

with open("file.xml", "r") as f:
    p = xml.sax.make_parser()
    handler = SaxExample()
    p.setContentHandler(handler)
    p.parse(f)
for k,v in all_customers.items():
    print("----")
    print("Customer id: %d" % (v.customerId,))
    print("Customer name: %s" % (v.name,))
    print("Customer account count: %d" % (v.accountCount,))
    print("Customer total balance: %.2f" % (v.totalBalance,))
    print("----")
