import bce.option as _opt
import bce.public.api as _public_api
import bce.public.printer as _public_printer

#  Create an option instance.
opt = _opt.Option()

class Equation():
    def __init__(self, equation):
        reactants, products = equation.split("=")
        self.reactants = reactants.split("+")
        self.products = products.split("+")

        self.result = _public_api.balance_chemical_equation(equation, opt, printer=_public_printer.PRINTER_TEXT, unknown_header="X")

Equations = []

with open("Equations.txt", "r") as f:
    for line in f.read().splitlines():
        Equations.append(Equation(line))

Objects = {}

import xmind  #加载包
from xmind.core.const import TOPIC_DETACHED
def design_sheet1(sheet1):
    root_topic1 = sheet1.getRootTopic()

    def getTopic(text):
        if not text in Objects:
            sub_topic = root_topic1.addSubTopic(topics_type=TOPIC_DETACHED)
            sub_topic.setTitle(text)
            Objects[text] = [sub_topic]
            return sub_topic
        else:
            return Objects[text][0]
    for equation in Equations:
        for reactant in equation.reactants:
            for product in equation.products:
                sheet1.createRelationship(getTopic(reactant).getID(), getTopic(product).getID(), equation.result) 

workbook = xmind.load("my.xmind")
design_sheet1(workbook.getPrimarySheet())
xmind.save(workbook, path='test.xmind')
