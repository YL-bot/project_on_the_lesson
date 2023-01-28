import requests
import sys
import pygame
import os

x, y = map(float, input("Введите координаты через пробел: ").split())
while not (-90 < y < 90 and -180 < y < 180):
    print("Неверные данные ")
    x, y = map(float, input("Введите координаты через пробел: ").split())
coords = f"{y} {x}"
print()
scale = list(map(float, input("Введите параметры масштаба через пробел: ").split()))
while not (0 < scale[0] < 50 and 0 < scale[1] < 50):
    print("Неверные данные ")
    scale = list(map(float, input("Введите параметры масштаба через пробел: ").split()))
scale = f"{scale[0]} {scale[1]}"
map_file = "map.png"
map_file1 = "map1.png"
map_file2 = "map2.png"


def get_map(toponym_coordinates, zoom, map_file, *pt):
    if pt:
        pt = ",".join(coords_of_city.split())
        map_request = f"http://static-maps.yandex.ru/1.x/?ll={','.join(toponym_coordinates.split())}&spn={','.join(zoom.split())}&l=map&pt={pt},pm2gnm1"
    else:
        map_request = f"http://static-maps.yandex.ru/1.x/?ll={','.join(toponym_coordinates.split())}&spn={','.join(zoom.split())}&l=map"
    response = requests.get(map_request)
    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)
    with open(map_file, "wb") as file:
        file.write(response.content)


def get_sat(toponym_coordinates, zoom, map_file, *pt):
    if pt:
        pt = ",".join(coords_of_city.split())
        map_request = f"http://static-maps.yandex.ru/1.x/?ll={','.join(toponym_coordinates.split())}&spn={','.join(zoom.split())}&l=sat&pt={pt},pm2gnm1"
    else:
        map_request = f"http://static-maps.yandex.ru/1.x/?ll={','.join(toponym_coordinates.split())}&spn={','.join(zoom.split())}&l=sat"
    response = requests.get(map_request)
    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)
    with open(map_file, "wb") as file:
        file.write(response.content)


def get_gb(toponym_coordinates, zoom, map_file, *pt):
    if pt:
        pt = ",".join(coords_of_city.split())
        map_request = f"http://static-maps.yandex.ru/1.x/?ll={','.join(toponym_coordinates.split())}&spn={','.join(zoom.split())}&l=sat,skl&pt={pt},pm2gnm1"
    else:
        map_request = f"http://static-maps.yandex.ru/1.x/?ll={','.join(toponym_coordinates.split())}&spn={','.join(zoom.split())}&l=sat,skl"
    response = requests.get(map_request)
    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)
    with open(map_file, "wb") as file:
        file.write(response.content)


def get_coords_for_city(city):
    geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={city}&format=json"
    response = requests.get(geocoder_request)
    if response:
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
        toponym_coodrinates = toponym["Point"]["pos"]
    else:
        toponym_coodrinates = ""
        print("Ошибка выполнения запроса:")
        print(geocoder_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
    return toponym_coodrinates


width, height = 600, 450
get_map(coords, scale, map_file)
get_sat(coords, scale, map_file1)
get_gb(coords, scale, map_file2)
pygame.init()
screen = pygame.display.set_mode((width, height))
slides = [pygame.image.load(map_file), pygame.image.load(map_file1), pygame.image.load(map_file2)]
running = True
i = 0
count = 0
active = False

color = (0, 0, 0)
font = pygame.font.Font(None, 20)
input_box = pygame.Rect(0, 0, 140, height // 4)
text = ""
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if input_box.collidepoint(event.pos):
                active = not active
            else:
                active = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            i += 1
            i = (i + 1) % 3 - 1
        if event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_RETURN:
                    coords_of_city = get_coords_for_city(str(text))
                    text = ''
                    get_map(coords_of_city, "0.5 0.5", map_file, coords_of_city)
                    get_sat(coords_of_city, "0.5 0.5", map_file1, coords_of_city)
                    get_gb(coords_of_city, "0.5 0.5", map_file2, coords_of_city)
                    slides = [pygame.image.load(map_file), pygame.image.load(map_file1), pygame.image.load(map_file2)]
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
    txt_surface = font.render(text, True, color)
    slide = slides[i]
    screen.blit(slide, (0, 0))
    pygame.draw.rect(screen, (255, 255, 255), input_box)
    screen.blit(font.render("Объект для поиска: ", True, (120, 120, 120)), (input_box.x + 5, input_box.y + 5))
    screen.blit(txt_surface, (input_box.x + 5, input_box.y + 20))
    pygame.display.flip()
pygame.quit()
os.remove(map_file)
