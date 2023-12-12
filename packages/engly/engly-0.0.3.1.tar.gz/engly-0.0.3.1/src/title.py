#!/usr/bin/python3
import os
import wx
import json
from os.path import expanduser
from libs.common import set_font, path
from libs.newdate import HistoryWrite
import word_list
import word_test
import reading
import history

class SampleFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, title=title, pos=(0, 0), size=(450, 550))
        self.home_directory = expanduser("~")
        self.flag = True
        #self.Bind(wx.EVT_CLOSE, self.onExit)
        self.__create_widget()
        self.__do_layout()
        self.__data_setup()

    def __create_widget(self):
        self.txt = wx.StaticText(self, label = "Menu")
        self.txt.SetFont(set_font(40))

        self.btn_list = wx.Button(self, label="List")
        self.btn_list.Bind(wx.EVT_BUTTON, self.list)

        self.btn_test = wx.Button(self, label="Test")
        self.btn_test.Bind(wx.EVT_BUTTON, self.test)

        self.btn_reading = wx.Button(self, label="Reading")
        self.btn_reading.Bind(wx.EVT_BUTTON, self.reading)

        self.btn_history = wx.Button(self, label="History")
        self.btn_history.Bind(wx.EVT_BUTTON, self.history)

        self.ctrl_apikey = wx.TextCtrl(self, -1, style=wx.TE_MULTILINE, size=(220,100))
        self.ctrl_apikey.Hide()

        self.btn_apikey = wx.Button(self, label="apikey")
        self.btn_apikey.Bind(wx.EVT_BUTTON, self.apikey)

        self.btn_save = wx.Button(self, label="save")
        self.btn_save.Bind(wx.EVT_BUTTON, self.save)
        self.btn_save.Hide()

    def __do_layout(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer_api = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.txt, flag=wx.ALIGN_CENTER | wx.ALL, border=10)
        sizer.Add(self.btn_list, flag=wx.ALIGN_CENTER | wx.ALL, border=10)
        sizer.Add(self.btn_test, flag=wx.ALIGN_CENTER | wx.ALL, border=10)
        sizer.Add(self.btn_reading, flag=wx.ALIGN_CENTER | wx.ALL, border=10)
        sizer.Add(self.btn_history, flag=wx.ALIGN_CENTER | wx.ALL, border=10)
        sizer.Add(self.btn_apikey, flag=wx.ALIGN_CENTER | wx.ALL, border=10)
        sizer_api.Add(self.ctrl_apikey, flag=wx.ALIGN_CENTER | wx.ALL, border=10)
        sizer_api.Add(self.btn_save, flag=wx.ALIGN_CENTER | wx.ALL, border=10)
        sizer.Add(sizer_api, flag=wx.ALIGN_CENTER | wx.ALL, border=10)
        self.SetSizer(sizer)

    def __data_setup(self):
        if not os.path.exists(self.home_directory + "/.engly_data"):
            home_dir = expanduser("~")
            data_dir = home_dir + "/.engly_data/data"
            fig_dir = home_dir + "/.engly_data/fig"
            api_dir = home_dir + "/.engly_data/api"
            res_json = data_dir + "/response.json"
            his_json = data_dir + "/history.json"
            word_json = data_dir + "/words.json"
            api_key = api_dir + "/apikey"
            os.makedirs(data_dir)
            os.makedirs(fig_dir)
            os.makedirs(api_dir)
            with open(res_json, "w") as file:
                json.dump({}, file, indent=2)
            with open(his_json, "w") as file:
                json.dump({}, file, indent=2)
            with open(word_json, "w") as file:
                json.dump({}, file, indent=2)
            with open(api_key, "w") as file:
                pass
            init = HistoryWrite()
            init.history_init()
        else:
            pass

        # gitのエラー直す

    def list(self, event):
        #subprocess.Popen(["python3", "word_list.py"])
        word_list.main()

    def test(self, event):
        #subprocess.Popen(["python3", "word_test.py"])
        word_test.main()

    def reading(self, event):
        #subprocess.Popen(["python3", "reading.py"])
        reading.main()

    def history(self, event):
        #subprocess.Popen(["python3", "history.py"])
        history.main()

    def apikey(self, event):
        if self.flag:
            self.ctrl_apikey.Show()
            self.btn_save.Show()
            self.flag = False
        else:
            self.ctrl_apikey.Hide()
            self.btn_save.Hide()
            self.flag = True
        self.Layout()

    def save(self, event):
        dlg = wx.MessageDialog(self, "APIキーを更新しますか？", "確認", wx.YES_NO | wx.ICON_QUESTION)
        if dlg.ShowModal() == wx.ID_YES:
            with open(path("apikey", "api"), "w") as f:
                f.write(self.ctrl_apikey.GetValue().strip())
            self.ctrl_apikey.Clear()
        else:
            dlg.Destroy()
        self.ctrl_apikey.Hide()
        self.btn_save.Hide()
        
    # xボタン押下時の処理
    def onExit(self, event):
        dlg = wx.MessageDialog(self, "プログラムを終了しますか？", "確認", wx.YES_NO | wx.ICON_QUESTION)
        if dlg.ShowModal() == wx.ID_YES:
            self.Destroy()  # ウィンドウを破棄してプログラムを終了
        else:
            dlg.Destroy()

# アプリケーションクラス
class SampleApp(wx.App):
    def OnInit(self):
        frame = SampleFrame(None, -1, "Title")
        self.SetTopWindow(frame)
        frame.Show(True)
        return True

def main():
    app = SampleApp()
    app.MainLoop()

#main()

# メイン
'''
if __name__ == "__main__":
    app = SampleApp()
    app.MainLoop()
'''