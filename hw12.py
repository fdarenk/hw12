import urllib.request as ur, re

def get_sets(links):
    set0 = get_set(read(get_html(links[0], 'utf-8'), '</strong>(.*?)<div class', 1))
    set1 = get_set(read(get_html(links[1], 'utf-8'), '<!-- anonsens 300 250 -->(.*?)</script>(.*?)<small style', 2))
    set2 = get_set(read(get_html(links[2], 'utf-8'), '\"headline description articleBody\">(.*?)<br clear=', 1))
    set3 = get_set(read(get_html(links[3], 'windows-1251'), '<!--детальный текст-->(.*?)<!--/детальный текст-->', 1))
    return set0, set1, set2, set3

def get_html(url, code):
    page = ur.urlopen(url)
    text = page.read().decode(code)
    return(text)

def read(text, reg, n):
    res = re.search(reg, text, flags=re.DOTALL)
    if res:
        article = res.group(n)
    regTag = re.compile('<.*?>', flags=re.U | re.DOTALL)
    article = regTag.sub("", article)
    return article

def get_set(text):
    words = text.split()
    ww = []
    for word in words:
        word = word.strip('.,!?«»()')
        if word != '–':
            ww.append(word.lower())
    return set(ww)

def main(links):
    sets = get_sets(links)
    common = sets[0] & sets[1] & sets[2] & sets[3]
    unique = sets[0].symmetric_difference(sets[1])
    unique = unique.symmetric_difference(sets[2])
    unique = unique.symmetric_difference(sets[3])
    write(common, 'common.txt')
    write(unique, 'unique.txt')

def write(s, path):
    array = list(s)
    array.sort()
    file = open(path, 'w', encoding='utf-8')
    for el in array:
        file.write(el + '\n')
    file.close()

if __name__ == '__main__':
    main(['http://planet-today.ru/novosti/nauka/item/58559-uchenye-sozdali-na-osnove-zolota-samyj-chernyj-material', 'http://anonsens.ru/9061_uchenye_sozdali_na_osnove_zolota_samyj_chernyj_material_alesya917', 'http://www.rzn.info/news/2016/12/4/uchenye-sozdali-na-osnove-zolota-samyy-chernyy-material.html', 'http://www.innov.ru/news/it/na-osnove-zolota-sozdan-s/'])
