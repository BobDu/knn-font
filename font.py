import requests
import re
from fontTools.ttLib import TTFont


def get_font_content():
    url = 'https://maoyan.com/board/1'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    font_url = 'http:' + re.findall(r"url\('(.*?\.woff)'\)", response.text)[0]
    print(font_url)
    return requests.get(font_url).content


def save_font():
    for i in range(10, 15):
        font_content = get_font_content()
        with open(f'./fonts/{i+1}.woff', 'wb') as f:
            f.write(font_content)
        print(f'./fonts/{i+1}.woff')


def get_coor_info(font, cli):
    # print(font.getGlyphOrder())
    # ['glyph00000', 'x', 'uniE083', 'uniF521', 'uniE40C', 'uniE60B', 'uniF352', 'uniEB37', 'uniF6CA', 'uniE064', 'uniF5A1', 'uniF1E9']
    # font.getGlyphOrder() 获取到的列表 是以 post -> extraNames -> psName 的顺序来排列的
    glyf_order = font.getGlyphOrder()[2:]
    info = list()
    for i, g in enumerate(glyf_order):
        # print(i, g)
        # 0 uniE083
        coors = font['glyf'][g].coordinates
        # 某个glyf下都会嵌套 contour -> pt, 但是 coordinates 属性只获取到了pt的 x, y 对于该pt属于哪个contour轮廓 以及该点是1轮廓上的点或0控制点这一信息是丢失了的
        # print(coors)
        # GlyphCoordinates([(420, 521),(408, 574),(386, 597),(349, 635),(302, 635),(248, 635),(220, 612),(177, 580),(154, 531),(141, 492),(137, 449),(128, 407),(128, 352),(161, 402),(254, 449),(306, 449),(395, 449),(522, 316),(522, 211),(522, 143),(493, 83),(463, 36),(412, -7),(360, -39),(284, -39),(180, -39),(39, 124),(39, 317),(39, 530),(117, 619),(185, 710),(301, 710),(388, 710),(443, 661),(498, 614),(510, 528),(420, 518),(142, 214),(143, 166),(154, 122),(182, 79),(254, 35),(292, 29),(347, 41),(386, 81),(430, 127),(430, 206),(428, 287),(381, 326),(349, 370),(228, 370),(142, 282),(142, 211)])
        coors = [v for coor in coors for v in coor]
        # print(coors)
        # [420, 521, 408, 574, 386, 597, 349, 635, 302, 635, 248, 635, 220, 612, 177, 580, 154, 531, 141, 492, 137, 449, 128, 407, 128, 352, 161, 402, 254, 449, 306, 449, 395, 449, 522, 316, 522, 211, 522, 143, 493, 83, 463, 36, 412, -7, 360, -39, 284, -39, 180, -39, 39, 124, 39, 317, 39, 530, 117, 619, 185, 710, 301, 710, 388, 710, 443, 661, 498, 614, 510, 528, 420, 518, 142, 214, 143, 166, 154, 122, 182, 79, 254, 35, 292, 29, 347, 41, 386, 81, 430, 127, 430, 206, 428, 287, 381, 326, 349, 370, 228, 370, 142, 282, 142, 211]
        coors.insert(0, cli[i])
        # print(coors)
        # [6, 420, 521, 408, 574, 386, 597, 349, 635, 302, 635, 248, 635, 220, 612, 177, 580, 154, 531, 141, 492, 137, 449, 128, 407, 128, 352, 161, 402, 254, 449, 306, 449, 395, 449, 522, 316, 522, 211, 522, 143, 493, 83, 463, 36, 412, -7, 360, -39, 284, -39, 180, -39, 39, 124, 39, 317, 39, 530, 117, 619, 185, 710, 301, 710, 388, 710, 443, 661, 498, 614, 510, 528, 420, 518, 142, 214, 143, 166, 154, 122, 182, 79, 254, 35, 292, 29, 347, 41, 386, 81, 430, 127, 430, 206, 428, 287, 381, 326, 349, 370, 228, 370, 142, 282, 142, 211]
        info.append(coors)
    return info


def get_font_data():
    infos = list()

    for i in range(1, 11):
        font = TTFont('./fonts/{}.woff'.format(i))
        cli = globals()['cli_{}'.format(i)]
        infos += get_coor_info(font, cli)
    return infos


cli_1 = [6, 7, 4, 9, 1, 2, 5, 0, 3, 8]
cli_2 = [1, 3, 2, 7, 6, 8, 9, 0, 4, 5]
cli_3 = [5, 8, 3, 0, 6, 7, 9, 1, 2, 4]
cli_4 = [9, 3, 4, 8, 7, 5, 2, 1, 6, 0]
cli_5 = [1, 5, 8, 0, 7, 9, 6, 3, 2, 4]
cli_6 = [5, 0, 6, 8, 9, 2, 3, 4, 1, 7]
cli_7 = [2, 1, 0, 4, 8, 6, 9, 3, 5, 7]
cli_8 = [4, 1, 8, 7, 5, 2, 0, 6, 9, 3]
cli_9 = [8, 2, 9, 6, 5, 4, 1, 7, 3, 0]
cli_10 = [4, 1, 9, 8, 3, 0, 6, 7, 5, 2]

if __name__ == '__main__':
    # fonttools暂时没有文档被发布,只能通过有的资料猜它怎么用了
    # ref: https://github.com/fonttools/fonttools/pull/1333
    # ref: https://groups.google.com/forum/#!topic/fonttools/DaRIok8RBdQ
    # ref: https://github.com/fonttools/fonttools/issues/997
    # print(get_font_data())
    # import numpy as np
    # import pandas as pd
    # from sklearn.impute import SimpleImputer
    # data = pd.DataFrame(get_font_data())
    # print(data)
    # imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
    # print(pd.DataFrame(imputer.fit_transform(data)))
    save_font()
