# PyXMLFrag: a powerful combined tree-based and event-based parser for XML

Typically, XML is either parsed by a tree-based parser or by an event-based parser. Event-based parsers are fast and have a low memory footprint, but a drawback is that it is cumbersome to write the required event handlers. Tree-based parsers make the code easier to write, to understand and to maintain but have a large memory footprint as a drawback. Often, XML is used for huge files such as database dumps that necessitate event-based parsing, or so it would appear at a glance, because a tree-based parser cannot hold the whole parse tree in memory at the same time.

## Example application: customers in a major bank

Let us consider an example application: a listing of a customers in a major bank that has 30 million customers. The test file is in the following format:

```
<allCustomers>
  <customer id="1">
    <name>Clark Henson</name>
    <accountCount>1</accountCount>
    <totalBalance>5085.96</totalBalance>
  </customer>
  <customer id="2">
    <name>Elnora Ericson</name>
    <accountCount>3</accountCount>
    <totalBalance>3910.11</totalBalance>
  </customer>
  ...
</allCustomers>
```

The example format requires about 130 bytes per customer plus customer name length. If we assume an average customer name is 15 characters long, the required storage is about 145 bytes per customer. For 30 million customers, this is 4 gigabytes. In the example, the file is read to the following structure:

```
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
```

## Parser with SAX

A SAX-based parser is implemented here:

```
import xml.sax
import io

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
```

It can be seen that the parser is quite cumbersome and the code to construct a customer is scattered to two different places. Yet it is fast and has a low memory footprint.

## Parse with ElementTree

Here is a parser implemented with ElementTree:

```
import xml.etree.ElementTree as ET

all_customers = {}

with open("file.xml", "r") as f:
    et = ET.fromstring(f.read())
    for cxml in et.iter('customer'):
        cid = int(cxml.attrib["id"])
        all_customers[cid] = Customer(customerId = cid, name = cxml.find('name').text,
            accountCount = int(cxml.find('accountCount').text),
            totalBalance = float(cxml.find('totalBalance').text))
```

The ElementTree-based parser is more satisfactory: it has the code to construct a customer object in only one place. Yet it is still a bit more complex than we would like to have. Additionally, the memory consumption of the ElementTree parser is too high to read the whole 4 gigabyte test file on most computers.

## Parser with the new library

What if we could combine the benefits of the SAX-based approach with the benefits of the ElementTree-based approach? A parse tree fragment for a single <customer> element is small enough to be kept in memory. This is what the new library is about. Here is the code to parse the customer file with the new library:

```
import pyxmlfrag

all_customers = {}

class MyExample(pyxmlfrag.XmlFragContentHandler):
    def startXMLElement(self, name, attrs):
        if self.check(["allCustomers", "customer"]):
            self.startFragmentCollection()
    def endXMLElement(self, name, df):
        if self.check(["allCustomers", "customer"]):
            cid = int(df.attrib["id"])
            all_customers[cid] = Customer(customerId = cid, name = df.find("name").text,
                accountCount = int(df.find("accountCount").text),
                totalBalance = float(df.find("totalBalance").text))
with open("file.xml", "r") as f:
    p = xml.sax.make_parser()
    handler = MyExample()
    p.setContentHandler(handler)
    p.parse(f)
```

Note how the code is significantly more simple than for the SAX-based approach. Performance is close to the SAX-based approach, and memory consumption is essentially the same as for SAX.

## License

All of the material related to PyXMLFrag is licensed under the following MIT license:

Copyright (C) 2023 Juha-Matti Tilli

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

