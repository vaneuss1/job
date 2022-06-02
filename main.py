import xml.etree.ElementTree as ET
from tqdm import tqdm


def search_atr(file_path):
    xml_file = ET.parse(file_path)
    labels = xml_file.find('meta').find('task').find('labels')
    attributes = {}
    for label in labels:
        label_name = label.find('name').text
        attr_list = [attr.find('name').text for attr in label.find('attributes').findall('attribute')]
        list_of_tuple_att = zip(*[iter(attr_list)] * 2)
        attributes[label_name] = [attr_tuples for attr_tuples in list_of_tuple_att]
    return attributes


def refactor_meta(file_path, attributes):
    xml_file = ET.parse(file_path)
    labels = xml_file.find('meta').find('task').find('labels')
    for label in tqdm(labels.findall('label')):
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

    xml_file.write(f"{file_path.split('.')[0]}_new.xml", encoding='utf-8')
    new_file = f"{file_path.split('.')[0]}_new.xml"
    return new_file


def refactor_attr(n_path):
    xml_file = ET.parse(n_path)
    for image in tqdm(xml_file.findall('image')):
        image_polygons = image.findall('polygon')
        for polygon in image_polygons:
            for i in polygon.findall('attribute'):
                text = i.text.strip()
                if text == 'true':
                    i.text = f"{i.attrib['name']}".lower()
                    for j in attributes[polygon.attrib['label']]:
                        if i.text == 'надпись':
                            i.attrib['name'] = 'Тип'
                            i.text = 'Надпись'
                        elif i.text == 'логотип':
                            i.attrib['name'] = 'Тип'
                            i.text = 'Логотип'
                        elif i.attrib['name'] in j:
                            i.attrib['name'] = '/'.join(j)
                elif text == 'false':
                    polygon.remove(i)
    xml_file.write(n_path, encoding='utf-8')
    new_file = n_path
    return new_file


def delete_dubles(n_path):
    xml_file = ET.parse(n_path)
    labels = xml_file.find('meta').find('task').find('labels')
    for label in tqdm(labels):
        atrs = label.find('attributes')
        atr_list = atrs.findall('attribute')
        visited = []
        for atr in atr_list:
            if atr.find('name').text in visited:
                atrs.remove(atr)
            else:
                visited.append(atr.find('name').text)
    xml_file.write(n_path, encoding='utf-8')
    new_file = n_path
    return new_file


def short_name(n_path):
    xml_file = ET.parse(n_path)
    images = xml_file.findall('image')
    for img in tqdm(images):
        img.attrib['name'] = img.attrib['name'].split('/')[-1]
    xml_file.write(n_path, encoding='utf-8')

if __name__ == '__main__':
    path = r''
    attributes = search_atr(path)
    n_p = refactor_meta(path, attributes)
    n_p = refactor_attr(n_p)
    n_p = delete_dubles(n_p)
    short_name(n_p)
