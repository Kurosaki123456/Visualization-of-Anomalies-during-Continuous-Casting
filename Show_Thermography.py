from PyQt5.QtWidgets import QMessageBox, QApplication
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg  # pyqt5的画布
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import __init__ as gl
import numpy as np
import matplotlib as mpl


plt.rcParams['font.sans-serif']=['SimHei'] #显示中文标签
plt.rcParams['axes.unicode_minus']=False   #这两行需要手动设置



class Figure_Thermography(FigureCanvasQTAgg):
    def __init__(self, number_index = 0):

        self.figs = Figure()

        super(Figure_Thermography, self).__init__(self.figs)  # 在父类FigureCanvasQTAgg中激活figs，否则绘图失败
        # 调整子图位置及间距
        self.figs.subplots_adjust(left=0.02, bottom=0.02, right=1, top=0.90, wspace=0.5, hspace=0.3)
        # 清除当前figure中的所有axes
        self.figs.clf()

        # 划分网格
        self.grid = plt.GridSpec(2, 9)

##########################################################################################################
        HEIGHT_COUNT = gl.Variable().HEIGHT_COUNT
        WIDE_COUNT = gl.Variable().WIDE_COUNT
##########################################################################################################


###################################################################################################################
        # 绘制温度条
        self.axes5 = self.figs.add_subplot(self.grid[0, 8])
        self.axes5.set_title("温度条", fontsize=16, pad=13)
        # 温度区间插值数量
        self.interpolation_num_Tem = 255
        nums_Tem = np.linspace(50, 150, self.interpolation_num_Tem)
        # 设置温度条的格子数目
        colorbars_Tem = np.zeros((self.interpolation_num_Tem, 1))
        for i in range(self.interpolation_num_Tem):
            colorbars_Tem[i] = nums_Tem[i]

        # 颜色区间范围将(0-255)归一化至(0-1)
        color_bartem = [(0.5, 0.5, 0), (1, 1, 0), (1, 0, 0), (0, 0, 1), (0, 0, 0)]
        # 自定义cmap方案，"my_color"为方案名称，color为颜色区间，N为在颜色区间内插值的点数
        cm_ColorBarTem = mpl.colors.LinearSegmentedColormap.from_list("my_color_bar", color_bartem, N = self.interpolation_num_Tem)
        # extent[x0, x1, y0, y1]分别代表x轴最左侧的值,x轴最右侧的值,y轴最下面的值，y轴最上面的值;origin='upper'代表图从上往下画(右上角为(0,0)),lower相反从下往上画(左下角为(0,0));
        # 主要关注y轴的值[50,150],x轴的值[-10,10]只是为了图像美观而设的值
        self.axes5.imshow(colorbars_Tem, cmap = cm_ColorBarTem, extent=[-10, 10, 50, 150])
        self.axes5.set_xticks([])
        # 设置y轴刻度范围
        self.axes5.set_yticks(np.arange(50, 160, 20))
######################################################################################################################

######################################################################################################################
        # 绘制温度速率条
        self.axes10 = self.figs.add_subplot(self.grid[1, 8])
        self.axes10.set_title("温度速率条", fontsize=16, pad=13)
        # 温度速率区间插值数量
        self.interpolation_num_TemV = 255
        nums_TemV = np.linspace(-1.5, 1.5, self.interpolation_num_TemV)
        # 设置温度速率条的格子数目
        colorbars_TemV = np.zeros((self.interpolation_num_TemV, 1))
        for i in range(self.interpolation_num_TemV):
            colorbars_TemV[i] = nums_TemV[i]
        # 颜色区间范围将(0-255)归一化至(0-1)
        color_bartemv = [(1, 0, 0), (0.7687, 0.3765, 0.3765), (1, 1, 1), (0.3765, 0.3765, 0.7687), (0, 0, 1)]
        # 自定义cmap方案，"my_color"为方案名称，color为颜色区间，N为在颜色区间内插值的点数
        cm_ColorBarTemV = mpl.colors.LinearSegmentedColormap.from_list("my_color_bartemv", color_bartemv, N = self.interpolation_num_TemV)
        # e = np.random.random((100, 40))
        # extent[x0, x1, y0, y1]分别代表x轴最左侧的值,x轴最右侧的值,y轴最下面的值，y轴最上面的值;origin='upper'代表图从上往下画,lower相反从下往上画
        self.axes10.imshow(colorbars_TemV, cmap=cm_ColorBarTemV, extent=[-0.3, 0.3, -1.5, 1.5], origin='upper')
        self.axes10.set_xticks([])
        # 设置y轴刻度范围
        self.axes10.set_yticks(np.arange(-1.5, 1.6, 0.3))
