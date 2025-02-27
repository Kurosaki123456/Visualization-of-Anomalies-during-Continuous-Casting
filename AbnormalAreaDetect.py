import numpy as np
import math
import __init__ as gl


class CPosition():
    def __init__(self, x, y):
        self.nX = x
        self.nY = y


class CCell():
    def __init__(self):

        self.m_nAbnormity_Area_Num = 0
        self.m_fTemperture_Vary_Rate = 0.
        self.m_bIs_Abnormal = False


class CAbnormalRegion():
    def __init__(self):

        self.m_nLeft = 0
        self.m_nRight = 0
        self.m_nBottom = 0
        self.m_nTop = 0
        self.m_nWidth = 0
        self.m_nHeight = 0
        self.m_nTotal_Count = 0
        self.m_fArea = 0
        self.m_Gave = 0     # 异常区域平均温度速率
        self.mfou_descriptor = 0
        self.m_nAbnormity_Area_Num = 0
        self.m_Central_Point = CPosition(x = 0, y = 0)
        self.m_posArea = []     #列表元素类型为CPosition
        self.m_posEdge = []     #列表元素类型为CPosition
        self.m_bDel = False


class CAbormityAreaDetect():
    def __init__(self):

        self.m_nlabel = 0  #区域标号
        #self.m_nNum_Row = 0     #异常区域的行数
        #self.m_nNum_Col = 0     #异常区域的列数
        self.m_nAbnormity_Area_Count = -1   #异常区域数目
        self.m_fTemperature_Rising_Rate_Limit = 0.3      #温度上升速率变化限制
        self.m_nDelete_Area_Count = 20   #点数小于一定值时，删除区域
        self.m_AbnormalRegion = []   #列表元素类型为CAbnormalRegion(每一时刻下异常区域集合)
        #self.m_CellInfor = np.empty((self.m_nNum_Row, self.m_nNum_Col), dtype = object)

        # 4邻域的连通域和 8邻域的连通域
        # [row, col]
        self.m_NEIGHBOR_HOODS_4 = True
        self.m_OFFSETS_4 = [[0, -1], [-1, 0], [0, 0], [1, 0], [0, 1]]

        self.m_NEIGHBOR_HOODS_8 = False
        self.m_OFFSETS_8 = [[-1, -1], [0, -1], [1, -1],
                     [-1, 0], [0, 0], [1, 0],
                     [-1, 1], [0, 1], [1, 1]]



    def Set_Cell_Num(self, nX, nY):

        self.m_nNum_Row = nX
        self.m_nNum_Col = nY

        #元素类型为CCell(元胞二维数组)
        self.m_CellInfor = np.empty((self.m_nNum_Row, self.m_nNum_Col), dtype = object)


    def Clear(self):

        for i in range(self.m_nNum_Row):
            for j in range(self.m_nNum_Col):
                self.m_CellInfor[i][j] = CCell()

        for i in range(len(self.m_AbnormalRegion)):
            self.m_AbnormalRegion[i] = CAbnormalRegion()


    def Set_Rising_Rate_Limit(self, fValue):
        self.m_fTemperature_Rising_Rate_Limit = fValue


    def Two_Pass(self, CellInfor, neighbor_hoods):
        if neighbor_hoods == self.m_NEIGHBOR_HOODS_4:
            offsets = self.m_OFFSETS_4
        elif neighbor_hoods == self.m_NEIGHBOR_HOODS_8:
            offsets = self.m_OFFSETS_8
        else:
            raise ValueError

        self.neighbor_value(CellInfor, offsets, False)
        self.neighbor_value(CellInfor, offsets, True)



    def neighbor_value(self, CellInfor, offsets, reverse=False):
        rows, cols = CellInfor.shape
        label_idx = 0
        rows_ = [0, rows, 1] if reverse == False else [rows - 1, -1, -1]
        cols_ = [0, cols, 1] if reverse == False else [cols - 1, -1, -1]
        for row in range(rows_[0], rows_[1], rows_[2]):
            for col in range(cols_[0], cols_[1], cols_[2]):
                label = 256
                if CellInfor[row][col].m_nAbnormity_Area_Num < 0.5:
                    continue
                for offset in offsets:
                    neighbor_row = min(max(0, row + offset[0]), rows - 1)
                    neighbor_col = min(max(0, col + offset[1]), cols - 1)
                    neighbor_val = CellInfor[neighbor_row, neighbor_col].m_nAbnormity_Area_Num   #逗号索引的方式只在numpy数组中适用
                    if neighbor_val < 0.5:
                        continue
                    label = neighbor_val if neighbor_val < label else label
                if label == 255:
                    label_idx += 1
                    label = label_idx
                CellInfor[row][col].m_nAbnormity_Area_Num = label


    def reorganize(self, CellInfor):
        index_map = []
        #points = []
        index = -1
        rows, cols = CellInfor.shape
        for row in range(rows):
            for col in range(cols):
                var = CellInfor[row][col].m_nAbnormity_Area_Num
                if var < 0.5:
                    continue
                if var in index_map:
                    index = index_map.index(var)
                    num = index + 1
                else:
                    index = len(index_map)
                    num = index + 1
                    index_map.append(var)
                    #points.append([])
                CellInfor[row][col].m_nAbnormity_Area_Num = num
                #points[index].append([row, col])


        for label in range(1, len(index_map) + 1):
            new_abnormalregion = CAbnormalRegion()

            for row in range(rows):
                for col in range(cols):
                    if self.m_CellInfor[row][col].m_nAbnormity_Area_Num == label:
                        pos = CPosition(row, col)
                        new_abnormalregion.m_posArea.append(pos)

            self.m_AbnormalRegion.append(new_abnormalregion)



    def Delete_And_Number(self):
        for i in range(len(self.m_AbnormalRegion)):
            size = len(self.m_AbnormalRegion[i].m_posArea)
            if size < self.m_nDelete_Area_Count:
                for j in range(size):
                    X0 = self.m_AbnormalRegion[i].m_posArea[j].nX
                    Y0 = self.m_AbnormalRegion[i].m_posArea[j].nY
                    self.m_CellInfor[X0][Y0] = CCell()
                self.m_AbnormalRegion[i].m_bDel = True
            else:
                continue

        self.m_AbnormalRegion = [x for x in self.m_AbnormalRegion if x.m_bDel == False]
        self.m_nAbnormity_Area_Count = len(self.m_AbnormalRegion)
        self.m_nlabel = self.m_nAbnormity_Area_Count

        for i in range(self.m_nAbnormity_Area_Count):
            for j in range(len(self.m_AbnormalRegion[i].m_posArea)):
                X1 = self.m_AbnormalRegion[i].m_posArea[j].nX
                Y1 = self.m_AbnormalRegion[i].m_posArea[j].nY
                self.m_CellInfor[X1][Y1].m_nAbnormity_Area_Num = i + 1

            self.m_AbnormalRegion[i].m_nTotal_Count = len(self.m_AbnormalRegion[i].m_posArea)
            self.m_AbnormalRegion[i].m_nAbnormity_Area_Num = i + 1



    def Contour_Extraction(self):
        # 边界起始点集合
        Edge_Start_Points = []
        label = 1
        # 求每个异常区域的起始点坐标
        for row in range(self.m_nNum_Row):
            for col in range(self.m_nNum_Col):
                if self.m_CellInfor[row][col].m_nAbnormity_Area_Num == label:   #异常区域编号从1开始索引
                    Edge_Start_Points.append((row, col))
                    label += 1

        # 搜索方向(八连通)
        Directions = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]

        for N in range(self.m_nAbnormity_Area_Count):
            # 在每次搜素新的黏结区域时将搜索方向重置(变为初始搜索方向水平向右)
            Search_Direction = 3
            Search_Times = 0
            Start_Point_Row = -1
            Start_Point_Col = -1
            Search_Point_Row = -1
            Search_Point_Col = -1

            while Search_Point_Row != Edge_Start_Points[N][0] or Search_Point_Col != Edge_Start_Points[N][1]:

                if not self.m_AbnormalRegion[N].m_posEdge:

                    Search_Point_Row = Edge_Start_Points[N][0]
                    Search_Point_Col = Edge_Start_Points[N][1]

                if 0 <= Search_Point_Row <= self.m_nNum_Row - 1 and 0 <= Search_Point_Col <= self.m_nNum_Col- 1:
                    if self.m_CellInfor[Search_Point_Row][Search_Point_Col].m_nAbnormity_Area_Num == N + 1:
                        Search_Times = 0
                        pos = CPosition(Search_Point_Row, Search_Point_Col)
                        self.m_AbnormalRegion[N].m_posEdge.append(pos)
                        # 更新搜索方向(逆时针旋转90°)
                        Search_Direction = Search_Direction - 2 if Search_Direction - 2 >= 0 else (Search_Direction - 2) + len(Directions)
                        # 更新起始搜索点
                        Start_Point_Row = Search_Point_Row
                        Start_Point_Col = Search_Point_Col
                        # 更新搜索方向
                        Search_Point_Row = Start_Point_Row + Directions[Search_Direction][0]
                        Search_Point_Col = Start_Point_Col + Directions[Search_Direction][1]

                    else:
                        # 顺时针旋转45°
                        Search_Direction = (Search_Direction + 1) % len(Directions)
                        Search_Times += 1
                        Search_Point_Row = Start_Point_Row + Directions[Search_Direction][0]
                        Search_Point_Col = Start_Point_Col + Directions[Search_Direction][1]

                else:
                    Search_Direction = (Search_Direction + 1) % len(Directions)
                    Search_Times += 1
                    Search_Point_Row = Start_Point_Row + Directions[Search_Direction][0]
                    Search_Point_Col = Start_Point_Col + Directions[Search_Direction][1]

                if Search_Times == len(Directions) - 1: # 旋转7个方向均未找到边界点(即轮廓点只有1个点),此时跳出循环搜索下一个连通区域
                    break




    def Calculate_Feature(self):
        for i in range(self.m_nlabel):
            sumx = 0
            sumy = 0
            Gsum = 0
            self.m_AbnormalRegion[i].m_nLeft = self.m_AbnormalRegion[i].m_posArea[0].nY
            self.m_AbnormalRegion[i].m_nRight = self.m_AbnormalRegion[i].m_posArea[0].nY
            self.m_AbnormalRegion[i].m_nTop = self.m_AbnormalRegion[i].m_posArea[0].nX
            self.m_AbnormalRegion[i].m_nBottom = self.m_AbnormalRegion[i].m_posArea[0].nX
            for j in range(len(self.m_AbnormalRegion[i].m_posArea)):
                x = self.m_AbnormalRegion[i].m_posArea[j].nX
                y = self.m_AbnormalRegion[i].m_posArea[j].nY
                sumx += x
                sumy += y
                Gsum += self.m_CellInfor[x][y].m_fTemperture_Vary_Rate
                if self.m_AbnormalRegion[i].m_posArea[j].nY < self.m_AbnormalRegion[i].m_nLeft:
                    self.m_AbnormalRegion[i].m_nLeft = self.m_AbnormalRegion[i].m_posArea[j].nY
                if self.m_AbnormalRegion[i].m_posArea[j].nY > self.m_AbnormalRegion[i].m_nRight:
                    self.m_AbnormalRegion[i].m_nRight = self.m_AbnormalRegion[i].m_posArea[j].nY
                if self.m_AbnormalRegion[i].m_posArea[j].nX < self.m_AbnormalRegion[i].m_nTop:
                    self.m_AbnormalRegion[i].m_nTop = self.m_AbnormalRegion[i].m_posArea[j].nX
                if self.m_AbnormalRegion[i].m_posArea[j].nX > self.m_AbnormalRegion[i].m_nBottom:
                    self.m_AbnormalRegion[i].m_nBottom = self.m_AbnormalRegion[i].m_posArea[j].nX

            self.m_AbnormalRegion[i].m_nWidth = self.m_AbnormalRegion[i].m_nRight - self.m_AbnormalRegion[i].m_nLeft + 1
            self.m_AbnormalRegion[i].m_nHeight = self.m_AbnormalRegion[i].m_nBottom - self.m_AbnormalRegion[i].m_nTop + 1
            self.m_AbnormalRegion[i].m_fArea = self.m_AbnormalRegion[i].m_nTotal_Count
            self.m_AbnormalRegion[i].m_Central_Point.nX = sumx // self.m_AbnormalRegion[i].m_nTotal_Count
            self.m_AbnormalRegion[i].m_Central_Point.nY = sumy // self.m_AbnormalRegion[i].m_nTotal_Count
            self.m_AbnormalRegion[i].m_Gave = Gsum / self.m_AbnormalRegion[i].m_nTotal_Count


            # 计算当前异常区域轮廓的傅里叶描述子
            Edge_num = len(self.m_AbnormalRegion[i].m_posEdge)
            set_fourier_points = 30     # 取前30个系数作为傅里叶描述子
            fourier_num = set_fourier_points + 1   # 实际的傅里叶描述子的数量(取前20个,加上第一个0共21个元素)
            f = np.zeros(Edge_num)     # 轮廓的实际描述子
            fd = np.zeros(fourier_num)
            for u in range(Edge_num):
                Sumx = 0
                Sumy = 0
                for p in range(Edge_num):
                    pX = self.m_AbnormalRegion[i].m_posEdge[p].nX
                    pY = self.m_AbnormalRegion[i].m_posEdge[p].nY
                    Sumx += float(pX * math.cos(2 * math.pi * u * p / Edge_num) + pY * math.sin(2 * math.pi * u * p / Edge_num))
                    Sumy += float(pY * math.cos(2 * math.pi * u * p / Edge_num) - pX * math.sin(2 * math.pi * u * p / Edge_num))

                f[u] = math.sqrt(Sumx * Sumx + Sumy * Sumy)

            # 傅里叶描述子归一化
            f[0] = 0
            fd[0] = 0
            for k in range(2, min(fourier_num + 1, Edge_num)):      # 这里取min是考虑了边界点个数小于设定的傅里叶系数个数的情况
                f[k] = f[k] / f[1]
                fd[k - 1] = f[k]

            # 计算傅里叶描述子模长(作为特征值)
            sumw = 0
            for w in range(1, fourier_num):
                sumw += fd[w] * fd[w]

            fea_fourier = math.sqrt(sumw)
            self.m_AbnormalRegion[i].mfou_descriptor = fea_fourier






