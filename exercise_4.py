import PySimpleGUI as sg
import copy
import re
import math

HOME_RODS = {1, 8}

CANVAS_HEIGHT = 300
CANVAS_WIDTH = 1000


class Disk:
    def __init__(self, width, color):
        self.width = width
        self.color = color


# находит оптимальный временный штевень для данного перемещения
def findOptimalTmpRod(startRod, goalRod):
    direction = int(goalRod - startRod) / (math.fabs(goalRod - startRod))
    if startRod in HOME_RODS:
        if math.fabs(goalRod - startRod) > 1:
            return startRod + direction
        else:
            return startRod + 2 * direction
    return startRod - direction


# создает инструкцию для одного простого одиночного перемещения
def createSingleInstruction(startRod, goalRod):
    return int(startRod), int(goalRod)


# создает инструкцию из одного или нескольких последовательных ходов
def createSimpleInstruction(startRod, goalRod):
    instruction = list()
    # определение знака направления. Слева направо: +; Справа налево -;
    direction = int((goalRod - startRod) / math.fabs(goalRod - startRod))
    if startRod in HOME_RODS and math.fabs(goalRod - startRod) != 1:
        tmpGoalRod = startRod + (2 * direction)
        instruction.append(createSingleInstruction(startRod, tmpGoalRod))
        startRod = tmpGoalRod
    while startRod != goalRod:
        tmpGoalRod = startRod + direction
        instruction.append(createSingleInstruction(startRod, tmpGoalRod))
        startRod = tmpGoalRod
    return instruction


# запуск алгоритма
def generateInstructionForOneTower(count, startRod, goalRod):
    instruction = list()
    if count == 1:
        instruction = instruction + createSimpleInstruction(startRod, goalRod)
        return instruction
    tmp = findOptimalTmpRod(startRod, goalRod)
    instruction = instruction + generateInstructionForOneTower(count - 1, startRod, tmp)
    instruction = instruction + generateInstructionForOneTower(1, startRod, goalRod)
    instruction = instruction + generateInstructionForOneTower(count - 1, tmp, goalRod)
    return instruction


# Рисует основание и штевни, возвращает словарь с координатами штевней
# indent - отступ от краев холста
def printShafts(graph, indent=20, shaft_thickness=5, shaft_amount=8, shaft_height=200, base_color="brown"):
    w, h = graph.get_size()

    # максимальный размер секции исходя из размеров холста
    # (а также максимальный размер обруча)
    section_size = (w - indent * 2) / 8

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
        disks.insert(0, Disk(diskWidth, randomColor()))
    return disks


# Генерирует и возвращает словарь с номером штевня и списком дисков, последний диск в списке - верхний диск
def generateStartedDisksPositionData(intCode):
    shaftStoreDict = dict()
    intCode = [int(x) for x in str(intCode)]
    for index, i in enumerate(intCode):
        shaftStoreDict[index + 1] = generateDisks(index + 1, i)
    return shaftStoreDict


# изменяет данные о позиции дисков в соответствии с переданной инструкцией
def modifyData(positionData, instructionsList):
    modifiedData = copy.deepcopy(positionData)
    for startRod, goalRod in instructionsList:
        currentDisk = modifiedData[startRod].pop(-1)
        modifiedData[goalRod].append(currentDisk)
    return modifiedData


# рисует диски исходя из словаря хранилища дисков и штевней и словаря с координатами штевней
def render(diskStoreDict, graph, diskHeight=10, shaftBottom=25):
    graph.erase()
    shaftCoordDict = printShafts(graph)
    for shaftI in range(len(diskStoreDict)):
        currentShaftCoord = int(shaftCoordDict[shaftI + 1])
        for diskI in range(len(diskStoreDict[shaftI + 1])):
            diskWidth = int(diskStoreDict[shaftI + 1][diskI].width) * 1.5
            firstCoord = ((currentShaftCoord - (diskWidth / 2)), shaftBottom + diskI * diskHeight)
            secondCoord = ((currentShaftCoord + (diskWidth / 2)), shaftBottom + diskI * diskHeight + diskHeight)
            graph.draw_oval(
                firstCoord,
                secondCoord,
                fill_color=diskStoreDict[shaftI + 1][diskI].color,
                line_color="black",
                line_width=1)


def randomColor():
    import random
    rand = lambda: random.randint(0, 255)
    return '#%02X%02X%02X' % (rand(), rand(), rand())


def main():
    sg.theme("DarkAmber")

    positionsData = generateStartedDisksPositionData("00000000")
    instructionsList = generateInstructionForOneTower(8, 1, 8)

    layout = [
        [sg.Text('Дисков в пирамиде: '), sg.Input("0", do_not_clear=True, key='-DISK_COUNT-'), sg.Button('Применить')],
        [sg.Text('', key='-ERROR_MSG-', text_color='red')],
        [sg.Graph(canvas_size=(CANVAS_WIDTH, CANVAS_HEIGHT), graph_top_right=(CANVAS_WIDTH, CANVAS_HEIGHT),
                  graph_bottom_left=(0, 0),
                  background_color="white", key='-GRAPH-')],
        [sg.Text("Ход: 0 из 0", key="-STEP_INFO-")],

        [sg.Slider(key='-STEP_SLIDER-', range=(0, 0), default_value=0, size=(90, 15), orientation='horizontal',
                   font=('Helvetica', 12), enable_events=True)],
    ]

    window = sg.Window("Drawing GUI", layout, finalize=True)

    graph = window["-GRAPH-"]

    modifyData(positionsData, instructionsList[:0])
    render(positionsData, graph)

    while True:
        event, values = window.read()
        if event == "-STEP_SLIDER-":
            step = int(values["-STEP_SLIDER-"])
            window["-STEP_INFO-"].update("Ход: " + str(step) + " из " + str(len(instructionsList)))
            modifiedPositionData = modifyData(positionsData, instructionsList[:step])
            render(modifiedPositionData, graph)
        if event == "Применить":
            diskCount = str(values["-DISK_COUNT-"])
            if re.fullmatch("\d+", diskCount):
                diskCount = str(int(diskCount))
            if re.fullmatch("\d", diskCount):
                window["-ERROR_MSG-"].Update("")
            else:
                diskCount = str(0)
                window.FindElement("-ERROR_MSG-").Update("Количество дисков должно быть в пределах от 0 - 9")

            positionsData = generateStartedDisksPositionData(diskCount + "0000000")
            instructionsList = []
            if int(diskCount) > 0:
                instructionsList = generateInstructionForOneTower(int(diskCount), 1, 8)
            window["-STEP_SLIDER-"].Update(0, range=(0, len(instructionsList)))
            window["-STEP_INFO-"].update("Ход: " + str(0) + " из " + str(len(instructionsList)))
            render(modifyData(positionsData, instructionsList[:0]), graph)

        if event == sg.WIN_CLOSED:
            break
            window.close()

main()