######################################################################################################################

######################################################################################################################
        # 绘制温度热像图
        color_tem = [(0, 0, 0), (0, 0, 1), (1, 0, 0), (1, 1, 0), (0.5, 0.5, 0)]
        cm_ColorTem = mpl.colors.LinearSegmentedColormap.from_list("my_color_tem", color_tem, N = self.interpolation_num_Tem)
        norm_tem = mpl.colors.Normalize(vmin=50, vmax=150)

        self.axes1 = self.figs.add_subplot(self.grid[0, 0:3])  # 第一行的前三列列都添加到ax1中
        self.axes1_img = self.axes1.imshow(np.random.random((HEIGHT_COUNT, WIDE_COUNT)), cmap = cm_ColorTem, norm = norm_tem, aspect = 'auto')
        self.axes1.set_title("外弧宽面T", fontsize=16, pad=8)
        self.axes1.set_yticks(np.arange(0, 120, 20))
        self.axes1.set_xticks([])
        # twiny函数建立孪生y轴(与原来的共享)，并建立新的x轴(位置在原来的对面)
        self.twinaxes1 = self.axes1.twiny()
        self.twinaxes1.set_xticks(np.arange(0, 350, 50))


        self.axes2 = self.figs.add_subplot(self.grid[0, 3:6])
        self.axes2_img = self.axes2.imshow(np.random.random((HEIGHT_COUNT, WIDE_COUNT)), cmap = cm_ColorTem, norm = norm_tem, aspect = 'auto')
        self.axes2.set_title("内弧宽面T", fontsize=16, pad=8)
        self.axes2.set_yticks(np.arange(0, 120, 20))
        self.axes2.set_xticks([])
        # twiny函数建立孪生y轴(与原来的共享)，并建立新的x轴(位置在原来的对面)
        self.twinaxes2 = self.axes2.twiny()
        self.twinaxes2.set_xticks(np.arange(0, 350, 50))


        self.axes3 = self.figs.add_subplot(self.grid[0, 6])
        self.axes3_img = self.axes3.imshow(np.random.random((HEIGHT_COUNT, WIDE_COUNT)), cmap = cm_ColorTem, norm = norm_tem, aspect = 'auto')
        self.axes3.set_title("右侧窄面T", fontsize=16, pad=8)
        # 选择aspect = 'auto'让图像像素点自动填充坐标轴(只是显示的时候会拉伸像素,不影响保存结果)
        self.axes3.set_yticks(np.arange(0, 120, 20))
        self.axes3.set_xticks([])
        # twiny函数建立孪生y轴(与原来的共享)，并建立新的x轴(位置在原来的对面)
        self.twinaxes3 = self.axes3.twiny()
        self.twinaxes3.set_xticks(np.arange(0, 60, 20))


        self.axes4 = self.figs.add_subplot(self.grid[0, 7])
        self.axes4_img = self.axes4.imshow(np.random.random((HEIGHT_COUNT, WIDE_COUNT)), cmap = cm_ColorTem, norm = norm_tem, aspect = 'auto')
        self.axes4.set_title("左侧窄面T", fontsize=16, pad=8)
        # 选择aspect = 'auto'让图像像素点自动填充坐标轴(只是显示的时候会拉伸像素,不影响保存结果)
        self.axes4.set_yticks(np.arange(0, 120, 20))
        self.axes4.set_xticks([])
        # twiny函数建立孪生y轴(与原来的共享)，并建立新的x轴(位置在原来的对面)
        self.twinaxes4 = self.axes4.twiny()
        self.twinaxes4.set_xticks(np.arange(0, 60, 20))

#####################################################################################################################