class Feature(CAbormityAreaDetect):
    def __init__(self):
        super(Feature, self).__init__()
        self.Mold_Nums = gl.Variable().Mold_Nums
        self.TimeMaxCount = gl.Variable().nTime_Window
        self.Time_interval = gl.Variable().Time_Interval


        self.m_AbnormalReion_Time_Change = np.empty((self.Mold_Nums, self.TimeMaxCount), dtype = object)
        for i in range(self.Mold_Nums):
            for j in range(self.TimeMaxCount):
                self.m_AbnormalReion_Time_Change[i][j] = CAbormityAreaDetect()


    def Feature_detection(self, Vx, Vy, Vc, Sticking_Expansion, Breakout_Center_Dis, tb, Height, Width, Area, Edgenum, Gave, Fourier, Sticking_Center, Abnormal_Center, Vertical_distance, Mold_Width, Mold_Thick, Casting_Speed, timenow):
        i_temp = -1
        HEIGHT_COUNT = gl.Variable().HEIGHT_COUNT
        WIDE_COUNT = gl.Variable().WIDE_COUNT
        NARROW_COUNT = gl.Variable().NARROW_COUNT

        Time_count = timenow
        #python里numpy默认的是浅拷贝，即拷贝的是对象的地址，结果是修改拷贝的值的时候原对象也会随之改变;
        #解决方案是使用ndarray.copy()进行深拷贝，即拷贝numpy对象中的数据，而不是地址
        self.m_AbnormalReion_Time_Change[tb][Time_count].m_AbnormalRegion = self.m_AbnormalRegion.copy()
        self.m_AbnormalReion_Time_Change[tb][Time_count].m_nAbnormity_Area_Count = self.m_nAbnormity_Area_Count
        if Time_count >= 5:
            n_now = len(self.m_AbnormalReion_Time_Change[tb][Time_count].m_AbnormalRegion)
            if n_now != 0:
                for i in range(n_now):
                    # 收集每个异常区域重心
                    Abnormal_CenterX = self.m_AbnormalRegion[i].m_Central_Point.nX
                    Abnormal_CenterY = self.m_AbnormalRegion[i].m_Central_Point.nY
                    Abnormal_Center[tb].append((Abnormal_CenterX, Abnormal_CenterY))
                    if self.m_AbnormalReion_Time_Change[tb][Time_count].m_AbnormalRegion[i].m_nTop != 0:
                        continue
                    else:
                        Cen_now_x = self.m_AbnormalReion_Time_Change[tb][Time_count].m_AbnormalRegion[i].m_Central_Point.nX
                        Cen_now_y = self.m_AbnormalReion_Time_Change[tb][Time_count].m_AbnormalRegion[i].m_Central_Point.nY

                        n_pre = len(self.m_AbnormalReion_Time_Change[tb][Time_count-self.Time_interval].m_AbnormalRegion)
                        if n_pre != 0:
                            for j in range(n_pre):
                                Cen_pre_x = self.m_AbnormalReion_Time_Change[tb][Time_count - self.Time_interval].m_AbnormalRegion[j].m_Central_Point.nX
                                Cen_pre_y = self.m_AbnormalReion_Time_Change[tb][Time_count - self.Time_interval].m_AbnormalRegion[j].m_Central_Point.nY
                                if self.m_AbnormalReion_Time_Change[tb][Time_count - self.Time_interval].m_AbnormalRegion[j].m_nTop != 0 or Cen_now_x < Cen_pre_x - 10 or abs(Cen_now_y - Cen_pre_y) >= 30:
                                    continue
                                else:

                                    kx = Vertical_distance / HEIGHT_COUNT
                                    if self.m_nNum_Col == WIDE_COUNT:
                                        ky = Mold_Width / WIDE_COUNT
                                    else:
                                        ky = Mold_Thick / NARROW_COUNT

                                Vx[tb].append((Cen_now_x - Cen_pre_x) * kx * 0.06 / self.Time_interval)   #单位是m/min
                                Vy[tb].append((Cen_pre_y - Cen_now_y) * ky * 0.06 / self.Time_interval)
                                Vc[tb].append(Casting_Speed)

                                ###################################################################计算黏结区域动态扩展面积
                                # 存储异常区域self.Time_interval内每秒钟重心距起点和终点距离值之和的最小值
                                dis_Cen_pre_list = []
                                # 存储异常区域self.Time_interval内每一时刻满足条件的所有异常区域重心距起点和终点距离和
                                dis_Cen_pre_t_list = []
                                # # 存储异常区域内高温度速率核心区所占比例(Tv>=0.6)
                                # pp_core_Tv = []
                                # 存储异常区域self.Time_interval内每一时刻满足条件的所有异常区域的面积值
                                abnormal_area_pre_t_list = []
                                # 面积异常值(用于搜索重心失败的情况)
                                Abnormal_Area_Max = 10000
                                # # 温度速率阈值(大于阈值的为高温度速率核心区)
                                # Tv_Thre = 0.6
                                # self.Time_interval时间范围内黏结区域重心距起点和终点的距离范围
                                dis_min = 2
                                dis_max = 71
                                # 存储从0时刻至self.Time_interval时刻黏结区域的面积
                                Sticking_Area = np.zeros(self.Time_interval + 1)
                                Sticking_Area[0] = self.m_AbnormalReion_Time_Change[tb][Time_count - self.Time_interval].m_AbnormalRegion[j].m_fArea * kx * ky * 0.01
                                Sticking_Area[self.Time_interval] = self.m_AbnormalReion_Time_Change[tb][Time_count].m_AbnormalRegion[i].m_fArea * kx * ky * 0.01
                                # # 存储从0时刻至self.Time_interval时刻高温度速率核心区的比例
                                # PP_High_Tv_Area = np.zeros(self.Time_interval + 1)
                                #
                                # core_Tv_num = 0
                                # for p in range(len(self.m_AbnormalReion_Time_Change[tb][Time_count - self.Time_interval].m_AbnormalRegion[j].m_posArea)):
                                #     pX = self.m_AbnormalReion_Time_Change[tb][Time_count - self.Time_interval].m_AbnormalRegion[j].m_posArea[p].nX
                                #     pY = self.m_AbnormalReion_Time_Change[tb][Time_count - self.Time_interval].m_AbnormalRegion[j].m_posArea[p].nY
                                #     if self.m_CellInfor[pX][pY].m_fTemperture_Vary_Rate >= Tv_Thre:
                                #         core_Tv_num += 1
                                #     else:
                                #         pass
                                # PP_High_Tv_Area[0] = core_Tv_num / self.m_AbnormalReion_Time_Change[tb][Time_count - self.Time_interval].m_AbnormalRegion[j].m_nTotal_Count
                                #
                                # core_Tv_num = 0
                                # for p in range(len(self.m_AbnormalReion_Time_Change[tb][Time_count].m_AbnormalRegion[i].m_posArea)):
                                #     pX = self.m_AbnormalReion_Time_Change[tb][Time_count].m_AbnormalRegion[i].m_posArea[p].nX
                                #     pY = self.m_AbnormalReion_Time_Change[tb][Time_count].m_AbnormalRegion[i].m_posArea[p].nY
                                #     if self.m_CellInfor[pX][pY].m_fTemperture_Vary_Rate >= Tv_Thre:
                                #         core_Tv_num += 1
                                #     else:
                                #         pass
                                # PP_High_Tv_Area[self.Time_interval] = core_Tv_num / self.m_AbnormalReion_Time_Change[tb][Time_count].m_AbnormalRegion[i].m_nTotal_Count


                                for t in range(1, self.Time_interval):
                                    dis_Cen_pre_t_list.clear()
                                    abnormal_area_pre_t_list.clear()
                                    # pp_core_Tv.clear()
                                    for num in range(self.m_AbnormalReion_Time_Change[tb][Time_count - t].m_nAbnormity_Area_Count):
                                        Cen_pre_t_x = self.m_AbnormalReion_Time_Change[tb][Time_count - t].m_AbnormalRegion[num].m_Central_Point.nX
                                        Cen_pre_t_y = self.m_AbnormalReion_Time_Change[tb][Time_count - t].m_AbnormalRegion[num].m_Central_Point.nY

                                        # 计算(Time_count - t)时刻黏结区域重心距起点和终点的欧式距离
                                        dis_Cen_pre = pow((pow(Cen_pre_t_x - Cen_pre_x, 2) + pow(Cen_pre_t_y - Cen_pre_y, 2)), 1/2)
                                        dis_Cen_now = pow((pow(Cen_pre_t_x - Cen_now_x, 2) + pow(Cen_pre_t_y - Cen_now_y, 2)), 1/2)
                                        dis_Cen_pre_t = dis_Cen_pre + dis_Cen_now
                                        if dis_min <= dis_Cen_pre_t <= dis_max and \
                                        self.m_AbnormalReion_Time_Change[tb][Time_count - t].m_AbnormalRegion[num].m_nTop == 0:
                                            dis_Cen_pre_t_list.append(dis_Cen_pre_t)
                                            abnormal_area_pre_t_list.append(self.m_AbnormalReion_Time_Change[tb][Time_count - t].m_AbnormalRegion[num].m_fArea * kx * ky * 0.01)
                                            # core_Tv_num = 0
                                            # for p in range(len(self.m_AbnormalReion_Time_Change[tb][Time_count - t].m_AbnormalRegion[num].m_posArea)):
                                            #     pX = self.m_AbnormalReion_Time_Change[tb][Time_count - t].m_AbnormalRegion[num].m_posArea[p].nX
                                            #     pY = self.m_AbnormalReion_Time_Change[tb][Time_count - t].m_AbnormalRegion[num].m_posArea[p].nY
                                            #     if self.m_CellInfor[pX][pY].m_fTemperture_Vary_Rate >= Tv_Thre:
                                            #         core_Tv_num += 1
                                            #     else:
                                            #         pass
                                            #
                                            # pp_core_Tv.append(core_Tv_num / self.m_AbnormalReion_Time_Change[tb][Time_count - t].m_AbnormalRegion[num].m_nTotal_Count)


                                        else:
                                            pass

                                    if dis_Cen_pre_t_list:
                                        dis_Cen_pre_list.append(min(dis_Cen_pre_t_list))
                                        dis_min_index = dis_Cen_pre_t_list.index(min(dis_Cen_pre_t_list))
                                        Sticking_Area[self.Time_interval - t] = abnormal_area_pre_t_list[dis_min_index]
                                                                              # = pp_core_Tv[dis_min_index]
                                    else:
                                        dis_Cen_pre_list.append([])
                                        Sticking_Area[self.Time_interval - t] = Abnormal_Area_Max

                                # 去除dis_Cen_pre_list中所有空列表
                                while dis_Cen_pre_list:
                                    if [] in dis_Cen_pre_list:
                                        dis_Cen_pre_list.remove([])
                                    else:
                                        break

                                # 退出while循环有两种情况:1.dis_Cen_pre_list中所有[]被去除但其本身不为空
                                # 2.dis_Cen_pre_list去除所有[]之后其本身也为[]不满足while循环条件
                                if dis_Cen_pre_list:
                                    Breakout_Center_Dis[tb].append((min(dis_Cen_pre_list), max(dis_Cen_pre_list)))
                                else:
                                    Breakout_Center_Dis[tb].append([])

                                # 计算黏结区域扩展面积因子
                                Area_Expansion_Factor = 0
                                for k in range(self.Time_interval):
                                    Area_Expansion_Factor += (Sticking_Area[k + 1] - Sticking_Area[k]) / Sticking_Area[k + 1]

                                Sticking_Expansion[tb].append(Area_Expansion_Factor)
                                #######################################################################################


                                if i == i_temp:
                                    Height[tb].append(Height[tb][-1])
                                    Width[tb].append(Width[tb][-1])
                                    Area[tb].append(Area[tb][-1])
                                    Edgenum[tb].append(Edgenum[tb][-1])
                                    Gave[tb].append(Gave[tb][-1])
                                    Fourier[tb].append(Fourier[tb][-1])
                                    Sticking_Center[tb].append(Sticking_Center[tb][-1])
                                    continue

                                i_temp = i
                                Height[tb].append(self.m_AbnormalRegion[i].m_nHeight * kx * 0.1)    #单位是cm
                                Width[tb].append(self.m_AbnormalRegion[i].m_nWidth * ky * 0.1)
                                Area[tb].append(self.m_AbnormalRegion[i].m_fArea * kx * ky * 0.01)     #单位是cm2
                                Edgenum[tb].append(len(self.m_AbnormalRegion[i].m_posEdge))
                                Gave[tb].append(self.m_AbnormalRegion[i].m_Gave)
                                Fourier[tb].append(self.m_AbnormalRegion[i].mfou_descriptor)
                                Center_X = self.m_AbnormalRegion[i].m_Central_Point.nX
                                Center_Y = self.m_AbnormalRegion[i].m_Central_Point.nY
                                Sticking_Center[tb].append((Center_X, Center_Y))





