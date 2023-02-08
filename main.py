import requests
import sys
import pygame
import os

x, y = map(float, input("Введите координаты через пробел: ").split())
while not (-90 < x < 90 and -180 < y < 180):
    print("Неверные данные ")
    x, y = map(float, input("Введите координаты через пробел: ").split())
coords = f"{y} {x}"
print()
scale = list(map(float, input("Введите параметры масштаба через пробел: ").split()))
while not (0 < scale[0] < 70 and 0 < scale[1] < 70):
    print("Неверные данные ")
    scale = list(map(float, input("Введите параметры масштаба через пробел: ").split()))
scale = f"{scale[0]} {scale[1]}"
map_file = "map.png"
map_file1 = "map1.png"
map_file2 = "map2.png"
adress_of_a_place = ""
index = ""


def get_map(toponym_coordinates, zoom, map_file, *pt):
    if pt:
        pt = ",".join(pt[0].split())
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
        pt = ",".join(pt[0].split())
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
        pt = ",".join(pt[0].split())
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


def get_full_adress(coords):
    global adress_of_a_place, tech_adress
    top = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={','.join(coords.split())}&format=json"
    response = requests.get(top).json()
    toponym = response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
    tech_adress = toponym_address
    q = len(toponym_address)
    s = ""
    idx = 0
    idx1 = 39
    while q > 40:
        q -= 40
        s += toponym_address[idx:idx1] + "\n"
        idx += 40
        idx1 += 40
    s += toponym_address[idx:idx1]
    adress_of_a_place = s


def get_index():
    global index
    r = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={tech_adress}&format=json"
    response = requests.get(r).json()
    top = response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    try:
        toponym_address = \
            top['metaDataProperty']['GeocoderMetaData']['AddressDetails']['Country']['AdministrativeArea']['Locality'][
                'Thoroughfare']['Premise']['PostalCode']['PostalCodeNumber']
        index = toponym_address
    except KeyError:
        index = ""


width, height = 600, 450
get_map(coords, scale, map_file)
get_sat(coords, scale, map_file1)
get_gb(coords, scale, map_file2)
get_full_adress(coords)
get_index()
pygame.init()
screen = pygame.display.set_mode((width, height))
slides = [pygame.image.load(map_file), pygame.image.load(map_file1), pygame.image.load(map_file2)]
running = True
i = 0
zoom = scale
count = 0
active = False

color = (0, 0, 0)
font = pygame.font.Font(None, 20)
input_box = pygame.Rect(0, 0, 300, height // 3)
btn_clear = pygame.Rect(0, 35, 80, 40)
btn_index = pygame.Rect(100, 35, 170, 40)
text = ""
txt = text
full_adress = ""
prev_adress = ""
q = coords
show_index = False
innput_box =  pygame.Rect(0, 0, 35, height // 3)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if innput_box.collidepoint(event.pos):
                active = True
                text = ""
            else:
                active = False

            if btn_clear.collidepoint(event.pos):
                text = txt
                coords = q
                full_adress = prev_adress
                get_map(coords, "0.5 0.5", map_file, coords)
                get_sat(coords, "0.5 0.5", map_file1, coords)
                get_gb(coords, "0.5 0.5", map_file2, coords)
                get_full_adress(coords)
                get_index()
                slides = [pygame.image.load(map_file), pygame.image.load(map_file1), pygame.image.load(map_file2)]
            if btn_index.collidepoint(event.pos):
                show_index = not show_index
            else:
                show_index = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            i += 1
            i = (i + 1) % 3 - 1
        if event.type == pygame.KEYDOWN and event.key == pygame.K_PAGEDOWN:
            zoom = zoom.split()
            if float(zoom[0]) >= 0 and float(zoom[0]) <= 70 and float(zoom[1]) >= 0 and float(zoom[1]) <= 70:
                zoom = f'{float(zoom[0]) + 1} {float(zoom[1]) + 1}'
            else:
                zoom = f'{float(zoom[0])} {float(zoom[1])}'
            if i == 0:
                os.remove(map_file)
                get_map(coords, zoom, map_file)
            elif i == 1:
                os.remove(map_file1)
                get_sat(coords, zoom, map_file1)
            elif i == -1:
                os.remove(map_file2)
                get_gb(coords, zoom, map_file2)
            slides = [pygame.image.load(map_file), pygame.image.load(map_file1), pygame.image.load(map_file2)]
        if event.type == pygame.KEYDOWN and event.key == pygame.K_PAGEUP:
            zoom = zoom.split()
            if float(zoom[0]) > 0 and float(zoom[1]) > 0:
                zoom = f'{float(zoom[0]) - 1} {float(zoom[1]) - 1}'
            else:
                zoom = f'{float(zoom[0])} {float(zoom[1])}'
            if i == 0:
                os.remove(map_file)
                get_map(coords, zoom, map_file)
            elif i == 1:
                os.remove(map_file1)
                get_sat(coords, zoom, map_file1)
            elif i == -1:
                os.remove(map_file2)
                get_gb(coords, zoom, map_file2)
            slides = [pygame.image.load(map_file), pygame.image.load(map_file1), pygame.image.load(map_file2)]
        if event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_RETURN:
                    txt = text
                    q = coords
                    coords = get_coords_for_city(str(text))
                    adress_prev = full_adress
                    get_map(coords, "0.5 0.5", map_file, coords)
                    get_sat(coords, "0.5 0.5", map_file1, coords)
                    get_gb(coords, "0.5 0.5", map_file2, coords)
                    get_full_adress(coords)
                    get_index()
                    prev_adress = full_adress
                    full_adress = adress_of_a_place
                    slides = [pygame.image.load(map_file), pygame.image.load(map_file1), pygame.image.load(map_file2)]
                    active = False
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
    txt_surface = font.render(text, True, color)
    slide = slides[i]
    screen.blit(slide, (0, 0))
    pygame.draw.rect(screen, (255, 255, 255), input_box)
    pygame.draw.rect(screen, (255, 0, 0), btn_clear)
    pygame.draw.rect(screen, (0, 255, 0), btn_index)
    screen.blit(font.render("Очистить", True, (0)), (btn_clear.x + 5, btn_clear.y + 5))
    screen.blit(font.render("Показывать индекс", True, (0)), (btn_index.x + 5, btn_index.y + 5))
    screen.blit(font.render("Объект для поиска: ", True, (120, 120, 120)), (input_box.x + 5, input_box.y + 5))
    lines = full_adress.splitlines()
    if show_index:
        lines += ["Почтовый индекс:"] + [index]
    for m, l in enumerate(lines):
        screen.blit(font.render(l, True, (120, 120, 120)), (btn_clear.x + 5, btn_clear.y + 40 + 20 * m))
    screen.blit(txt_surface, (input_box.x + 5, input_box.y + 20))
    pygame.display.flip()
pygame.quit()
