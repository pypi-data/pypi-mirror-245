import flet as ft
from .ui_status_text import StatusText

imu0_panel = ft.Row(
                    [
                        ft.Container(
                            ft.Row(
                                [ft.Text("IMU0", color="#4d4d4d", font_family="Sans",weight=ft.FontWeight.W_500, size=14  ),
                                 ft.Container(
                                    StatusText("imu0"),
                                 )],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            ),
                            bgcolor="#f2f2f2",
                            padding=10,
                            width=300,
                        )
                    ], alignment=ft.MainAxisAlignment.CENTER, )