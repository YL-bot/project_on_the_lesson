import requests
import sys
import pygame
import os

x, y = map(float, input("Введите координаты через пробел: ").split())
while not (-90 < y < 90 and -180 < y < 180):
    print("Неверные данные ")
    x, y = map(float, input("Введите координаты через пробел: ").split())
coords = f"{y} {x}"

scale = list(map(int, input("Введите параметры масштаба через пробел: ").split()))
while not (0 < scale[0] < 50 and 0 < scale[1] < 50):
    print("Неверные данные ")
    scale = list(map(int, input("Введите параметры масштаба через пробел: ").split()))
scale = f"{scale[0]} {scale[1]}"
map_file = "map.png"
map_file1 = "map1.png"
map_file2 = "map2.png"


def get_map(toponym_coordinates, zoom, map_file):
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={','.join(toponym_coordinates.split())}&spn={','.join(zoom.split())}&l=map"
    response = requests.get(map_request)
    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)
    with open(map_file, "wb") as file:
        file.write(response.content)


def get_sat(toponym_coordinates, zoom, map_file):
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={','.join(toponym_coordinates.split())}&spn={','.join(zoom.split())}&l=sat"
    response = requests.get(map_request)
    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)
    with open(map_file, "wb") as file:
        file.write(response.content)


def get_gb(toponym_coordinates, zoom, map_file):
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={','.join(toponym_coordinates.split())}&spn={','.join(zoom.split())}&l=sat,skl"
    response = requests.get(map_request)
    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)
    with open(map_file, "wb") as file:
        file.write(response.content)


get_map(coords, scale, map_file)
get_sat(coords, scale, map_file1)
get_gb(coords, scale, map_file2)
pygame.init()
screen = pygame.display.set_mode((600, 450))
slides = [pygame.image.load(map_file), pygame.image.load(map_file1), pygame.image.load(map_file2)]
running = True
i = 0
print("Презентация о снимках знаменитых пустынь: Сахара, Атакама, Виктория соотв.")
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
            i += 1
            i = (i + 1) % 3 - 1
    slide = slides[i]
    screen.blit(slide, (0, 0))
    pygame.display.flip()
pygame.quit()
os.remove(map_file)
