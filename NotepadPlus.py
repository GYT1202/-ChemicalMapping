#这是篇没有任何注释的代码，请见谅~

from xml.etree.ElementInclude import include
import bce.option as _opt
import bce.public.api as _public_api
import bce.public.printer as _public_printer

import json, sys

import xmind
from xmind.core.const import TOPIC_DETACHED

#  Create an option instance.
opt = _opt.Option()

class Equation():
    def __init__(self, equation):
        self.raw = equation
        reactants, products = equation.split("=")
        self.reactants = reactants.split("+")
        self.products = products.split("+")

        self.result = _public_api.balance_chemical_equation(equation, opt, printer=_public_printer.PRINTER_TEXT, unknown_header="X")

class ChemicalMapping():
    def __init__(self):
        self.objects = {}
        self.equations = []
        self.data = []
    
    def readData(self, filename="save.json"):
        with open(filename, "r") as f:
            self.objects = json.load(f)
        for obj in self.objects.values():
            for t in obj["to"].values():
                if not t in self.equations:
                    self.equations.append(t)
            for f in obj["from"].values():
                if not f in self.equations:
                    self.equations.append(f)

    def summonObjects(self):
        for equation in self.equations:
            reactants, products = equation.split("=")
            reactants = reactants.split("+")
            products = products.split("+")

            for reactant in reactants:
                if not reactant in self.objects.keys():
                    self.objects[reactant] = {"to":{}, "from":{}, "isPrecipitation":False, "isGas":False}
                for product in products:
                    self.objects[reactant]["to"][product] = equation
            
            for product in products:
                if not product in self.objects.keys():
                    self.objects[product] = {"to":{}, "from":{}, "isPrecipitation":False, "isGas":False}
                for reactant in reactants:
                    self.objects[product]["from"][reactant] = equation
    
    def saveData(self, filename="save.json"):
        with open(filename, "w") as f:
            json.dump(self.objects, f)
    
    def toXmind(self, objName, tdeepth=10, filename="result.xmind"):
        workbook = xmind.load("in.xmind")
        sheet = workbook.getPrimarySheet()
        root_topic = sheet.getRootTopic()

        summonedTopics = root_topic.getSubTopics()
        root_topic.setTitle(objName)
        summoned = {topic.getTitle():topic for topic in summonedTopics}
        summoned[objName] = root_topic

        rs = {}

        def createOBJ(text, deepth):
            if deepth == 0:return
            if not text in summoned.keys():
                summoned[text] = root_topic.addSubTopic(topics_type=TOPIC_DETACHED)
                summoned[text].setTitle(text)
            for t, equation in self.objects[text]["to"].items():
                if t in summoned.keys():
                    txt = text + " " + t
                    if txt in rs.keys():
                        rb = rs[txt].getTitle()
                        if rb != equation:
                            rs[txt].setTitle(rs[txt].getTitle()+"\n"+equation)
                    else:
                        rs[txt] = sheet.createRelationship(summoned[text].getID(), summoned[t].getID(), equation)
                else:createOBJ(t, deepth - 1)
            for f, equation in self.objects[text]["from"].items():
                if f in summoned.keys():
                    txt = f + " " + text
                    if txt in rs.keys():
                        rb = rs[txt].getTitle()
                        if rb != equation:
                            rs[txt].setTitle(rs[txt].getTitle()+"\n"+equation)
                    else:
                        rs[txt] = sheet.createRelationship(summoned[f].getID(), summoned[text].getID(), equation)
                else:createOBJ(f, deepth - 1)

        createOBJ(objName, tdeepth)

        xmind.save(workbook, path=filename)


ChemicalMapping()

from PIL import Image, ImageFont, ImageDraw
import tkinter as tk
from tkinter import ttk
import requests.sessions
from tkinter import font as tkFont
import re, execjs, json, random
from datetime import datetime

import ctypes
def hideConsole():
  """
  Hides the console window in GUI mode. Necessary for frozen application, because
  this application support both, command line processing AND GUI mode and theirfor
  cannot be run via pythonw.exe.
  """
 
  whnd = ctypes.windll.kernel32.GetConsoleWindow()
  if whnd != 0:
    ctypes.windll.user32.ShowWindow(whnd, 0)
    # if you wanted to close the handles...
    #ctypes.windll.kernel32.CloseHandle(whnd)

