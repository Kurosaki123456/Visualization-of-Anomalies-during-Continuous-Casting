import numpy as np
import pandas as pd

# 设置全局字典变量
def _init():
    global _global_dict
    _global_dict = {}


def set_value(name, value):
    _global_dict[name] = value


def get_value(name, defValue=None):
    try:
        return _global_dict[name]
    except KeyError:
        return defValue



def loadDataSet(fileName):
    """
    读取数据
    ----------
    param fileName : fileName\n
        源数据文件路径\n
    return : 二维数组\n
        源数据
    """
    dataSet = []
    fr = open(fileName, "r")
    for line in fr.readlines():
        lineData = []
        lineColumn = line.strip().split()
        for column in range(len(lineColumn)):
            if column < 4:
                lineData.append(str(lineColumn[column]))
            else:
                if '#' in lineColumn[column]:
                    lineData.append(float("-1.00"))
                else:
                    lineData.append(float(lineColumn[column]))
        dataSet.append(lineData)
    return dataSet



# 加载黏结特征向量样本集
def load_feature_vector(fileName):

    data_name = fileName
    # 读取csv文件中的特定列并指定数据类型(默认会把第一行当作表头)
    data = pd.read_csv(data_name, encoding = 'gb2312').values

    return data




class Variable():
    def __init__(self, plant = "南钢", accident = "漏钢"):
        super(Variable, self).__init__()

        # 观察纵裂纹时起始时刻为读入时刻提前185s(120s有效数据 + 65s无效数据)
        self.nTime_Advance = 185
        # 观察纵裂纹时结束时刻为读入时刻滞后60s
        self.nTime_Lag = 60
        #设置观测时间窗口长度,前5s为无效数据, 保证显示60s的漏钢有效数据和120s的纵裂有效数据(前65s为无效数据)
        self.nTime_Window = 65 if accident == "漏钢" else self.nTime_Advance + self.nTime_Lag if accident == "纵裂" else None
        #纵裂可视化计算均值时间窗口长度
        self.nTime_Spread = 65
        #第一排与第三排热电偶间距为235mm
        self.Dis_First_Third_Row = 235
        #结晶器铜板数量
        self.Mold_Nums = 4

        #浇铸参数
        self.fSlab_Width = np.zeros(self.nTime_Window)
        self.fSlab_Thick = np.zeros(self.nTime_Window)
        self.fCasting_Speed = np.zeros(self.nTime_Window)
        self.fMold_Level = np.zeros(self.nTime_Window)
        self.fTundishTem = np.zeros(self.nTime_Window)
        self.fMoldFrequency = np.zeros(self.nTime_Window)
        self.fMoldStroke = np.zeros(self.nTime_Window)
        self.fMoldNonSinuFac = np.zeros(self.nTime_Window)

        #存储初始温度数据
        self.Tc_Num_Broad = 57 if plant == "南钢" else 21 if plant == "鞍钢" else -1    #宽面热电偶数
        self.Tc_Num_Narrow = 3
        self.fMoldBroadOuterTem = np.zeros((self.nTime_Window, self.Tc_Num_Broad))
        self.fMoldBroadInnerTem = np.zeros((self.nTime_Window, self.Tc_Num_Broad))
        self.fMoldNarrowLeftTem = np.zeros((self.nTime_Window, self.Tc_Num_Narrow))
        self.fMoldNarrowRightTem = np.zeros((self.nTime_Window, self.Tc_Num_Narrow))

        #检查热电偶温度是否正常
        self.fErrorThermoLimitMin = 10.
        self.fErrorThermoLimitMax = 250.

        #代表当前时刻电偶是否异常的bool型变量
        self.bMoldBroadInnerTem = np.empty(self.Tc_Num_Broad)
        self.bMoldBroadOuterTem = np.empty(self.Tc_Num_Broad)
        self.bMoldNarrowLeftTem = np.empty(self.Tc_Num_Narrow)
        self.bMoldNarrowRightTem = np.empty(self.Tc_Num_Narrow)

        #当前时刻校正后的温度
        self.fCalibrateMouldBroadInnerTem = np.zeros(self.Tc_Num_Broad)
        self.fCalibrateMouldBroadOuterTem = np.zeros(self.Tc_Num_Broad)
        self.fCalibrateMouldNarrowLeftTem = np.zeros(self.Tc_Num_Narrow)
        self.fCalibrateMouldNarrowRightTem = np.zeros(self.Tc_Num_Narrow)

        #结晶器进水口温度
        self.fMouldInTemerature = 0.

        #当前时刻测点温度(校正后)
        self.CEDIAN_HEIGHT = 3
        self.CEDIAN_WIDE = self.Tc_Num_Broad // 3   # "/"为浮点数除法，返回浮点结果；"//"表示整数除法，返回不大于结果的的一个最大整数
        self.fTemInnerWide = np.zeros((self.CEDIAN_HEIGHT, self.CEDIAN_WIDE))
        self.fTemOuterWide = np.zeros((self.CEDIAN_HEIGHT, self.CEDIAN_WIDE))
        self.fTemLeftNarrow = np.zeros(self.Tc_Num_Narrow)
        self.fTemRightNarrow = np.zeros(self.Tc_Num_Narrow)

        #当前时刻四个面的温度数组
        self.HEIGHT_COUNT = 100    #漏钢高度方向插值点点数
        self.WIDE_COUNT = 300      #宽度方向插值点点数
        self.NARROW_COUNT = 40     #厚度方向插值点点数
        self.fOuterWide = np.zeros((self.HEIGHT_COUNT, self.WIDE_COUNT))
        self.fInnerWide = np.zeros((self.HEIGHT_COUNT, self.WIDE_COUNT))
        self.fRightNarrow = np.zeros((self.HEIGHT_COUNT, self.NARROW_COUNT))
        self.fLeftNarrow = np.zeros((self.HEIGHT_COUNT, self.NARROW_COUNT))

        #当前时刻四个面的温度变化速率数组
        self.fOuterWide_Trick = np.zeros((self.HEIGHT_COUNT, self.WIDE_COUNT))
        self.fInnerWide_Trick = np.zeros((self.HEIGHT_COUNT, self.WIDE_COUNT))
        self.fRightNarrow_Trick = np.zeros((self.HEIGHT_COUNT, self.NARROW_COUNT))
        self.fLeftNarrow_Trick = np.zeros((self.HEIGHT_COUNT, self.NARROW_COUNT))

        self.HEIGHT_COUNT_CRACK = 120  #纵裂高度方向插值点点数(观测时间窗口长度)
        self.fOuterWideCrack = np.zeros((self.CEDIAN_HEIGHT, self.HEIGHT_COUNT_CRACK, self.WIDE_COUNT))
        self.fInnerWideCrack = np.zeros((self.CEDIAN_HEIGHT, self.HEIGHT_COUNT_CRACK, self.WIDE_COUNT))
        self.fRightNarrowCrack = np.zeros((self.CEDIAN_HEIGHT, self.HEIGHT_COUNT_CRACK, self.NARROW_COUNT))
        self.fLeftNarrowCrack = np.zeros((self.CEDIAN_HEIGHT, self.HEIGHT_COUNT_CRACK, self.NARROW_COUNT))

        self.fOuterWide_TrickCrack = np.zeros((self.CEDIAN_HEIGHT, self.HEIGHT_COUNT_CRACK, self.WIDE_COUNT))
        self.fInnerWide_TrickCrack = np.zeros((self.CEDIAN_HEIGHT, self.HEIGHT_COUNT_CRACK, self.WIDE_COUNT))
        self.fRightNarrow_TrickCrack = np.zeros((self.CEDIAN_HEIGHT, self.HEIGHT_COUNT_CRACK, self.NARROW_COUNT))
        self.fLeftNarrow_TrickCrack = np.zeros((self.CEDIAN_HEIGHT, self.HEIGHT_COUNT_CRACK, self.NARROW_COUNT))

        #四个面的温度数组队列
        self.Time_Interval = 5
        self.fOuterWideQueue = np.zeros((self.Time_Interval + 1, self.HEIGHT_COUNT, self.WIDE_COUNT))
        self.fInnerWideQueue = np.zeros((self.Time_Interval + 1, self.HEIGHT_COUNT, self.WIDE_COUNT))
        self.fRightNarrowQueue = np.zeros((self.Time_Interval + 1, self.HEIGHT_COUNT, self.NARROW_COUNT))
        self.fLeftNarrowQueue = np.zeros((self.Time_Interval + 1, self.HEIGHT_COUNT, self.NARROW_COUNT))
        #定义结晶器各个面的长度及插分网格
        self.fWideLength = 3010.
        self.fWideGrid = 0.
        self.fHeightLength = 900.
        self.fHeightGrid = 0.
        self.fNarrowLength = 234.
        self.fNarrowGrid = 0.
        #定义热电偶在横向和纵向安插距离
        self.fWideHengXiangJuLi = np.array([0., 155., 305., 455., 605., 755., 905., 1055., 1205., 1355., 1505., 1655., 1805., 1955., 2105., 2255., 2405., 2555., 2705., 2855., 3010.])
        self.fZongXiangJuLi = np.array([0., 210., 325., 445., 900.])
        self.fNarrowHengXiangJuLi = np.array([0., 167., 234.])


    def ReadProData(self, data_show):
        # i表示当前时刻(从Time_Start开始计)
        for i in range(len(data_show)):
            self.fSlab_Width[i] = data_show[i][4]  # 第5个值为板坯宽度
            self.fSlab_Thick[i] = data_show[i][5]  # 第6个值为板坯厚度
            self.fCasting_Speed[i] = data_show[i][6]
            self.fMold_Level[i] = data_show[i][7]
            self.fTundishTem[i] = data_show[i][8]
            self.fMoldFrequency[i] = data_show[i][9]
            self.fMoldStroke[i] = data_show[i][10]
            self.fMoldNonSinuFac[i] = data_show[i][11]

            Num_Tem_Data = 2 * (self.Tc_Num_Broad + self.Tc_Num_Narrow)  # 温度数据的个数
            data_show_Tem = data_show[i][-Num_Tem_Data:]  # 将当前时刻温度数据单独取出

            self.fMoldBroadOuterTem[i][:] = data_show_Tem[:self.Tc_Num_Broad]
            self.fMoldNarrowRightTem[i][:] = data_show_Tem[self.Tc_Num_Broad: self.Tc_Num_Broad + self.Tc_Num_Narrow]
            self.fMoldBroadInnerTem[i][:] = data_show_Tem[self.Tc_Num_Broad + self.Tc_Num_Narrow:
                                                          self.Tc_Num_Broad + self.Tc_Num_Narrow + self.Tc_Num_Broad]
            self.fMoldNarrowLeftTem[i][:] = data_show_Tem[-self.Tc_Num_Narrow:]



    def CheckThermocouples(self, time_idx):
        for i in range(self.Tc_Num_Broad):
            if self.fMoldBroadInnerTem[time_idx][i] < self.fErrorThermoLimitMin or \
                    self.fMoldBroadInnerTem[time_idx][i] > self.fErrorThermoLimitMax:
                self.bMoldBroadInnerTem[i] = False
            else:
                self.bMoldBroadInnerTem[i] = True

            if self.fMoldBroadOuterTem[time_idx][i] < self.fErrorThermoLimitMin or \
                    self.fMoldBroadOuterTem[time_idx][i] > self.fErrorThermoLimitMax:
                self.bMoldBroadOuterTem[i] = False
            else:
                self.bMoldBroadOuterTem[i] = True

        for j in range(self.Tc_Num_Narrow):
            if self.fMoldNarrowLeftTem[time_idx][j] < self.fErrorThermoLimitMin or \
                    self.fMoldNarrowLeftTem[time_idx][j] > self.fErrorThermoLimitMax:
                self.bMoldNarrowLeftTem[j] = False
            else:
                self.bMoldNarrowLeftTem[j] = True

            if self.fMoldNarrowRightTem[time_idx][j] < self.fErrorThermoLimitMin or \
                    self.fMoldNarrowRightTem[time_idx][j] > self.fErrorThermoLimitMax:
                self.bMoldNarrowRightTem[j] = False
            else:
                self.bMoldNarrowRightTem[j] = True


    def CalibrateTemprature(self, time_idx):
        fBIAve = np.zeros(3)
        fBOAve = np.zeros(3)
        nBICount = np.zeros(3)
        nBOCount = np.zeros(3)
        fNLAve = 0.0
        fNRAve = 0.0
        nNLCount = 0
        nNRCount = 0

        for i in range(self.Tc_Num_Broad):
            if self.bMoldBroadInnerTem[i] == True:
                fBIAve[i % 3] += self.fMoldBroadInnerTem[time_idx][i]
                nBICount[i % 3] += 1
            if self.bMoldBroadOuterTem[i] == True:
                fBOAve[i % 3] += self.fMoldBroadOuterTem[time_idx][i]
                nBOCount[i % 3] += 1

        for j in range(self.Tc_Num_Narrow):
            if self.bMoldNarrowLeftTem[j] == True:
                fNLAve += self.fMoldNarrowLeftTem[time_idx][j]
                nNLCount += 1
            if self.bMoldNarrowRightTem[j] == True:
                fNRAve += self.fMoldNarrowRightTem[time_idx][j]
                nNRCount += 1

        for p in range(self.Tc_Num_Broad):
            if self.bMoldBroadInnerTem[p] == False and nBICount[p % 3] != 0:
                self.fCalibrateMouldBroadInnerTem[p] = fBIAve[p % 3] / nBICount[p % 3]
            else:
                self.fCalibrateMouldBroadInnerTem[p] = self.fMoldBroadInnerTem[time_idx][p]

            if self.bMoldBroadOuterTem[p] == False and nBOCount[p % 3] != 0:
                self.fCalibrateMouldBroadOuterTem[p] = fBOAve[p % 3] / nBOCount[p % 3]
            else:
                self.fCalibrateMouldBroadOuterTem[p] = self.fMoldBroadOuterTem[time_idx][p]

        for q in range(self.Tc_Num_Narrow):
            if self.bMoldNarrowLeftTem[q] == False:
                if nNLCount != 0:
                    self.fCalibrateMouldNarrowLeftTem[q] = fNLAve / nNLCount + 10.0 * (1 - q)
                else:
                    self.fCalibrateMouldNarrowLeftTem[q] = (fBIAve[q % 3] / nBICount[q % 3] + fBOAve[q % 3] / nBOCount[
                        q % 3]) / 2 - 8.0 * (3 - q)
            else:
                self.fCalibrateMouldNarrowLeftTem[q] = self.fMoldNarrowLeftTem[time_idx][q]

            if self.bMoldNarrowRightTem[q] == False:
                if nNRCount != 0:
                    self.fCalibrateMouldNarrowRightTem[q] = fNRAve / nNRCount + 10.0 * (1 - q)
                else:
                    self.fCalibrateMouldNarrowRightTem[q] = (fBIAve[q % 3] / nBICount[q % 3] + fBOAve[q % 3] /
                                                                  nBOCount[q % 3]) / 2 - 8.0 * (3 - q)
            else:
                self.fCalibrateMouldNarrowRightTem[q] = self.fMoldNarrowRightTem[time_idx][q]


    def RefreshData(self, time_idx):
        for i in range(self.Tc_Num_Broad):
            self.fTemInnerWide[i % 3][i // 3] = self.fCalibrateMouldBroadInnerTem[i]
            self.fTemOuterWide[i % 3][i // 3] = self.fCalibrateMouldBroadOuterTem[i]

        for j in range(self.Tc_Num_Narrow):
            self.fTemLeftNarrow[j] = self.fCalibrateMouldNarrowLeftTem[j]
            self.fTemRightNarrow[j] = self.fCalibrateMouldNarrowRightTem[j]

        if abs(self.fSlab_Thick[time_idx] - 220) < 5.0:
            self.fSlab_Thick[time_idx] = 230.0

        if abs(self.fSlab_Thick[time_idx] - 320) < 5.0:
            self.fSlab_Thick[time_idx] = 333.33


    def PushTemperature_InQueue(self):
        for i in range(self.Time_Interval, 0, -1):  # 时间倒序
            # QApplication.processEvents()为处理事件函数, 实现一边执行耗时程序(如for循环等)，一边刷新页面的功能，使程序运行流畅
            self.fOuterWideQueue[i] = self.fOuterWideQueue[i - 1]  # 将后一秒的数据冲洗掉
            self.fInnerWideQueue[i] = self.fInnerWideQueue[i - 1]
            self.fRightNarrowQueue[i] = self.fRightNarrowQueue[i - 1]
            self.fLeftNarrowQueue[i] = self.fLeftNarrowQueue[i - 1]


    def CalculateTemMapCrack(self, time_idx):

        self.fNarrowLength = self.fSlab_Thick[time_idx]
        self.fNarrowHengXiangJuLi[2] = self.fNarrowLength
        self.fNarrowHengXiangJuLi[1] = self.fNarrowLength / 2
        self.fNarrowGrid = self.fNarrowLength / self.NARROW_COUNT

        self.fWideGrid = self.fWideLength / self.WIDE_COUNT
        self.fHeightGrid = self.fHeightLength / self.HEIGHT_COUNT_CRACK

        for row in range(self.CEDIAN_HEIGHT):
            #分别更新用三排热电偶温度插值按时序传播所得到的铜板热像图
            self.CalculateWideCrack(self.fTemOuterWide[row], self.fOuterWideCrack[row], time_idx)
            self.CalculateWideCrack(self.fTemInnerWide[row], self.fInnerWideCrack[row], time_idx)
            self.CalculateNarrowCrack(self.fTemRightNarrow[row], self.fRightNarrowCrack[row], 0, row)
            self.CalculateNarrowCrack(self.fTemLeftNarrow[row], self.fLeftNarrowCrack[row], 1, row)



    def CalculateWideCrack(self, fWideCeDianTem, fWideTem, time_idx):

        CEDIAN_WIDE = self.CEDIAN_WIDE
        HEIGHT_COUNT_CRACK = self.HEIGHT_COUNT_CRACK
        WIDE_COUNT_CRACK = self.WIDE_COUNT

        fMouldWidthStart = (self.fWideHengXiangJuLi[CEDIAN_WIDE + 1] - self.fSlab_Width[time_idx]) / 2
        fMouldWidthEnd = fMouldWidthStart + self.fSlab_Width[time_idx]
        fInWaterTem = self.fMouldInTemerature

        for i in range(HEIGHT_COUNT_CRACK - 1, 0, -1):
            for j in range(WIDE_COUNT_CRACK):
                fWideTem[i][j] = fWideTem[i - 1][j]


        fHengXiangWenDu = np.zeros(CEDIAN_WIDE + 2)


        fHengXiangWenDu[0] = fInWaterTem
        for j in range(CEDIAN_WIDE):
            fHengXiangWenDu[1 + j] = fWideCeDianTem[j]
        fHengXiangWenDu[CEDIAN_WIDE + 1] = fInWaterTem

        fY = np.zeros(self.WIDE_COUNT)

        self.GetValueSpline(CEDIAN_WIDE + 2, self.fWideHengXiangJuLi, fHengXiangWenDu, fMouldWidthStart, fMouldWidthEnd,
                       self.WIDE_COUNT, fY)

        for j in range(WIDE_COUNT_CRACK):
            fWideTem[0][j] = fY[j]


    def CalculateNarrowCrack(self, fNarrowCeDian, fNarrowTem, nNarrow, row):

        CEDIAN_NARROW = 1  # 窄面横向只有1列热电偶

        HEIGHT_COUNT_CRACK = self.HEIGHT_COUNT_CRACK
        WIDE_COUNT_CRACK = self.WIDE_COUNT
        NARROW_COUNT_CRACK = self.NARROW_COUNT

        for i in range(HEIGHT_COUNT_CRACK - 1, 0, -1):
            for j in range(NARROW_COUNT_CRACK):
                fNarrowTem[i][j] = fNarrowTem[i - 1][j]


        fHengXiangWenDu = np.zeros(CEDIAN_NARROW + 2)

        fHengXiangWenDu[1] = fNarrowCeDian

        if nNarrow == 0:
            fHengXiangWenDu[0] = self.fOuterWideCrack[row][0][WIDE_COUNT_CRACK - 1]
            fHengXiangWenDu[CEDIAN_NARROW + 1] = self.fInnerWideCrack[row][0][0]
        else:
            fHengXiangWenDu[0] = self.fInnerWideCrack[row][0][WIDE_COUNT_CRACK - 1]
            fHengXiangWenDu[CEDIAN_NARROW + 1] = self.fOuterWideCrack[row][0][0]


        fY = np.zeros(self.NARROW_COUNT)

        self.GetValueSpline(CEDIAN_NARROW + 2, self.fNarrowHengXiangJuLi, fHengXiangWenDu, 0.
                       , self.fNarrowLength, self.NARROW_COUNT, fY)

        for j in range(self.NARROW_COUNT):
            fNarrowTem[0][j] = fY[j]




    def CalculateTemMap(self, time_idx):

        self.fNarrowLength = self.fSlab_Thick[time_idx]
        self.fNarrowHengXiangJuLi[2] = self.fNarrowLength
        self.fNarrowHengXiangJuLi[1] = self.fNarrowLength / 2
        self.fNarrowGrid = self.fNarrowLength / self.NARROW_COUNT

        self.fWideGrid = self.fWideLength / self.WIDE_COUNT
        self.fHeightGrid = self.fHeightLength / self.HEIGHT_COUNT

        self.CalculateWide(self.fTemOuterWide, self.fOuterWide, 0, time_idx)
        self.CalculateWide(self.fTemInnerWide, self.fInnerWide, 1, time_idx)
        self.CalculateNarrow(self.fTemRightNarrow, self.fRightNarrow, 0)
        self.CalculateNarrow(self.fTemLeftNarrow, self.fLeftNarrow, 1)



    def CalculateWide(self, fWideCeDianTem, fWideTem, nWide, time_idx):
        fTemAdjust = 30.0
        CEDIAN_HEIGHT = self.CEDIAN_HEIGHT
        CEDIAN_WIDE = self.CEDIAN_WIDE
        fMouldWidthStart = (self.fWideHengXiangJuLi[CEDIAN_WIDE + 1] - self.fSlab_Width[time_idx]) / 2
        fMouldWidthEnd = fMouldWidthStart + self.fSlab_Width[time_idx]
        fInWaterTem = self.fMouldInTemerature
        nCol = np.zeros(CEDIAN_WIDE, dtype = int)

        for i in range(CEDIAN_WIDE):
            nCol[i] = self.fWideHengXiangJuLi[i + 1] // self.fWideGrid

        fZongXiangWenDu = np.zeros(CEDIAN_HEIGHT + 2)

        for i in range(CEDIAN_WIDE):
            fZongXiangWenDu[0] = fWideCeDianTem[0][i] + fTemAdjust
            for j in range(CEDIAN_HEIGHT):
                fZongXiangWenDu[1 + j] = fWideCeDianTem[j][i]
            fZongXiangWenDu[CEDIAN_HEIGHT + 1] = fWideCeDianTem[2][i] - fTemAdjust

            fY = np.zeros(self.HEIGHT_COUNT)

            self.GetValueSpline(CEDIAN_HEIGHT + 2, self.fZongXiangJuLi, fZongXiangWenDu, self.fZongXiangJuLi[1],
                           self.fZongXiangJuLi[CEDIAN_HEIGHT], self.HEIGHT_COUNT, fY)

            for j in range(self.HEIGHT_COUNT):
                fWideTem[j][nCol[i]] = fY[j]

        fHengXiangWenDu = np.zeros(CEDIAN_WIDE + 2)

        for i in range(self.HEIGHT_COUNT):
            fHengXiangWenDu[0] = fInWaterTem
            for j in range(CEDIAN_WIDE):
                fHengXiangWenDu[1 + j] = fWideTem[i][nCol[j]]
            fHengXiangWenDu[CEDIAN_WIDE + 1] = fInWaterTem

            fY = np.zeros(self.WIDE_COUNT)

            self.GetValueSpline(CEDIAN_WIDE + 2, self.fWideHengXiangJuLi, fHengXiangWenDu, fMouldWidthStart, fMouldWidthEnd,
                           self.WIDE_COUNT, fY)

            for j in range(self.WIDE_COUNT):
                fWideTem[i][j] = fY[j]

        # 当前时刻温度数据更新为温度插值后的结果
        if nWide == 0:
            self.fOuterWideQueue[0] = fWideTem
        else:
            self.fInnerWideQueue[0] = fWideTem


    def CalculateNarrow(self, fNarrowCeDian, fNarrowTem, nNarrow):
        fTemAdjust = 30.0

        CEDIAN_HEIGHT = self.CEDIAN_HEIGHT
        CEDIAN_NARROW = 1  # 窄面横向只有1列热电偶

        nCol = int(self.fNarrowHengXiangJuLi[1] // self.fNarrowGrid)
        fZongXiangWenDu = np.zeros(CEDIAN_HEIGHT + 2)

        fZongXiangWenDu[0] = fNarrowCeDian[0] + fTemAdjust
        for i in range(CEDIAN_HEIGHT):
            fZongXiangWenDu[i + 1] = fNarrowCeDian[i]
        fZongXiangWenDu[CEDIAN_HEIGHT + 1] = fNarrowCeDian[2] - fTemAdjust

        fY = np.zeros(self.HEIGHT_COUNT)

        self.GetValueSpline(CEDIAN_HEIGHT + 2, self.fZongXiangJuLi, fZongXiangWenDu, self.fZongXiangJuLi[1],
                       self.fZongXiangJuLi[CEDIAN_HEIGHT], self.HEIGHT_COUNT, fY)

        for i in range(self.HEIGHT_COUNT):
            fNarrowTem[i][nCol] = fY[i]

        for i in range(self.HEIGHT_COUNT):
            fHengXiangWenDu = np.zeros(CEDIAN_NARROW + 2)
            fHengXiangWenDu[1] = fNarrowTem[i][nCol]

            if nNarrow == 0:
                fHengXiangWenDu[0] = self.fOuterWide[i][self.WIDE_COUNT - 1]
                fHengXiangWenDu[CEDIAN_NARROW + 1] = self.fInnerWide[i][0]
            else:
                fHengXiangWenDu[0] = self.fInnerWide[i][self.WIDE_COUNT - 1]
                fHengXiangWenDu[CEDIAN_NARROW + 1] = self.fOuterWide[i][0]

            fY = np.zeros(self.NARROW_COUNT)

            self.GetValueSpline(CEDIAN_NARROW + 2, self.fNarrowHengXiangJuLi, fHengXiangWenDu, 0.
                           , self.fNarrowLength, self.NARROW_COUNT, fY)

            for j in range(self.NARROW_COUNT):
                fNarrowTem[i][j] = fY[j]

        # 当前时刻温度数据更新为温度插值后的结果
        if nNarrow == 0:
            self.fRightNarrowQueue[0] = fNarrowTem
        else:
            self.fLeftNarrowQueue[0] = fNarrowTem


    def GetValueSpline(self, n, x, y, fXStart, fXEnd, nCalCount, fY):
        dy = np.zeros(n, dtype=float)
        s = np.zeros(n, dtype=float)
        s[0] = dy[0]
        dy[0] = 0.
        h0 = x[1] - x[0]

        for j in range(1, n - 1):
            h1 = x[j + 1] - x[j]
            alpha = h0 / (h0 + h1)
            beta = (1.0 - alpha) * (y[j] - y[j - 1]) / h0
            beta = 3.0 * (beta + alpha * (y[j + 1] - y[j]) / h1)
            dy[j] = -alpha / (2.0 + (1.0 - alpha) * dy[j - 1])
            s[j] = beta - (1.0 - alpha) * s[j - 1]
            s[j] = s[j] / (2.0 + (1.0 - alpha) * dy[j - 1])
            h0 = h1

        for j in range(n - 2, -1, -1):
            dy[j] = dy[j] * dy[j + 1] + s[j]

        for j in range(n - 1):
            s[j] = x[j + 1] - x[j]

        for m in range(nCalCount):
            t = fXStart + 1. * m * (fXEnd - fXStart) / nCalCount
            if t >= x[n - 1]:
                i = n - 2
            else:
                i = 0
                while t > x[i + 1]:
                    i += 1

            h1 = (x[i + 1] - t) / s[i]
            h0 = h1 ** 2

            z = (3.0 * h0 - 2.0 * h0 * h1) * y[i]
            z += s[i] * (h0 - h0 * h1) * dy[i]

            h1 = (t - x[i]) / s[i]
            h0 = h1 ** 2
            z += (3.0 * h0 - 2.0 * h0 * h1) * y[i + 1]
            z -= s[i] * (h0 - h0 * h1) * dy[i + 1]

            fY[m] = float(z)


    def TrickTemperature(self):

        Time_Interval = self.Time_Interval

        self.fOuterWide_Trick = (self.fOuterWideQueue[0] - self.fOuterWideQueue[Time_Interval]) / Time_Interval
        self.fInnerWide_Trick = (self.fInnerWideQueue[0] - self.fInnerWideQueue[Time_Interval]) / Time_Interval
        self.fRightNarrow_Trick = (self.fRightNarrowQueue[0] - self.fRightNarrowQueue[Time_Interval]) / Time_Interval
        self.fLeftNarrow_Trick = (self.fLeftNarrowQueue[0] - self.fLeftNarrowQueue[Time_Interval]) / Time_Interval


    def TrickTemperatureCrack(self):

        HEIGHT_COUNT_CRACK = self.HEIGHT_COUNT_CRACK
        WIDE_COUNT_CRACK = self.WIDE_COUNT
        NARROW_COUNT_CRACK = self.NARROW_COUNT

        for row in range(self.CEDIAN_HEIGHT):
            for i in range(HEIGHT_COUNT_CRACK - 1, 0, -1):
                for j in range(WIDE_COUNT_CRACK):
                    self.fOuterWide_TrickCrack[row][i][j] = self.fOuterWide_TrickCrack[row][i - 1][j]
                    self.fInnerWide_TrickCrack[row][i][j] = self.fInnerWide_TrickCrack[row][i - 1][j]

                    if j < NARROW_COUNT_CRACK:
                        self.fRightNarrow_TrickCrack[row][i][j] = self.fRightNarrow_TrickCrack[row][i - 1][j]
                        self.fLeftNarrow_TrickCrack[row][i][j] = self.fLeftNarrow_TrickCrack[row][i - 1][j]

        for row in range(self.CEDIAN_HEIGHT):
            fOuterWide_TrickCrackMean = np.mean(self.fOuterWideCrack[row][1 : 1 + self.nTime_Spread], axis = 0)
            fInnerWide_TrickCrackMean = np.mean(self.fInnerWideCrack[row][1 : 1 + self.nTime_Spread], axis = 0)
            fRightNarrow_TrickCrackMean = np.mean(self.fRightNarrowCrack[row][1: 1 + self.nTime_Spread], axis = 0)
            fLeftNarrow_TrickCrackMean = np.mean(self.fLeftNarrowCrack[row][1: 1 + self.nTime_Spread], axis = 0)

            self.fOuterWide_TrickCrack[row][0] = self.fOuterWideCrack[row][0] - fOuterWide_TrickCrackMean
            self.fInnerWide_TrickCrack[row][0] = self.fInnerWideCrack[row][0] - fInnerWide_TrickCrackMean
            self.fRightNarrow_TrickCrack[row][0] = self.fRightNarrowCrack[row][0] - fRightNarrow_TrickCrackMean
            self.fLeftNarrow_TrickCrack[row][0] = self.fLeftNarrowCrack[row][0] - fLeftNarrow_TrickCrackMean