#####################################################################################################################
        # 绘制温度速率热像图

        color_temv = [(0, 0, 1), (0.3765, 0.3765, 0.7687), (1, 1, 1), (0.7687, 0.3765, 0.3765), (1, 0, 0)]
        cm_ColorTemV = mpl.colors.LinearSegmentedColormap.from_list("my_color_temv", color_temv, N = self.interpolation_num_TemV)
        norm_temv = mpl.colors.Normalize(vmin = -1.5, vmax = 1.5)
        gl.set_value("cm_ColorTemV", cm_ColorTemV)

        self.axes6 = self.figs.add_subplot(self.grid[1, 0:3])  # 第一行的前三列列都添加到ax1中
        self.axes6_img = self.axes6.imshow(np.random.random((HEIGHT_COUNT, WIDE_COUNT)), cmap = cm_ColorTemV, norm = norm_temv, aspect = 'auto')
        self.axes6.set_yticks(np.arange(0, 120, 20))
        self.axes6.set_xticks([])
        # twiny函数建立孪生y轴(与原来的共享)，并建立新的x轴(位置在原来的对面)
        self.twinaxes6 = self.axes6.twiny()
        self.twinaxes6.set_xticks(np.arange(0, 350, 50))


        self.axes7 = self.figs.add_subplot(self.grid[1, 3:6])
        self.axes7_img = self.axes7.imshow(np.random.random((HEIGHT_COUNT, WIDE_COUNT)), cmap = cm_ColorTemV, norm = norm_temv, aspect = 'auto')
        self.axes7.set_yticks(np.arange(0, 120, 20))
        self.axes7.set_xticks([])
        # twiny函数建立孪生y轴(与原来的共享)，并建立新的x轴(位置在原来的对面)
        self.twinaxes7 = self.axes7.twiny()
        self.twinaxes7.set_xticks(np.arange(0, 350, 50))


        self.axes8 = self.figs.add_subplot(self.grid[1, 6])
        self.axes8_img = self.axes8.imshow(np.random.random((HEIGHT_COUNT, WIDE_COUNT)), cmap = cm_ColorTemV, norm = norm_temv, aspect = 'auto')
        # 选择aspect = 'auto'让图像像素点自动填充坐标轴(只是显示的时候会拉伸像素,不影响保存结果)
        self.axes8.set_yticks(np.arange(0, 120, 20))
        self.axes8.set_xticks([])
        # twiny函数建立孪生y轴(与原来的共享)，并建立新的x轴(位置在原来的对面)
        self.twinaxes8 = self.axes8.twiny()
        self.twinaxes8.set_xticks(np.arange(0, 60, 20))


        self.axes9 = self.figs.add_subplot(self.grid[1, 7])
        self.axes9_img = self.axes9.imshow(np.random.random((HEIGHT_COUNT, WIDE_COUNT)), cmap = cm_ColorTemV, norm = norm_temv, aspect = 'auto')
        # 选择aspect = 'auto'让图像像素点自动填充坐标轴(只是显示的时候会拉伸像素,不影响保存结果)
        self.axes9.set_yticks(np.arange(0, 120, 20))
        self.axes9.set_xticks([])
        # twiny函数建立孪生y轴(与原来的共享)，并建立新的x轴(位置在原来的对面)
        self.twinaxes9 = self.axes9.twiny()
        self.twinaxes9.set_xticks(np.arange(0, 60, 20))


        self.number_index = number_index

        # if self.number_index == 0:
        #     self.figs.suptitle("The window of visualizing the images!", x = 0.5, y = 0.6, fontsize = 40,color = "k", alpha = 0.25)

    def LoadSampleInfo(self):

        if self.number_index != 0:
            # 获取当前数据源(南钢/鞍钢)
            DirPlantPath = gl.get_value("DirPlantPath")
            DirPlantPath_List = DirPlantPath.split("/")
            DataSrc = "南钢" if DirPlantPath_List[1] == "NanGang" else "鞍钢" if DirPlantPath_List[1] == "AnGang" else "None"
            gl.set_value('Data_Source', DataSrc)

            # 初始化variable对象
            variable = gl.Variable(plant = gl.get_value('Data_Source'), accident = gl.get_value("accident_type"))
            gl.set_value('Variable', variable)      #定义为全局字典变量

            Sample_List_Path = gl.get_value('SampleList')
            Sample_List = gl.loadDataSet(Sample_List_Path)

            # 设置全局变量
            date = Sample_List[self.number_index - 1][0]
            time = Sample_List[self.number_index - 1][1]
            sample_type = "漏钢" if Sample_List[self.number_index - 1][2] == "B" else "误报" \
                if Sample_List[self.number_index - 1][2] == "F" else "稳态"

            year, month, day = date[0:4], date[5:7], date[8:10]
            hour, minute, second = time[0:2], time[3:5], time[6:8]

            gl.set_value('TotalNum', len(Sample_List))
            gl.set_value('year', year)
            gl.set_value('month', month)
            gl.set_value('day', day)
            gl.set_value('hour', hour)
            gl.set_value('minute', minute)
            gl.set_value('second', second)
            gl.set_value('number_index', self.number_index)
            gl.set_value('SampleType', sample_type)
            gl.set_value("date", date)
            gl.set_value("time", time)


            try:
                paths = ""
                for i in range(len(DirPlantPath_List)):
                    paths += DirPlantPath_List[i] + "\\"
                filepath = paths + year + "\\" + month + "\\" + day + "\\PR" + year + month + day + "_" + hour + ".txt"
                gl.set_value("file_path", filepath)
                self.data_T = gl.loadDataSet(filepath)

            except Exception as err:
                print(err)
                QMessageBox.warning(self, "", "数据源不存在!", QMessageBox.Yes)

            nAlarm_Time = 0
            for i in range(len(self.data_T)):
                if self.data_T[i][1] == time:
                    nAlarm_Time = i
                    break

            gl.set_value("Alarm_Time", nAlarm_Time)

            nTime_Start = max(nAlarm_Time - variable.nTime_Window, 0)

            #选取在Time_Window内的数据
            variable.ReadProData(self.data_T[nTime_Start : nAlarm_Time])     #读入样例数据

            Slider_Time_List = []
            #将滑块数值与对应数据时刻对应起来
            for i in range(0, min(variable.nTime_Window, nAlarm_Time)):
                    dict = {i : self.data_T[i + nTime_Start][1]}
                    Slider_Time_List.append(dict)

            gl.set_value("Slider_Time", Slider_Time_List)


        else:
            QMessageBox.warning(self, "警告", "数据加载失败!", QMessageBox.Ok)



    def PlotImg(self, drawdata):

        if self.number_index != 0:

            # # 清除当前figure中的所有axes
            # self.figs.clf()

            self.axes1_img.set_data(drawdata['fOuterWide'])
            self.axes2_img.set_data(drawdata['fInnerWide'])
            self.axes3_img.set_data(drawdata['fRightNarrow'])
            self.axes4_img.set_data(drawdata['fLeftNarrow'])


            self.axes6_img.set_data(drawdata['fOuterWide_Trick'])
            self.axes7_img.set_data(drawdata['fInnerWide_Trick'])
            self.axes8_img.set_data(drawdata['fRightNarrow_Trick'])
            self.axes9_img.set_data(drawdata['fLeftNarrow_Trick'])


            # for i in range(len(drawdata['Abnormal_Center'][0])):
            #     Abnormal_nX_0 = drawdata['Abnormal_Center'][0][i][0]
            #     Abnormal_nY_0 = drawdata['Abnormal_Center'][0][i][1]
            #     self.axes6.scatter(Abnormal_nY_0, Abnormal_nX_0, color = 'black', s = 20)
            #
            # if not drawdata['Vx'][0]:
            #     self.axes6.set_title("外弧宽面Tv(无特征)", fontsize = 16, color = 'black', pad = 7)
            # else:
            #     self.axes6.set_title("外弧宽面Tv(有特征)", fontsize = 16, color = 'brown', fontweight = 'bold', pad = 7)
            #     for j in range(len(drawdata['Vx'][0])):
            #         Central_nX_0 = drawdata['Sticking_Center'][0][j][0]
            #         Central_nY_0 = drawdata['Sticking_Center'][0][j][1]
            #         self.axes6.scatter(Central_nY_0, Central_nX_0, color = 'blue', s = 20)     # 标注黏结区域重心位置
            #
            #
            #
            #
            #
            # for i in range(len(drawdata['Abnormal_Center'][2])):
            #     Abnormal_nX_2 = drawdata['Abnormal_Center'][2][i][0]
            #     Abnormal_nY_2 = drawdata['Abnormal_Center'][2][i][1]
            #     self.axes7.scatter(Abnormal_nY_2, Abnormal_nX_2, color = 'black', s = 20)
            #
            # if not drawdata['Vx'][2]:
            #     self.axes7.set_title("内弧宽面Tv(无特征)", fontsize = 16, color = 'black', pad = 7)
            # else:
            #     self.axes7.set_title("内弧宽面Tv(有特征)", fontsize = 16, color = 'brown', fontweight = 'bold', pad = 7)
            #     for j in range(len(drawdata['Vx'][2])):
            #         Central_nX_2 = drawdata['Sticking_Center'][2][j][0]
            #         Central_nY_2 = drawdata['Sticking_Center'][2][j][1]
            #         self.axes7.scatter(Central_nY_2, Central_nX_2, color = 'blue', s = 20)
            #
            #
            #
            #
            #
            # for i in range(len(drawdata['Abnormal_Center'][1])):
            #     Abnormal_nX_1 = drawdata['Abnormal_Center'][1][i][0]
            #     Abnormal_nY_1 = drawdata['Abnormal_Center'][1][i][1]
            #     self.axes8.scatter(Abnormal_nY_1, Abnormal_nX_1, color = 'black', s = 20)
            #
            # if not drawdata['Vx'][1]:
            #     self.axes8.set_title("右侧窄面Tv(无)", fontsize = 16, color = 'black', pad = 7)
            # else:
            #     self.axes8.set_title("右侧窄面Tv(有)", fontsize = 16, color = 'brown', fontweight = 'bold', pad = 7)
            #     for j in range(len(drawdata['Vx'][1])):
            #         Central_nX_1 = drawdata['Sticking_Center'][1][j][0]
            #         Central_nY_1 = drawdata['Sticking_Center'][1][j][1]
            #         self.axes8.scatter(Central_nY_1, Central_nX_1, color = 'blue', s = 20)
            #
            #
            #
            #
            # for i in range(len(drawdata['Abnormal_Center'][3])):
            #     Abnormal_nX_3 = drawdata['Abnormal_Center'][3][i][0]
            #     Abnormal_nY_3 = drawdata['Abnormal_Center'][3][i][1]
            #     self.axes9.scatter(Abnormal_nY_3, Abnormal_nX_3, color = 'black', s = 20)
            #
            # if not drawdata['Vx'][3]:
            #     self.axes9.set_title("左侧窄面Tv(无)", fontsize = 16, color = 'black', pad = 7)
            # else:
            #     self.axes9.set_title("左侧窄面Tv(有)", fontsize = 16, color = 'brown', fontweight = 'bold', pad = 7)
            #     for j in range(len(drawdata['Vx'][3])):
            #         Central_nX_3 = drawdata['Sticking_Center'][3][j][0]
            #         Central_nY_3 = drawdata['Sticking_Center'][3][j][1]
            #         self.axes9.scatter(Central_nY_3, Central_nX_3, color = 'blue', s = 20)



