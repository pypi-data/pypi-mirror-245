import asyncio
import flet as ft
from flet import ButtonStyle
import pyperclip
from .vrobots_bridge import BRIDGE, WebSocketList
from .ui_components.ui_status_text import StatusText
from .ui_components.ui_multirotor_panel import mr_panel
from .ui_components.ui_msd_panel import msd_panel
from .ui_components.ui_heli_panel import heli_panel
from .ui_components.ui_imu0_panel import imu0_panel


async def app(page: ft.Page):

    ws_url = "ws://localhost:12740"

    async def button_clicked(e):
        pyperclip.copy(ws_url)
        page.snack_bar = ft.SnackBar(
            ft.Text(f"Copied to clipboard:  {ws_url}"))
        page.snack_bar.open = True
        await page.update_async()

    page.title = "Ubicoders Virtual Robots Bridge"
    page.window_width = 390
    page.window_height = 600
    page.bgcolor = "#ffffff"

    page.theme = ft.Theme(
        scrollbar_theme=ft.ScrollbarTheme(
            thumb_visibility=True,
            thumb_color="#fcba03",
        ),
    )

    img = ft.Image(
        src="https://jdhgeiavsn.ubicoders.com/cms/assets/5a473edc-e639-4fa7-8982-adc7211c47cd",
        width=300,
        height=100,
        fit=ft.ImageFit.CONTAIN,
    )

    txt_title = ft.Text("Virtual Robots Bridge Running at", color="#4d4d4d",
                        font_family="Sans",
                        weight=ft.FontWeight.W_900,
                        size=14)
    txt_title2 = ft.Text(ws_url, color="#059669",
                         font_family="Sans",
                         weight=ft.FontWeight.W_500,
                         size=14)

    await page.add_async(
        ft.Column(
            [
                # StatusText(1),
                ft.Row(
                    [img, ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [ft.Container(
                        ft.Column(
                            [txt_title,
                             ft.Row(
                                 [txt_title2,
                                  ft.TextButton(text="COPY",
                                                height=25,
                                                style=ButtonStyle(
                                                    color="#ffffff",
                                                    bgcolor="#6366f1",
                                                    padding=0
                                                ), on_click=button_clicked), ],
                                 alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                             ), ]
                        ),
                        padding=10,
                        bgcolor="#f2f2f2",
                        blend_mode=ft.BlendMode.MULTIPLY,
                        border_radius=5,
                        width=300,

                    )],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [ft.Container(
                        ft.Text("Virtual Robots", color="#4d4d4d", font_family="Sans",
                                weight=ft.FontWeight.W_900, size=14),
                        padding=10,
                        width=300,

                    )],
                    alignment=ft.MainAxisAlignment.CENTER,

                ),
                mr_panel,
                msd_panel,
                heli_panel,
                imu0_panel,
            ],

            alignment=ft.MainAxisAlignment.START,
        ),

    )


def gui_app_run():
    BRIDGE.start()
    #ft.app(target=main, view=ft.AppView.WEB_BROWSER)
    ft.app(target=app)


if __name__ == '__main__':
    gui_app_run()
