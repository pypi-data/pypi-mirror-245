#!/usr/bin/python3
import wx
from libs.common import json_open, json_write, path, set_font, add_word

class MyFrame(wx.Frame):
    def __init__(self, parent, ID, title):
        # わからん
        wx.Frame.__init__(self, parent, title=title, pos=(0, 0), size=(800, 400))
        # words.jsonのパス
        self.filename = path("words.json")
        # おまじない
        #self.Bind(wx.EVT_CLOSE, self.onExit)
        self.__set_word()
        self.__create_widget()
        self.__do_layout()
        self.Show()

    # # 単語リストと辞書型の意味リストを作成
    def __set_word(self):
        self.wordlist = [""]
        self.meaninglist = {}
        # jsonファイルの読み込み
        json_data = json_open(self.filename)
        for key, value in json_data.items():
            self.wordlist.append(key)
            self.meaninglist[key] = value["meaning"]

    def __create_widget(self):
        # コンボボックス
        self.combobox = wx.ComboBox(self, choices=self.wordlist, style=wx.CB_DROPDOWN | wx.CB_SORT)
        # 選択した英単語の意味を表示するボタン
        self.btn_show = wx.Button(self, -1, "show")
        self.btn_show.Bind(wx.EVT_BUTTON, self.push_show)

        # 選択した英単語を削除するボタン
        self.btn_delete = wx.Button(self, -1, "delete")
        self.btn_delete.Bind(wx.EVT_BUTTON, self.push_delete)
        self.btn_delete.Disable()

        # 英単語の意味を表示するテキスト
        self.txt_meaning = wx.StaticText(self, -1, "", style=wx.TE_CENTER)
        self.txt_meaning.SetFont(set_font(25))

        # 単語検索と単語入力を区切る線
        line = "─────────────────────────────────────────────────────────────"
        self.txt_line = wx.StaticText(self, -1, line, style=wx.TE_CENTER)

        # word入力の案内
        self.word = wx.StaticText(self, -1, "word", style=wx.TE_CENTER)
        # wordを入力するためのテキストボックス
        self.txtCtrl_word = wx.TextCtrl(self, -1, size=(430, 25) )
        
        # meaning入力の案内
        self.meaning = wx.StaticText(self, -1, "meaning", style=wx.TE_CENTER)
        # meaningを入力するためのテキストボックス
        self.txtCtrl_meaning = wx.TextCtrl(self, -1, size=(430, 25) )
        
        # 入力したwordとmeaningを追加するボタン
        self.btn_add = wx.Button(self, -1, "add")
        self.btn_add.Bind(wx.EVT_BUTTON, self.push_add)

        # 追加が成功したことを報告するためのテキスト
        self.txt_success = wx.StaticText(self, -1, "", style=wx.TE_CENTER)
        self.txt_success.SetForegroundColour('#0000FF')
        self.txt_success.SetFont(set_font(15))

    def __do_layout(self):
        # *.Add(部品、位置、余白入れる位置、余白px)
        # VERTICAL:縦, HORIZONTAL:横
        sizer_all = wx.BoxSizer(wx.VERTICAL)

        # コンボボックスとshowボタンの配置
        sizer_wl = wx.BoxSizer(wx.HORIZONTAL)
        sizer_wl.Add(self.combobox, flag=wx.ALIGN_CENTER | wx.TOP, border=10)
        sizer_wl.Add(self.btn_show, flag=wx.ALIGN_CENTER | wx.LEFT | wx.TOP, border=10)
        sizer_wl.Add(self.btn_delete, flag=wx.ALIGN_CENTER | wx.LEFT | wx.TOP, border=10)
        sizer_all.Add(sizer_wl, flag=wx.ALIGN_CENTER | wx.BOTTOM, border=20)
        
        # 意味を表示するテキストの配置
        sizer_all.Add(self.txt_meaning, flag=wx.ALIGN_CENTER)

        # 単語検索と単語入力を区切る線の配置
        sizer_all.Add(self.txt_line, flag=wx.ALIGN_CENTER | wx.ALL, border=20)

        # 単語入力用のテキストボックスの配置
        sizer_wd = wx.BoxSizer(wx.HORIZONTAL)
        sizer_wd.Add(self.word, flag=wx.ALIGN_CENTER)
        sizer_wd.Add(self.txtCtrl_word, flag=wx.ALIGN_CENTER | wx.LEFT, border=35)
        sizer_all.Add(sizer_wd, flag=wx.ALIGN_CENTER | wx.ALL, border=5)

        # 意味入力用のテキストボックスの配置
        sizer_mn = wx.BoxSizer(wx.HORIZONTAL)
        sizer_mn.Add(self.meaning, flag=wx.ALIGN_CENTER)
        sizer_mn.Add(self.txtCtrl_meaning, flag=wx.ALIGN_CENTER | wx.LEFT, border=10)
        sizer_all.Add(sizer_mn, flag=wx.ALIGN_CENTER | wx.ALL, border=5)

        # 単語追加成功報告テキストの配置
        sizer_all.Add(self.btn_add, flag=wx.ALIGN_CENTER)
        sizer_all.Add(self.txt_success, flag=wx.ALIGN_CENTER | wx.LEFT, border=10)

        # 配置の確定？
        self.SetSizer(sizer_all)

    # showボタン押下時の処理
    def push_show(self, event):
        self.select_word = self.combobox.GetValue()
        # 存在しない単語が入力された時のエラー表示
        if self.meaninglist.get(self.select_word) is None:
            self.txt_meaning.SetLabel("Unregistered word")
            self.txt_meaning.SetForegroundColour('#FF0000')
        else: # 文字数によってフォントサイズを変更する
            if len(self.meaninglist[self.select_word]) > 30:
                self.txt_meaning.SetFont(set_font(20))
            else:
                self.txt_meaning.SetFont(set_font(25))
            # 意味の表示
            self.txt_meaning.SetLabel(self.meaninglist[self.select_word])
            self.txt_meaning.SetForegroundColour('#000000')
        self.btn_delete.Enable()
        # レイアウト整理
        self.Layout()

    # deleteボタン押下時の処理
    def push_delete(self, event):
        json_data = json_open(self.filename)
        if self.select_word in json_data:
            del json_data[self.select_word]
        json_write(self.filename, json_data)
        self.combobox.SetStringSelection(self.select_word)
        self.combobox.Delete(self.combobox.GetSelection())
        self.combobox.SetValue('')
        self.txt_meaning.SetLabel("Deleted " + self.select_word)
        self.txt_meaning.SetForegroundColour('#0000FF')
        self.btn_delete.Disable()
        self.Layout()

    # addボタン押下時の処理
    def push_add(self, event):
        word = self.txtCtrl_word.GetValue().strip() #空白とか消す
        meaning = self.txtCtrl_meaning.GetValue().strip()
        if word != "" and meaning != "": #テキストボックスが空白でなければ
            # 単語の追加
            add_word(word, meaning, self.filename)
            # 成功時のメッセージ表示
            self.txt_success.SetForegroundColour('#0000FF')
            self.txt_success.SetLabel( "\"" + word + "\" " + "added.")
            # 単語をコンボボックスに追加、意味を紐づける
            self.combobox.Append(self.txtCtrl_word.GetValue())
            self.meaninglist[self.txtCtrl_word.GetValue()] = meaning
            # テキストボックスを空にする
            self.txtCtrl_word.Clear()
            self.txtCtrl_meaning.Clear()
        else: # エラーメッセージの表示
            self.txt_success.SetForegroundColour('#FF0000')
            self.txt_success.SetLabel("Enter a word and meaning.")
        # レイアウト整理
        self.Layout()

    # xボタン押下時の処理
    def onExit(self, event):
        dlg = wx.MessageDialog(self, "プログラムを終了しますか？", "確認", wx.YES_NO | wx.ICON_QUESTION)
        if dlg.ShowModal() == wx.ID_YES:
            self.Destroy()  # ウィンドウを破棄してプログラムを終了
        else:
            dlg.Destroy()

class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, -1, "Wordlist")
        self.SetTopWindow(frame)
        frame.Show(True)
        return True

#if __name__ == '__main__':
def main():
    app = MyApp()
    app.MainLoop()

#main()