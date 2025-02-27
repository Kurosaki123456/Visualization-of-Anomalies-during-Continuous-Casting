from PyQt5.QtWidgets import QMessageBox, QApplication
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg  # pyqt5的画布
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import __init__ as gl
import numpy as np
import matplotlib as mpl
from matplotlib.cm import ScalarMappable


plt.rcParams['font.sans-serif']=['SimHei'] #显示中文标签
plt.rcParams['axes.unicode_minus']=False   #这两行需要手动设置



class Figure_Tem_Difference_Thermography(FigureCanvasQTAgg):
    def __init__(self, number_index = 0):

        self.figs = Figure()

        super(Figure_Tem_Difference_Thermography, self).__init__(self.figs)  # 在父类FigureCanvasQTAgg中激活figs，否则绘图失败
        # 调整子图位置及间距
        self.figs.subplots_adjust(left=0.02, bottom=0.02, right=1, top=0.90, wspace=0.5, hspace=0.3)

        ##################################################################
        # 划分网格
        self.grid = plt.GridSpec(2, 9)
        ##################################################################
        # 清除当前figure中的所有axes
        self.figs.clf()
        ##################################################################
        #绘制温度条
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
        self.axes5.imshow(colorbars_Tem, cmap=cm_ColorBarTem, extent=[-10, 10, 50, 150])
        self.axes5.set_xticks([])
        # 设置y轴刻度范围
        self.axes5.set_yticks(np.arange(50, 160, 20))
        ##################################################################################################

        HEIGHT_COUNT = gl.Variable().HEIGHT_COUNT_CRACK
        WIDE_COUNT = gl.Variable().WIDE_COUNT

        ##################################################################################################
        # 绘制温度差值条
        self.axes10 = self.figs.add_subplot(self.grid[1, 8])
        self.axes10.set_title("温度差值条", fontsize=16, pad=13)
        # 温度差值区间插值数量
        self.interpolation_num_TemD = 255
        nums_TemD = np.linspace(-10, 6, self.interpolation_num_TemD)
        # 设置温度差值条的格子数目
        colorbars_TemD = np.zeros((self.interpolation_num_TemD, 1))
        for i in range(self.interpolation_num_TemD):
            colorbars_TemD[i] = nums_TemD[i]
        # 颜色区间范围将(0-255)归一化至(0-1)
        #将具体温度数值与颜色值对应(注意两者均需要归一化至(0, 1)之间)
        color_bartemd = [(1, 0, 0), (0, 0.3451, 0.1882), (0, 0.3451, 0.1882), (0, 0, 1),(0, 0, 0.5882)]
        # cmap_bartemd = mpl.colors.ListedColormap(color_bartemd)

        value_color_bartemd = np.array([-10.0, -8.0, -6.0, 4.0, 6.0])
        norm_value_color_bartemd = plt.Normalize(min(value_color_bartemd), max(value_color_bartemd))
        tuples_value_color_bartemd = list(zip(map(norm_value_color_bartemd, value_color_bartemd), color_bartemd))

        # 自定义cmap方案，"my_color"为方案名称，color为颜色区间，N为在颜色区间内插值的点数
        cm_ColorBarTemD = mpl.colors.LinearSegmentedColormap.from_list("my_color_bartemd", tuples_value_color_bartemd,
                                                                       N = self.interpolation_num_TemD)

        # extent[x0, x1, y0, y1]分别代表x轴最左侧的值,x轴最右侧的值,y轴最下面的值，y轴最上面的值;origin='upper'代表图从上往下画,lower相反从下往上画
        self.axes10.imshow(colorbars_TemD, cmap = cm_ColorBarTemD, norm = norm_value_color_bartemd, extent=[-1.6, 1.5, -10.0, 6.0], origin='upper')
        self.axes10.set_xticks([])
        # 设置y轴刻度范围
        self.axes10.set_yticks(np.arange(-10.0, 7.0, 2.0))
        ##################################################################################################

        ##################################################################################################
        # 绘制温度图所需颜色参数
        color_tem = [(0, 0, 0), (0, 0, 1), (1, 0, 0), (1, 1, 0), (0.5, 0.5, 0)]
        self.cm_ColorTem = mpl.colors.LinearSegmentedColormap.from_list("my_color_tem", color_tem, N = self.interpolation_num_Tem)
        self.norm_tem = mpl.colors.Normalize(vmin=50, vmax=150)

        #添加温度热像图子图
        self.axes1 = self.figs.add_subplot(self.grid[0, 0:3])  # 第一行的前三列列都添加到ax1中
        self.axes1.set_title("外弧宽面T", fontsize=16, pad=8)
        self.axes1_img = self.axes1.imshow(np.random.random((HEIGHT_COUNT, WIDE_COUNT)), cmap = self.cm_ColorTem, norm = self.norm_tem, aspect = 'auto')  # aspect = 'auto'自动填充区域
        self.axes1.set_yticks(np.arange(0, 140, 20))
        self.axes1.set_xticks([])
        # twiny函数建立孪生y轴(与原来的共享)，并建立新的x轴(位置在原来的对面)
        self.twinaxes1 = self.axes1.twiny()
        self.twinaxes1.set_xticks(np.arange(0, 350, 50))

        self.axes2 = self.figs.add_subplot(self.grid[0, 3:6])
        self.axes2.set_title("内弧宽面T", fontsize=16, pad=8)
        self.axes2_img = self.axes2.imshow(np.random.random((HEIGHT_COUNT, WIDE_COUNT)), cmap = self.cm_ColorTem, norm = self.norm_tem, aspect = 'auto')
        self.axes2.set_yticks(np.arange(0, 140, 20))
        self.axes2.set_xticks([])
        # twiny函数建立孪生y轴(与原来的共享)，并建立新的x轴(位置在原来的对面)
        self.twinaxes2 = self.axes2.twiny()
        self.twinaxes2.set_xticks(np.arange(0, 350, 50))

        self.axes3 = self.figs.add_subplot(self.grid[0, 6])
        self.axes3.set_title("右侧窄面T", fontsize=16, pad=8)
        # 选择aspect = 'auto'让图像像素点自动填充坐标轴(只是显示的时候会拉伸像素,不影响保存结果)
        self.axes3_img = self.axes3.imshow(np.random.random((HEIGHT_COUNT, WIDE_COUNT)), cmap = self.cm_ColorTem, norm = self.norm_tem, aspect = 'auto')
        self.axes3.set_yticks(np.arange(0, 140, 20))
        self.axes3.set_xticks([])
        # twiny函数建立孪生y轴(与原来的共享)，并建立新的x轴(位置在原来的对面)
        self.twinaxes3 = self.axes3.twiny()
        self.twinaxes3.set_xticks(np.arange(0, 60, 20))

        self.axes4 = self.figs.add_subplot(self.grid[0, 7])
        self.axes4.set_title("左侧窄面T", fontsize=16, pad=8)
        # 选择aspect = 'auto'让图像像素点自动填充坐标轴(只是显示的时候会拉伸像素,不影响保存结果)
        self.axes4_img = self.axes4.imshow(np.random.random((HEIGHT_COUNT, WIDE_COUNT)), cmap = self.cm_ColorTem, norm = self.norm_tem, aspect = 'auto')
        self.axes4.set_yticks(np.arange(0, 140, 20))
        self.axes4.set_xticks([])
        # twiny函数建立孪生y轴(与原来的共享)，并建立新的x轴(位置在原来的对面)
        self.twinaxes4 = self.axes4.twiny()
        self.twinaxes4.set_xticks(np.arange(0, 60, 20))
        ##################################################################################################

        ##################################################################################################
        # 绘制温差图所需颜色参数
        color_temd = [(0, 0, 0.5882), (0, 0, 1), (0, 0.3451, 0.1882), (0, 0.3451, 0.1882), (1, 0, 0)]
        value_color_temd = np.array([-10.0, -8.0, -6.0, 4.0, 6.0])
        norm_value_color_temd = plt.Normalize(min(value_color_temd), max(value_color_temd))
        tuples_value_color_temd = list(zip(map(norm_value_color_temd, value_color_temd), color_temd))

        self.cm_ColorTemD = mpl.colors.LinearSegmentedColormap.from_list("my_color_temd", tuples_value_color_temd,N = self.interpolation_num_TemD)
        self.norm_temd = mpl.colors.Normalize(vmin=-10.0, vmax=6.0)
        gl.set_value("cm_ColorTemD", self.cm_ColorTemD)

        # 添加温度差值热像图子图
        self.axes6 = self.figs.add_subplot(self.grid[1, 0:3])  # 第一行的前三列列都添加到ax1中
        self.axes6.set_title("外弧宽面Td",fontsize = 16, pad = 7)
        self.axes6_img = self.axes6.imshow(np.random.random((HEIGHT_COUNT, WIDE_COUNT)), cmap = self.cm_ColorTemD, norm = self.norm_temd, aspect = 'auto')
        self.axes6.set_yticks(np.arange(0, 140, 20))
        self.axes6.set_xticks([])
        #twiny函数建立孪生y轴(与原来的共享)，并建立新的x轴(位置在原来的对面)
        self.twinaxes6 = self.axes6.twiny()
        self.twinaxes6.set_xticks(np.arange(0, 350, 50))


        self.axes7 = self.figs.add_subplot(self.grid[1, 3:6])
        self.axes7.set_title("内弧宽面Td", fontsize = 16, pad = 7)
        self.axes7_img = self.axes7.imshow(np.random.random((HEIGHT_COUNT, WIDE_COUNT)), cmap = self.cm_ColorTemD, norm = self.norm_temd, aspect = 'auto')
        self.axes7.set_yticks(np.arange(0, 140, 20))
        self.axes7.set_xticks([])
        # twiny函数建立孪生y轴(与原来的共享)，并建立新的x轴(位置在原来的对面)
        self.twinaxes7 = self.axes7.twiny()
        self.twinaxes7.set_xticks(np.arange(0, 350, 50))


        self.axes8 = self.figs.add_subplot(self.grid[1, 6])
        self.axes8.set_title("右侧窄面Td", fontsize = 16, pad = 7)
        # 选择aspect = 'auto'让图像像素点自动填充坐标轴(只是显示的时候会拉伸像素,不影响保存结果)
        self.axes8_img = self.axes8.imshow(np.random.random((HEIGHT_COUNT, WIDE_COUNT)), cmap = self.cm_ColorTemD, norm = self.norm_temd, aspect = 'auto')
        self.axes8.set_yticks(np.arange(0, 140, 20))
        self.axes8.set_xticks([])
        # twiny函数建立孪生y轴(与原来的共享)，并建立新的x轴(位置在原来的对面)
        self.twinaxes8 = self.axes8.twiny()
        self.twinaxes8.set_xticks(np.arange(0, 60, 20))


        self.axes9 = self.figs.add_subplot(self.grid[1, 7])
        self.axes9.set_title("左侧窄面Td", fontsize = 16, pad = 7)
        # 选择aspect = 'auto'让图像像素点自动填充坐标轴(只是显示的时候会拉伸像素,不影响保存结果)
        self.axes9_img = self.axes9.imshow(np.random.random((HEIGHT_COUNT, WIDE_COUNT)), cmap = self.cm_ColorTemD, norm = self.norm_temd, aspect = 'auto')
        self.axes9.set_yticks(np.arange(0, 140, 20))
        self.axes9.set_xticks([])
        # twiny函数建立孪生y轴(与原来的共享)，并建立新的x轴(位置在原来的对面)
        self.twinaxes9 = self.axes9.twiny()
        self.twinaxes9.set_xticks(np.arange(0, 60, 20))
        ##################################################################################################
        self.number_index = number_index

        # if self.number_index == 0:
        #
        #     self.figs.suptitle("The window of visualizing the images!", x=0.5, y=0.6, fontsize=40, color="k", alpha=0.25)

    def LoadSampleInfoCrack(self):

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
            column = Sample_List[self.number_index - 1][2]

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
            gl.set_value('column', column)
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



            nTime_Start = max(nAlarm_Time - variable.nTime_Advance, 0)
            nTime_End = min(nAlarm_Time + variable.nTime_Lag, len(self.data_T))

            #选取在Time_Window内的数据
            variable.ReadProData(self.data_T[nTime_Start : nTime_End])     #读入样例数据
            nTime_Duration = nTime_End - nTime_Start
            gl.set_value("nTime_Duration", nTime_Duration)
            # 将预警时间设为nTime_Duration(想显示245s,实际上只读取到了nTime_End时刻的数据文件已经结束了,EOF到达文件末尾,所以实际上只持续了nTime_Duration秒)
            gl.set_value("Alarm_Time", nTime_Duration)

            Slider_Time_List = []
            #将滑块数值与对应数据时刻对应起来
            for i in range(0, nTime_Duration):
                    dict = {i : self.data_T[i + nTime_Start][1]}
                    Slider_Time_List.append(dict)

            gl.set_value("Slider_Time", Slider_Time_List)


        else:
            QMessageBox.warning(self, "警告", "数据加载失败!", QMessageBox.Ok)



    def PlotImgCrack(self, drawdata, line):

        if self.number_index != 0:

