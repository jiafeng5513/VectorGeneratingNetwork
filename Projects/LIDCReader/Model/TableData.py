from PyQt5.QtGui import QStandardItem
from PyQt5.QtWidgets import QHeaderView

import logging

class TableData():
    def TableViewInit(self, tableView, Model):
        '''表格初始化'''
        try:
            self.DataModel = Model
            self.tableView = tableView

            self.HeaderList = []
            for i in range(1, 5):
                self.HeaderList.append("医生"+str(i))
            self.vHeaderList = []
            self.vHeaderList.append("医生ID")
            self.vHeaderList.append("结节数")
            self.vHeaderList.append(">3mm结节数")
            self.vHeaderList.append("非结节数")
            self.DataModel.setHorizontalHeaderLabels(self.HeaderList)
            self.DataModel.setVerticalHeaderLabels(self.vHeaderList)

            self.tableView.setModel(self.DataModel)

            # 填满窗口
            # self.tableView.horizontalHeader().setStretchLastSection(True)
            self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            return True
        except Exception as e:
            logging(e)

    def Model_setItem(self, row, column, data):
        '''表格添加数据：第row行，column列数据更改为data'''
        self.DataModel.setItem(row, column, QStandardItem(data))