class BaiDuFanYi():
    def __init__(self):
        self.homeUrl = "https://fanyi.baidu.com/"
        self.transUrl = "https://fanyi.baidu.com/v2transapi"
        self.headers = {
        'User-Agent':
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
        }
        self.gtk = None
        self.token = None
        self.s = requests.Session()
        self.get_params()
        self.get_params()
    def get_sign(self, query_string):
        JS_CODE = """
        function a(r, o) {
        for (var t = 0; t < o.length - 2; t += 3) {
        var a = o.charAt(t + 2);
        a = a >= "a" ? a.charCodeAt(0) - 87 : Number(a),
        a = "+" === o.charAt(t + 1) ? r >>> a: r << a,
        r = "+" === o.charAt(t) ? r + a & 4294967295 : r ^ a
        }
        return r
        }
        var C = null;
        var token = function(r, _gtk) {
        var o = r.length;
        o > 30 && (r = "" + r.substr(0, 10) + r.substr(Math.floor(o / 2) - 5, 10) + r.substring(r.length, r.length - 10));
        var t = void 0,
        t = null !== C ? C: (C = _gtk || "") || "";
        for (var e = t.split("."), h = Number(e[0]) || 0, i = Number(e[1]) || 0, d = [], f = 0, g = 0; g < r.length; g++) {
        var m = r.charCodeAt(g);
        128 > m ? d[f++] = m: (2048 > m ? d[f++] = m >> 6 | 192 : (55296 === (64512 & m) && g + 1 < r.length && 56320 === (64512 & r.charCodeAt(g + 1)) ? (m = 65536 + ((1023 & m) << 10) + (1023 & r.charCodeAt(++g)), d[f++] = m >> 18 | 240, d[f++] = m >> 12 & 63 | 128) : d[f++] = m >> 12 | 224, d[f++] = m >> 6 & 63 | 128), d[f++] = 63 & m | 128)
        }
        for (var S = h,
        u = "+-a^+6",
        l = "+-3^+b+-f",
        s = 0; s < d.length; s++) S += d[s],
        S = a(S, u);
        return S = a(S, l),
        S ^= i,
        0 > S && (S = (2147483647 & S) + 2147483648),
        S %= 1e6,
        S.toString() + "." + (S ^ h)
        }
        """
        return execjs.compile(JS_CODE).call('token', query_string, self.gtk)
    def get_params(self):
        r = self.s.get(self.homeUrl, headers=self.headers)
        self.gtk = re.findall(r"window.gtk = '(.*?)';", r.text)[0]
        self.token = re.findall(r"token: '(.*?)',", r.text)[0]

    def translate(self, query_string):
        sign = self.get_sign(query_string)
        data = {
        'from': 'zh',
        'to': 'en',
        'query': query_string,
        'simple_means_flag': 3,
        'sign': sign,
        'token': self.token,
        }
        res = self.s.post(url=self.transUrl, data=data, headers=self.headers)
        return res.json()

