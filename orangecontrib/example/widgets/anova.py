from AnyQt.QtWidgets import QLabel
import Orange
import numpy
from Orange.widgets.widget import OWWidget, Output, Input
from Orange.widgets.settings import Setting
from Orange.widgets import gui

class Anova(OWWidget):
    # Widget needs a name, or it is considered an abstract widget
    # and not shown in the menu.
    name = "Anova"
    icon = "icons/anova.svg"
    want_main_area = True

    class Inputs:
        data = Input("Data", Orange.data.Table)

    proportion = Setting(50)
    columnList = set(["a", "b", "c"])
    commitOnChange = Setting(0)

    def __init__(self):
        super().__init__()
        self.optionsBox = gui.widgetBox(self.controlArea, "Options")
        gui.spin(
            self.optionsBox,
            self,
            "proportion",
            minv=10,
            maxv=90,
            step=10,
            label="Sample Size [%]:",
            callback=[self.selection, self.checkCommit],
        )

        gui.separator(self.controlArea)

        self.listBox = gui.widgetBox(self.controlArea, "Columns")
        gui.listBox(
            self.listBox,
            self,
            value="columnList",
            labels="columnList",
            callback=[self.selection, self.checkCommit]
        )

    @Inputs.data
    def set_data(self, dataset):
        if dataset is not None:
            self.dataset = dataset
            self.optionsBox.setDisabled(False)
            self.selection()
        else:
            self.dataset = None
            self.sample = None
            self.optionsBox.setDisabled(False)
        self.commit()

    def selection(self):
        if self.dataset is None:
            return

        n_selected = int(numpy.ceil(len(self.dataset) * self.proportion / 100.0))
        indices = numpy.random.permutation(len(self.dataset))
        indices = indices[:n_selected]
        self.sample = self.dataset[indices]

    def commit(self):
        self.Outputs.sample.send(self.sample)

    def checkCommit(self):
        if self.commitOnChange:
            self.commit()



if __name__ == "__main__":
    from Orange.widgets.utils.widgetpreview import WidgetPreview  # since Orange 3.20.0
    WidgetPreview(Anova).run()