class CMoldPlate():
    def __init__(self):
        self.m_nHeight_Count = 0
        self.m_nWide_Row_Count = 0
        self.m_nNarrow_Row_Count = 0

        self.Mold_Nums = gl.Variable().Mold_Nums

        self.Height = []
        self.Width = []
        self.Area = []
        self.Edgenum = []   #黏结区域轮廓点数量
        self.Vx = []
        self.Vy = []
        self.Vc = []
        self.Gave = []
        self.Fourier = []
        self.Sticking_Center = []
        # 包含了各铜板所有异常区域重心的列表
        self.Abnormal_Center = []
        # 各铜板所有黏结区域加权扩展面积
        self.Sticking_Expansion = []
        # 各铜板黏结区域在5s内重心距起点和终点距离之和的最值
        self.Breakout_Center_Dis = []

        self.m_LeftNarrow = Feature()
        self.m_OuterWide = Feature()
        self.m_RightNarrow = Feature()
        self.m_InnerWide = Feature()

        self.CEDIAN_HEIGHT = gl.Variable().CEDIAN_HEIGHT

        self.m_LeftNarrowCrack = np.empty(self.CEDIAN_HEIGHT, dtype = object)
        self.m_OuterWideCrack = np.empty(self.CEDIAN_HEIGHT, dtype = object)
        self.m_RightNarrowCrack = np.empty(self.CEDIAN_HEIGHT, dtype = object)
        self.m_InnerWideCrack = np.empty(self.CEDIAN_HEIGHT, dtype = object)


        for row in range(self.CEDIAN_HEIGHT):

            self.m_LeftNarrowCrack[row] = Feature()
            self.m_OuterWideCrack[row] = Feature()
            self.m_RightNarrowCrack[row] = Feature()
            self.m_InnerWideCrack[row] = Feature()


        self.HEIGHT_COUNT = gl.Variable().HEIGHT_COUNT
        self.WIDE_COUNT = gl.Variable().WIDE_COUNT
        self.NARROW_COUNT = gl.Variable().NARROW_COUNT


    def Set_Grid_Num(self, nWideRow, nNarrowRow, nHeight):

        self.m_OuterWide.Set_Cell_Num(nHeight, nWideRow)
        self.m_InnerWide.Set_Cell_Num(nHeight, nWideRow)
        self.m_LeftNarrow.Set_Cell_Num(nHeight, nNarrowRow)
        self.m_RightNarrow.Set_Cell_Num(nHeight, nNarrowRow)

    def Set_Grid_NumCrack(self, nWideRow, nNarrowRow, nHeight):

        for row in range(self.CEDIAN_HEIGHT):

            self.m_OuterWideCrack[row].Set_Cell_Num(nHeight, nWideRow)
            self.m_InnerWideCrack[row].Set_Cell_Num(nHeight, nWideRow)
            self.m_LeftNarrowCrack[row].Set_Cell_Num(nHeight, nNarrowRow)
            self.m_RightNarrowCrack[row].Set_Cell_Num(nHeight, nNarrowRow)

    def Initialize(self):

        if gl.get_value("accident_type") == "漏钢":

            fTemperature_Rising_Rate_Limit = 0.3

            self.m_LeftNarrow.Set_Rising_Rate_Limit(fTemperature_Rising_Rate_Limit)
            self.m_OuterWide.Set_Rising_Rate_Limit(fTemperature_Rising_Rate_Limit)
            self.m_RightNarrow.Set_Rising_Rate_Limit(fTemperature_Rising_Rate_Limit)
            self.m_InnerWide.Set_Rising_Rate_Limit(fTemperature_Rising_Rate_Limit)

            HEIGHT_COUNT = gl.Variable().HEIGHT_COUNT
            WIDE_COUNT = gl.Variable().WIDE_COUNT
            NARROW_COUNT = gl.Variable().NARROW_COUNT

            self.Set_Grid_Num(WIDE_COUNT, NARROW_COUNT, HEIGHT_COUNT)

        elif gl.get_value("accident_type") == "纵裂":

            fTemperature_Rising_Rate_Limit = -8.0

            for row in range(self.CEDIAN_HEIGHT):

                self.m_LeftNarrowCrack[row].Set_Rising_Rate_Limit(fTemperature_Rising_Rate_Limit)
                self.m_OuterWideCrack[row].Set_Rising_Rate_Limit(fTemperature_Rising_Rate_Limit)
                self.m_RightNarrowCrack[row].Set_Rising_Rate_Limit(fTemperature_Rising_Rate_Limit)
                self.m_InnerWideCrack[row].Set_Rising_Rate_Limit(fTemperature_Rising_Rate_Limit)

            HEIGHT_COUNT = gl.Variable().HEIGHT_COUNT_CRACK
            WIDE_COUNT = gl.Variable().WIDE_COUNT
            NARROW_COUNT = gl.Variable().NARROW_COUNT

            self.Set_Grid_NumCrack(WIDE_COUNT, NARROW_COUNT, HEIGHT_COUNT)

        else:
            print("铜板初始化出错!")

    def Clear(self, accidentType):

        if accidentType == "漏钢":

            self.m_LeftNarrow.Clear()
            self.m_OuterWide.Clear()
            self.m_RightNarrow.Clear()
            self.m_InnerWide.Clear()

        elif accidentType == "纵裂":

            for row in range(self.CEDIAN_HEIGHT):

                self.m_LeftNarrowCrack[row].Clear()
                self.m_OuterWideCrack[row].Clear()
                self.m_RightNarrowCrack[row].Clear()
                self.m_InnerWideCrack[row].Clear()

        else:
            print("铜板数据清空失败!")

    def Load_Data_Judge_Status(self, pfWideOuter, pfRightNarrow, pfWideInner, pfLeftNarrow):

        for i in range(self.m_OuterWide.m_nNum_Row):
            for j in range(self.m_OuterWide.m_nNum_Col):

                if pfWideOuter[i][j] < self.m_OuterWide.m_fTemperature_Rising_Rate_Limit:
                    self.m_OuterWide.m_CellInfor[i][j].m_bIs_Abnormal = False
                    self.m_OuterWide.m_CellInfor[i][j].m_nAbnormity_Area_Num = 0
                    self.m_OuterWide.m_CellInfor[i][j].m_fTemperture_Vary_Rate = pfWideOuter[i][j] = 0
                else:
                    self.m_OuterWide.m_CellInfor[i][j].m_bIs_Abnormal = True
                    self.m_OuterWide.m_CellInfor[i][j].m_nAbnormity_Area_Num = 255
                    self.m_OuterWide.m_CellInfor[i][j].m_fTemperture_Vary_Rate = pfWideOuter[i][j]


                if pfWideInner[i][j] < self.m_InnerWide.m_fTemperature_Rising_Rate_Limit:
                    self.m_InnerWide.m_CellInfor[i][j].m_bIs_Abnormal = False
                    self.m_InnerWide.m_CellInfor[i][j].m_nAbnormity_Area_Num = 0
                    self.m_InnerWide.m_CellInfor[i][j].m_fTemperture_Vary_Rate = pfWideInner[i][j] = 0
                else:
                    self.m_InnerWide.m_CellInfor[i][j].m_bIs_Abnormal = True
                    self.m_InnerWide.m_CellInfor[i][j].m_nAbnormity_Area_Num = 255
                    self.m_InnerWide.m_CellInfor[i][j].m_fTemperture_Vary_Rate = pfWideInner[i][j]

                if j < self.m_RightNarrow.m_nNum_Col:

                    if pfRightNarrow[i][j] < self.m_RightNarrow.m_fTemperature_Rising_Rate_Limit:
                        self.m_RightNarrow.m_CellInfor[i][j].m_bIs_Abnormal = False
                        self.m_RightNarrow.m_CellInfor[i][j].m_nAbnormity_Area_Num = 0
                        self.m_RightNarrow.m_CellInfor[i][j].m_fTemperture_Vary_Rate = pfRightNarrow[i][j] = 0
                    else:
                        self.m_RightNarrow.m_CellInfor[i][j].m_bIs_Abnormal = True
                        self.m_RightNarrow.m_CellInfor[i][j].m_nAbnormity_Area_Num = 255
                        self.m_RightNarrow.m_CellInfor[i][j].m_fTemperture_Vary_Rate = pfRightNarrow[i][j]


                    if pfLeftNarrow[i][j] < self.m_LeftNarrow.m_fTemperature_Rising_Rate_Limit:
                        self.m_LeftNarrow.m_CellInfor[i][j].m_bIs_Abnormal = False
                        self.m_LeftNarrow.m_CellInfor[i][j].m_nAbnormity_Area_Num = 0
                        self.m_LeftNarrow.m_CellInfor[i][j].m_fTemperture_Vary_Rate = pfLeftNarrow[i][j] = 0
                    else:
                        self.m_LeftNarrow.m_CellInfor[i][j].m_bIs_Abnormal = True
                        self.m_LeftNarrow.m_CellInfor[i][j].m_nAbnormity_Area_Num = 255
                        self.m_LeftNarrow.m_CellInfor[i][j].m_fTemperture_Vary_Rate = pfLeftNarrow[i][j]



    def Load_Data_Judge_Status_Crack(self, pfWideOuter, pfRightNarrow, pfWideInner, pfLeftNarrow):

        for row in range(self.CEDIAN_HEIGHT):
            for i in range(self.m_OuterWideCrack[row].m_nNum_Row):
                for j in range(self.m_OuterWideCrack[row].m_nNum_Col):

                    self.m_OuterWideCrack[row].m_CellInfor[i][j].m_fTemperture_Vary_Rate = pfWideOuter[row][i][j]
                    self.m_InnerWideCrack[row].m_CellInfor[i][j].m_fTemperture_Vary_Rate = pfWideInner[row][i][j]

                    if pfWideOuter[row][i][j] > self.m_OuterWideCrack[row].m_fTemperature_Rising_Rate_Limit:
                        self.m_OuterWideCrack[row].m_CellInfor[i][j].m_bIs_Abnormal = False
                        self.m_OuterWideCrack[row].m_CellInfor[i][j].m_nAbnormity_Area_Num = 0

                    else:
                        self.m_OuterWideCrack[row].m_CellInfor[i][j].m_bIs_Abnormal = True
                        self.m_OuterWideCrack[row].m_CellInfor[i][j].m_nAbnormity_Area_Num = 255


                    if pfWideInner[row][i][j] > self.m_InnerWideCrack[row].m_fTemperature_Rising_Rate_Limit:
                        self.m_InnerWideCrack[row].m_CellInfor[i][j].m_bIs_Abnormal = False
                        self.m_InnerWideCrack[row].m_CellInfor[i][j].m_nAbnormity_Area_Num = 0

                    else:
                        self.m_InnerWideCrack[row].m_CellInfor[i][j].m_bIs_Abnormal = True
                        self.m_InnerWideCrack[row].m_CellInfor[i][j].m_nAbnormity_Area_Num = 255


                    if j < self.m_RightNarrowCrack[row].m_nNum_Col:

                        self.m_RightNarrowCrack[row].m_CellInfor[i][j].m_fTemperture_Vary_Rate = pfRightNarrow[row][i][j]
                        self.m_LeftNarrowCrack[row].m_CellInfor[i][j].m_fTemperture_Vary_Rate = pfLeftNarrow[row][i][j]

                        if pfRightNarrow[row][i][j] > self.m_RightNarrowCrack[row].m_fTemperature_Rising_Rate_Limit:
                            self.m_RightNarrowCrack[row].m_CellInfor[i][j].m_bIs_Abnormal = False
                            self.m_RightNarrowCrack[row].m_CellInfor[i][j].m_nAbnormity_Area_Num = 0

                        else:
                            self.m_RightNarrowCrack[row].m_CellInfor[i][j].m_bIs_Abnormal = True
                            self.m_RightNarrowCrack[row].m_CellInfor[i][j].m_nAbnormity_Area_Num = 255


                        if pfLeftNarrow[row][i][j] > self.m_LeftNarrowCrack[row].m_fTemperature_Rising_Rate_Limit:
                            self.m_LeftNarrowCrack[row].m_CellInfor[i][j].m_bIs_Abnormal = False
                            self.m_LeftNarrowCrack[row].m_CellInfor[i][j].m_nAbnormity_Area_Num = 0

                        else:
                            self.m_LeftNarrowCrack[row].m_CellInfor[i][j].m_bIs_Abnormal = True
                            self.m_LeftNarrowCrack[row].m_CellInfor[i][j].m_nAbnormity_Area_Num = 255



    def Detect_Abnormal_Area(self):

        NEIGHBOR_HOODS_PLAN = self.m_OuterWide.m_NEIGHBOR_HOODS_8

        # 区域连通性标记
        self.m_OuterWide.Two_Pass(self.m_OuterWide.m_CellInfor, NEIGHBOR_HOODS_PLAN)
        self.m_OuterWide.reorganize(self.m_OuterWide.m_CellInfor)

        self.m_RightNarrow.Two_Pass(self.m_RightNarrow.m_CellInfor, NEIGHBOR_HOODS_PLAN)
        self.m_RightNarrow.reorganize(self.m_RightNarrow.m_CellInfor)

        self.m_InnerWide.Two_Pass(self.m_InnerWide.m_CellInfor, NEIGHBOR_HOODS_PLAN)
        self.m_InnerWide.reorganize(self.m_InnerWide.m_CellInfor)

        self.m_LeftNarrow.Two_Pass(self.m_LeftNarrow.m_CellInfor, NEIGHBOR_HOODS_PLAN)
        self.m_LeftNarrow.reorganize(self.m_LeftNarrow.m_CellInfor)


        # 将小区域删除
        self.m_OuterWide.Delete_And_Number()
        self.m_RightNarrow.Delete_And_Number()
        self.m_InnerWide.Delete_And_Number()
        self.m_LeftNarrow.Delete_And_Number()

        # 轮廓提取
        self.m_OuterWide.Contour_Extraction()
        self.m_RightNarrow.Contour_Extraction()
        self.m_InnerWide.Contour_Extraction()
        self.m_LeftNarrow.Contour_Extraction()



    def Detect_Abnormal_AreaCrack(self):

        for row in range(self.CEDIAN_HEIGHT):

            NEIGHBOR_HOODS_PLAN = self.m_OuterWideCrack[row].m_NEIGHBOR_HOODS_8

            #区域连通性标记
            self.m_OuterWideCrack[row].Two_Pass(self.m_OuterWideCrack[row].m_CellInfor, NEIGHBOR_HOODS_PLAN)
            self.m_OuterWideCrack[row].reorganize(self.m_OuterWideCrack[row].m_CellInfor)

            self.m_RightNarrowCrack[row].Two_Pass(self.m_RightNarrowCrack[row].m_CellInfor, NEIGHBOR_HOODS_PLAN)
            self.m_RightNarrowCrack[row].reorganize(self.m_RightNarrowCrack[row].m_CellInfor)

            self.m_InnerWideCrack[row].Two_Pass(self.m_InnerWideCrack[row].m_CellInfor, NEIGHBOR_HOODS_PLAN)
            self.m_InnerWideCrack[row].reorganize(self.m_InnerWideCrack[row].m_CellInfor)

            self.m_LeftNarrowCrack[row].Two_Pass(self.m_LeftNarrowCrack[row].m_CellInfor, NEIGHBOR_HOODS_PLAN)
            self.m_LeftNarrowCrack[row].reorganize(self.m_LeftNarrowCrack[row].m_CellInfor)


            #将小区域删除
            self.m_OuterWideCrack[row].Delete_And_Number()
            self.m_RightNarrowCrack[row].Delete_And_Number()
            self.m_InnerWideCrack[row].Delete_And_Number()
            self.m_LeftNarrowCrack[row].Delete_And_Number()



    def Cal_Feature(self, var, timenow):
        #计算静态特征
        self.m_OuterWide.Calculate_Feature()
        self.m_RightNarrow.Calculate_Feature()
        self.m_InnerWide.Calculate_Feature()
        self.m_LeftNarrow.Calculate_Feature()

        Slab_Width = var.fSlab_Width[timenow]
        Slab_Thick = var.fSlab_Thick[timenow]
        Casting_Speed = var.fCasting_Speed[timenow]

        tb = 0
        Simulation_Range = gl.Variable().Dis_First_Third_Row

        self.Height.clear()
        self.Width.clear()
        self.Area.clear()
        self.Edgenum.clear()
        self.Vx.clear()
        self.Vy.clear()
        self.Vc.clear()
        self.Gave.clear()
        self.Fourier.clear()
        self.Sticking_Center.clear()
        self.Abnormal_Center.clear()
        self.Sticking_Expansion.clear()
        self.Breakout_Center_Dis.clear()


        for _ in range(self.Mold_Nums):
            self.Height.append([])
            self.Width.append([])
            self.Area.append([])
            self.Edgenum.append([])
            self.Vx.append([])
            self.Vy.append([])
            self.Vc.append([])
            self.Gave.append([])
            self.Fourier.append([])
            self.Sticking_Center.append([])
            self.Abnormal_Center.append([])
            self.Sticking_Expansion.append([])
            self.Breakout_Center_Dis.append([])



        #计算动态特征
        self.m_OuterWide.Feature_detection(self.Vx, self.Vy, self.Vc, self.Sticking_Expansion, self.Breakout_Center_Dis, tb, self.Height, self.Width, self.Area, self.Edgenum, self.Gave,
                                           self.Fourier, self.Sticking_Center, self.Abnormal_Center, Simulation_Range, Slab_Width, Slab_Thick, Casting_Speed, timenow)
        tb += 1
        self.m_RightNarrow.Feature_detection(self.Vx, self.Vy, self.Vc, self.Sticking_Expansion, self.Breakout_Center_Dis, tb, self.Height, self.Width, self.Area, self.Edgenum, self.Gave,
                                             self.Fourier, self.Sticking_Center, self.Abnormal_Center, Simulation_Range, Slab_Width, Slab_Thick, Casting_Speed, timenow)
        tb += 1
        self.m_InnerWide.Feature_detection(self.Vx, self.Vy, self.Vc, self.Sticking_Expansion, self.Breakout_Center_Dis, tb, self.Height, self.Width, self.Area, self.Edgenum, self.Gave,
                                           self.Fourier, self.Sticking_Center, self.Abnormal_Center, Simulation_Range, Slab_Width, Slab_Thick, Casting_Speed, timenow)
        tb += 1
        self.m_LeftNarrow.Feature_detection(self.Vx, self.Vy, self.Vc, self.Sticking_Expansion, self.Breakout_Center_Dis, tb, self.Height, self.Width, self.Area, self.Edgenum, self.Gave,
                                            self.Fourier, self.Sticking_Center, self.Abnormal_Center, Simulation_Range, Slab_Width, Slab_Thick, Casting_Speed, timenow)