#ARLRDBD.TTF
class E():
    def __init__(self):
        self.fanyi = BaiDuFanYi()
        self.chemicalMapping = ChemicalMapping()
        self.exchanges = []
        self.root = tk.Tk()
        
        self.font_i = self.font_i_title = ""
        self.fonti = ImageFont.truetype("simsun.ttc", 50, encoding="utf-8")
        self.font_size = 14
        self.font = ("Consolas", self.font_size)
        self.fonti_title = ImageFont.truetype("simsun.ttc", 100, encoding="utf-8")
        
        self.root.after(600000, self.saver)
        def save_d():
            self.saveFile()
            self.root.destroy()
        self.root.protocol('WM_DELETE_WINDOW', save_d)
        self.root.title("Learn Words Better")
        self.root.geometry("1200x800")
        self.editing = True

        self.mainEdit = tk.Text(self.root, bd=0, font=self.font)
    
        self.mainEdit.bind("<Return>", self.enter)
        self.mainEdit.bind("<Control-MouseWheel>", self.mouseWheel)
        self.mainEdit.bind("<Shift-Return>", self.shift_enter)

        self.mainEdit.pack(fill="both", expand=True)

        self.read()

        self.root.mainloop()

    def read(self, filename=None):
        try:
            with open(filename if filename else (datetime.now().strftime('%Y-%m-%d')+".txt"), "r") as f:
                self.mainEdit.insert("end", f.read())
        except:pass

    def enter(self, e):
        cmd = self.mainEdit.get("insert linestart", "insert lineend")
        if cmd == "c":
            self.mainEdit.delete("insert linestart", "end")
            self.save()
        elif cmd == "c -mixed":
            self.mainEdit.delete("insert linestart", "end")
            self.save(mixed=True)
        elif cmd[:7] == "toXmind":
            self.mainEdit.delete("insert linestart", "end")
            es = self.mainEdit.get("1.0", "end").split("\n")
            for e in es:
                if e:self.chemicalMapping.equations.append(e)
            self.chemicalMapping.summonObjects()
            self.chemicalMapping.saveData()
            ops = cmd.split(" ")
            if len(ops) == 2:ops += [10, "result.xmind"]
            if len(ops) == 3:ops += ["result.xmind"]
            self.chemicalMapping.toXmind(ops[1], int(ops[2]) + 1, ops[3])
        elif cmd[:6] == ":font ":
            self.mainEdit.delete("insert linestart", "end")
            fonts = cmd.split(" ")
            self.fontSeter(fonts[1], fonts[2])
        elif cmd[0] == "r":
            self.mainEdit.delete("insert linestart", "end")
            cs = cmd.split(" ")
            if len(cs) == 1:
                self.read()
            else:
                self.read(cs[1])
    
    def complete_choosing(self, chooser, fan=True):
        p = chooser.get()
        self.mainEdit.delete("insert-1l linestart", "end")
        
        start, end = 0, len(p)
        for i, s in enumerate(p):
            if s == "]": start = i + 1
            if s == "~" and fan: end = i
        
        for exchange in self.exchanges:
            p = p.replace(exchange, "_"*len(exchange))

        self.mainEdit.insert("end", "\n"+str(p[start:end])+"\n")
        self.mainEdit.focus()

    def shift_enter(self, e):
        if self.editing:
            #self.editing = False

            chooser = ttk.Combobox(self.mainEdit, font=self.font, width=100)
            chooser["value"] = self.get_sentences(self.mainEdit.get("insert linestart", "insert lineend"))
            
            self.mainEdit.delete("insert linestart", "end")
            self.mainEdit.insert("end", "\n")

            self.mainEdit.window_create("end", window=chooser)
            #chooser.bind("<<ComboboxSelected>>", lambda e: self.complete_choosing(chooser))
            chooser.bind("<Return>", lambda e: self.complete_choosing(chooser))
            chooser.bind("<Shift-Return>", lambda e: self.complete_choosing(chooser, False))

            chooser.focus()
            self.root.after(3, lambda : chooser.event_generate('<Down>'))
    
    def get_sentences(self, word_in):
        result_a = []
        self.exchanges = []
        result = self.fanyi.translate(word_in)
        if "dict_result" in result.keys():
            if "exchange" in result["dict_result"]["simple_means"]:
                [self.exchanges.extend(exchanges) for exchanges in result["dict_result"]["simple_means"]["exchange"].values()]
            if "menus" in result["dict_result"]["collins"].keys():
                for menu in result["dict_result"]["collins"]["menus"]:
                    for entry in menu["entry"]:
                        if entry["type"] != "mean": continue
                        for value in entry["value"]:
                            for mean_type in value["mean_type"]:
                                if mean_type["info_type"] != "example": continue
                                for example in mean_type["example"]:
                                    result_a.append("[{}][{}]{}~{}".format(value["posp"][0]["label"], value["tran"], example["ex"], example["tran"]))
            else:
                for entry in result["dict_result"]["collins"]["entry"]:
                    if entry["type"] != "mean": continue
                    for value in entry["value"]:
                        for mean_type in value["mean_type"]:
                            if mean_type["info_type"] != "example": continue
                            for example in mean_type["example"]:
                                result_a.append("[{}][{}]{}~{}".format(value["posp"][0]["label"], value["tran"], example["ex"], example["tran"]))
        for sentence in json.loads(result["liju_result"]["double"]):
            e, c = "", ""
            for word in sentence[0]:e += word[0] + ' '
            for charactor in sentence[1]:c += charactor[0] + ''
            result_a.append("[{}]{}~{}".format(sentence[2], e, c))
        self.exchanges.append(word_in)
        return result_a
    
    def mouseWheel(self, e):
        if e.delta > 0:
            self.font_size += 1
        elif e.delta < 0:
            self.font_size -= 1
        if e != 0:
            self.font = ("Consolas", self.font_size)
            self.mainEdit.config(font=self.font)
    
    def saver(self):
        self.root.after(600000, self.saver)
        self.saveFile()
    
    def saveFile(self):
        with open(datetime.now().strftime('%Y-%m-%d')+".txt", "w") as f:
            f.write(self.mainEdit.get("1.0", "end"))
    
    def fontSeter(self, font, font_title):
        if font != self.font_i:
            self.font_i = font
            self.fonti = ImageFont.truetype(self.font_i, 50, encoding="utf-8")
        if font_title != self.font_i_title:
            self.font_i_title = font_title
            self.fonti_title = ImageFont.truetype(self.font_i_title, 100, encoding="utf-8")

    def save(self, filename="result.png", mixed=False):
        img = Image.new("RGB", size=[2479, 3508], color=(255,69,0))
        draw = ImageDraw.Draw(img)
        hc, title, line, word, line_start, last_key, last_keyi = "", False, 20, False, -1, "", ""
        draw.rectangle(xy=(20, 20, 2458, 3487), fill=(230, 230, 230))
        strs = self.mainEdit.get("1.0", "end")   

        buffer = {}

        for str in strs:
            if str == "$": title = True
            elif str == "#": word = True
            elif str == "\n":
                if word:
                    buffer[last_key][hc] = []
                    last_keyi = hc
                    word = False
                elif title: 
                    buffer[hc] = {}
                    last_key = hc
                    title = False
                else:
                    buffer[last_key][last_keyi].append(hc)
                hc = ""
            else:
                hc += str
        if mixed:
            for title, text in buffer.items():
                line += 40
                draw.text(((2479 - self.fonti_title.getsize(title)[0]) / 2, line), title, font = self.fonti_title, fill=(0,0,0))
                line += 100
                xl,xr = line, line + len(text.keys()) * 50
                draw.rectangle(xy=(50, xl, 2429, xr), fill=(255, 255, 255))
                draw.rectangle(xy=(50, xl, 70, xr), fill=(0, 0, 0))
                draw.rectangle(xy=(2409, xl, 2429, xr), fill=(0, 0, 0))
                for word in text.keys():
                    draw.text((90, line), word, font = self.fonti, fill=(0,0,0))
                    line += 50
                result_buffer = []
                for texts in text.values():
                    result_buffer.extend(texts)
                random.shuffle(result_buffer)
                for sentence in result_buffer:
                    draw.text((90, line), sentence, font = self.fonti, fill=(0,0,0))
                    line += 50
        else:
            for title, text in buffer.items():
                line += 50
                draw.text(((2479 - self.fonti_title.getsize(title)[0]) / 2, line), title, font = self.fonti_title, fill=(0,0,0))
                line += 100
                for word, texts in text.items():
                    xl,xr = line + 50, line + len(texts) * 50 + 50
                    draw.rectangle(xy=(50, xl, 2429, xr), fill=(255, 255, 255))
                    draw.rectangle(xy=(50, xl, 70, xr), fill=(0, 0, 0))
                    draw.rectangle(xy=(2409, xl, 2429, xr), fill=(0, 0, 0))
                    draw.text((50, line), word, font = self.fonti, fill=(0,0,0))
                    line += 50
                    for sentence in texts:
                        draw.text((90, line), sentence, font = self.fonti, fill=(0,0,0))
                        line += 50
        img.save(filename)
        img.show()

hideConsole()             
E()
