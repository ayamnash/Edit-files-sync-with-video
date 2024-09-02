import flet as ft
import threading
import time
import os
from flet import FilePicker, FilePickerResultEvent
class NavDraw(ft.NavigationDrawer):
    def __init__(self, page,pick_file_callback):
        self.page = page
        self.pick_file_callback = pick_file_callback
        self.page.drawer = ft.NavigationDrawer(
            on_change=self.on_drawer_change,
            controls=[
                ft.Container(height=12),
                ft.Divider(thickness=2),
                ft.NavigationDrawerDestination(
                    icon_content=ft.Icon(ft.icons.MAIL_OUTLINED),
                    label="About",
                    selected_icon=ft.icons.INFO,
                ),ft.NavigationDrawerDestination(
                    icon_content=ft.Icon(ft.icons.FILE_OPEN_ROUNDED),
                    label="Pick video file",
                    selected_icon=ft.icons.INFO,
                ),
            ],
        )

    def show_drawer(self, e):
        self.page.drawer.open = True
        self.page.drawer.update()

    def hide_drawer(self, e):
        self.page.drawer.open = False
        self.page.drawer.update()

    def on_drawer_change(self, e):
        if e.control.selected_index == 0:  # "Item 1" is at index 0
            self.naser(e)
        if e.control.selected_index == 1:  # "ayman" is at index 1
            self.pick_file_callback(e)
            self.hide_drawer(e)



    def naser(self, e):
        alert_dialog = diaolog = ft.AlertDialog(
            title=ft.Row(
                controls=[
                    ft.Text( "Instructions", size=30, color="pink600", italic=True
                    )

                ]

            ),

            content=ft.Column(
                controls=[
                    ft.Column(
                        controls=[
                        ft.Divider(),

                            ft.ResponsiveRow(
                                controls=[
                                    ft.IconButton(
                                        icon=ft.icons.ADD,
                                        icon_size=15,
                                         icon_color=ft.colors.WHITE,
                                        bgcolor=ft.colors.GREEN_300,
                                        
                                        
                                    ),
                                    ft.Text(
                                value='for increase the speed of scrolling',
                               
                                color=ft.colors.BLACK,
                                size=15
                            )
                                ],
                                spacing=4,
                                vertical_alignment='start',
                                alignment='start',
                                
                            ),
                            ft.Divider(),

                            ft.ResponsiveRow(
                                controls=[
                                    ft.IconButton(
                                        icon=ft.icons.REMOVE,
                                        icon_size=15,
                                        bgcolor=ft.colors.GREEN_300,
                                        icon_color=ft.colors.WHITE,
                                        
                                        
                                    ),
                                    ft.Text(
                                value='for Decrease the speed of scrolling',
                                
                                color=ft.colors.BLACK,
                                size=15
                            )
                                ],
                                spacing=4,
                                vertical_alignment='start',
                                alignment='start',
                                
                            ),ft.Divider(),
                            ft.ResponsiveRow(
                                controls=[
                                    ft.IconButton(
                                        icon=ft.icons.SAVE,
                                        icon_size=15,
                                        bgcolor=ft.colors.GREEN_300,
                                        icon_color=ft.colors.WHITE,
                                        
                                        
                                    ),
                                    ft.Text(
                                value='Save Changes',
                                color=ft.colors.BLACK,
                                size=15
                            )
                                ],
                                spacing=4,
                                vertical_alignment='start',
                                alignment='start',
                                
                            ),ft.Divider(),
                            ft.TextButton(
                                'Watch the \nYouTube video',
                                on_click=self.open_link,icon="VIDEO_LIBRARY",
                                 icon_color="green400",
                                style=ft.ButtonStyle(
            color=ft.colors.BLUE,  # Set the text color here
        ),
                               
                            ),
                            ft.Divider(),

                            
                            ft.TextButton(
                                'To contact the developer \ntelegram ',
                                on_click=self.open_link,icon="TELEGRAM",
                                 icon_color="green400",
                                style=ft.ButtonStyle(
            color=ft.colors.BLUE,  # Set the text color here
        ),
                               
                            )
                            ,

                            
                           
                            
                        ],
                        
                    
                        
                   )
                ],
                
                horizontal_alignment='start',
                scroll= ft.ScrollMode.ALWAYS
                
            )
        
        ,


            # actions=[ft.TextButton(text="Close", on_click=self.close_dialog)],
            # open=True,
            
        )
        self.page.overlay.append(alert_dialog)
        alert_dialog.open = True
        self.page.update()
        
        # self.page.dialog = diaolog 
        # self.page.update() 
        # self.page.dialog = alert_dialog
        # alert_dialog.open = True
        # self.page.update()
    def close_dialog(self, e):
        if self.page.overlay and len(self.page.overlay) > 0:
            dialog = self.page.overlay.pop()
            if isinstance(dialog, ft.AlertDialog):
                dialog.open = False
        self.page.update()
    def open_link(self,e):
        self.page.launch_url("https://t.me/ayamnash")    