############################################################################
            # 绘制温度热像图
            self.axes1_img.set_data(drawdata['fOuterWideCrack'][line])
            self.axes2_img.set_data(drawdata['fInnerWideCrack'][line])
            self.axes3_img.set_data(drawdata['fRightNarrowCrack'][line])
            self.axes4_img.set_data(drawdata['fLeftNarrowCrack'][line])
############################################################################


############################################################################
            # 绘制温度差值热像图
            self.axes6_img.set_data(drawdata['fOuterWide_TrickCrack'][line])
            self.axes7_img.set_data(drawdata['fInnerWide_TrickCrack'][line])
            self.axes8_img.set_data(drawdata['fRightNarrow_TrickCrack'][line])
            self.axes9_img.set_data(drawdata['fLeftNarrow_TrickCrack'][line])

            # 保存图像操作比较耗时
            #self.figs.savefig("SaveTest.jpg")  此时保存的是一整张大图(包含所有子图，而且子图间距与设定的不同)
############################################################################

        else:
            QMessageBox.warning(self, "警告", "数据加载失败！", QMessageBox.Ok)

    def CrackImageToFile(self, drawdata, ImgName, Mold, line):

        if Mold == "外弧宽面Td":
            MoldName = 'fOuterWide_TrickCrack'
        elif Mold == "内弧宽面Td":
            MoldName = 'fInnerWide_TrickCrack'
        elif Mold == "右侧窄面Td":
            MoldName = 'fRightNarrow_TrickCrack'
        elif Mold == "左侧窄面Td":
            MoldName = 'fLeftNarrow_TrickCrack'
        else:
            MoldName = None
        # 保存图像(imsave方法将数组保存为图像)
        plt.imsave(ImgName, drawdata[MoldName][line], vmin = -10.0, vmax = 6.0, cmap = gl.get_value("cm_ColorTemD"), dpi = 600)
