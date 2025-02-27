import __init__ as gl
from multiprocessing import Process, Manager
from AbnormalAreaDetect import CMoldPlate
import os
import pandas as pd


def calculate_process(var, m_MoldPlate, End_Time, accident_type, Cal_Result, dict_result, sample_data, nTime_Start):

    var = var

    for timenow in range(End_Time):

        print("计算开始时的timenow = ", timenow)

        # 将起点归零，减少建立数组时所需大小，例要取a[10:20]的数据至少要开a[20]的数组，起点归零后为a[0:10],只需开a[10]的数组
        var.CheckThermocouples(timenow)  # 检查热电偶温度
        var.CalibrateTemprature(timenow,)  # 校正“坏”热电偶温度
        var.RefreshData(timenow)  # 将校正后的温度赋值给温度数组
        var.PushTemperature_InQueue()
        var.CalculateTemMap(timenow)
        var.TrickTemperature()

        # m_fOuterWide_Trick = var.fOuterWide_Trick
        # m_fRightNarrow_Trick = var.fRightNarrow_Trick
        # m_fInnerWide_Trick = var.fInnerWide_Trick
        # m_fLeftNarrow_Trick = var.fLeftNarrow_Trick

        # Clear_Mold(m_MoldPlate)
        # Load_Data_Judge_Status(m_MoldPlate, m_fOuterWide_Trick, m_fRightNarrow_Trick, m_fInnerWide_Trick, m_fLeftNarrow_Trick)
        m_MoldPlate.Clear(accident_type)
        m_MoldPlate.Load_Data_Judge_Status(var.fOuterWide_Trick, var.fRightNarrow_Trick, var.fInnerWide_Trick, var.fLeftNarrow_Trick)
        m_MoldPlate.Detect_Abnormal_Area()
        m_MoldPlate.Cal_Feature(var, timenow)

        dict_result['fOuterWide'] = var.fOuterWide.copy()
        dict_result['fInnerWide'] = var.fInnerWide.copy()
        dict_result['fRightNarrow'] = var.fRightNarrow.copy()
        dict_result['fLeftNarrow'] = var.fLeftNarrow.copy()

        dict_result['fOuterWide_Trick'] = var.fOuterWide_Trick.copy()
        dict_result['fInnerWide_Trick'] = var.fInnerWide_Trick.copy()
        dict_result['fRightNarrow_Trick'] = var.fRightNarrow_Trick.copy()
        dict_result['fLeftNarrow_Trick'] = var.fLeftNarrow_Trick.copy()


        dict_result['Vx'] = m_MoldPlate.Vx.copy()
        dict_result['Vy'] = m_MoldPlate.Vy.copy()
        dict_result['Vc'] = m_MoldPlate.Vc.copy()
        dict_result['Height'] = m_MoldPlate.Height.copy()
        dict_result['Width'] = m_MoldPlate.Width.copy()
        dict_result['Area'] = m_MoldPlate.Area.copy()
        dict_result['Edgenum'] = m_MoldPlate.Edgenum.copy()
        dict_result['Gave'] = m_MoldPlate.Gave.copy()
        dict_result['Fourier'] = m_MoldPlate.Fourier.copy()
        # dict_result['Breakout_Center_Dis'] = m_MoldPlate.Breakout_Center_Dis.copy()
        dict_result['Sticking_Expansion'] = m_MoldPlate.Sticking_Expansion.copy()


        # 见https://www.jianshu.com/p/52676b93430d,Manager对象无法监测到它引用的可变对象值的修改，
        # 需要通过触发__setitem__方法来让它获得通知
        temp = Cal_Result[timenow]
        temp.append(dict_result.copy())     #浅拷贝(不随对象值的改变而改变)
        Cal_Result[timenow] = temp
        # Cal_Result[timenow].append(dict_result)
        timenow += 1
        print("计算结束后的timenow = ", timenow)
        print()
        # time.sleep(0.1)       #休眠100 ms

    print("done!")