# ###################################################################################################################
#             # 绘制温度条
#             self.axes5 = self.figs.add_subplot(self.grid[0, 8])
#             self.axes5.set_title("温度条", fontsize=16, pad=13)
#             # 温度区间插值数量
#             self.interpolation_num_Tem = 255
#             nums_Tem = np.linspace(50, 150, self.interpolation_num_Tem)
#             # 设置温度条的格子数目
#             colorbars_Tem = np.zeros((self.interpolation_num_Tem, 1))
#             for i in range(self.interpolation_num_Tem):
#                 colorbars_Tem[i] = nums_Tem[i]
#
#             # 颜色区间范围将(0-255)归一化至(0-1)
#             color_bartem = [(0.5, 0.5, 0), (1, 1, 0), (1, 0, 0), (0, 0, 1), (0, 0, 0)]
#             # 自定义cmap方案，"my_color"为方案名称，color为颜色区间，N为在颜色区间内插值的点数
#             cm_ColorBarTem = mpl.colors.LinearSegmentedColormap.from_list("my_color_bar", color_bartem,
#                                                                           N=self.interpolation_num_Tem)
#             # extent[x0, x1, y0, y1]分别代表x轴最左侧的值,x轴最右侧的值,y轴最下面的值，y轴最上面的值;origin='upper'代表图从上往下画(右上角为(0,0)),lower相反从下往上画(左下角为(0,0));
#             # 主要关注y轴的值[50,150],x轴的值[-10,10]只是为了图像美观而设的值
#             self.axes5.imshow(colorbars_Tem, cmap=cm_ColorBarTem, extent=[-10, 10, 50, 150])
#             self.axes5.set_xticks([])
#             # 设置y轴刻度范围
#             self.axes5.set_yticks(np.arange(50, 160, 20))
# ######################################################################################################################
#
# ######################################################################################################################
#             # 绘制温度速率条
#             self.axes10 = self.figs.add_subplot(self.grid[1, 8])
#             self.axes10.set_title("温度速率条", fontsize=16, pad=13)
#             # 温度速率区间插值数量
#             self.interpolation_num_TemV = 255
#             nums_TemV = np.linspace(-1.5, 1.5, self.interpolation_num_TemV)
#             # 设置温度速率条的格子数目
#             colorbars_TemV = np.zeros((self.interpolation_num_TemV, 1))
#             for i in range(self.interpolation_num_TemV):
#                 colorbars_TemV[i] = nums_TemV[i]
#             # 颜色区间范围将(0-255)归一化至(0-1)
#             color_bartemv = [(1, 0, 0), (0.7687, 0.3765, 0.3765), (1, 1, 1), (0.3765, 0.3765, 0.7687), (0, 0, 1)]
#             # 自定义cmap方案，"my_color"为方案名称，color为颜色区间，N为在颜色区间内插值的点数
#             cm_ColorBarTemV = mpl.colors.LinearSegmentedColormap.from_list("my_color_bartemv", color_bartemv,
#                                                                            N=self.interpolation_num_TemV)
#             # e = np.random.random((100, 40))
#             # extent[x0, x1, y0, y1]分别代表x轴最左侧的值,x轴最右侧的值,y轴最下面的值，y轴最上面的值;origin='upper'代表图从上往下画,lower相反从下往上画
#             self.axes10.imshow(colorbars_TemV, cmap=cm_ColorBarTemV, extent=[-0.3, 0.3, -1.5, 1.5], origin='upper')
#             self.axes10.set_xticks([])
#             # 设置y轴刻度范围
#             self.axes10.set_yticks(np.arange(-1.5, 1.6, 0.3))
# ######################################################################################################################
#
# ######################################################################################################################
#             # 绘制温度热像图
#             color_tem = [(0, 0, 0), (0, 0, 1), (1, 0, 0), (1, 1, 0), (0.5, 0.5, 0)]
#             cm_ColorTem = mpl.colors.LinearSegmentedColormap.from_list("my_color_tem", color_tem, N = self.interpolation_num_Tem)
#             norm_tem = mpl.colors.Normalize(vmin = 50, vmax = 150)
#
#
#             self.axes1 = self.figs.add_subplot(self.grid[0, 0:3])  # 第一行的前三列列都添加到ax1中
#             self.axes1.imshow(drawdata['fOuterWide'], cmap = cm_ColorTem, norm = norm_tem, aspect = 'auto')
#             self.axes1.set_title("外弧宽面T", fontsize=16, pad=8)
#             self.axes1.set_yticks(np.arange(0, 120, 20))
#             self.axes1.set_xticks([])
#             # twiny函数建立孪生y轴(与原来的共享)，并建立新的x轴(位置在原来的对面)
#             self.twinaxes1 = self.axes1.twiny()
#             self.twinaxes1.set_xticks(np.arange(0, 350, 50))
#
#
#             self.axes2 = self.figs.add_subplot(self.grid[0, 3:6])
#             self.axes2.imshow(drawdata['fInnerWide'], cmap = cm_ColorTem, norm = norm_tem, aspect = 'auto')
#             self.axes2.set_title("内弧宽面T", fontsize=16, pad=8)
#             self.axes2.set_yticks(np.arange(0, 120, 20))
#             self.axes2.set_xticks([])
#             # twiny函数建立孪生y轴(与原来的共享)，并建立新的x轴(位置在原来的对面)
#             self.twinaxes2 = self.axes2.twiny()
#             self.twinaxes2.set_xticks(np.arange(0, 350, 50))
#
#
#             self.axes3 = self.figs.add_subplot(self.grid[0, 6])
#             self.axes3.imshow(drawdata['fRightNarrow'], cmap = cm_ColorTem, norm = norm_tem, aspect = 'auto')
#             self.axes3.set_title("右侧窄面T", fontsize=16, pad=8)
#             # 选择aspect = 'auto'让图像像素点自动填充坐标轴(只是显示的时候会拉伸像素,不影响保存结果)
#             self.axes3.set_yticks(np.arange(0, 120, 20))
#             self.axes3.set_xticks([])
#             # twiny函数建立孪生y轴(与原来的共享)，并建立新的x轴(位置在原来的对面)
#             self.twinaxes3 = self.axes3.twiny()
#             self.twinaxes3.set_xticks(np.arange(0, 60, 20))
#
#
#             self.axes4 = self.figs.add_subplot(self.grid[0, 7])
#             self.axes4.imshow(drawdata['fLeftNarrow'], cmap = cm_ColorTem, norm = norm_tem, aspect = 'auto')
#             self.axes4.set_title("左侧窄面T", fontsize=16, pad=8)
#             # 选择aspect = 'auto'让图像像素点自动填充坐标轴(只是显示的时候会拉伸像素,不影响保存结果)
#             self.axes4.set_yticks(np.arange(0, 120, 20))
#             self.axes4.set_xticks([])
#             # twiny函数建立孪生y轴(与原来的共享)，并建立新的x轴(位置在原来的对面)
#             self.twinaxes4 = self.axes4.twiny()
#             self.twinaxes4.set_xticks(np.arange(0, 60, 20))
#
# #####################################################################################################################
#
#
# #####################################################################################################################
#             #绘制温度速率热像图
#
#             color_temv = [(0, 0, 1), (0.3765, 0.3765, 0.7687), (1, 1, 1), (0.7687, 0.3765, 0.3765), (1, 0, 0)]
#             cm_ColorTemV = mpl.colors.LinearSegmentedColormap.from_list("my_color_temv", color_temv, N = self.interpolation_num_TemV)
#             norm_temv = mpl.colors.Normalize(vmin = -1.5, vmax = 1.5)
#             gl.set_value("cm_ColorTemV", cm_ColorTemV)
#
#
#             self.axes6 = self.figs.add_subplot(self.grid[1, 0:3])  # 第一行的前三列列都添加到ax1中
#             self.axes6.imshow(drawdata['fOuterWide_Trick'], cmap = cm_ColorTemV, norm = norm_temv, aspect = 'auto')
#             self.axes6.set_yticks(np.arange(0, 120, 20))
#             self.axes6.set_xticks([])
#             # twiny函数建立孪生y轴(与原来的共享)，并建立新的x轴(位置在原来的对面)
#             self.twinaxes6 = self.axes6.twiny()
#             self.twinaxes6.set_xticks(np.arange(0, 350, 50))
#             for i in range(len(drawdata['Abnormal_Center'][0])):
#                 Abnormal_nX_0 = drawdata['Abnormal_Center'][0][i][0]
#                 Abnormal_nY_0 = drawdata['Abnormal_Center'][0][i][1]
#                 self.axes6.scatter(Abnormal_nY_0, Abnormal_nX_0, color = 'black', s = 20)
#
#             if not drawdata['Vx'][0]:
#                 self.axes6.set_title("外弧宽面Tv(无特征)", fontsize = 16, color = 'black', pad = 7)
#             else:
#                 self.axes6.set_title("外弧宽面Tv(有特征)", fontsize = 16, color = 'brown', fontweight = 'bold', pad = 7)
#                 for j in range(len(drawdata['Vx'][0])):
#                     Central_nX_0 = drawdata['Sticking_Center'][0][j][0]
#                     Central_nY_0 = drawdata['Sticking_Center'][0][j][1]
#                     self.axes6.scatter(Central_nY_0, Central_nX_0, color = 'blue', s = 20)    # 标注黏结区域重心位置,s为点大小
#
#
#
#             self.axes7 = self.figs.add_subplot(self.grid[1, 3:6])
#             self.axes7.imshow(drawdata['fInnerWide_Trick'], cmap = cm_ColorTemV, norm = norm_temv, aspect = 'auto')
#             self.axes7.set_yticks(np.arange(0, 120, 20))
#             self.axes7.set_xticks([])
#             # twiny函数建立孪生y轴(与原来的共享)，并建立新的x轴(位置在原来的对面)
#             self.twinaxes7 = self.axes7.twiny()
#             self.twinaxes7.set_xticks(np.arange(0, 350, 50))
#             for i in range(len(drawdata['Abnormal_Center'][2])):
#                 Abnormal_nX_2 = drawdata['Abnormal_Center'][2][i][0]
#                 Abnormal_nY_2 = drawdata['Abnormal_Center'][2][i][1]
#                 self.axes7.scatter(Abnormal_nY_2, Abnormal_nX_2, color = 'black', s = 20)
#
#             if not drawdata['Vx'][2]:
#                 self.axes7.set_title("内弧宽面Tv(无特征)", fontsize = 16, color = 'black', pad = 7)
#             else:
#                 self.axes7.set_title("内弧宽面Tv(有特征)", fontsize = 16, color = 'brown', fontweight = 'bold', pad = 7)
#                 for j in range(len(drawdata['Vx'][2])):
#                     Central_nX_2 = drawdata['Sticking_Center'][2][j][0]
#                     Central_nY_2 = drawdata['Sticking_Center'][2][j][1]
#                     self.axes7.scatter(Central_nY_2, Central_nX_2, color = 'blue', s = 20)
#
#
#
#             self.axes8 = self.figs.add_subplot(self.grid[1, 6])
#             self.axes8.imshow(drawdata['fRightNarrow_Trick'], cmap = cm_ColorTemV, norm = norm_temv, aspect = 'auto')
#             # 选择aspect = 'auto'让图像像素点自动填充坐标轴(只是显示的时候会拉伸像素,不影响保存结果)
#             self.axes8.set_yticks(np.arange(0, 120, 20))
#             self.axes8.set_xticks([])
#             # twiny函数建立孪生y轴(与原来的共享)，并建立新的x轴(位置在原来的对面)
#             self.twinaxes8 = self.axes8.twiny()
#             self.twinaxes8.set_xticks(np.arange(0, 60, 20))
#             for i in range(len(drawdata['Abnormal_Center'][1])):
#                 Abnormal_nX_1 = drawdata['Abnormal_Center'][1][i][0]
#                 Abnormal_nY_1 = drawdata['Abnormal_Center'][1][i][1]
#                 self.axes8.scatter(Abnormal_nY_1, Abnormal_nX_1, color = 'black', s = 20)
#
#             if not drawdata['Vx'][1]:
#                 self.axes8.set_title("右侧窄面Tv(无)", fontsize = 16, color = 'black', pad = 7)
#             else:
#                 self.axes8.set_title("右侧窄面Tv(有)", fontsize = 16, color = 'brown', fontweight = 'bold', pad = 7)
#                 for j in range(len(drawdata['Vx'][1])):
#                     Central_nX_1 = drawdata['Sticking_Center'][1][j][0]
#                     Central_nY_1 = drawdata['Sticking_Center'][1][j][1]
#                     self.axes8.scatter(Central_nY_1, Central_nX_1, color = 'blue', s = 20)
#
#
#             self.axes9 = self.figs.add_subplot(self.grid[1, 7])
#             self.axes9.imshow(drawdata['fLeftNarrow_Trick'], cmap = cm_ColorTemV, norm = norm_temv, aspect = 'auto')
#             # 选择aspect = 'auto'让图像像素点自动填充坐标轴(只是显示的时候会拉伸像素,不影响保存结果)
#             self.axes9.set_yticks(np.arange(0, 120, 20))
#             self.axes9.set_xticks([])
#             # twiny函数建立孪生y轴(与原来的共享)，并建立新的x轴(位置在原来的对面)
#             self.twinaxes9 = self.axes9.twiny()
#             self.twinaxes9.set_xticks(np.arange(0, 60, 20))
#             for i in range(len(drawdata['Abnormal_Center'][3])):
#                 Abnormal_nX_3 = drawdata['Abnormal_Center'][3][i][0]
#                 Abnormal_nY_3 = drawdata['Abnormal_Center'][3][i][1]
#                 self.axes9.scatter(Abnormal_nY_3, Abnormal_nX_3, color = 'black', s = 20)
#
#             if not drawdata['Vx'][3]:
#                 self.axes9.set_title("左侧窄面Tv(无)", fontsize = 16, color = 'black', pad = 7)
#             else:
#                 self.axes9.set_title("左侧窄面Tv(有)", fontsize = 16, color = 'brown', fontweight = 'bold', pad = 7)
#                 for j in range(len(drawdata['Vx'][3])):
#                     Central_nX_3 = drawdata['Sticking_Center'][3][j][0]
#                     Central_nY_3 = drawdata['Sticking_Center'][3][j][1]
#                     self.axes9.scatter(Central_nY_3, Central_nX_3, color = 'blue', s = 20)
#
#
#             # 保存图像操作比较耗时
#             #self.figs.savefig("SaveTest.jpg")  此时保存的是一整张大图(包含所有子图，而且子图间距与设定的不同)
# ####################################################################################################################


        else:
            QMessageBox.warning(self, "警告", "数据加载失败！", QMessageBox.Ok)

    def ImageToFile(self, drawdata, ImgName, Mold):

        if Mold == "外弧宽面Tv":
            MoldName = 'fOuterWide_Trick'
        elif Mold == "内弧宽面Tv":
            MoldName = 'fInnerWide_Trick'
        elif Mold == "右侧窄面Tv":
            MoldName = 'fRightNarrow_Trick'
        elif Mold == "左侧窄面Tv":
            MoldName = 'fLeftNarrow_Trick'
        else:
            MoldName = None
        # 保存图像(imsave方法将数组保存为图像)
        plt.imsave(ImgName, drawdata[MoldName], vmin = -1.5, vmax = 1.5, cmap = gl.get_value("cm_ColorTemV"), dpi = 600)
