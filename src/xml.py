 1/1: %save xmltojson.log
 1/2: a = 5
 1/3: %save xmltojson.log
 1/4: %save x
 1/5: %save -f
 1/6: %save -f x.log
 1/7: %save -f x.log 0
 1/8: %save -f x.log 15
 1/9: %save -f x.log 1-15
 2/1: from pathlib import Path
 2/2: import json
 2/3: import xmljson
 2/4: sourceDir = Path("/home/sam/LexisNexisCorpus/104440/")
 2/5: files = [f for f in sourceDir.iterdir() if f.is_file()]
 2/6: files
 2/7: import re
 2/8: courtCaseRegex = "<courtCaseDoc.*/courtCaseDoc>"
 2/9:
for file in files[:10]: 
    with file.open() as infile: 
        for m in re.finditer(infile.read(), courtCaseRegex):
            print(m)
2/10:
for file in files[:10]: 
    with file.open() as infile: 
        for m in re.finditer(courtCaseRegex, infile.read()):
            print(m)
2/11: allConverters = [("Abdera", xmljson.Abdera()),("BadgerFish",xmljson.BadgerFish()),("Cobra", xmljson.Cobra()),("gdata",xmljson.GData()),("Parker",xmljson.Parker()),("Yahoo",xmljson.Yahoo())]
2/12:
for file in files[:10]: 
    with file.open() as infile: 
        for m in re.finditer(courtCaseRegex, infile.read()):
            print(m.string)
2/13: outDir = Path("/home/sam/LexisNexisCorpus/104440_json/")
2/14: pathToOutFile = outDir / "test.txt"
2/15:
with pathToOutFile.open('w') as outfile: 
    outfile.write("test")
2/16:
for file in files[:2]: 
    with file.open() as infile: 
        for m in re.finditer(courtCaseRegex, infile.read()):
            for cname, converter in allConverters: 
                pathToOutFile = outDir / "_".join(cname, file.name()) + ".json"
2/17:
for file in files[:2]: 
    with file.open() as infile: 
        for m in re.finditer(courtCaseRegex, infile.read()):
            for cname, converter in allConverters: 
                pathToOutFile = outDir / "_".join(cname, file.name()) + ".json"
2/18:
for file in files[:2]: 
    with file.open() as infile: 
        for m in re.finditer(courtCaseRegex, infile.read()):
            for cname, converter in allConverters: 
                pathToOutFile = outDir / "_".join(cname, file.name()) + ".json"
2/19:
for file in files[:2]: 
    with file.open() as infile: 
        for m in re.finditer(courtCaseRegex, infile.read()):
            for cname, converter in allConverters: 
                pathToOutFile = outDir / "_".join(cname, file.name) + ".json"
2/20:
for file in files[:2]: 
    with file.open() as infile: 
        for m in re.finditer(courtCaseRegex, infile.read()):
            for cname, converter in allConverters: 
                pathToOutFile = outDir / "_".join((cname, file.name)) + ".json"
2/21:
for file in files[:2]: 
    with file.open() as infile: 
        for m in re.finditer(courtCaseRegex, infile.read()):
            for cname, converter in allConverters: 
                pathToOutFile = outDir /( "_".join((cname, file.name)) + ".json")
2/22: from xml.etree.ElementTree import fromstring
2/23:
for file in files[:2]: 
    with file.open() as infile: 
        for m in re.finditer(courtCaseRegex, infile.read()):
            for cname, converter in allConverters: 
                pathToOutFile = outDir /( "_".join((cname, file.name)) + ".json")
                with pathToOutFile.open('w') as outfile: 
                    outfile.write(json.dumps(converter.data(fromstring(m.string))))
2/24:
for file in files[:2]: 
    with file.open() as infile: 
        for m in re.finditer(courtCaseRegex, infile.read()):
            for cname, converter in allConverters: 
                pathToOutFile = outDir /( "_".join((cname, file.name)) + ".json")
                with pathToOutFile.open('w') as outfile: 
                    xml = fromstring(m.string)
                    print(xml)
