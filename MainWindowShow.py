import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog, QGridLayout, QLabel, QSizePolicy, QPushButton,\
QTableWidgetItem, QHeaderView, QMessageBox, QInputDialog, QAbstractItemView
from MainWindow import Ui_MainWindow
from PyQt5.QtCore import QTimer, QDateTime, Qt, QRect, QThread, pyqtSignal, QObject, QMutex, QWaitCondition
from Show_Thermography import Figure_Thermography
from Show_Tem_Difference_Thermography import Figure_Tem_Difference_Thermography
from Add_New_Feature import Batch_Adding_Features
import __init__ as gl
from AbnormalAreaDetect import CMoldPlate
import time
import threading
from multiprocessing import Process, Manager, Pipe, Value, freeze_support
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd


# def cal1():
#     var_plant = gl.gl.get_value('Variable')
#     time_idx = gl.gl.get_value("current_time")
#
#     CalculateWide(var_plant.fTemOuterWide, var_plant.fOuterWide, 0,
#                   var_plant, time_idx)
#
# def cal2():
#     var_plant = gl.gl.get_value('Variable')
#     time_idx = gl.gl.get_value("current_time")
#
#     CalculateWide(var_plant.fTemInnerWide, var_plant.fInnerWide, 1, var_plant, time_idx)
#
# def cal3():
#     var_plant = gl.gl.get_value('Variable')
#
#     CalculateNarrow(var_plant.fTemRightNarrow, var_plant.fRightNarrow, 0, var_plant)
#
# def cal4():
#     var_plant = gl.gl.get_value('Variable')
#
#     CalculateNarrow(var_plant.fTemLeftNarrow, var_plant.fLeftNarrow, 1, var_plant)
#
# # 进程池必须在if __name__ == "__main__":下使用，否则会报错
# with ThreadPoolExecutor(max_workers=3) as t:
#     t.submit(cal1)
#     t.submit(cal2)
#     t.submit(cal3)
#     t.submit(cal4)

gl._init()

# bStopStatus = False
# bFineTune = False
#
#
# class CallThread(QObject):
#     drawsignal = pyqtSignal(object)
#     end = pyqtSignal()
#     calprogress = pyqtSignal()
#
#     def __init__(self, timeinterval, mutex, cond, text = ""):
#         super(CallThread, self).__init__()
#         self.timeinterval = timeinterval
#         self.mtx = mutex
#         self.codt = cond
#         self.buttontext = text
#
#
#     def getmainsignal(self, text):
#
#         self.buttontext = text
#
#     def work(self):
#
#         global bStopStatus, bFineTune, Cal_Result
#         with Manager() as manager:
#             while True:
#
#                 if bStopStatus == False:
#
#                     timenow = gl.get_value("current_time")
#
#                     print("调用开始时的timenow = ", timenow)
#                     #timenow等于设定的观测时间窗口大小或报警时刻时退出循环
#                     if timenow < self.timeinterval and timenow < gl.get_value("Alarm_Time"):
#
#                         if Cal_Result[timenow] == []:
#                             self.calprogress.emit()
#                             # 阻塞其它线程直至信号处理完成，有其它线程唤醒才继续往下执行
#                             # self.mtx.lock()
#                             # try:
#                             #     self.codt.wait(self.mtx)
#                             # finally:
#                             #     self.mtx.unlock()
#                         else:
#                             # self.mtx.lock()
#                             self.drawsignal.emit(Cal_Result[timenow][0])
#                             # 阻塞其它线程直至信号处理完成，有其它线程唤醒才继续往下执行
#
#                             # try:
#                             #     self.codt.wait(self.mtx)
#                             # finally:
#                             #     self.mtx.unlock()
#
#                             # print("访问当前铜板数据Area为:", Cal_Result[timenow][0]['Area'])
#                             gl.set_value("current_time", gl.get_value("current_time") + 1)
#                             print("调用结束后的timenow = ", gl.get_value("current_time"))
#                             print()
#                             time.sleep(1)
#
#
#                             #微调结束恢复到暂停状态
#                             if bFineTune == True:
#                                 bFineTune = False
#                                 bStopStatus = True
#                                 self.buttontext = ""
#
#
#                     else:
#                         break
#
#                 else:
#                     #暂停(挂起)线程
#                     time.sleep(0.1)  # 必须有self.sleep 可以有效降低cpu消耗
#                     #发送信号，如果判断当前触发单机按钮事件则改变全局布尔变量的值
#                     if self.buttontext != "":
#                         bStopStatus = False
#                         bFineTune = True
#                         if self.buttontext == "前一秒":
#                             #特征计算有问题!!!
#                             gl.set_value("current_time", gl.get_value("current_time") - 1)
#                         elif self.buttontext == "后一秒":
#                             #特征计算有问题!!!
#                             gl.set_value("current_time", gl.get_value("current_time") + 1)
#                         else:
#                             print("微调按钮出错!")
#
#                     else:
#                         continue
#
#
#             self.end.emit()
#
#
#
#
# class CalculateThread(QObject):
#
#     # CalFinished = pyqtSignal()
#     # AbnormalQuit = pyqtSignal()
#
#     def __init__(self, timeinterval, var, AlarmTime, CurrentTime):
#         super(CalculateThread, self).__init__()
#         self.timeinterval = timeinterval
#         self.vari = var
#         self.alarmtime = AlarmTime
#         self.currenttime = CurrentTime
#
#     def calculate(self, out_pipe, in_pipe):
#
#         cal_out_pipe = out_pipe
#         cal_in_pipe = in_pipe
#
#         cal_out_pipe.close()
#
#         var = self.vari
#         m_MoldPlate = CMoldPlate()
#         m_MoldPlate.Initialize()
#
#         global Cal_Result
#         with Manager() as manager:
#             Cal_Result = manager.list([])
#         for _ in range(min(self.timeinterval, self.alarmtime)):
#             Cal_Result.append([])
#
#         timenow = self.currenttime
#         if timenow != 0:
#             cal_in_pipe.send("滑块未置0!")
#             # self.AbnormalQuit.emit()
#         else:
#
#             #判断Cal_Result中是否还有空列表(是否计算完成)
#             while [] in Cal_Result:
#
#                 dict_result = manager.dict()
#                 print("计算开始时的timenow = ", timenow)
#
#                 # 将起点归零，减少建立数组时所需大小，例要取a[10:20]的数据至少要开a[20]的数组，起点归零后为a[0:10],只需开a[10]的数组
#                 CheckThermocouples(timenow, var)  # 检查热电偶温度
#                 CalibrateTemprature(timenow, var)  # 校正“坏”热电偶温度
#                 RefreshData(timenow, var)  # 将校正后的温度赋值给温度数组
#                 PushTemperature_InQueue(var)
#                 CalculateTemMap(timenow, var)
#                 TrickTemperature(var)
#
#                 m_fOuterWide_Trick = var.fOuterWide_Trick
#                 m_fRightNarrow_Trick = var.fRightNarrow_Trick
#                 m_fInnerWide_Trick = var.fInnerWide_Trick
#                 m_fLeftNarrow_Trick = var.fLeftNarrow_Trick
#
#                 # Clear_Mold(m_MoldPlate)
#                 # Load_Data_Judge_Status(m_MoldPlate, m_fOuterWide_Trick, m_fRightNarrow_Trick, m_fInnerWide_Trick, m_fLeftNarrow_Trick)
#                 m_MoldPlate.Clear()
#                 m_MoldPlate.Load_Data_Judge_Status(m_fOuterWide_Trick, m_fRightNarrow_Trick, m_fInnerWide_Trick, m_fLeftNarrow_Trick)
#                 m_MoldPlate.Detect_Abnormal_Area()
#                 m_MoldPlate.Cal_Feature(var, timenow)
#
#                 dict_result['fOuterWide'] = var.fOuterWide.copy()
#                 dict_result['fInnerWide'] = var.fInnerWide.copy()
#                 dict_result['fRightNarrow'] = var.fRightNarrow.copy()
#                 dict_result['fLeftNarrow'] = var.fLeftNarrow.copy()
#
#                 dict_result['fOuterWide_Trick'] = var.fOuterWide_Trick.copy()
#                 dict_result['fInnerWide_Trick'] = var.fInnerWide_Trick.copy()
#                 dict_result['fRightNarrow_Trick'] = var.fRightNarrow_Trick.copy()
#                 dict_result['fLeftNarrow_Trick'] = var.fLeftNarrow_Trick.copy()
#
#
#                 dict_result['Vx'] = m_MoldPlate.Vx.copy()
#                 dict_result['Vy'] = m_MoldPlate.Vy.copy()
#                 dict_result['Vc'] = m_MoldPlate.Vc.copy()
#                 dict_result['Height'] = m_MoldPlate.Height.copy()
#                 dict_result['Width'] = m_MoldPlate.Width.copy()
#                 dict_result['Area'] = m_MoldPlate.Area.copy()
#
#                 temp = Cal_Result[timenow]
#                 temp.append(dict_result)
#                 Cal_Result[timenow] = temp
#                 timenow += 1
#                 print("计算结束后的timenow = ", timenow)
#                 print()
#                 time.sleep(0.1)       #休眠100 ms
#
#
#             cal_in_pipe.send("计算进程完成!")
#             cal_in_pipe.close()
#             self.CalFinished.emit()




