import math

HOME_RODS = {1, 8}


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
    return {int(startRod), int(goalRod)}


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
def generateInstruction(count, startRod, goalRod):
    instruction = list()
    if count == 1:
        instruction = instruction + createSimpleInstruction(startRod, goalRod)
        return instruction
    tmp = findOptimalTmpRod(startRod, goalRod)
    instruction = instruction + generateInstruction(count - 1, startRod, tmp)
    instruction = instruction + generateInstruction(1, startRod, goalRod)
    instruction = instruction + generateInstruction(count - 1, tmp, goalRod)
    return instruction
