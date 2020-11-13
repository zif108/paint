import sys

from PyQt5 import uic
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QBrush, QColor, QPainter, QPen, QPixmap, QPolygon
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QColorDialog, QLabel, QFileDialog

lx = 0
ly = 0
color = (0, 0, 0)

tr_top = 0
tr_left = 0

eraser = False

thickness = 5
first = True


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
            # painter.drawEllipse(self.x - 5, self.y - 5, 5, 5)


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
            self.pen = QPen(QColor(212, 208, 200))

        self.pen.setWidth(thickness)

    def draw(self, painter):
        if not eraser:
            # painter.setBrush(QBrush(QColor(color[0], color[1], color[2])))
            painter.setPen(self.pen)
            painter.drawLine(self.sx, self.sy, self.ex, self.ey)
        else:
            painter.setBrush(QBrush(QColor(212, 208, 200)))
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


# Класс треугольника
class Triangle:
    def __init__(self, top_x, top_y, left_x, left_y, right_x, right_y):
        global color
        global thickness
        global tr_top
        global tr_left
        global first
        self.top_x = top_x
        self.top_y = top_y
        self.left_x = left_x
        self.left_y = left_y
        self.right_x = right_x
        self.right_y = right_y

        # tr_top = self.top_x, self.top_y
        tr_left = self.left_x  # Точка с постоянным x
        self.pen = QPen(QColor(color[0], color[1], color[2]))
        self.pen.setWidth(thickness)

        # точки
        self.points = QPolygon([
            QPoint(self.top_x, self.top_y),
            QPoint(self.left_x, self.left_y),
            QPoint(self.right_x, self.right_y)
        ])

    def draw(self, painter):
        painter.drawPolygon(self.points)
        painter.setBrush(QBrush(QColor(0, 0, 0, 0)))
        painter.setPen(QPen(QColor(0, 0, 0, 0)))
        # рисуем


class Rectangle:
    def __init__(self, x, y, width, hight):
        global color
        global thickness
        self.x = x
        self.y = y
        self.width = width
        self.hight = hight

        self.pen = QPen(QColor(color[0], color[1], color[2]))
        self.pen.setWidth(thickness)

    def draw(self, painter):
        painter.setBrush(QBrush(QColor(0, 0, 0, 0)))
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
                    Triangle(event.x(), event.y() - 1, event.x() - 1, event.y(), event.x() + 1,
                             event.y()))
                print(self.objects)
                print(tr_left)
                self.update()

            elif self.instrument == 'eraser':
                if self.instrument == 'brush':
                    self.objects.append(BrushPoint(event.x(), event.y()))
                    self.update()

    def mouseMoveEvent(self, event):
        global lx
        global ly
        global tr_left
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
            # Изменение фигуры при рисовании
            elif self.instrument == 'triangle':
                a = (event.x() - tr_left) / 2
                self.objects[-1].top_x = a
                self.objects[-1].top_y = event.y()
                self.objects[-1].left_x = tr_left
                self.objects[-1].rigtht_x = event.x()  # Присваиваем event.x()
                print('tr_left', tr_left, 'event_x', event.x(), 'ev_y', event.y())
                print('Top')
                print('x', self.objects[-1].top_x)
                print('y', self.objects[-1].top_y)
                print('Left')
                print('x', self.objects[-1].left_x)
                print('y', self.objects[-1].left_y)
                print('Right')
                print('x', self.objects[-1].right_x)  # Но здесь совсем другое значение: каждый раз просто прибавляется 2
                print('y', self.objects[-1].right_y)

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

    def color(self):
        global color
        col = QColorDialog.getColor()
        if col.isValid():
            color = col.red(), col.green(), col.blue()

    def triangle(self):
        self.instrument = 'triangle'

    def rectangle(self):
        self.instrument = 'rectangle'

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

    def very_thick(self):
        global thickness
        thickness = 20


class Program(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('paint.ui', self)

        self.setCentralWidget(Canvas())
        self.brush.triggered.connect(self.centralWidget().setBrush)
        self.line.triggered.connect(self.centralWidget().setLine)
        self.circle.triggered.connect(self.centralWidget().setCircle)
        self.triangle.triggered.connect(self.centralWidget().triangle)
        self.lastik.triggered.connect(self.centralWidget().setEraser)
        self.color.triggered.connect(self.centralWidget().color)
        self.rectangle.triggered.connect(self.centralWidget().rectangle)

        self.thin.triggered.connect(self.centralWidget().thin)
        self.not_thin.triggered.connect(self.centralWidget().not_thin)
        self.average.triggered.connect(self.centralWidget().average)
        self.thick.triggered.connect(self.centralWidget().thick)
        self.very_thick.triggered.connect(self.centralWidget().very_thick)

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
