import asyncio
import flet as ft

async def main(page: ft.Page) -> None:
    page.title = "Rocket Clicker"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#141221"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.fonts = {"FulboArgenta": "fonts/FulboArgenta.ttf"}
    page.theme = ft.Theme(font_family="FulboArgenta")

    def on_tap_down(event: ft.ContainerTapEvent):
        global tap_position
        tap_position = (event.local_x, event.local_y)

    async def upgrade_clicks():
        score.data -= price.data
        price.data * 2.5
        
        await page.update_async()

    async def score_up(event: ft.ContainerTapEvent) -> None:
        score.data += clicks.data
        score.value = str(score.data)

        image.scale = 0.95

        score_counter.size = 54
        score_counter.value = f"+{str(clicks.data)}"
        score_counter.right = 0
        score_counter.left = tap_position[0]
        score_counter.top = tap_position[1]
        score_counter.bottom = 0

        progress_bar.value += (1 / 100)

        if(score.data % 100 == 0):
            page.snack_bar = ft.SnackBar(
                content=ft.Text(
                    value="🚀 +100",
                    size=20,
                    color="#1E90FF",
                    text_align=ft.TextAlign.CENTER
                ),
                bgcolor="#25223a"
            )
            page.snack_bar.open = True
            progress_bar.value = 0

        await page.update_async()

        await asyncio.sleep(0.2)
        image.scale = 1
        score_counter.size = 0

        await page.update_async()
        
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(regenEnergy())
    # loop.close()


    clicks = ft.Text(value="1", size=0, data=1)
    score = ft.Text(value="0", size=100, data=0)
    score_counter =  ft.Text(
        size=50, animate_opacity=ft.Animation(duration=600, curve=ft.AnimationCurve.BOUNCE_IN)
    )
    image = ft.Image(
        src="Rocket.png",
        fit=ft.ImageFit.CONTAIN,
        animate_scale=ft.Animation(duration=600, curve=ft.AnimationCurve.EASE)
    )
    progress_bar = ft.ProgressBar(
        value=0,
        width=page.width - 100,
        bar_height=20,
        color="#1E90FF",
        bgcolor="#FFF0F5"
    )
    upg_clicks = ft.Text(value="Улучшить Клик", size=50, animate_scale=ft.Animation(duration=600, curve=ft.AnimationCurve.EASE), data=clicks.data)
    price = ft.Text(value="\n\n1000", size=25, data=1000)
    await page.add_async(
        score,
        ft.Container(
            content=ft.Stack(controls=[
                image,
                score_counter
            ]),
            on_click=score_up,
            on_tap_down=on_tap_down,
            margin=ft.Margin(0, 0, 0, 30)
        ),
        ft.Container(
            content=progress_bar,
            border_radius=ft.BorderRadius(10, 10, 10, 10)
        ),
        ft.Container(
            content=ft.Stack(controls=[
                upg_clicks,
                ft.Text(value="\n\n\n\nСтоимость: "),
                price,
            ]),
            on_click=upgrade_clicks,
            on_tap_down=on_tap_down
        )
    )

if __name__ == "__main__":
    ft.app(target=main, view=ft.WEB_BROWSER, port=8000)