def Batch_Adding_Features():

    # 加载批处理样本信息
    # 获取当前数据源(南钢/鞍钢)
    DirPlantPath = gl.get_value("DirPlantPath")
    DirPlantPath_List = DirPlantPath.split("/")
    DataSrc = "南钢" if DirPlantPath_List[1] == "NanGang" else "鞍钢" if DirPlantPath_List[1] == "AnGang" else "None"
    gl.set_value('Data_Source', DataSrc)

    # 初始化variable对象
    variable = gl.Variable(plant=gl.get_value('Data_Source'), accident=gl.get_value("accident_type"))
    gl.set_value('Variable', variable)  # 定义为全局字典变量

    Sample_List_Path = gl.get_value('SampleList')
    Sample_List = gl.load_feature_vector(Sample_List_Path)


    process_is_running = False  # 检查当前是否有进程在运行
    # 开始对每一个样本进行计算
    for sample_index in range(len(Sample_List)):

        print("当前处理的是列表中的第{}个文件".format(sample_index + 1))

        date = Sample_List[sample_index][2]
        time = Sample_List[sample_index][3]
        mold = Sample_List[sample_index][4]

        if mold == "外弧宽面Tv":
            Moldindex = 0
        elif mold == "内弧宽面Tv":
            Moldindex = 2
        elif mold == "右侧窄面Tv":
            Moldindex = 1
        elif mold == "左侧窄面Tv":
            Moldindex = 3
        else:
            Moldindex = None

        sample_type = Sample_List[sample_index][5]

        Vx_raw = Sample_List[sample_index][6]
        Vy_raw = Sample_List[sample_index][7]
        Vc_raw = Sample_List[sample_index][8]
        Height_raw = Sample_List[sample_index][9]
        Width_raw = Sample_List[sample_index][10]
        Area_raw = Sample_List[sample_index][11]
        Gave_raw = Sample_List[sample_index][12]
        Fourier_raw = Sample_List[sample_index][13]




        year, month, day = date[0:4], date[5:7], date[8:10]
        hour, minute, second = time[0:2], time[3:5], time[6:8]

        gl.set_value('TotalNum', len(Sample_List))
        gl.set_value('year', year)
        gl.set_value('month', month)
        gl.set_value('day', day)
        gl.set_value('hour', hour)
        gl.set_value('minute', minute)
        gl.set_value('second', second)
        gl.set_value('SampleType', sample_type)


        try:
            paths = ""
            for i in range(len(DirPlantPath_List)):
                paths += DirPlantPath_List[i] + "\\"
            filepath = paths + year + "\\" + month + "\\" + day + "\\PR" + year + month + day + "_" + hour + ".txt"
            gl.set_value("file_path", filepath)
            sample_data_T = gl.loadDataSet(filepath)

        except Exception as err:
            print(err)
            print("加载原温度文件错误!")

        nFeature_Time = 0
        for i in range(len(sample_data_T)):
            if sample_data_T[i][1] == time:
                nFeature_Time = i
                break

        gl.set_value("nFeature_Time", nFeature_Time)
        # 从特征提取时刻前15s开始回溯(注意!!!提前量要给足,要保证特征提取时刻和其前5秒均为有效数据
        # 若提前量太少则其前5秒的时刻为无效数据,计算Vx,Vy会出错)
        nSeconds_before = 15
        nSec_after = 5
        nTime_Start = max(nFeature_Time - nSeconds_before, 0)
        nTime_End = min(nFeature_Time + nSec_after, len(sample_data_T))
        nTime_Duration = nTime_End - nTime_Start

        # 读取数据
        variable.ReadProData(sample_data_T[nTime_Start: nTime_End])  # 读入样例数据


        # 启动新进程计算
        accident_type = gl.get_value("accident_type")
        #在主线程中定义Manager类型的列表和字典，子线程中对其修改值同时会更改主线程中该变量的值，即数据共享
        Cal_Result = Manager().list()
        dict_result = Manager().dict()

        for _ in range(nTime_Duration):
            Cal_Result.append([])

        m_MoldPlate = CMoldPlate()
        m_MoldPlate.Initialize()

        calprocess = Process(target = calculate_process, args = (variable, m_MoldPlate, nTime_Duration, accident_type, Cal_Result, dict_result, sample_data_T, nTime_Start))
        # 设置子进程为守护进程，即主进程结束后子进程也相应结束
        calprocess.daemon = True
        calprocess.start()
        process_is_running = True
        # 阻塞主进程等待子进程运行完成
        calprocess.join()

        # 判断当前子进程是否存在并且正在运行
        if process_is_running == True:
            if calprocess.is_alive() == True:
                # 终止当前计算子进程再开启新的计算子进程
                calprocess.terminate()
                calprocess.join()
            else:
                pass
        else:
            pass


        # 向文件中输出特征(原+新)
        # Slider_Value对应nFeature_Time时刻(从nTime_Start开始计算)
        Slider_Value = nFeature_Time - nTime_Start
        drawdata = Cal_Result[Slider_Value][0]

        # 判断原始提取各特征是否与当前计算特征相同
        sticker_num = -1
        for sticker in range(len(drawdata['Vx'][Moldindex])):
            if format(Vx_raw, '.3f') == format(drawdata['Vx'][Moldindex][sticker], '.3f') and \
                format(Vy_raw, '.3f') == format(drawdata['Vy'][Moldindex][sticker], '.3f') and \
                format(Vc_raw, '.3f') == format(drawdata['Vc'][Moldindex][sticker], '.3f') and \
                format(Height_raw, '.3f') == format(drawdata['Height'][Moldindex][sticker], '.3f') and \
                format(Width_raw, '.3f') == format(drawdata['Width'][Moldindex][sticker], '.3f') and \
                format(Area_raw, '.3f') == format(drawdata['Area'][Moldindex][sticker], '.3f') and \
                format(Gave_raw, '.3f') == format(drawdata['Gave'][Moldindex][sticker], '.3f') and \
                format(Fourier_raw, '.3f') == format(drawdata['Fourier'][Moldindex][sticker], '.3f'):

                sticker_num = sticker

            else:
                continue


        # 利用format函数保留特定的小数位数
        sticker_dict = {"钢厂": [DataSrc], "日期": date, "时间": [time],
                        "铜板": [mold], "类型": [sample_type],
                        "Vx": format(drawdata['Vx'][Moldindex][sticker_num], '.3f'),
                        "Vy": format(drawdata['Vy'][Moldindex][sticker_num], '.3f'),
                        "Vc": format(drawdata['Vc'][Moldindex][sticker_num], '.3f'),
                        # "Breakout_Center_Dis_Min": format(drawdata['Breakout_Center_Dis'][Moldindex][sticker_num][0], '.3f'),
                        # "Breakout_Center_Dis_Max": format(drawdata['Breakout_Center_Dis'][Moldindex][sticker_num][1], '.3f'),
                        "Sticking_Expansion": format(drawdata['Sticking_Expansion'][Moldindex][sticker_num], '.3f'),
                        "Height": format(drawdata['Height'][Moldindex][sticker_num], '.3f'),
                        "Width": format(drawdata['Width'][Moldindex][sticker_num], '.3f'),
                        "Area": format(drawdata['Area'][Moldindex][sticker_num], '.3f'),
                        "Edgenum": format(drawdata['Edgenum'][Moldindex][sticker_num], '.3f'),
                        "Gave": format(drawdata['Gave'][Moldindex][sticker_num], '.3f'),
                        "Fourier": format(drawdata['Fourier'][Moldindex][sticker_num], '.3f')}


        # 保存特征向量
        try:

            # filename = "黏结区域特征向量(添加新特征).csv"
            filename = "黏结区域特征向量(全部样本添加新特征).csv"
            if not os.path.exists(filename):
                data = pd.DataFrame(sticker_dict)  # sticker_dict需要是字典格式
                # mode='a'表示追加, index=True表示给每行数据加索引序号, header=False表示不加标题
                data.to_csv(filename, mode='a', index=False, header=True, encoding='GB18030')
            else:
                # 若文件已存在，则追加数据时不需要加标题
                data = pd.DataFrame(sticker_dict)
                data.to_csv(filename, mode='a', index=False, header=False, encoding='GB18030')

            print("特征保存成功!")

        except IOError:

            print("文件打开或写入异常,特征保存失败!")