# pool = ThreadPoolExecutor(max_workers = 7)




def calculate_crack_process(var, m_MoldPlate, End_Time, accident_type, Cal_Result, dict_result):

    var = var

    for timenow in range(End_Time):

        print("计算开始时的timenow = ", timenow)

        # 将起点归零，减少建立数组时所需大小，例要取a[10:20]的数据至少要开a[20]的数组，起点归零后为a[0:10],只需开a[10]的数组
        var.CheckThermocouples(timenow)  # 检查热电偶温度
        var.CalibrateTemprature(timenow)  # 校正“坏”热电偶温度
        var.RefreshData(timenow)  # 将校正后的温度赋值给温度数组
        # var.PushTemperature_InQueue()
        var.CalculateTemMapCrack(timenow)
        var.TrickTemperatureCrack()

        # Clear_Mold(m_MoldPlate)
        # Load_Data_Judge_Status(m_MoldPlate, m_fOuterWide_Trick, m_fRightNarrow_Trick, m_fInnerWide_Trick, m_fLeftNarrow_Trick)
        m_MoldPlate.Clear(accident_type)
        m_MoldPlate.Load_Data_Judge_Status_Crack(var.fOuterWide_TrickCrack, var.fRightNarrow_TrickCrack,
                                                 var.fInnerWide_TrickCrack, var.fLeftNarrow_TrickCrack)
        m_MoldPlate.Detect_Abnormal_AreaCrack()
        # m_MoldPlate.Cal_Feature(var, timenow)

        dict_result['fOuterWideCrack'] = var.fOuterWideCrack.copy()
        dict_result['fInnerWideCrack'] = var.fInnerWideCrack.copy()
        dict_result['fRightNarrowCrack'] = var.fRightNarrowCrack.copy()
        dict_result['fLeftNarrowCrack'] = var.fLeftNarrowCrack.copy()

        dict_result['fOuterWide_TrickCrack'] = var.fOuterWide_TrickCrack.copy()
        dict_result['fInnerWide_TrickCrack'] = var.fInnerWide_TrickCrack.copy()
        dict_result['fRightNarrow_TrickCrack'] = var.fRightNarrow_TrickCrack.copy()
        dict_result['fLeftNarrow_TrickCrack'] = var.fLeftNarrow_TrickCrack.copy()

        # if timenow == 191:
        #
        #     with open("Crack_Sample_4_Tem_Diff.csv", 'a') as f:
        #         for i in range(var.fOuterWide_TrickCrack[1].shape[0]):
        #             for j in range(var.fOuterWide_TrickCrack[1].shape[1]):
        #                 f.write(str(i + 1))
        #                 f.write(",")
        #                 f.write(str(j + 1))
        #                 f.write(",")
        #                 f.write(str(var.fOuterWide_TrickCrack[1][i][j]))
        #                 f.write("\n")
        #
        #     print("Array saved to Crack_Sample_4_Tem_Diff.csv")
        #
        # else:
        #     pass

        # dict_result['Vx'] = m_MoldPlate.Vx.copy()
        # dict_result['Vy'] = m_MoldPlate.Vy.copy()
        # dict_result['Vc'] = m_MoldPlate.Vc.copy()
        # dict_result['Height'] = m_MoldPlate.Height.copy()
        # dict_result['Width'] = m_MoldPlate.Width.copy()
        # dict_result['Area'] = m_MoldPlate.Area.copy()

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



def calculate_process(var, m_MoldPlate, End_Time, accident_type, Cal_Result, dict_result):

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


        # if timenow == 55:
        #
        #     with open("Breakout_Sample_4_Tem_rate.csv", 'a') as f:
        #         for i in range(var.fInnerWide_Trick.shape[0]):
        #             for j in range(var.fInnerWide_Trick.shape[1]):
        #                 f.write(str(i + 1))
        #                 f.write(",")
        #                 f.write(str(j + 1))
        #                 f.write(",")
        #                 f.write(str(var.fInnerWide_Trick[i][j]))
        #                 f.write("\n")
        #
        #     print("Array saved to Breakout_Sample_4_Tem_rate.csv")
        #
        # else:
        #     pass



        dict_result['Vx'] = m_MoldPlate.Vx.copy()
        dict_result['Vy'] = m_MoldPlate.Vy.copy()
        dict_result['Vc'] = m_MoldPlate.Vc.copy()
        dict_result['Height'] = m_MoldPlate.Height.copy()
        dict_result['Width'] = m_MoldPlate.Width.copy()
        dict_result['Area'] = m_MoldPlate.Area.copy()
        dict_result['Gave'] = m_MoldPlate.Gave.copy()
        dict_result['Fourier'] = m_MoldPlate.Fourier.copy()
        dict_result['Sticking_Center'] = m_MoldPlate.Sticking_Center.copy()
        dict_result['Abnormal_Center'] = m_MoldPlate.Abnormal_Center.copy()
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




