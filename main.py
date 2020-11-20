import sys

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor, QPainter, QPen
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QColorDialog, QFileDialog

lx = 0
ly = 0
color = (0, 0, 0)

eraser = False
highlight = False
flag = False

thickness = 5


class BrushPoint:
    def __init__(self, x, y):
        global lx
        global ly
        global color
        self.x = x
        self.y = y
        self.color = color

        lx = self.x
        ly = self.y

        self.r = color[0]
        self.g = color[1]
        self.b = color[2]

    def draw(self, painter):
        if not eraser:
            painter.setBrush(QBrush(QColor(self.r, self.g, self.b)))
            painter.setPen(QColor(self.r, self.g, self.b))
        else:
            painter.setBrush(QBrush(QColor(255, 255, 255)))
            painter.setPen(QColor(255, 255, 255))


class Line:
    def __init__(self, sx, sy, ex, ey):
        global color
        global thickness
        self.sx = sx
        self.sy = sy
        self.ex = ex
        self.ey = ey
        if not eraser:
            self.pen = QPen(QColor(color[0], color[1], color[2]))

        else:
            self.pen = QPen(QColor(255, 255, 255))

        self.pen.setWidth(thickness)

    def draw(self, painter):
        if not eraser:
            painter.setPen(self.pen)
            painter.drawLine(self.sx, self.sy, self.ex, self.ey)
        else:
            painter.setBrush(QBrush(QColor(255, 255, 255)))
            painter.setPen(self.pen)
            painter.drawLine(self.sx, self.sy, self.ex, self.ey)


class Circle:
    def __init__(self, cx, cy, x, y):
        global color
        global thickness
        self.cx = cx
        self.cy = cy
        self.x = x
        self.y = y
        self.pen = QPen(QColor(color[0], color[1], color[2]))

        self.pen.setWidth(thickness)

    def draw(self, painter):
        painter.setBrush(QBrush(QColor(0, 0, 0, 0)))
        painter.setPen(self.pen)
        radius = int(((self.cx - self.x) ** 2 + (self.cy - self.y) ** 2) ** 0.5)
        painter.drawEllipse(self.cx - radius, self.cy - radius, 2 * radius, 2 * radius)


class Triangle:
    def __init__(self, top_x, top_y, left_x, left_y, right_x, right_y):
        global color
        global thickness
        self.top_x = top_x
        self.top_y = top_y
        self.left_x = left_x
        self.left_y = left_y
        self.right_x = right_x
        self.right_y = right_y

        self.pen = QPen(QColor(color[0], color[1], color[2]))
        self.pen.setWidth(thickness)

    def draw(self, painter):
        painter.setBrush(QBrush(QColor(0, 0, 0, 0)))
        painter.setPen(QPen(self.pen))
        painter.drawLine(self.left_x, self.left_y, self.top_x, self.top_y)
        painter.drawLine(self.top_x, self.top_y, self.right_x, self.right_y)
        painter.drawLine(self.right_x, self.right_y, self.left_x, self.left_y)


class Rectangle:
    def __init__(self, x, y, width, hight):
        global color
        global thickness
        global highlight
        self.x = x
        self.y = y
        self.width = width
        self.hight = hight
        self.fon = 0
        self.r = 173
        self.g = 173
        self.b = 173
        if not highlight:
            self.pen = QPen(QColor(color[0], color[1], color[2]))
            self.pen.setWidth(thickness)
        else:
            self.pen = QPen(QColor(173, 173, 173))
            self.pen.setStyle(Qt.DashLine)
            self.pen.setWidth(2)

    def draw(self, painter):
        if not highlight:
            painter.setBrush(QBrush(QColor(0, 0, 0, 0)))
            painter.setPen(self.pen)
            painter.drawRect(self.x, self.y, self.width, self.hight)
        else:
            painter.setBrush(QBrush(QColor(self.r, self.g, self.b, self.fon)))
            painter.setPen(self.pen)
            painter.drawRect(self.x, self.y, self.width, self.hight)


class Highlight:
    def __init__(self, x, y, width, hight):
        global color
        global thickness
        global highlight
        self.x = x
        self.y = y
        self.width = width
        self.hight = hight
        self.fon = 0
        self.r = 173
        self.g = 173
        self.b = 173
        self.pen = QPen(QColor(173, 173, 173))
        self.pen.setStyle(Qt.DashLine)
        self.pen.setWidth(2)

    def draw(self, painter):
        painter.setBrush(QBrush(QColor(self.r, self.g, self.b, self.fon)))
        painter.setPen(self.pen)
        painter.drawRect(self.x, self.y, self.width, self.hight)


