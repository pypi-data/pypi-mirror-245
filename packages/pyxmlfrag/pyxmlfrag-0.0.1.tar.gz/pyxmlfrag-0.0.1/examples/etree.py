import xml.etree.ElementTree as ET

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

with open("file.xml", "r") as f:
    et = ET.fromstring(f.read())
    for cxml in et.iter('customer'):
        cid = int(cxml.attrib["id"])
        all_customers[cid] = Customer(customerId = cid, name = cxml.find('name').text,
            accountCount = int(cxml.find('accountCount').text),
            totalBalance = float(cxml.find('totalBalance').text))
for k,v in all_customers.items():
    print("----")
    print("Customer id: %d" % (v.customerId,))
    print("Customer name: %s" % (v.name,))
    print("Customer account count: %d" % (v.accountCount,))
    print("Customer total balance: %.2f" % (v.totalBalance,))
    print("----")