class MyMainWindow(QMainWindow, Ui_MainWindow, QWidget):

    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        # 建立主界面
        self.setupUi(self)  # 参数加self,表示传入当前类(MyMainWindow)的一个实例，它作为子类可以调用父类和子类的方法，
                            # 可以看做父类的实例(即QMainWindow的一个实例)

        # 每秒动态刷新界面
        self.timer_now = QTimer()
        self.timer_now.timeout.connect(self.startrefresh)


        # 向主窗口添加画布
        self.canvas_blank = Figure_Thermography()
        self.GridLayout_Figure.addWidget(self.canvas_blank, 0, 0, 1, 1)


        # 设置布尔变量判断当前是否有子进程正在运行
        self.process_is_running = False
        # 判断开始按钮是否被点击过
        self.Button_Start_clicked = False

        # #实例化画图线程类
        # self.thread1 = QThread()
        # #实例化线程锁对象
        # self.mutex = QMutex()
        # #实例化QWaitCondition对象
        # self.cond = QWaitCondition()
        # # 实例化自定义CallThread类对象
        # self.callthread = CallThread(timeinterval = gl.Variable(plant = gl.get_value("Data_Source"),
        #                                                         accident = gl.get_value("accident_type")).nTime_Window,
        #                                                         mutex = self.mutex, cond = self.cond)
        # # QThread只是管理线程的类，需把实例化的线程用moveToThread移到QThread中管理
        # self.callthread.moveToThread(self.thread1)
        # #线程开始执行之前，从相关线程发射信号
        # self.thread1.started.connect(self.callthread.work)
        # #接收信号
        # self.callthread.drawsignal.connect(self.startrefresh)
        # self.callthread.end.connect(self.endrefresh)
        # self.callthread.calprogress.connect(self.progresswarning)



        #设置当前时刻(水平滑块位置、开始按钮运行起始点)
        self.horizontalSlider.valueChanged.connect(self.ValueChange)
        gl.set_value("current_time", self.horizontalSlider.value())


        #绑定按钮信号与槽实践
        self.Button_ChooseFile.clicked.connect(self.chooseFileMethod)   #选择文件显示样本信息
        self.Button_Load_Switch.clicked.connect(self.Load_Switch_Index)
        self.Button_Start.clicked.connect(self.ClickedBtnStart)
        #self.Button_Start.clicked.connect(self.RefreshCurImage)
        self.Button_End.clicked.connect(self.ClickedBtnEnd)
        self.Button_Pre_Sec.clicked.connect(self.timetune)
        self.Button_Nex_Sec.clicked.connect(self.timetune)
        self.Button_PreviousFile.clicked.connect(self.LoadPreviousFile)
        self.Button_NextFile.clicked.connect(self.LoadNextFile)
        self.Button_Save_Image.clicked.connect(self.SaveImage)
        self.Button_Save_Feature.clicked.connect(self.SaveFeature)
        self.Button_Add_New_Feature.clicked.connect(self.AddNewFeature)


    def timetune(self):
        if self.LineEdit_SampleIndex.text() == "":
            QMessageBox.information(self, "提示", "请先选择文件!", QMessageBox.Ok)

        else:
            # 实现前一秒后一秒按钮功能
            if self.sender().text() == "前一秒":
                if not self.Button_Start_clicked:
                    QMessageBox.information(self, "消息", "请先点击开始按钮!", QMessageBox.Ok)
                else:

                    self.GridLayout_Figure.removeWidget(self.canvas_refresh)
                    gl.set_value("current_time", gl.get_value("current_time") - 1)
                    timenow = gl.get_value("current_time")

                    if timenow >= 0:
                        # 判断当前时刻画图所需数据是否计算完成，若未完成则等待
                        if not self.Cal_Result[timenow]:
                            gl.set_value("current_time", gl.get_value("current_time") + 1)
                            QMessageBox.information(self, "消息", "当前时刻数据未计算完成，请等待!", QMessageBox.Ok)
                            self.ClickedBtnEnd()
                        else:

                            self.horizontalSlider.setValue(timenow)
                            if gl.get_value("accident_type") == "漏钢":

                                self.canvas_refresh.PlotImg(self.Cal_Result[timenow][0])
                                # self.canvas_refresh.draw()
                                self.canvas_refresh.figs.canvas.draw()  # 画布重绘
                                self.canvas_refresh.figs.canvas.flush_events()  # 画布刷新
                                self.GridLayout_Figure.addWidget(self.canvas_refresh, 0, 0, 1, 1)

                            elif gl.get_value("accident_type") == "纵裂":

                                self.canvas_refresh.PlotImgCrack(self.Cal_Result[timenow][0], self.line)
                                # self.canvas_refresh.draw()
                                self.canvas_refresh.figs.canvas.draw()  # 画布重绘
                                self.canvas_refresh.figs.canvas.flush_events()  # 画布刷新
                                self.GridLayout_Figure.addWidget(self.canvas_refresh, 0, 0, 1, 1)

                            else:
                                QMessageBox.information(self, "消息", "异常类型出错!", QMessageBox.Ok)


                    else:
                        gl.set_value("current_time", self.horizontalSlider.value())
                        QMessageBox.information(self, "消息", "已经到达初始时刻!", QMessageBox.Ok)

            elif self.sender().text() == "后一秒":

                if not self.Button_Start_clicked:
                    QMessageBox.information(self, "消息", "请先点击开始按钮!", QMessageBox.Ok)
                else:

                    self.GridLayout_Figure.removeWidget(self.canvas_refresh)
                    gl.set_value("current_time", gl.get_value("current_time") + 1)
                    timenow = gl.get_value("current_time")

                    if timenow < gl.Variable(plant = gl.get_value("Data_Source"),
                    accident = gl.get_value("accident_type")).nTime_Window and \
                    timenow < gl.get_value("Alarm_Time"):

                        # 判断当前时刻画图所需数据是否计算完成，若未完成则等待
                        if not self.Cal_Result[timenow]:
                            gl.set_value("current_time", gl.get_value("current_time") - 1)
                            QMessageBox.information(self, "消息", "当前时刻数据未计算完成，请等待!", QMessageBox.Ok)
                            self.ClickedBtnEnd()

                        else:

                            self.horizontalSlider.setValue(timenow)

                            if gl.get_value("accident_type") == "漏钢":

                                self.canvas_refresh.PlotImg(self.Cal_Result[timenow][0])
                                # self.canvas_refresh.draw()
                                self.canvas_refresh.figs.canvas.draw()  # 画布重绘
                                self.canvas_refresh.figs.canvas.flush_events()  # 画布刷新
                                self.GridLayout_Figure.addWidget(self.canvas_refresh, 0, 0, 1, 1)

                            elif gl.get_value("accident_type") == "纵裂":

                                self.canvas_refresh.PlotImgCrack(self.Cal_Result[timenow][0], self.line)
                                # self.canvas_refresh.draw()
                                self.canvas_refresh.figs.canvas.draw()  # 画布重绘
                                self.canvas_refresh.figs.canvas.flush_events()  # 画布刷新
                                self.GridLayout_Figure.addWidget(self.canvas_refresh, 0, 0, 1, 1)

                            else:
                                QMessageBox.information(self, "消息", "异常类型出错!", QMessageBox.Ok)


                    else:
                        gl.set_value("current_time", self.horizontalSlider.value())
                        QMessageBox.information(self, "消息", "运行结束!", QMessageBox.Ok)
            else:

                QMessageBox.warning(self, "警告", "微调出错!", QMessageBox.Ok)

    def ValueChange(self):

        gl.set_value("current_time", self.horizontalSlider.value())

        Slider_Value = self.horizontalSlider.value()
        self.Slider_Time_Label.setText(gl.get_value("Slider_Time")[Slider_Value][Slider_Value])

    #点击开始按钮逐秒显示可视化图像
    def ClickedBtnStart(self):

        if self.LineEdit_SampleIndex.text() == "":
            QMessageBox.information(self, "提示", "请先选择文件!", QMessageBox.Ok)

        else:
            # 开始按钮被点击后，才会定义self.canvas_refresh对象，才能使用"前一秒"、"后一秒"功能
            self.Button_Start_clicked = True

            gl.set_value("current_time", self.horizontalSlider.value())

            if gl.get_value("accident_type") == "漏钢":
                self.canvas_refresh = Figure_Thermography(number_index=self.number_index)
            elif gl.get_value("accident_type") == "纵裂":
                self.canvas_refresh = Figure_Tem_Difference_Thermography(number_index=self.number_index)

                SelectedRow = self.Select_Mold_ComboBox.currentText().strip()
                if SelectedRow == "第一排":
                    self.line = 0
                elif SelectedRow == "第二排":
                    self.line = 1
                elif SelectedRow == "第三排":
                    self.line = 2
                else:
                    QMessageBox.information(self, "消息", "请选择有效的电偶排数!", QMessageBox.Ok)
            else:
                QMessageBox.information(self, "提示", "异常类型出错!", QMessageBox.Ok)

            self.GridLayout_Figure.removeWidget(self.canvas_blank)  # 移除初始化界面
            self.timer_now.start(1000)  # 1000 ms刷新一次


    def ClickedBtnEnd(self):

        if self.LineEdit_SampleIndex.text() == "":
            QMessageBox.information(self, "提示", "请先选择文件!", QMessageBox.Ok)

        else:
            self.timer_now.stop()

            if gl.get_value("current_time") == gl.Variable(plant = gl.get_value("Data_Source"),
                                                           accident = gl.get_value("accident_type")).nTime_Window or \
            gl.get_value("current_time") == gl.get_value("Alarm_Time"):

                QMessageBox.information(self, "消息", "运行结束!", QMessageBox.Ok)

    def startrefresh(self):

        # 每秒刷新图像时移除原有图像
        self.GridLayout_Figure.removeWidget(self.canvas_refresh)

        gl.set_value("current_time", gl.get_value("current_time") + 1)
        timenow = gl.get_value("current_time")
        accident_type = gl.get_value("accident_type")

        if timenow < gl.Variable(plant = gl.get_value("Data_Source"),
                                accident = accident_type).nTime_Window and timenow < gl.get_value("Alarm_Time"):

            # 判断当前时刻画图所需数据是否计算完成，若未完成则等待
            if not self.Cal_Result[timenow]:
                gl.set_value("current_time", gl.get_value("current_time") - 1)
                QMessageBox.information(self, "消息", "当前时刻数据未计算完成，请等待!", QMessageBox.Ok)
                self.ClickedBtnEnd()
            else:

                self.horizontalSlider.setValue(timenow)

                if accident_type == "漏钢":

                    self.canvas_refresh.PlotImg(self.Cal_Result[timenow][0])
                    # 重要!!!需要调用draw函数来绘图,否则图像不会实时更新
                    # self.canvas_refresh.draw()
                    self.canvas_refresh.figs.canvas.draw()      # 画布重绘
                    self.canvas_refresh.figs.canvas.flush_events()      # 画布刷新
                    self.GridLayout_Figure.addWidget(self.canvas_refresh, 0, 0, 1, 1)

                elif accident_type == "纵裂":

                    self.canvas_refresh.PlotImgCrack(self.Cal_Result[timenow][0], self.line)
                    # self.canvas_refresh.draw()
                    self.canvas_refresh.figs.canvas.draw()      # 画布重绘
                    self.canvas_refresh.figs.canvas.flush_events()      # 画布刷新
                    self.GridLayout_Figure.addWidget(self.canvas_refresh, 0, 0, 1, 1)
                else:
                    QMessageBox.information(self, "消息", "异常类型出错!", QMessageBox.Ok)
                    self.ClickedBtnEnd()


        else:
            self.ClickedBtnEnd()

        # 唤醒其它线程
        # self.cond.wakeAll()
        # #调用raise_()函数将控件置顶, self.pushButton是建立在self.widget上的，所以将self.widget置顶即可
        # self.widget.raise_()


    # 动态显示当前时间
    def setDateTimeInfo(self):
        time = QDateTime.currentDateTime()
        timeDisplay = time.toString("yyyy-MM-dd hh:mm:ss dddd")
        self.Label_Time_Now.setText(timeDisplay)


    #以table形式汇总样本信息
    def chooseFileMethod(self):

        fileName, _ = QFileDialog.getOpenFileName(self, "选取文件", '.', "All Files(*);;Text ""Files(*.txt)")

        if fileName != "":  # 防止打开而没有选取文件时导致的路径为空
            data_Sample_Information = gl.loadDataSet(fileName)

            self.tableWidget_Sample_Information.setRowCount(len(data_Sample_Information))
            self.tableWidget_Sample_Information.setColumnCount(len(data_Sample_Information[0]))
            # 禁止编辑单元格内容
            self.tableWidget_Sample_Information.setEditTriggers(QAbstractItemView.NoEditTriggers)

            if data_Sample_Information[0][2] == "F" or data_Sample_Information[0][2] == "B" or\
                data_Sample_Information[0][2] == "S":
                # 设定异常类型
                gl.set_value("accident_type", "漏钢")
                self.tableWidget_Sample_Information.setHorizontalHeaderLabels(["Data", "Time", "Type"])
            else:
                # 设定异常类型
                gl.set_value("accident_type", "纵裂")
                self.tableWidget_Sample_Information.setHorizontalHeaderLabels(["Data", "Time", "Column"])
            #根据内容自动调整宽度
            self.tableWidget_Sample_Information.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            for row in range(len(data_Sample_Information)):
                for column in range(len(data_Sample_Information[row])):
                    item = QTableWidgetItem(str(data_Sample_Information[row][column]))
                    self.tableWidget_Sample_Information.setItem(row, column, item)

        else:
            QMessageBox.warning(self, "警告", "请先选择有效的数据文件!", QMessageBox.Ok)

        gl.set_value('SampleList', fileName)


    def Load_Switch_Index(self):
        # 加载/跳转按钮的功能：（1）当未开始绘图时，加载数据信息；（2）跳转绘图时，直接跳转对应序号的图像，未输入序号时跳转到第一个图像
        num = self.LineEdit_Switch.text()

        dirPath = QFileDialog.getExistingDirectory(None, '获取文件夹路径', 'E:\\')  # 设置E盘为默认打开目录
        if dirPath != "":
            gl.set_value('DirPlantPath', dirPath)

            if num == "":
                self.number_index = 1
                self.DisplaySampleInfo()
            else:
                self.number_index = int(num)
                self.DisplaySampleInfo()
                self.LineEdit_Switch.setText("")
        else:
            QMessageBox.warning(self, "警告", "请先选择有效数据路径!", QMessageBox.Ok)


    def LoadPreviousFile(self):
        # 点击上一个文件按钮时，加载上一个索引对应的文件
        self.DetectProcess()

        if self.LineEdit_SampleIndex.text() == "":
            QMessageBox.information(self, "提示", "请先选择文件!", QMessageBox.Ok)
        else:
            Totalnum = gl.get_value('TotalNum')
            self.number_index -= 1
            if self.number_index >= 1:
                self.DisplaySampleInfo()
            else:
                reply = QMessageBox.question(self, "询问对话框", "当前是第一个文件, 是否跳转到最后一个？", QMessageBox.Yes | QMessageBox.No)
                if reply == QMessageBox.Yes:
                    self.number_index = Totalnum
                    self.DisplaySampleInfo()

    def LoadNextFile(self):
        # 点击下一个文件按钮时，绘制下一个索引对应的图像
        self.DetectProcess()

        if self.LineEdit_SampleIndex.text() == "":
            QMessageBox.information(self, "提示", "请先选择文件!", QMessageBox.Yes)
        else:
            Totalnum = gl.get_value('TotalNum')
            self.number_index += 1
            if self.number_index <= Totalnum:
                self.DisplaySampleInfo()
            else:
                reply = QMessageBox.question(self, "询问对话框", "当前已是最后一个文件, 是否从头开始？", QMessageBox.Yes | QMessageBox.No)
                if reply == QMessageBox.Yes:
                    self.number_index = 1
                    self.DisplaySampleInfo()


    def DisplaySampleInfo(self):

        self.DetectProcess()

        if gl.get_value("accident_type") == "漏钢":

            self.sampleinfo = Figure_Thermography(number_index=self.number_index)
            self.sampleinfo.LoadSampleInfo()       #调用加载数据方法

            #多进程之间数据不共享，所以只能通过传参的方式进行通信
            # cal_out_pipe, cal_in_pipe = Pipe(True)

            var = gl.get_value('Variable')
            AlarmTime = gl.get_value("Alarm_Time")
            End_Time = min(gl.Variable(plant = gl.get_value("Data_Source"),
            accident = gl.get_value("accident_type")).nTime_Window, AlarmTime)
            accident_type = gl.get_value("accident_type")
            self.horizontalSlider.setMaximum(End_Time - 1)
            #在主线程中定义Manager类型的列表和字典，子线程中对其修改值同时会更改主线程中该变量的值，即数据共享
            self.Cal_Result = Manager().list()
            self.dict_result = Manager().dict()

            for _ in range(End_Time):
                self.Cal_Result.append([])

            m_MoldPlate = CMoldPlate()
            m_MoldPlate.Initialize()

            self.calprocess = Process(target = calculate_process, args = (var, m_MoldPlate, End_Time, accident_type, self.Cal_Result, self.dict_result))
            # 设置子进程为守护进程，即主进程结束后子进程也相应结束
            self.calprocess.daemon = True
            self.calprocess.start()
            self.process_is_running = True
            #不能阻塞主线程否则会导致主界面失去响应无法按开始键刷新界面
            #calprocess.join()

            #Pipe参数为True代表管道是双向的，既能接收数据也能发送数据
            #https://blog.csdn.net/qq_38638132/article/details/109605012
            # cal_out_pipe, cal_in_pipe = Pipe(True)
            #
            # self.calprocess = Process(target=calculate_test, args = (var, AlarmTime, CurrentTime, cal_out_pipe, cal_in_pipe))
            # self.calprocess.start()
            #
            # #关闭主线程中的输入端，只剩输出端来接收数据
            # cal_in_pipe.close()
            #
            # try:
            #     self.cal = cal_out_pipe.recv()
            #     print(self.cal[58][0]['Area'])
            #     # if msg == "滑块未置0!":
            #     #     self.calprocess.join()
            #     #     QMessageBox.critical(self, "错误", "初始5秒数据无效，请将滑块置于0位置!", QMessageBox.Ok)
            #     # elif msg == "计算进程完成!":
            #     #     self.calprocess.join()
            #     #     QMessageBox.information(self, "消息", "计算进程已完成!", QMessageBox.Ok)
            # except EOFError:
            #     """ 当out_pipe接受不到输出的时候且输入被关闭的时候，会抛出EORFError，可以捕获并且退出子进程 """
            #     print("数据接收异常!")

            # 启动计算线程(同一个线程只有在完全退出之后才能再次启动!!!)
            # self.thread2.start()
            # pool.submit(self.calculatethread.calculate)

            # #调用raise_()函数将控件置顶, self.pushButton是建立在self.widget上的，所以将self.widget置顶即可
            # self.widget.raise_()
            self.LineEdit_SampleType.setText(gl.get_value('SampleType'))
            self.LineEdit_Year.setText(gl.get_value('year'))
            self.LineEdit_Month.setText(gl.get_value('month'))
            self.LineEdit_Day.setText(gl.get_value('day'))
            self.LineEdit_Hour.setText(gl.get_value('hour'))
            self.LineEdit_Minute.setText(gl.get_value('minute'))
            self.LineEdit_Second.setText(gl.get_value('second'))
            self.LineEdit_SampleIndex.setText(str(self.number_index) + " / " + str(gl.get_value('TotalNum')))
            self.LineEdit_FileInformation.setText(gl.get_value("file_path"))

            # 绘制当前数据样本信息
            self.Label_Sample_Now.setText("#" + str(self.number_index) + "  " + gl.get_value('Data_Source') + "  " +
            gl.get_value("date") + "  " + gl.get_value("time") + "  " + gl.get_value("SampleType"))


            #清空下拉列表,添加新项目
            self.Select_Mold_ComboBox.clear()
            rows = ["       外弧宽面Tv", "       内弧宽面Tv", "       右侧窄面Tv", "       左侧窄面Tv"]
            self.Select_Mold_ComboBox.addItems(rows)


            self.Initial_Time_Label.setText(gl.get_value("Slider_Time")[0][0])
            self.End_Time_Label.setText(gl.get_value("Slider_Time")[End_Time - 1][End_Time - 1])
            Slider_Value = self.horizontalSlider.value()
            self.Slider_Time_Label.setText(gl.get_value("Slider_Time")[Slider_Value][Slider_Value])

            QMessageBox.information(self, "消息", "初始5秒为无效数据，请将滑块置于0位置加载数据!", QMessageBox.Ok)

        elif gl.get_value("accident_type") == "纵裂":

            self.sampleinfo = Figure_Tem_Difference_Thermography(number_index=self.number_index)
            self.sampleinfo.LoadSampleInfoCrack()       #调用加载数据方法

            #多进程之间数据不共享，所以只能通过传参的方式进行通信
            # cal_out_pipe, cal_in_pipe = Pipe(True)

            var = gl.get_value('Variable')
            End_Time = gl.get_value("nTime_Duration")
            accident_type = gl.get_value("accident_type")
            self.horizontalSlider.setMaximum(End_Time - 1)
            #在主线程中定义Manager类型的列表和字典，子线程中对其修改值同时会更改主线程中该变量的值，即数据共享
            self.Cal_Result = Manager().list()
            self.dict_result = Manager().dict()

            for _ in range(End_Time):
                self.Cal_Result.append([])

            m_MoldPlate = CMoldPlate()
            m_MoldPlate.Initialize()

            self.calprocess = Process(target = calculate_crack_process, args = (var, m_MoldPlate, End_Time, accident_type, self.Cal_Result, self.dict_result))
            self.calprocess.daemon = True
            self.calprocess.start()
            self.process_is_running = True

            #不能阻塞主线程否则会导致主界面失去响应无法按开始键刷新界面
            #calprocess.join()

            #Pipe参数为True代表管道是双向的，既能接收数据也能发送数据
            #https://blog.csdn.net/qq_38638132/article/details/109605012
            # cal_out_pipe, cal_in_pipe = Pipe(True)
            #
            # self.calprocess = Process(target=calculate_test, args = (var, AlarmTime, CurrentTime, cal_out_pipe, cal_in_pipe))
            # self.calprocess.start()
            #
            # #关闭主线程中的输入端，只剩输出端来接收数据
            # cal_in_pipe.close()
            #
            # try:
            #     self.cal = cal_out_pipe.recv()
            #     print(self.cal[58][0]['Area'])
            #     # if msg == "滑块未置0!":
            #     #     self.calprocess.join()
            #     #     QMessageBox.critical(self, "错误", "初始5秒数据无效，请将滑块置于0位置!", QMessageBox.Ok)
            #     # elif msg == "计算进程完成!":
            #     #     self.calprocess.join()
            #     #     QMessageBox.information(self, "消息", "计算进程已完成!", QMessageBox.Ok)
            # except EOFError:
            #     """ 当out_pipe接受不到输出的时候且输入被关闭的时候，会抛出EORFError，可以捕获并且退出子进程 """
            #     print("数据接收异常!")

            # 启动计算线程(同一个线程只有在完全退出之后才能再次启动!!!)
            # self.thread2.start()
            # pool.submit(self.calculatethread.calculate)

            # #调用raise_()函数将控件置顶, self.pushButton是建立在self.widget上的，所以将self.widget置顶即可
            # self.widget.raise_()
            self.LineEdit_SampleType.setText(gl.get_value('column'))
            self.Label_SampleType.setText("列数")
            self.LineEdit_Year.setText(gl.get_value('year'))
            self.LineEdit_Month.setText(gl.get_value('month'))
            self.LineEdit_Day.setText(gl.get_value('day'))
            self.LineEdit_Hour.setText(gl.get_value('hour'))
            self.LineEdit_Minute.setText(gl.get_value('minute'))
            self.LineEdit_Second.setText(gl.get_value('second'))
            self.LineEdit_SampleIndex.setText(str(self.number_index) + " / " + str(gl.get_value('TotalNum')))
            self.LineEdit_FileInformation.setText(gl.get_value("file_path"))

            # 绘制当前数据样本信息
            self.Label_Sample_Now.setText("#" + str(self.number_index) + "  " + gl.get_value('Data_Source') + "  " +
            gl.get_value("date") + "  " + gl.get_value("time") + "  " + gl.get_value("column") + "列")


            self.Initial_Time_Label.setText(gl.get_value("Slider_Time")[0][0])
            self.End_Time_Label.setText(gl.get_value("Slider_Time")[End_Time - 1][End_Time - 1])
            Slider_Value = self.horizontalSlider.value()
            self.Slider_Time_Label.setText(gl.get_value("Slider_Time")[Slider_Value][Slider_Value])

            #清空下拉列表,添加新项目
            self.Select_Mold_ComboBox.clear()
            rows = ["         第一排", "         第二排", "         第三排"]
            self.Select_Mold_ComboBox.addItems(rows)

            QMessageBox.information(self, "消息", "初始65秒为无效数据，请将滑块置于0位置加载数据!", QMessageBox.Ok)
            QMessageBox.information(self, "消息", "请选择合适的电偶排数!", QMessageBox.Ok)

        else:
            QMessageBox.information(self, "提示", "异常类型出错!", QMessageBox.Ok)


    def SaveImage(self):

        if gl.get_value("accident_type") == "漏钢":

            Slider_Value = self.horizontalSlider.value()
            Slider_Time = gl.get_value("Slider_Time")[Slider_Value][Slider_Value]
            Selected_Mold = self.Select_Mold_ComboBox.currentText().strip()    #调用strip方法去掉多余的空格
            reply = QMessageBox.question(self, "提示", "是否保存{}{}图像？".format(Slider_Time, Selected_Mold), QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:

                Saved_Types = ('漏钢', '误报', '稳态')
                # 自定义QInputDialog类对象实现调整窗口大小以适应标题长度(解决窗口标题文字显示不全的问题)
                input_dialog_3 = QInputDialog(self)
                # input_dialog_1.setInputMode(QInputDialog.TextInput)
                input_dialog_3.setWindowTitle("请选择保存类型")
                input_dialog_3.setLabelText("类型列表")
                input_dialog_3.setComboBoxEditable(False)
                input_dialog_3.setComboBoxItems(Saved_Types)
                input_dialog_3.resize(220, 100)
                input_dialog_3.show()

                if input_dialog_3.exec_() == input_dialog_3.Accepted:
                    Selected_Type = input_dialog_3.textValue()  # 点击ok 后 获取输入对话框内容

                    # # 保存图像索引信息
                    # with open(".//漏钢图像索引.txt",'a') as file:
                    #     file.write(gl.get_value("Data_Source"))
                    #     file.write('\t')
                    #     file.write(gl.get_value("date"))
                    #     file.write('\t')
                    #     file.write(Slider_Time)
                    #     file.write('\t')
                    #     file.write(Selected_Mold)
                    #     file.write('\t')
                    #     file.write(Selected_Type)
                    #     file.write('\n')

                    # 保存图像
                    filedir1 = "南钢图像//" if gl.get_value("Data_Source") == "南钢" else "鞍钢图像//" if gl.get_value("Data_Source") == "鞍钢" else None
                    filedir2 = "漏钢样本//"
                    filedir3 = "漏钢//" if Selected_Type == "漏钢" else "误报//" if Selected_Type == "误报" else "稳态//" if Selected_Type == "稳态" else None
                    #一个点(.)代表当前目录，两个点(..)代表上级目录
                    ImgPath = os.path.join(".//", filedir1, filedir2, filedir3)

                    #若文件路径不存在，则创建文件路径
                    if not os.path.exists(ImgPath):
                        os.makedirs(ImgPath)

                    drawdata = self.Cal_Result[Slider_Value][0]

                    date = gl.get_value("date")
                    datenew = '.'.join(date.split('/'))

                    time = Slider_Time
                    timenew = '.'.join(time.split(':'))

                    ImgName = ImgPath + datenew + "  " + timenew + "  " + Selected_Mold + ".jpg"
                    Figure_Thermography().ImageToFile(drawdata, ImgName, Selected_Mold)

                    if os.path.exists(ImgName):
                        QMessageBox.information(self, "消息", "图像保存成功!", QMessageBox.Ok)
                    else:
                        QMessageBox.information(self, "消息", "图像保存失败!", QMessageBox.Ok)

                else:
                    pass

            else:
                pass

        elif gl.get_value("accident_type") == "纵裂":

            Slider_Value = self.horizontalSlider.value()
            Slider_Time = gl.get_value("Slider_Time")[Slider_Value][Slider_Value]
            Selected_Row = self.Select_Mold_ComboBox.currentText().strip()    #调用strip方法去掉多余的空格
            Molds = ('外弧宽面Td', '内弧宽面Td', '右侧窄面Td', '左侧窄面Td')
            # 自定义QInputDialog类对象实现调整窗口大小以适应标题长度(解决窗口标题文字显示不全的问题)
            input_dialog_0 = QInputDialog(self)
            input_dialog_0.setInputMode(QInputDialog.TextInput)
            input_dialog_0.setWindowTitle("请选择铜板")
            input_dialog_0.setLabelText("铜板列表")
            input_dialog_0.setComboBoxEditable(False)
            input_dialog_0.setComboBoxItems(Molds)
            input_dialog_0.resize(200, 100)
            input_dialog_0.show()
            if input_dialog_0.exec_() == input_dialog_0.Accepted:
                Selected_Mold = input_dialog_0.textValue()  # 点击ok 后 获取输入对话框内容
                reply = QMessageBox.question(self, "提示", "是否保存{}电偶拓出的{}{}图像？".format(Selected_Row, Slider_Time,
                                                                        Selected_Mold), QMessageBox.Yes | QMessageBox.No)
                if reply == QMessageBox.Yes:
                    Saved_Types = ('纵裂', '稳态', '不确定')
                    #自定义QInputDialog类对象实现调整窗口大小以适应标题长度(解决窗口标题文字显示不全的问题)
                    input_dialog_1 = QInputDialog(self)
                    input_dialog_1.setInputMode(QInputDialog.TextInput)
                    input_dialog_1.setWindowTitle("请选择保存类型")
                    input_dialog_1.setLabelText("类型列表")
                    input_dialog_1.setComboBoxEditable(False)
                    input_dialog_1.setComboBoxItems(Saved_Types)
                    input_dialog_1.resize(220, 100)
                    input_dialog_1.show()

                    if input_dialog_1.exec_() == input_dialog_1.Accepted:
                        Selected_Type = input_dialog_1.textValue()  # 点击ok 后 获取输入对话框内容

                        # 保存图像索引信息
                        with open(".//纵裂图像索引.txt",'a') as file:
                            file.write(gl.get_value("Data_Source"))
                            file.write('\t')
                            file.write(gl.get_value("date"))
                            file.write('\t')
                            file.write(Slider_Time)
                            file.write('\t')
                            file.write(Selected_Row)
                            file.write('\t')
                            file.write(Selected_Mold)
                            file.write('\t')
                            file.write(gl.get_value("column"))
                            file.write('\t')
                            file.write(Selected_Type)
                            file.write('\n')


                        # 保存图像
                        filedir1 = "南钢图像//" if gl.get_value("Data_Source") == "南钢" else "鞍钢图像//" if gl.get_value("Data_Source") == "鞍钢" else None
                        filedir2 = "纵裂样本//"
                        filedir3 = "纵裂//" if Selected_Type == "纵裂" else "稳态//" if Selected_Type == "稳态" else \
                            "不确定//" if Selected_Type == "不确定" else None
                        #一个点(.)代表当前目录，两个点(..)代表上级目录
                        ImgPath = os.path.join(".//", filedir1, filedir2, filedir3)

                        if not os.path.exists(ImgPath):
                            os.makedirs(ImgPath)

                        drawdata = self.Cal_Result[Slider_Value][0]

                        date = gl.get_value("date")
                        datenew = '.'.join(date.split('/'))

                        time = Slider_Time
                        timenew = '.'.join(time.split(':'))

                        ImgName = ImgPath + datenew + "  " + timenew + "  " + Selected_Row + "  " +  Selected_Mold + \
                                  "  " + gl.get_value("column") + ".jpg"

                        Figure_Tem_Difference_Thermography().CrackImageToFile(drawdata, ImgName, Selected_Mold, self.line)

                        if os.path.exists(ImgName):
                            QMessageBox.information(self, "消息", "图像保存成功!", QMessageBox.Ok)
                        else:
                            QMessageBox.information(self, "消息", "图像保存失败!", QMessageBox.Ok)

                else:
                    pass

        else:
            QMessageBox.information(self, "提示", "异常类型出错!", QMessageBox.Ok)


    def SaveFeature(self):
        # 提取黏结区域特征时注意:当前时刻和前5秒时刻均为有效数据才行，故提取时刻点需在起始点10s以后(前5秒为无效数据+5秒无效特征共10秒)
        if gl.get_value("accident_type") == "漏钢":

            Slider_Value = self.horizontalSlider.value()
            Slider_Time = gl.get_value("Slider_Time")[Slider_Value][Slider_Value]
            Selected_Mold = self.Select_Mold_ComboBox.currentText().strip()    #调用strip方法去掉多余的空格
            reply = QMessageBox.question(self, "提示", "是否保存{}{}特征？".format(Slider_Time, Selected_Mold), QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                drawdata = self.Cal_Result[Slider_Value][0]

                if Selected_Mold == "外弧宽面Tv":
                    Moldindex = 0
                elif Selected_Mold == "内弧宽面Tv":
                    Moldindex = 2
                elif Selected_Mold == "右侧窄面Tv":
                    Moldindex = 1
                elif Selected_Mold == "左侧窄面Tv":
                    Moldindex = 3
                else:
                    Moldindex = None


                sticker_list = []
                for sticker in range(len(drawdata['Vx'][Moldindex])):
                    sticker_list.append(
                    'Vx' + '[' + str(sticker) + ']' + ':' + str(format(drawdata['Vx'][Moldindex][sticker], '.3f')) + "  "+
                    'Vy' + '[' + str(sticker) + ']' + ':' + str(format(drawdata['Vy'][Moldindex][sticker], '.3f')) + "  " +
                    'Vc' + '[' + str(sticker) + ']' + ':' + str(format(drawdata['Vc'][Moldindex][sticker], '.3f'))  + "  " +
                    'Sticking_Expansion' + '[' + str(sticker) + ']' + ':' + str(format(drawdata['Sticking_Expansion'][Moldindex][sticker], '.3f')) + "  " +
                    'Height' + '[' + str(sticker) + ']' + ':' + str(format(drawdata['Height'][Moldindex][sticker], '.3f')) + "  " +
                    'Width' + '[' + str(sticker) + ']'+ ':' + str(format(drawdata['Width'][Moldindex][sticker], '.3f')) + "  " +
                    'Area' + '[' + str(sticker) + ']'+ ':' + str(format(drawdata['Area'][Moldindex][sticker], '.3f')) + "  " +
                    'Gave' + '[' + str(sticker) + ']'+ ':' + str(format(drawdata['Gave'][Moldindex][sticker], '.3f')) + "  " +
                    'Fourier' + '[' + str(sticker) + ']'+ ':' + str(format(drawdata['Fourier'][Moldindex][sticker], '.3f')) + "  " +
                    'Sticking_CenterX' + '[' + str(sticker) + ']'+ ':' + str(format(drawdata['Sticking_Center'][Moldindex][sticker][0], '.0f')) + "  " +
                    'Sticking_CenterY' + '[' + str(sticker) + ']'+ ':' + str(format(drawdata['Sticking_Center'][Moldindex][sticker][1], '.0f')))



                # 当前时刻没有可提取的特征
                if sticker_list == []:
                    sticker_list.append("当前时刻无可提取特征")
                else:
                    pass

                input_dialog_2 = QInputDialog(self)
                # input_dialog_2.setInputMode(QInputDialog.TextInput)
                input_dialog_2.setWindowTitle("请选择黏结区域")
                input_dialog_2.setLabelText("黏结区域列表")
                input_dialog_2.setComboBoxEditable(False)
                input_dialog_2.setComboBoxItems(sticker_list)   #sticker_list为可迭代的对象，数据类型为str
                input_dialog_2.resize(500, 200)
                input_dialog_2.show()

                if input_dialog_2.exec_() == input_dialog_2.Accepted:
                    sticker_region = input_dialog_2.textValue()  # 点击ok 后 获取输入对话框内容
                    if sticker_region != "当前时刻无可提取特征":
                        self.sticker_num = int(sticker_region[3])

                        Saved_Types = ('漏钢', '误报', '稳态')
                        # 自定义QInputDialog类对象实现调整窗口大小以适应标题长度(解决窗口标题文字显示不全的问题)
                        input_dialog_4 = QInputDialog(self)
                        # input_dialog_1.setInputMode(QInputDialog.TextInput)
                        input_dialog_4.setWindowTitle("请选择保存类型")
                        input_dialog_4.setLabelText("类型列表")
                        input_dialog_4.setComboBoxEditable(False)
                        input_dialog_4.setComboBoxItems(Saved_Types)
                        input_dialog_4.resize(220, 100)
                        input_dialog_4.show()

                        if input_dialog_4.exec_() == input_dialog_4.Accepted:
                            Selected_Type = input_dialog_4.textValue()  # 点击ok 后 获取输入对话框内容

                            # 利用format函数保留特定的小数位数
                            sticker_dict = {"钢厂": [gl.get_value("Data_Source")], "日期": [gl.get_value("date")],
                                            "时间": [Slider_Time],
                                            "铜板": [Selected_Mold], "类型": [Selected_Type],
                                            "Vx": format(drawdata['Vx'][Moldindex][self.sticker_num], '.3f'),
                                            "Vy": format(drawdata['Vy'][Moldindex][self.sticker_num], '.3f'),
                                            "Vc": format(drawdata['Vc'][Moldindex][self.sticker_num], '.3f'),
                                            "Sticking_Expansion": format(drawdata['Sticking_Expansion'][Moldindex][self.sticker_num], '.3f'),
                                            "Height": format(drawdata['Height'][Moldindex][self.sticker_num], '.3f'),
                                            "Width": format(drawdata['Width'][Moldindex][self.sticker_num], '.3f'),
                                            "Area": format(drawdata['Area'][Moldindex][self.sticker_num], '.3f'),
                                            "Gave": format(drawdata['Gave'][Moldindex][self.sticker_num], '.3f'),
                                            "Fourier": format(drawdata['Fourier'][Moldindex][self.sticker_num], '.3f')
                                            }

                            # 保存特征向量
                            try:

                                filename = "黏结区域特征向量.csv"
                                if not os.path.exists(filename):
                                    data = pd.DataFrame(sticker_dict)  # sticker_dict需要是字典格式
                                    # mode='a'表示追加, index=True表示给每行数据加索引序号, header=False表示不加标题
                                    data.to_csv(filename, mode='a', index=False, header=True, encoding='GB18030')
                                else:
                                    # 若文件已存在，则追加数据时不需要加标题
                                    data = pd.DataFrame(sticker_dict)
                                    data.to_csv(filename, mode='a', index=False, header=False, encoding='GB18030')

                                QMessageBox.information(self, "消息", "特征保存成功!", QMessageBox.Ok)

                            except IOError:

                                QMessageBox.information(self, "消息", "文件打开或写入异常,特征保存失败!", QMessageBox.Ok)

                        else:
                            pass

                    else:
                        QMessageBox.information(self, "消息", "当前时刻无可提取特征!", QMessageBox.Ok)


                else:
                    pass

            else:
                pass

        elif gl.get_value("accident_type") == "纵裂":
            pass

        else:
            QMessageBox.information(self, "提示", "异常类型出错!", QMessageBox.Ok)



    def AddNewFeature(self):
        # 选取批处理文件路径及数据源路径
        fileName, _ = QFileDialog.getOpenFileName(self, "请选取批处理文件", '.', "All Files(*);;Excel""Files(*.csv)")

        if fileName != "":  # 防止打开而没有选取文件时导致的路径为空
            gl.set_value("accident_type", "漏钢")
            gl.set_value('SampleList', fileName)

            dirPath = QFileDialog.getExistingDirectory(self, '获取数据源路径', 'E:\\')  # 设置E盘为默认打开目录
            if dirPath != "":
                gl.set_value('DirPlantPath', dirPath)
                # 按照选择的已有文件列表批量添加新特征
                QMessageBox.information(self, "消息", "开始批量计算!", QMessageBox.Ok)
                Batch_Adding_Features()
                QMessageBox.information(self, "消息", "批量输出结束!", QMessageBox.Ok)


            else:
                QMessageBox.warning(self, "警告", "添加数据源路径错误!", QMessageBox.Ok)


        else:
            QMessageBox.warning(self, "警告", "选取批处理文件错误!", QMessageBox.Ok)




    def DetectProcess(self):

        # 判断当前子进程是否存在并且正在运行
        if self.process_is_running == True:
            if self.calprocess.is_alive() == True:
                # 终止当前计算子进程再开启新的计算子进程
                self.calprocess.terminate()
                self.calprocess.join()
            else:
                pass
        else:
            pass




if __name__ == "__main__":

    # 解决pyqt5多进程程序打包后，运行出现多个窗口的问题
    freeze_support()
    app = QApplication(sys.argv)
    myWindow = MyMainWindow()
    myWindow.show()
    sys.exit(app.exec_())