2/25:
for file in files[:2]: 
    with file.open() as infile: 
        for m in re.finditer(courtCaseRegex, infile.read()):
            for cname, converter in allConverters: 
                pathToOutFile = outDir /( "_".join((cname, file.name)) + ".json")
                with pathToOutFile.open('w') as outfile: 
                    print(m.string)
                    xml = fromstring(m.string)
                    print(xml)
2/26: courtCaseRegex = "<courtCaseDoc.*?/courtCaseDoc>"
2/27:
for file in files[:2]: 
    with file.open() as infile: 
        for m in re.match(courtCaseRegex, infile.read()): 
            print(m.string)
2/28:
for file in files[:2]: 
    with file.open() as infile: 
        print(infile.read())
        for m in re.match(courtCaseRegex, infile.read()): 
            print(m.string)
2/29:
for file in files[:2]: 
    with file.open() as infile: 
        print(infile.read())
        for m in re.finditer(courtCaseRegex, infile.read()): 
            print(m.string)
2/30:
for file in files[:2]: 
    with file.open() as infile: 
        print(infile.read())
        for m in re.findall(courtCaseRegex, infile.read()): 
            print(m)
2/31:
for file in files[:2]: 
    with file.open() as infile: 
        print(infile.read())
        a = re.findall(courtCaseRegex, infile.read())
        for m in re.findall(courtCaseRegex, infile.read()): 
            print(m)
2/32: a
2/33:
for file in files[:2]: 
    with file.open() as infile:
        text = infile.read()
        a = re.findall(courtCaseRegex, text)
        for m in re.findall(courtCaseRegex, text): 
            print(m)
2/34: a
2/35: len(a)
2/36: a[0]
2/37:
for file in files[:2]: 
    with file.open() as infile:
        text = infile.read() 
        for m in re.findall(courtCaseRegex,text):
            for cname, converter in allConverters: 
                pathToOutFile = outDir /( "_".join((cname, file.name)) + ".json")
                with pathToOutFile.open('w') as outfile: 
                    print(m.string)
                    xml = fromstring(m.string)
                    print(xml)
2/38:
for file in files[:2]: 
    with file.open() as infile:
        text = infile.read() 
        for m in re.findall(courtCaseRegex,text):
            for cname, converter in allConverters: 
                pathToOutFile = outDir /( "_".join((cname, file.name)) + ".json")
                with pathToOutFile.open('w') as outfile: 
                    xml = fromstring(m)
                    print(xml)
2/39:
for file in files[:2]: 
    with file.open() as infile:
        text = infile.read() 
        for m in re.findall(courtCaseRegex,text):
            for cname, converter in allConverters: 
                pathToOutFile = outDir /( "_".join((cname, file.name)) + ".json")
                with pathToOutFile.open('w') as outfile: 
                    xml = fromstring(m)
                    json.dump(outfile, converter.data(xml))
2/40:
for file in files[:2]: 
    with file.open() as infile:
        text = infile.read() 
        for m in re.findall(courtCaseRegex,text):
            for cname, converter in allConverters: 
                pathToOutFile = outDir /( "_".join((cname, file.name)) + ".json")
                with pathToOutFile.open('w') as outfile: 
                    xml = fromstring(m)
                    outfile.write(json.dumps(converter.data(xml)))
2/41:
for file in files[:2]: 
    with file.open() as infile:
        text = infile.read() 
        for m in re.findall(courtCaseRegex,text):
            for cname, converter in allConverters: 
                pathToOutFile = outDir /( "_".join((cname, file.name)) + ".json")
                with pathToOutFile.open('w') as outfile: 
                    xml = fromstring(m)
                    outfile.write(json.dumps(converter.data(xml)), indent=1)
2/42:
for file in files[:2]: 
    with file.open() as infile:
        text = infile.read() 
        for m in re.findall(courtCaseRegex,text):
            for cname, converter in allConverters: 
                pathToOutFile = outDir /( "_".join((cname, file.name)) + ".json")
                with pathToOutFile.open('w') as outfile: 
                    xml = fromstring(m)
                    outfile.write(json.dumps(converter.data(xml), indent=1))
2/43: %history xmltojson
2/44: %history xmltojson.log
   1: %history -g -f xml.py
