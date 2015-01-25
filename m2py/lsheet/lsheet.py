#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
https://www.youtube.com/watch?v=KuFbGXSFx_I
"""

from subprocess import Popen

from m2py.lsheet import uno
import hof
import pprint

ctx = uno.getComponentContext()
smgr = ctx.ServiceManager

NoConnectionException = uno.getClass("com.sun.star.connection.NoConnectException")
RuntimeException = uno.getClass("com.sun.star.uno.RuntimeException")
ErrorCodeIOException = uno.getClass("com.sun.star.task.ErrorCodeIOException")
PropertyValue = uno.getClass("com.sun.star.beans.PropertyValue")


def dialog():
    oDM = smgr.createInstance("com.sun.star.awt.UnoControlDialogModel")
    oDM.Width = 240
    oDM.Height = 150
    oDialog = smgr.createInstance("com.sun.star.awt.UnoControlDialog")
    oDialog.setModel(oDM)
    oDialog.setVisible(True)


# Generate some useful constants
EMPTY = uno.Enum("com.sun.star.table.CellContentType", "EMPTY")
TEXT = uno.Enum("com.sun.star.table.CellContentType", "TEXT")
FORMULA = uno.Enum("com.sun.star.table.CellContentType", "FORMULA")
VALUE = uno.Enum("com.sun.star.table.CellContentType", "VALUE")



def start_soffice():
    p = Popen(["soffice", '''--accept="socket,host=localhost,port=2002;urp;"'''])
    return p


class SOffice:
    def __init__(self):
        self.local = uno.getComponentContext()
        self.resolver = self.local.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver",
                                                                            self.local)
        self.context = self.resolver.resolve("uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext")
        self.desktop = self.context.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop", self.context)
        self.document = self.desktop.getCurrentComponent()


    def new_document(self, doctype):
        """
        :param doctype: "scalc", "swriter"
        :return:
        """
        doc = self.desktop.loadComponentFromURL("private:factory/{}".format(doctype), "_blank", 0, ())
        return doc


    def new_calc(self):
        return Osheet(self.desktop.loadComponentFromURL("private:factory/scalc", "_blank", 0, ()))

    def open(self, filename):
        url = uno.systemPathToFileUrl(filename)
        doc = self.desktop.loadComponentFromURL(url, "_blank", 0, ())
        return Osheet(doc)


class Cell:

    def __init__(self, cellboject):
        self.cell = cellboject

    @property
    def type(self):
        """
        :return: 'EMPTY', 'TEXT', 'VALUE'
        """
        return self.cell.getType().value

    @property
    def classtype(self):
        """
        :return:  'ScCellObj', 'ScCellRangeObj'
        """
        return self.cell.getImplementationName()

    def is_text(self):
        return self.type == "TEXT"

    def is_empty(self):
        return self.type == "EMPTY"

    def is_value(self):
        return self.type == "VALUE"

    def is_formula(self):
        return self.type == "FORMULA"


    def is_cell(self):
        return self.classtype == 'ScCellObj'

    def is_range(self):
        return self.classtype == 'ScCellRangeObj'


    @property
    def value(self):

        if self.is_range():
            return self.cell.getDataArray()

        if self.is_value():
            return self.cell.getValue()

        elif self.is_text():
            return self.cell.getString()

    @value.setter
    def value(self, _val):

        if self.is_range():
            self.cell.setDataArray(tuple(_val))
            return

        if isinstance(_val, str):
            self.cell.setString(_val)

        elif isinstance(_val, float) or isinstance(_val, int):
            self.cell.setValue(_val)

    @property
    def absname(self):
        return self.cell.AbsoluteName


    @property
    def row(self):
        return self.cell.CellAddress.value.Row

    @property
    def col(self):
        return self.cell.CellAddress.value.Column

    @property
    def addr(self):

        if self.is_cell():
            return self.row, self.col

        if self.is_range():
            a = self.cell.getRangeAddress()
            return (a.StartRow, a.StartColumn), (a.EndRow, a.EndColumn)


    @property
    def formula(self):
        return self.cell.getFormula()

    @formula.setter
    def formula(self, _form):
        self.cell.setFormula(_form)


    def __str__(self):
        return pprint.pformat(self.value)

    def __repr__(self):
        return pprint.pformat(self.value)


class Sheet:
    def __init__(self, sheet_object):
        self.sh = sheet_object

    def cell(self, row, col):
        return Cell(self.sh.getCellByPosition(row, col))

    def range(self, rangename):
        return Cell(self.sh.getCellRangeByName(rangename))

    def pos(self, row0, col0, row1, col1):
        """
        :param row0:
        :param col0:
        :param row1:
        :param col1:
        :return:

        http://www.openoffice.org/api/docs/common/ref/com/sun/star/table/XCellRange.html#getCellRangeByPosition
        """
        return Cell(self.sh.getCellRangeByPosition(col0, row0, col1, row1))

    def named_ranges(self):
        return self.sh.NamedRanges.getElementNames()

    def named_range_cells(self, name):
        return Cell(self.sh.NamedRanges.getByName(name).getReferredCells())


    @property
    def name(self):
        return self.sh.getName()

    @name.setter
    def name(self, _name):
        self.sh.setName(_name)

    def rows_names(self):
        return self.sh.getRowDescriptions()

    def cols_names(self):
        return self.sh.getColumnDescriptions()

    @property
    def size(self):
        return len(self.rows_names()), len(self.cols_names())

    def all(self):
        """
        :return: Tuple containing the value of all cells in the sheet
        """
        nrows, ncols = self.size
        return self.pos(0, 0, nrows, ncols).value


class Osheet:

    def __init__(self, doc):
        self.doc = doc

    def sheet(self, name_or_index):

        if isinstance(name_or_index, str):
            sheet = self.doc.Sheets.getByName(name_or_index)

        elif isinstance(name_or_index, int):
            sheet = self.doc.Sheets.getByIndex(name_or_index)
        else:
            raise Exception("Expected int or str")

        return Sheet(sheet)

    def selection(self):
        return Cell(self.doc.getCurrentSelection())

    def selection_rows(self):
        return Cell(self.doc.getCurrentSelection()).value

    def selection_cols(self):
        return hof.transpose(self.selection_rows())

    def active_sheet(self):
        return Sheet(self.doc.CurrentController.getActiveSheet())

    @property
    def title(self):
        return self.doc.getTtile()

    @property
    def location(self):
        return self.doc.getLocation()

    def __str__(self):
        return '''Spreadsheet: {}'''.format(self.location)

    def __repr__(self):
        return self.__str__()

    def close(self):
        self.doc.close(True)

office = SOffice()

#doc = office.new_calc()
doc = office.open("/home/tux/test1.ods")

print(doc)

sh = doc.sheet(0)

r = sh.range("C11:D19")


xyz = sh.named_range_cells("COLUMNSXYZ")

print(xyz)