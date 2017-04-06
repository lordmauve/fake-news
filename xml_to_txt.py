from xml.etree.ElementTree import parse

with open('newsspace_titles.txt', 'w', encoding='utf8') as out:
    doc = parse(open('newsspace200.xml'))
    for e in doc.getroot():
        if e.tag == 'title':
            print(e.text, file=out)
