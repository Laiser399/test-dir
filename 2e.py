import logging


logging.basicConfig(format = u'time: "%(asctime)s", levelname: "%(levelname)s", message: "%(message)s"', level = logging.DEBUG, filename='1.log')
# %(filename)s
# %(lineno)d

logging.info('Program start!')

print('Enter file name: ', end='')
FileName = input()


try:
    file = open(FileName, 'r')
except BaseException:
    logging.error(f'Error opening file with name "{FileName}"!')
    exit(1)
numStr = 1
numCol = 1
buf = ''
Array = []
readNow = False
numVariables = -1

DNumLine = 1
DLinePos = 1
for line in file:
    for c in line:
        if c.isdigit() or (c == '-'):
            if (c == '-') and (buf != ''):
                logging.error(f'Error in line {DNumLine}, pos {DLinePos}!')
                file.close()
                exit(1)
            buf += c
            readNow = True
        elif c.isspace():
            if readNow == True:
                if ((numVariables != -1) and ((numStr > numVariables) or (numCol > numVariables + 1))):
                    logging.error(f'Error in line {DNumLine}, pos {DLinePos}!')
                    file.close()
                    exit(1)

                if Array.__len__() < numStr:
                    Array.append([])
                if Array[numStr - 1].__len__() < numCol:
                    Array[numStr - 1].append(int(buf))
                readNow = False

                numCol += 1
                buf = ''
            else:
                continue
        else:
            logging.error(f'Error in line {DNumLine}, pos {DLinePos}!')
            file.close()
            exit(1)
        DLinePos += 1

    #konez stroki
    if readNow == True:
        if Array.__len__() < numStr:
            Array.append([])
        if Array[numStr - 1].__len__() < numCol:
            Array[numStr - 1].append(int(buf))
        readNow = False
        numCol += 1
        buf = ''

    if numVariables == -1:
        if Array.__len__() == 0:
            logging.error(f'Error in line {DNumLine}, pos {DLinePos}!')
            file.close()
            exit(1)
        numVariables = Array[0].__len__() - 1
    if numStr == numVariables:
        break
    numStr += 1
    numCol = 1
    if numStr > numVariables:
        break
    DNumLine += 1
    DLinePos = 1
file.close()


MainCoef = []
FreeCoef = []
i1 = 0
while i1 < numVariables:
    MainCoef.append([])
    i2 = 0
    while i2 < numVariables:
        MainCoef[i1].append(Array[i1][i2])
        i2 += 1
    FreeCoef.append(Array[i1][numVariables])
    i1 += 1



if (Array.__len__() == 0) or (numVariables <= 1) or (numVariables != Array.__len__()):
    logging.error('Array is clear or number of variable is not equal to the number of lines!')
    exit(1)

#по столбцам
iCol = 0
while iCol < numVariables:
    #поиск ненулевого элемента
    iSearchNoZero = iCol
    while iSearchNoZero < numVariables:
        if Array[iSearchNoZero][iCol] != 0:
            break
        iSearchNoZero += 1
    if iSearchNoZero == numVariables:
        logging.info('Determinant = 0!')
        exit(0)
    #свап строк
    if iSearchNoZero != iCol:
        i = iCol
        #по столбцам
        while i < numVariables + 1:
            tm = Array[iCol][i]
            Array[iCol][i] = Array[iSearchNoZero][i]
            Array[iSearchNoZero][i] = tm
            i += 1
    #вычитание из нижних строк
    #по строкам
    iR = iCol + 1
    while iR < numVariables:
        #отношение
        if Array[iR][iCol] != 0:
            ratio = Array[iR][iCol] / Array[iCol][iCol]
            Array[iR][iCol] = 0
            iC = iCol + 1
            while iC < numVariables + 1:
                Array[iR][iC] = Array[iR][iC] - ratio * Array[iCol][iC]
                iC += 1
        iR += 1
    iCol += 1

#обратный ход
#по столбцам с последней переменной
iCol = numVariables - 1
while iCol >= 0:
    #ставим на предпоследнюю строку
    iRow = iCol - 1
    while iRow >= 0:
        if Array[iRow][iCol] != 0:
            # отношение
            ratio = Array[iRow][iCol] / Array[iCol][iCol]
            Array[iRow][iCol] = 0
            Array[iRow][numVariables] = Array[iRow][numVariables] - ratio * Array[iCol][numVariables]


        iRow -= 1

    iCol -= 1

result = []
for i in range(numVariables):
    result.append(Array[i][numVariables] / Array[i][i])



logging.info(f'CoefficientsOfX: {MainCoef}, freeCoefficients: {FreeCoef}, result: {result}')

logging.info('Program finish without errors!')