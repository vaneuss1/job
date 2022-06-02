import xml.etree.ElementTree as ET


def main(file_path):
    root = ET.parse(file_path)
    labels = root.find('meta').find('task').find('labels')

    #search all attrubutes#
    attributes = {}
    for label in labels:
        label_name = label.find('name').text
        attr_list = [attr.find('name').text for attr in label.find('attributes').findall('attribute')]
        list_of_tuple_att = zip(*[iter(attr_list)] * 2)
        attributes[label_name] = [attr_tuples for attr_tuples in list_of_tuple_att]

    #refactor meta labels#
    for label in labels.findall('label'):
        for atr in label.find('attributes'):
            for value in attributes.get(label.find('name').text):
                if atr.find('name').text == 'Дополнительная' or atr.find('name').text == 'Надпись':
                    atr.find('name').text = 'Тип'
                    atr.find('values').text = 'Логотип\nНадпись'
                    atr.find('default_value').text = 'Логотип'
                elif atr.find('name').text in value:
                    if atr.find('name').text in ('Зад', 'Перед', 'Лево', 'Право'):
                        val = '\n'.join(value) + '\nнет уточнения'
                        atr.find('values').text = val.lower()
                    else:
                        val = '\n'.join(value)
                        atr.find('values').text = val.lower()
                    atr.find('name').text = '/'.join(value).lower().capitalize()
                    atr.find('default_value').text = value[0].lower()

    #refactor attrubutes#
    for image in root.findall('image'):
        image_polygons = image.findall('polygon')
        for polygon in image_polygons:
            for i in list(polygon):
                if i.text == 'true':
                    i.text = i.attrib['name'].lower()
                    for j in attributes[polygon.attrib['label']]:
                        if i.text == 'надпись':
                            i.attrib['name'] = 'Тип'
                            i.text = 'Надпись'
                        elif i.text == 'логотип':
                            i.attrib['name'] = 'Тип'
                            i.text = 'Логотип'
                        elif i.attrib['name'] in j:
                            i.attrib['name'] = '/'.join(j)
                else:
                    polygon.remove(i)
            for attr in polygon.findall('attribute'):
                if attr.text == 'true':
                    attr.text = attr.attrib['name'].lower()
    #rewrite

    root.write(f"{file_path.split('.')[0]}+_new.xml", encoding='utf-8')

    #Delete dubles#
    for label in labels:
        atrs = label.find('attributes')
        atr_list = atrs.findall('attribute')
        visited = []
        for atr in atr_list:
            if atr.find('name').text in visited:
                atrs.remove(atr)
            else:
                visited.append(atr.find('name').text)

    root.write(f"{file_path.split('.')[0]}_new.xml", encoding='utf-8')


if __name__ == '__main__':
    file_path = r''
    main(file_path)