class Canvas(QWidget):
    def __init__(self):
        super(Canvas, self).__init__()

        self.objects = []
        self.instrument = 'brush'

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        for obj in self.objects:
            obj.draw(painter)
        painter.end()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.instrument == 'brush':
                self.objects.append(BrushPoint(event.x(), event.y()))
                self.update()
            elif self.instrument == 'line':
                self.objects.append(Line(event.x(), event.y(), event.x(), event.y()))
                self.update()
            elif self.instrument == 'circle':
                self.objects.append(Circle(event.x(), event.y(), event.x(), event.y()))
                self.update()

            elif self.instrument == 'rectangle':
                self.objects.append(Rectangle(event.x(), event.y(), 1, 1))
                self.update()

            elif self.instrument == 'triangle':
                self.objects.append(
                    Triangle(event.x(), event.y(), event.x(), event.y(), event.x(),
                             event.y()))
                self.update()

            elif self.instrument == 'highlight':
                self.objects.append(Highlight(event.x(), event.y(), 1, 1))
                self.update()

            elif self.instrument == 'eraser':
                if self.instrument == 'brush':
                    self.objects.append(BrushPoint(event.x(), event.y()))
                    self.update()

    def mouseMoveEvent(self, event):
        global lx
        global ly
        global flag
        if event.buttons() and Qt.LeftButton:
            if self.instrument == 'brush':
                self.objects.append(Line(lx, ly, event.x(), event.y()))
                self.objects.append(BrushPoint(event.x(), event.y()))
                self.update()

            elif self.instrument == 'line':
                self.objects[-1].ex = event.x()
                self.objects[-1].ey = event.y()
                self.update()

            elif self.instrument == 'circle':
                self.objects[-1].x = event.x()
                self.objects[-1].y = event.y()
                self.update()

            elif self.instrument == 'rectangle':
                self.objects[-1].width = event.x() - self.objects[-1].x
                self.objects[-1].hight = event.y() - self.objects[-1].y
                self.update()

            elif self.instrument == 'highlight':
                self.objects[-1].width = event.x() - self.objects[-1].x
                self.objects[-1].hight = event.y() - self.objects[-1].y
                self.update()
                flag = True

            elif self.instrument == 'triangle':
                self.objects[-1].top_x = (event.x() + self.objects[-1].left_x) / 2
                self.objects[-1].top_y = event.y()
                self.objects[-1].right_x = event.x()
                self.update()

    def setBrush(self):
        global eraser
        self.instrument = 'brush'
        eraser = False

    def setLine(self):
        global eraser
        eraser = False
        self.instrument = 'line'

    def setCircle(self):
        global eraser
        self.instrument = 'circle'
        eraser = False

    def setEraser(self):
        global eraser
        eraser = True
        self.instrument = 'brush'

    def highlight_(self):
        global highlight
        self.instrument = 'highlight'
        highlight = True

    def delete_(self):
        global flag
        if flag:
            self.objects[-1].stil = Qt.SolidLine
            self.objects[-1].r = 255
            self.objects[-1].g = 255
            self.objects[-1].b = 255
            self.objects[-1].fon = 255
            self.objects[-1].pen = QPen(QColor(255, 255, 255))
            self.update()

    def color(self):
        global color
        col = QColorDialog.getColor()
        if col.isValid():
            color = col.red(), col.green(), col.blue()

    def triangle(self):
        self.instrument = 'triangle'

    def rectangle(self):
        global highlight
        self.instrument = 'rectangle'
        highlight = False

    def thin(self):
        global thickness
        thickness = 1

    def not_thin(self):
        global thickness
        thickness = 2.5

    def average(self):
        global thickness
        thickness = 5

    def thick(self):
        global thickness
        thickness = 10


class Program(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('paint.ui', self)

        self.setCentralWidget(Canvas())
        self.brush.triggered.connect(self.centralWidget().setBrush)
        self.line.triggered.connect(self.centralWidget().setLine)
        self.circle.triggered.connect(self.centralWidget().setCircle)
        self.triangle.triggered.connect(self.centralWidget().triangle)
        self.rectangle.triggered.connect(self.centralWidget().rectangle)
        self.lastik.triggered.connect(self.centralWidget().setEraser)
        self.color.triggered.connect(self.centralWidget().color)
        self.highlight.triggered.connect(self.centralWidget().highlight_)
        self.delete_2.triggered.connect(self.centralWidget().delete_)

        self.thin.triggered.connect(self.centralWidget().thin)
        self.not_thin.triggered.connect(self.centralWidget().not_thin)
        self.average.triggered.connect(self.centralWidget().average)
        self.thick.triggered.connect(self.centralWidget().thick)

        self.save.triggered.connect(self.save_)

    def save_(self):
        fname = QFileDialog.getSaveFileName(self, 'Cохранить как', 'img.jpg')[0]
        self.centralWidget().grab().save(fname)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    prog = Program()
    prog.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
