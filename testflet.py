import time
from time import sleep
import flet as ft

def main(page: ft.Page):
    page.title = "Auto-scrolling ListView"
    page.window_width = 400
    page.window_height = 600
    page.window_resizable = False
    page.scroll = "ADAPTIVE"

    array = []
    def func(array):
        for i in range(50):
            array.append(i)
            print(i)
            page.add(ft.Text(f"{i}"))
            page.update()
            sleep(1)


    # count = 1
    #
    # for i in range(0, 60):
    #     lv.controls.append(ft.Text(f"Line {count}"))
    #     count += 1

    # page.add(lv)
    # func(lv)

    def start(e):
        page.route = "/chat"
        page.clean()
        func(array)

    chatGPTtoken = ft.TextField(label="chat-GPT токен")
    pictoken = ft.TextField(label="Picovoice токен")

    def go_settings(e):
        page.route = "/settings"
        page.clean()
        page.add(
            ft.AppBar(title=ft.Text("Настройки"), bgcolor=ft.colors.SURFACE_VARIANT),
            ft.Stack([
                chatGPTtoken,
            ],
                height=50),
            ft.ElevatedButton("Сохранить!", ),
            ft.Stack([
                pictoken,
                ft.ElevatedButton("Сохранить!", top=65, ),
                ft.ElevatedButton("Настройки", top=342, on_click=go_settings),
                ft.ElevatedButton("Домой", top=342, left=137, on_click=go_home),
                ft.ElevatedButton("Команды", top=342, left=245, ),

            ],
                height=500,
                width=500,
            )
        )
        page.update()


    def go_home(e):
        page.route = "/"
        page.clean()
        page.add(
            ft.AppBar(title=ft.Text("Главная"), bgcolor=ft.colors.SURFACE_VARIANT),
            ft.Stack([
                ft.ElevatedButton("Старт", top=300, width=170, left=95, bgcolor="#0136A0", color="#FDF5E6",),
                ft.ElevatedButton("Cтоп", top=350, width=170, left=95, bgcolor="#EB4C42", color="#FDF5E6",),
                ft.ElevatedButton("Настройки", top=444, on_click=go_settings),
                ft.ElevatedButton("Домой", top=444, left=137, on_click=go_home),
                ft.ElevatedButton("Команды", top=444, left=245, ),

            ],
                width=400,
                height=600
            )
        )
        page.update()

    page.add(
        ft.AppBar(title=ft.Text("Главная"), bgcolor=ft.colors.SURFACE_VARIANT),
        ft.Stack([
            ft.ElevatedButton("Старт", top=300, width=170, left=95, bgcolor="#0136A0", color="#FDF5E6", on_click=start),
            ft.ElevatedButton("Cтоп", top=350, width=170, left=95, bgcolor="#EB4C42", color="#FDF5E6",),
            ft.ElevatedButton("Настройки", top=444, on_click=go_settings),
            ft.ElevatedButton("Домой", top=444, left=137, on_click=go_home),
            ft.ElevatedButton("Команды", top=444, left=245),
        ],
            width=400,
            height=600
        )
    )




ft.app(target=main)