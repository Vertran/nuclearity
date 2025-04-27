import pygame
import pygame.draw
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import math

pygame.init()
screen = pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL)
pygame.mouse.set_visible(False)
pygame.event.set_grab(True)

# ==== Настройка OpenGL ====
glEnable(GL_DEPTH_TEST)
glMatrixMode(GL_PROJECTION)
gluPerspective(75, 800 / 600, 0.1, 100.0)
glMatrixMode(GL_MODELVIEW)

# ==== Камера ====
cam_pos = np.array([0.0, 1.0, 5.0], dtype=float)
cam_yaw, cam_pitch = 0.0, 0.0
cam_vel_y = 0.0
on_ground = True
gravity = -9.8

# ==== Интерфейс-поверхность ====
ui_surface = pygame.Surface((256, 256))
font = pygame.font.SysFont("Arial", 24)
button_rect = pygame.Rect(78, 100, 100, 50)

def render_ui():
    ui_surface.fill((30, 30, 30))
    pygame.draw.rect(ui_surface, (200, 0, 0), button_rect)
    text = font.render("Click Me!", True, (255, 255, 255))
    ui_surface.blit(text, (button_rect.x + 10, button_rect.y + 10))

def surface_to_texture(surf):
    raw = pygame.image.tostring(surf, "RGBA", True)
    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, surf.get_width(), surf.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, raw)
    return tex_id

# ==== Интерфейс-плоскость ====
def draw_ui_plane(texture_id):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex3f(-1, 1.5, -2)
    glTexCoord2f(1, 0); glVertex3f(1, 1.5, -2)
    glTexCoord2f(1, 1); glVertex3f(1, -0.5, -2)
    glTexCoord2f(0, 1); glVertex3f(-1, -0.5, -2)
    glEnd()
    glDisable(GL_TEXTURE_2D)

# ==== Перемещение и взгляд ====
def update_camera():
    glLoadIdentity()
    dir = np.array([
        math.cos(math.radians(cam_pitch)) * math.sin(math.radians(cam_yaw)),
        math.sin(math.radians(cam_pitch)),
        math.cos(math.radians(cam_pitch)) * math.cos(math.radians(cam_yaw))
    ])
    center = cam_pos + dir
    gluLookAt(*cam_pos, *center, 0, 1, 0)

# ==== Обработка клика ====
def get_mouse_ray():
    x, y = pygame.mouse.get_pos()
    x = (2.0 * x) / 800 - 1.0
    y = 1.0 - (2.0 * y) / 600
    z = -1.0
    inv_proj = np.linalg.inv(np.array(glGetDoublev(GL_PROJECTION_MATRIX)))
    inv_view = np.linalg.inv(np.array(glGetDoublev(GL_MODELVIEW_MATRIX)))
    ray_clip = np.array([x, y, z, 1.0])
    ray_eye = inv_proj @ ray_clip
    ray_eye = np.array([ray_eye[0], ray_eye[1], -1.0, 0.0])
    ray_world = inv_view @ ray_eye
    ray_world = ray_world[:3]
    ray_world /= np.linalg.norm(ray_world)
    return cam_pos.copy(), ray_world

def ray_ui_intersect(ray_origin, ray_dir):
    plane_z = -2
    t = (plane_z - ray_origin[2]) / ray_dir[2]
    if t < 0: return None
    hit = ray_origin + ray_dir * t
    x, y = hit[0], hit[1]
    if -1 <= x <= 1 and -0.5 <= y <= 1.5:
        u = (x + 1) / 2 * ui_surface.get_width()
        v = (1.5 - y) / 2 * ui_surface.get_height()
        return int(u), int(v)
    return None

# ==== Основной цикл ====
clock = pygame.time.Clock()
while True:
    dt = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            exit()
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            origin, direction = get_mouse_ray()
            result = ray_ui_intersect(origin, direction)
            if result:
                mx, my = result
                if button_rect.collidepoint(mx, my):
                    print("Кнопка нажата!")

    # Мышь
    mx, my = pygame.mouse.get_rel()
    cam_yaw -= mx * 0.1
    cam_pitch -= my * 0.1
    cam_pitch = max(-89, min(89, cam_pitch))

    # Движение
    keys = pygame.key.get_pressed()
    speed = 5 * dt
    dir = np.array([
        math.cos(math.radians(cam_pitch)) * math.sin(math.radians(cam_yaw)),
        0,
        math.cos(math.radians(cam_pitch)) * math.cos(math.radians(cam_yaw))
    ])
    dir /= np.linalg.norm(dir)
    right = np.cross(dir, [0, 1, 0])
    right /= np.linalg.norm(right)

    if keys[K_w]: cam_pos += dir * speed
    if keys[K_s]: cam_pos -= dir * speed
    if keys[K_a]: cam_pos -= right * speed
    if keys[K_d]: cam_pos += right * speed

    # Прыжок
    if keys[K_SPACE] and on_ground:
        cam_vel_y = 5.5
        on_ground = False

    cam_vel_y += gravity * dt
    cam_pos[1] += cam_vel_y * dt
    if cam_pos[1] < 1.0:
        cam_pos[1] = 1.0
        cam_vel_y = 0
        on_ground = True

    # Интерфейс → текстура
    render_ui()
    ui_tex = surface_to_texture(ui_surface)


    # Рендер
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    update_camera()
    draw_ui_plane(ui_tex)
    glDeleteTextures(1, [ui_tex])
    pygame.display.flip()
