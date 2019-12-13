import io

import numpy as np
import matplotlib.pyplot as plt
import bezier
from fontTools.ttLib import TTFont
from fontTools.misc.xmlWriter import XMLWriter

from lxml import etree


def draw_all_fonts(ttf_font):
    glyf_order = font.getGlyphOrder()[2:]
    print(glyf_order)
    for one_glyf_name in glyf_order:
        xml_str_f = io.StringIO()
        writer = XMLWriter(xml_str_f)
        font['glyf'][one_glyf_name].toXML(writer, ttf_font)
        xml_str_f.seek(0)
        xml_str = xml_str_f.read()
        one_glyf = etree.HTML(xml_str.encode())
        contours = one_glyf.xpath('//contour')
        contour_list = list()
        for contour in contours:
            points = contour.xpath('./pt')
            point_list = list()
            for point in points:
                x = int(point.xpath('./@x')[0])
                y = int(point.xpath('./@y')[0])
                on = int(point.xpath('./@on')[0])
                point_list.append((x, y, on))
            contour_list.append(point_list)
        draw_font(one_glyf_name, contour_list)


def draw_font(font_name, contour_list):
    plt.title(font_name)

    for contour in contour_list:
        i = 0
        while True:
            p1 = contour[i]
            if p1[2] == 1:
                plt.scatter(*p1[:2], color='r', marker='.')
            if p1[2] == 0:
                plt.scatter(*p1[:2], color='b', marker='x')
            if i == len(contour) - 1:
                break
            p2 = contour[i + 1]
            if p1[2] == 0 and p2[2] == 0:
                contour.insert(i + 1, ((p1[0] + p2[0]) // 2, (p1[1] + p2[1]) // 2, 1))
            else:
                i += 1
        i = 0
        while i < len(contour):
            p1 = contour[i]
            if i + 1 == len(contour):
                p2 = contour[0]
            else:
                p2 = contour[i + 1]
            if p2[2] == 1:
                plt.plot(*list(zip(p1, p2))[:2], color='black')
                i += 1
            elif p2[2] == 0:
                if i + 2 == len(contour):
                    p3 = contour[0]
                else:
                    p3 = contour[i + 2]
                nodes = np.asfortranarray((list(zip(p1, p2, p3))[:2]), dtype=np.float)
                curve = bezier.Curve(nodes, degree=6)
                s_vals = np.linspace(0.0, 1.0, 30)
                data=curve.evaluate_multi(s_vals)
                plt.plot(*data, color='black')
                i += 2
    plt.show()


if __name__ == '__main__':
    file_path = './fonts/1.woff'
    print(file_path)
    font = TTFont(file_path)
    draw_all_fonts(font)

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
