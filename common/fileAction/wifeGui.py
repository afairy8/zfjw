import wx
from common.fileAction import wife
class WifeGui(wx.App):

    def OnInit(self):
        self.frame=wx.Frame(parent=None,title='wifeMain',size=(800,800))
        self.pannel=wx.Panel(self.frame,-1)
        ###条件部分pos(列坐标，行坐标）
        self.label1=wx.StaticText(self.pannel,-1,'选择操作：',pos=(200,150))
        self.label2=wx.StaticText(self.pannel,-1,'文件路径：',pos=(200,220))
        self.label3=wx.StaticText(self.pannel,-1,'合并方式：',pos=(200,290))
        self.label4=wx.StaticText(self.pannel,-1,'结果文件名：',pos=(200,360))
        ###单选部分
        self.action=wx.ComboBox(self.pannel,value='操作类型',choices=['合并xlsx',''],
                              size=(70,70),pos=(270,150))##合并操作
        self.path=wx.ComboBox(self.pannel,value='选择路径',choices=['当前（不含子路径）','所有（包含子路径）'],
                              size=(70,70),pos=(270,220))
        self.saveMet=wx.ComboBox(self.pannel,value='结果存储方式',choices=['一个工作表','多个工作表'],
                              size=(70,70),pos=(270,290))
        self.saveFileKeyWord=wx.TextCtrl(self.pannel,-1,size=(50,40),pos=(270,360))##结果文件关键字
        ##按钮
        self.confirm=wx.Button(self.pannel,-1,'确认',pos=(400,400))
        self.cancel=wx.Button(self.pannel,-1,'取消',pos=(520,400))
        self.Bind(wx.EVT_BUTTON,self.onConfirm,self.confirm)
        self.Bind(wx.EVT_BUTTON,self.onCancle,self.cancel)
        self.frame.Show()
        return True
    def onCombox(self):
        pass

    def onConfirm(self,event):
        action=self.action.GetValue()
        if action=='合并xlsx':
            action='merge'
        path=self.path.GetValue()
        if path=='当前（不含子路径）':
            path='curr'
        elif path=='所有（包含子路径）':
            path='all'
        else:
            path='curr'
        saveMet=self.saveMet.GetValue()
        if saveMet=='一个工作表':
            saveMet='1'
        elif saveMet=='多个工作表':
            saveMet='2'
        else:
            saveMet='1'
        saveFileKeyWord=self.saveFileKeyWord.GetValue()
        if wife.merge(action=action,curr=path,posix=saveMet,resfileName=saveFileKeyWord):
            wx.MessageBox('合并完成！')
        else:
            wx.MessageBox('失败!')

    def onCancle(self,event):
        self.frame.Close(force=True)

gui=WifeGui()
gui.MainLoop()