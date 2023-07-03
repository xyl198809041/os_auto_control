# 版本号
v = '2023.06.30.21'
server_v = v

# 系统进程白名单
process_white_list = ['System Idle Process', 'System', 'Registry', 'RuntimeBroker.exe', 'ctfmon.exe', 'smss.exe',
                      'wininit.exe', 'svchost.exe', 'lsass.exe', 'msedge.exe', 'csrss.exe', 'SearchApp.exe',
                      'services.exe', 'fontdrvhost.exe', 'explorer.exe', 'StartMenuExperienceHost.exe',
                      'SecurityHealthService.exe', 'pycharm64.exe', 'WUDFHost.exe', 'igfxCUIServiceN.exe',
                      'taskhostw.exe', 'MemCompression', 'SettingSyncHost.exe', 'spoolsv.exe', 'wlanext.exe',
                      'conhost.exe', 'IntelCpHDCPSvc.exe', 'OfficeClickToRun.exe', 'hc_engine.exe', 'EasiUpdate.exe',
                      'IntelAudioService.exe', 'esif_uf.exe', 'SangforPW.exe', 'RtkAudUService64.exe',
                      'UserOOBEBroker.exe', 'SurfaceService.exe', 'MsMpEng.exe', 'SangforUDProtect.exe',
                      'YourPhone.exe', 'SearchProtocolHost.exe', 'HuoChat.exe', 'LockApp.exe', 'dasHost.exe',
                      'SgrmBroker.exe', 'GoogleCrashHandler64.exe', 'WinStore.App.exe', 'winlogon.exe', 'dllhost.exe',
                      'baidupinyin.exe', 'TabTip.exe', 'FileCoAuth.exe', 'commsapps.exe', 'SearchIndexer.exe',
                      'WDADesktopService.exe', 'ShellExperienceHost.exe', 'OneDrive.exe', 'python.exe', 'pptim.exe',
                      'Ssms.exe', 'GoogleCrashHandler.exe', 'SystemSettings.exe', 'dwm.exe', 'NisSrv.exe',
                      'igfxEMN.exe', 'TextInputHost.exe', 'SearchFilterHost.exe', 'WordIm.exe', 'ChsIME.exe',
                      'sihost.exe', 'fsnotifier64.exe', 'Video.UI.exe', 'ApplicationFrameHost.exe',
                      'Microsoft.Photos.exe', 'HxTsr.exe',
                      # 以上是我系统上的软件
                      'smss.exe', 'svchost.exe', 'Code.exe', 'SynTPHelper.exe', 'csrss.exe', 'wininit.exe',
                      'conhost.exe', 'services.exe', 'lsass.exe', 'winlogon.exe', 'fontdrvhost.exe',
                      'SearchFilterHost.exe',
                      'RtkAudioService.exe', 'CodeHelper.exe', 'dwm.exe', 'driver.exe', 'SearchProtocolHost.exe',
                      'HipsDaemon.exe', 'MemCompression', 'audiodg.exe', 'usysdiag.exe', 'wsctrlsvc.exe',
                      'spoolsv.exe', 'taskhostw.exe', 'dasHost.exe', 'ApplicationFrameHost.exe', 'FamItrf2.Exe',
                      'BtwRSupportService.exe', 'EasiUpdate.exe', 'fpCSEvtSvc.exe', 'SynTPEnhService.exe',
                      'rserver3.exe', 'valWBFPolicyService.exe', 'PPTService.exe', 'explorer.exe', 'HipsTray.exe',
                      'dllhost.exe', 'SystemSettings.exe', 'RtHDVBg.exe', 'SeewoLink.exe', 'SynTPEnh.exe',
                      'sihost.exe', 'SecurityHealthService.exe', 'SeewoLinkService.exe', 'ShellExperienceHost.exe',
                      'SearchUI.exe', 'RuntimeBroker.exe', 'ctfmon.exe', 'TabTip.exe', 'FamItrfc.Exe', 'alg.exe',
                      'WindowsInternal.ComposableShell.Experiences.TextInput.InputApp.exe', 'baidupinyin.exe',
                      'SearchIndexer.exe', 'POWERPNT.EXE', 'WmiPrvSE.exe', 'python.exe', 'winpty-agent.exe',
                      'powershell.exe', "TrustedInstaller.exe",
                      "TiWorker.exe",
                      "WhiteboardWRT.exe",
                      "smartscreen.exe",
                      "baidunetdisk.exe",
                      "baidunetdiskhost.exe",
                      "baidunetdiskrender.exe",
                      "yundetectservice.exe",
                      "identity_helper.exe",
                      "XLLiveUD.exe",
                      "DownloadSDKServer.exe",
                      "Thunder.exe",
                      "WeChatStore.exe",
                      "xlbrowsershell.exe",
                      "OpenWith.exe",
                      "rundll32.exe",
                      "backgroundTaskHost.exe",
                      "ScreenClippingHost.exe",
                      'LogonUI.exe',
                      'rdpclip.exe',
                      'TSTheme.exe',
                      'AtBroker.exe',
                      'Taskmgr.exe',
                      'chrome.exe',
                      'WMIADAP.exe',
                      'UpdateNotificationMgr.exe',
                      'GoogleUpdate.exe',
                      'SpeechRuntime.exe',
                      'RtHDVCpl.exe',
                      'SppExtComObj.Exe',
                      'sppsvc.exe',
                      'igfxTray.exe',
                      'igfxHK.exe',
                      'igfxEM.exe',
                      'pythonw.exe',
                      'PresentationFontCache.exe',
                      'telnetd.exe',
                      'BaiduPinyinCore.exe',
                      'EasiUpdate3Protect.exe',
                      'EasiUpdate3.exe',
                      'CompatTelRunner.exe',
                      'igfxCUIService.exe',
                      'HRUpdate.exe',
                      'BugReport.exe',
                      'QQ.exe',
                      'WeChat.exe',
                      'wechatweb.exe',
                      'QQProtect.exe',
                      'nvvsvc.exe',
                      'Defrag.exe',
                      'nvxdsync.exe',
                      'nvvsvc.exe',
                      'imeconfig.exe',
                      'QQPlayer.exe',
                      'DrvCeox86.exe',
                      'cmd.exe',
                      'python.exe',
                      'pythonw.exe',
                      'pip.exe',
                      'HiteDriver.exe',
                      'py.exe',
                      'Promethean Calib.exe',
                      'nvtray.exe',
                      'NvBackend.exe',
                      'bdimeupdate.exe',
                      'hkcmd.exe',
                      'igfxpers.exe',
                      'igfxtray.exe',
                      'NVDisplay.Container.exe',
                      'WeChatApp.exe'
                      # 以上是教室机器上的软件
                      ]

process_black_list = []

process_not_in_list = []

Copyright_white_list = ['Microsoft']

Copyright_back_list = ['下载器', '360']

process_allow_now_list = {}