def main(page: ft.Page):
    page.window_icon = None
    WIDTH: int = page.width
    HEIGHT: int = page.height
    page.scroll = True
   
    row_height = 48
    
    
    
    
    current_srt_file_path = None
    editable_rows = []
    video_control = None
    subtitles = []
    video = None
    video_position_text = ft.Text("Current: 0:00")
    video_duration_text = ft.Text("V.Duration:")

    
    
    
    
    srt_column = ft.Column(scroll=ft.ScrollMode.AUTO, height=HEIGHT*0.6, width=WIDTH * 0.9)
    srt_column1 = ft.ResponsiveRow(
    controls=[
        ft.Container(content=srt_column, col={"xs": 12})
    ]
)

    
    video_position_text = ft.Text("Current: 0:00")
    video_duration_text = ft.Text("V.Duration:")

    
    duration_text = ft.Text(value="")
    video_container = ft.Container(height=HEIGHT*0.30,width=WIDTH *0.95)  # Container to hold the video
    video_container1= ft.ResponsiveRow(
    controls=[
        ft.Container(content=video_container, col={"xs": 12})
    ]
)

    def pick_srt_result(e: ft.FilePickerResultEvent):
        nonlocal current_srt_file_path, subtitles
        if not e.files:
            return
        if e.files:
            file = e.files[0]
            current_srt_file_path = file.path
            try:
                with open(file.path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    srt_column.controls.clear()
                    editable_rows.clear()
                    subtitles = parse_srt(content)
                    for timestamp, text in subtitles:
                        add_editable_row(timestamp, text)
                    page.update()
            except FileNotFoundError:
                srt_column.controls.append(ft.Text("File not found or inaccessible."))
                page.update()
            except Exception as ex:
                srt_column.controls.append(ft.Text(f"An error occurred: {str(ex)}"))
                page.update()

    def parse_srt(content):
        subtitles = []
        blocks = content.split("\n\n")
        for block in blocks:
            lines = block.strip().split("\n")
            if len(lines) >= 3:
                timestamp = lines[1]
                text = " ".join(lines[2:])
                subtitles.append((timestamp, text))
        return subtitles

    def pick_srt_clicked(e):
        
        srt_picker.pick_files(allowed_extensions=["srt"])

    def add_editable_row(timestamp, text):
        timestamp_field = ft.TextField(value=timestamp, expand=4, text_size=11,)
        text_field = ft.TextField(value=text, expand=3, text_size=12,multiline=True,)
        row = ft.Row([timestamp_field, text_field])
        srt_column.controls.append(row)
        editable_rows.append({"timestamp": timestamp_field, "text": text_field})
    file_picker = FilePicker()
    page.overlay.append(file_picker)
    def save_edits(e):
        if current_srt_file_path:
            try:
                # Ensure path is valid and writable
                if not os.access(current_srt_file_path, os.W_OK):
                    show_snackbar("File is not writable. Ensure proper permissions.")
                    return
                
                with open(current_srt_file_path, 'w', encoding='utf-8') as f:
                    for i, row in enumerate(editable_rows):
                        f.write(f"{i + 1}\n")
                        f.write(f"{row['timestamp'].value}\n")
                        f.write(f"{row['text'].value}\n\n")
                show_snackbar("Changes saved successfully.")
            except Exception as ex:
                show_snackbar(f"An error occurred while saving: {str(ex)}")
    def pick_file (e):
   
        video_picker.pick_files(allow_multiple=False, file_type=ft.FilePickerFileType.VIDEO)                 

    def show_snackbar(message):
        snack_bar = ft.SnackBar(content=ft.Text(message), open=True)
        
        page.overlay.append(snack_bar)
        page.update()


    video = None
    def update_video_position():
        while video and video.is_playing:

            try:
                position_ms = video.get_current_position()
                position_sec = position_ms / 1000
                video_position_text.value = f"Current: {time.strftime('%M:%S', time.gmtime(position_sec))}"
                page.update()
                
                target_row_index = None
                for index, row in enumerate(editable_rows):
                    timestamp = row['timestamp'].value
                    
                    row_time_sec = timestamp_to_seconds(timestamp)
                    if row_time_sec > position_sec:
                        target_row_index = max(0, index - 1)
                        break

                if target_row_index is None:
                    target_row_index = len(editable_rows) - 1

                
                scroll_position = (target_row_index * row_height)
                srt_column.scroll_to(offset=scroll_position, duration=50)
                page.update()

            except Exception as e:
                pass

            time.sleep(1)
    def load_video(e: ft.FilePickerResultEvent):
        nonlocal video
        if not e.files:
            return 
        if e.files:
            picked_video_path = e.files[0].path
            
            
            picked_video = ft.VideoMedia(picked_video_path)
            video = ft.Video(
                aspect_ratio=16/9,
                autoplay=False,
                
                playlist=[picked_video],
                playlist_mode=ft.PlaylistMode.NONE,
            )
            video_container.content = video
            page.update()
        time.sleep(1)
        duration_ms = video.get_duration()
        duration_sec = duration_ms / 1000
        video_duration_text.value = f"V.Duration: {time.strftime('%M:%S', time.gmtime(duration_sec))}"
        faster_sw.visible = True
        pause_button.visible=True
        play_button.visible=True
        save_button.visible=True
        pscroll.visible=True
        mscroll.visible=True

        page.update()
    def play_video(e):
        # if video_container.content:
        #     video_container.content.play()
            
        #     page.update()
        if video:
            video.play()
            threading.Thread(target=update_video_position, daemon=True).start()
            page.update()
    def pause_video(e):
        if video_container.content:
            video_container.content.pause()
            page.update()

    
    def increase_row_height(e):
        nonlocal row_height
        row_height += 1  # Increase the row height by 50
        page.update()
    def decrease_row_height(e):
        nonlocal row_height
        row_height -= 1  # Increase the row height by 50
        page.update() 

    def timestamp_to_seconds(timestamp):
        try:
            start_time = timestamp.split(' --> ')[0]
            parts = start_time.split(':')
            hours, minutes, seconds = parts
            seconds = float(seconds.replace(',', '.'))
            return int(hours) * 3600 + int(minutes) * 60 + seconds
        except Exception as e:
            return 0
    def playback_rate(e):
        video.playback_rate = e.control.value   
        spe.value=  f"play  x{faster_sw.value}" 
        page.update()
    faster_sw = ft.Dropdown(
        width=100,
        height=21,
        bgcolor=ft.colors.WHITE,
        visible=False,  # Initially hidden
        label='Speed',
        label_style=ft.TextStyle(
            size=8,  # Set the label font size here
            color=ft.colors.BLACK,
            weight=ft.FontWeight.BOLD,
        ), 

        options=[
            ft.dropdown.Option("1.1"),
            ft.dropdown.Option("1.25"),
            ft.dropdown.Option("1.75"),
            ft.dropdown.Option("2"),
            ft.dropdown.Option("0.9"),
            ft.dropdown.Option("0.75"),
            ft.dropdown.Option("0.5"),
            ft.dropdown.Option("0.25"),
        ],
        text_style=ft.TextStyle(
            size=12,
            bgcolor=ft.colors.GREEN  # Set the font size here
            
        ),
        on_change=playback_rate
    ) 
    def on_resize(e):
        # Update container size when the window is resized
        contentall.width = page.width
        contentall.height = page.height
        page.update()   
        print('s')

    srt_picker = ft.FilePicker(on_result=pick_srt_result)
    video_picker = ft.FilePicker(on_result=load_video)
    page.overlay.extend([srt_picker, video_picker])

    pick_video_button = ft.ElevatedButton(content=ft.Text(
            "pick video file",
            size=12,  # Set the font size here
            
        ),on_click= pick_file,

    )
    
    srtt = ft.ElevatedButton(content=ft.Text(
            "pick srt file",
            size=12,  # Set the font size here
            
        ),on_click=pick_srt_clicked)
    save_button = ft.IconButton(
        visible=False,
        padding=0,
        icon=ft.icons.SAVE,
        icon_size=30,
        icon_color=ft.colors.BLUE,
        bgcolor=ft.colors.GREEN_300,
        opacity=0.9,
        on_click=save_edits
    )

    button_row = ft.ResponsiveRow(
    controls=[
        ft.Container(content=pick_video_button, col={"xs": 5}),
        ft.Container(content=srtt, col={"xs": 4}),
        ft.Container(content=save_button, col={"xs": 3}),
    ]
    , alignment=ft.MainAxisAlignment.SPACE_BETWEEN
)
    ND=NavDraw(page, pick_file)
    spe = ft.Text("play", size=11,color=ft.colors.BLACK)
    play_button = ft.ElevatedButton(visible=False,
    content=ft.Container(
            content=ft.Row(
                [
                    ft.Icon(ft.icons.PLAY_ARROW, size=16),  # Adjusted icon size for better alignment
                    spe,
                ],
                spacing=0,  # No space between icon and text
                alignment=ft.MainAxisAlignment.START,  # Align content to start (left)
                vertical_alignment=ft.CrossAxisAlignment.CENTER,  # Center align vertically
            ),
            padding=ft.padding.only(left=2, right=8, top=0, bottom=0),  # Minimal left padding
        ),
        style=ft.ButtonStyle(
            padding=0,  # Remove default button padding
            shape=ft.RoundedRectangleBorder(radius=4),  # Optional: rounded corners
        ),
   

    on_click=play_video
)
    pau=ft.Text('paus', size=11,color=ft.colors.BLACK)
    pause_button = ft.ElevatedButton(visible=False,
    content=ft.Container(
            content=ft.Row(
                [
                    ft.Icon(ft.icons.PLAY_ARROW, size=16),  # Adjusted icon size for better alignment
                    pau,
                ],
                spacing=0,  # No space between icon and text
                alignment=ft.MainAxisAlignment.START,  # Align content to start (left)
                vertical_alignment=ft.CrossAxisAlignment.CENTER,  # Center align vertically
            ),
            padding=ft.padding.only(left=2, right=8, top=0, bottom=0),  # Minimal left padding
        ),
        style=ft.ButtonStyle(
            padding=0,  # Remove default button padding
            shape=ft.RoundedRectangleBorder(radius=4),  # Optional: rounded corners
        ),
   

    on_click=pause_video
)
    
    ttt =ft.Row(
    controls=[ ft.IconButton(
                                            icon=ft.icons.MENU,
                                            icon_size=30,
                                            icon_color=ft.colors.BLUE,
                                            bgcolor=ft.colors.GREEN_200,
                                            opacity=0.9,
                                            width=60,
                                            height=40,
                                            alignment=ft.alignment.center, on_click=ND.show_drawer),
                                            ft.Text("Edit srt supported video", size=16,weight='bold',color=ft.colors.WHITE),  # Added text here
                                            ],
                                            alignment=ft.MainAxisAlignment.CENTER,  # Center-align the row contents
                                            vertical_alignment=ft.CrossAxisAlignment.CENTER,  # Vertically center the contents
                                        )

    tt1=ft.Container(
    content=ft.Row(
        controls=[ttt]
    ),
    bgcolor=ft.colors.BLUE_400,
    width=WIDTH

)
    pscroll = ft.ElevatedButton(visible=False,
    content=ft.Text(
        "+",
        weight=ft.FontWeight.BOLD  # Make the text bold
    ),
    on_click=increase_row_height,
    width=50
)

    mscroll = ft.ElevatedButton(visible=False,
    content=ft.Text(
        "-",
        weight=ft.FontWeight.BOLD  # Make the text bold
    ),
    on_click=decrease_row_height,
    width=50
)
    video_controls = ft.ResponsiveRow(
    controls=[
        ft.Container(content=play_button, col={"xs": 4}),
        ft.Container(content=pause_button, col={"xs": 4}),
        ft.Container(content=pscroll, col={"xs": 2}),
        ft.Container(content=mscroll, col={"xs": 2}),
    ],
    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
)
    ayman= ft.Row([video_position_text,video_duration_text,faster_sw])
    contentall = ft.Column( expand=True,controls=[
        ft.Row([tt1]),
        button_row,
        ayman,

        video_container1,  # Video container placed before SRT column
        duration_text,
        video_controls,
        
       srt_column1,
    ],width=WIDTH*0.95,scroll='auto')

    
    page.add(ft.SafeArea(content=contentall))
    page.update()
    
    page.on_resized = on_resize

ft.app(target=main, assets_dir="assets")