# my ID 70153452

import PySimpleGUI as sg

CANVAS_HEIGHT = 300
CANVAS_WIDTH = 1000


# Рисует основание и штевни, возвращает словарь с координатами штевней
# indent - отступ от краев холста
def printShafts(graph, indent=20, shaft_thickness=5, shaft_amount=8, shaft_height=200, base_color="brown"):
    w, h = graph.get_size()

    # максимальный размер секции исходя из размеров холста
    # (а также максимальный размер обруча)
    section_size = (w - indent * 2) / 8
    print("Размер секции: " + str(section_size))

    # рисуем основу
    graph.DrawRectangle(
        (indent, indent),
        (w - indent, shaft_thickness + indent),
        fill_color=base_color,
        line_color=base_color,
        line_width=2
    )

    # словарь с координатами центра шпинделей по оси x
    shaftDict = dict()

    # рисуем шпиндели
    for i in range(shaft_amount):
        shaftDict[i + 1] = i * section_size + indent + section_size / 2
        graph.DrawRectangle(
            (i * section_size + indent + section_size / 2 - shaft_thickness / 2, indent),
            (i * section_size + indent + section_size / 2 + shaft_thickness / 2,
             shaft_height + indent + shaft_thickness),
            fill_color=base_color,
            line_color=base_color,
            line_width=2
        )
    return shaftDict


# генерирует список дисков (толщину дисков) исходя из номера штевня и количеству дисков
# по формуле M * 10 + N, где M - номер штевня, N - номер диска сверху вниз
def generateDisks(shaftNum, diskCount):
    disks = list()
    for i in range(diskCount):
        diskWidth = (shaftNum * 10) + i + 1
        disks.insert(0, diskWidth)
    return disks


# Генерирует и возвращает словарь с номером штевня и списком дисков, последний диск в списке - верхний диск
def generateDisksOnShafts(intCode):
    shaftStoreDict = dict()
    intCode = [int(x) for x in str(intCode)]
    for index, i in enumerate(intCode):
        shaftStoreDict[index + 1] = generateDisks(index + 1, i)
    return shaftStoreDict


# рисует диски исходя из словаря хранилища дисков и штевней и словаря с координатами штевней
def printDisks(diskStoreDict, shaftCoordDict, graph, diskHeight=10, shaftBottom=25):
    for shaftI in range(len(diskStoreDict)):
        currentShaftCoord = int(shaftCoordDict[shaftI + 1])
        for diskI in range(len(diskStoreDict[shaftI + 1])):
            diskWidth = int(diskStoreDict[shaftI + 1][diskI])
            firstCoord = ((currentShaftCoord - (diskWidth / 2)), shaftBottom + diskI * diskHeight)
            secondCoord = ((currentShaftCoord + (diskWidth / 2)), shaftBottom + diskI * diskHeight + diskHeight)
            disk = graph.draw_oval(
                firstCoord,
                secondCoord,
                fill_color=randomColor(),
                line_color="black",
                line_width=1)


def randomColor():
    import random
    rand = lambda: random.randint(0, 255)
    return ('#%02X%02X%02X' % (rand(), rand(), rand()))


def main():
    layout = [
        [sg.Graph(canvas_size=(CANVAS_WIDTH, CANVAS_HEIGHT), graph_top_right=(CANVAS_WIDTH, CANVAS_HEIGHT),
                  graph_bottom_left=(0, 0),
                  background_color="white", key='-GRAPH-')]
    ]

    window = sg.Window("Drawing GUI", layout, finalize=True)

    graph = window["-GRAPH-"]
    # circle = graph.draw_oval((0, 0), (100, 100), fill_color="red", line_color="black", line_width=1)
    # graph.move_figure(circle, 100, 200)

    shaftCoord = printShafts(graph)
    print(shaftCoord)
    print(shaftCoord[1])
    diskStore = generateDisksOnShafts(70153452)
    printDisks(diskStore, shaftCoord, graph)

    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        window.close()


main()
# print(generateDisksOnShafts(80000000))
