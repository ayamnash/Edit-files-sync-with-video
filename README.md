This  application for edit the SRT file. you can pick up srt file and video .
github link

 I tried to make it working well on Android, but the problem is Android refuses to save changes even though I gave it permissions due to my lack of experience in dealing with mobile applications.
Anyway, anyone can deal with permissions, as this code works on mobile phones in any vertical or horizontal direction.
i installed https://github.com/flet-dev/flet-build-template/tree/0.24.0
 and i tried many commands like
flet build apk --template-dir "C:\Users\ayman\Srt_V_EdIt\flet-build-template" --include-packages  flet_video -vv 
it is not working
i tried using permission_handler in my code like these
ph = ft.PermissionHandler()
page.overlay.append(ph)
def request_permission(e):
      ......
also
def open_app_settings(e):
    o = ph.open_app_settings()
    page.add(ft.Text(f"App Settings: {o}"))
flet build apk --template-dir "C:\Users\ayman\Srt_V_EdIt\flet-build-template" --include-packages flet_permission_handler flet_video -vv
I have attached a screen recorder to explain the issue
