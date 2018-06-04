from bs4 import BeautifulSoup

xml_path = 'G:/DataSet/TCIA_LIDC-IDRI/LIDC-IDRI/LIDC-IDRI-0001/1.3.6.1.4.1.14519.5.2.1.6279.6001.298806137288633453246975630178/1.3.6.1.4.1.14519.5.2.1.6279.6001.179049373636438705059720603192/069.xml'
# xml_path = 'e:/Python/VectorGeneratingNetwork/Projects/LIDCReader/example.xml'
with open(xml_path, 'r') as xml_file:
        markup = xml_file.read()
xml = BeautifulSoup(markup, features="xml")

patient_id = xml.LidcReadMessage.ResponseHeader.SeriesInstanceUid.text
print("===>Patient id="+patient_id)
reading_sessions = xml.LidcReadMessage.find_all("readingSession")

for reading_session in reading_sessions:
    nodules = reading_session.find_all("unblindedReadNodule")
    for nodule in nodules:
        nodule_id = nodule.noduleID.text
        print("====>nodule_id:"+nodule_id)
        nonNoduleID=nodule.nonNoduleID.text
        print("======>nonNoduleID:"+nodule_id)
rois = nodule.find_all("roi")

