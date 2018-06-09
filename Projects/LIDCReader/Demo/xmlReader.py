from bs4 import BeautifulSoup

xml_path = 'F:/TCIA_LIDC-IDRI/LIDC-IDRI/LIDC-IDRI-0001/1.3.6.1.4.1.14519.5.2.1.6279.6001.298806137288633453246975630178/1.3.6.1.4.1.14519.5.2.1.6279.6001.179049373636438705059720603192/069.xml'

with open(xml_path, 'r') as xml_file:
        markup = xml_file.read()
xml = BeautifulSoup(markup, features="xml")
"header msg"
SeriesInstanceUID = xml.LidcReadMessage.ResponseHeader.SeriesInstanceUid.text
print("===>Series Instance UID=" + SeriesInstanceUID)
StudyInstanceUID = xml.LidcReadMessage.ResponseHeader.StudyInstanceUID.text
print("===>Study Instance UID=" + SeriesInstanceUID)

"找到所有的readingSession,理论上应有1~4个"
reading_sessions = xml.LidcReadMessage.find_all("readingSession")
"迭代readingSession"
for reading_session in reading_sessions:
    DoctorID = reading_session.servicingRadiologistID.text
    print ("Doctor :"+str(DoctorID))
    subtlety = reading_session.subtlety.text
    internalStructure= reading_session.internalStructure.text
    calcification= reading_session.calcification.text
    sphericity= reading_session.sphericity.text
    margin= reading_session.margin.text
    lobulation= reading_session.lobulation.text
    spiculation= reading_session.spiculation.text
    texture= reading_session.texture.text
    malignancy= reading_session.malignancy.text
    print("subtlety:" + subtlety)
    print("internalStructure:" + internalStructure)
    print("calcification:" + calcification)
    print("sphericity:" + sphericity)
    print("margin:" + margin)
    print("lobulation:" + lobulation)
    print("spiculation:" + spiculation)
    print("texture:" + texture)
    print("malignancy:" + malignancy)

    unblindedReadNodules = reading_session.find_all("unblindedReadNodule")
    print("unblindedReadNodules数量:"+str(len(unblindedReadNodules)))

    for nodule in unblindedReadNodules:
        nodule_id = nodule.noduleID.text
        print("====>nodule_id:"+nodule_id)
        rois = nodule.find_all("roi")

    nonNodules = reading_session.find_all("nonNodules")
    print("nonNodules:" + str(len(nonNodules)))
    for nodule in nonNodules:
        nodule_id = nodule.nonNoduleID.text
        print("====>nonNoduleID:" + nodule_id)
    print("************************************************************************")


