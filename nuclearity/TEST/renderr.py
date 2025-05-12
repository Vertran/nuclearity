import glfw
from OpenGL.GL import *
import numpy as np
import pyrr
import os

# ========== Загрузка модели ==========
def load_obj(filename):
    vertices = []
    normals = []
    texcoords = []
    faces = []

    material = None
    materials = {}

    dirname = "c:\\Games\\nuclearity\\nuclearity\\TEST\\" # Путь к папке
    mtlfile = None

    with open(dirname + filename, "r") as f:
        for line in f:
            if line.startswith('mtllib'):
                mtlfile = os.path.join(dirname, line.split()[1])
            elif line.startswith('v '):
                vertices.append(list(map(float, line.strip().split()[1:])))
            elif line.startswith('vn '):
                normals.append(list(map(float, line.strip().split()[1:])))
            elif line.startswith('vt '):
                texcoords.append(list(map(float, line.strip().split()[1:])))
            elif line.startswith('usemtl'):
                material = line.strip().split()[1]
            elif line.startswith('f '):
                face = []
                for vertex in line.strip().split()[1:]:
                    values = vertex.split('/')
                    vert_idx = int(values[0]) - 1
                    tex_idx = int(values[1]) - 1 if len(values) > 1 and values[1] else 0
                    norm_idx = int(values[2]) - 1 if len(values) > 2 and values[2] else 0
                    face.append((vert_idx, tex_idx, norm_idx))
                faces.append((face, material))

    if mtlfile:
        materials = load_mtl(mtlfile)

    return vertices, texcoords, normals, faces, materials

def load_mtl(filename):
    materials = {}
    current = None

    with open(filename, "r") as f:
        for line in f:
            if line.startswith('newmtl'):
                current = line.strip().split()[1]
                materials[current] = {}
            elif current:
                if line.startswith('Kd'):
                    materials[current]['Kd'] = list(map(float, line.strip().split()[1:]))
    return materials

# ========== Инициализация окна ==========
if not glfw.init():
    raise Exception("glfw can not be initialized!")

window = glfw.create_window(800, 600, "OBJ Viewer", None, None)

if not window:
    glfw.terminate()
    raise Exception("glfw window can not be created!")

glfw.make_context_current(window)
glEnable(GL_DEPTH_TEST)

# ========== Загрузка данных ==========
vertices, texcoords, normals, faces, materials = load_obj("model.obj")

# Собираем данные
vertex_data = []

for face, material in faces:
    for vert_idx, tex_idx, norm_idx in face:
        vertex_data.extend(vertices[vert_idx])
        if normals:
            vertex_data.extend(normals[norm_idx])
        else:
            vertex_data.extend([0.0, 0.0, 1.0])

vertex_data = np.array(vertex_data, dtype=np.float32)

# ========== Создание VBO ==========
vao = glGenVertexArrays(1)
vbo = glGenBuffers(1)

glBindVertexArray(vao)
glBindBuffer(GL_ARRAY_BUFFER, vbo)
glBufferData(GL_ARRAY_BUFFER, vertex_data.nbytes, vertex_data, GL_STATIC_DRAW)

# Позиция
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * vertex_data.itemsize, ctypes.c_void_p(0))
glEnableVertexAttribArray(0)
# Нормаль
glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * vertex_data.itemsize, ctypes.c_void_p(3 * vertex_data.itemsize))
glEnableVertexAttribArray(1)

# ========== Шейдеры ==========
vertex_src = """
# version 330
layout(location = 0) in vec3 a_position;
layout(location = 1) in vec3 a_normal;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

out vec3 frag_pos;
out vec3 frag_normal;

void main()
{
    frag_pos = vec3(model * vec4(a_position, 1.0));
    frag_normal = mat3(transpose(inverse(model))) * a_normal;
    gl_Position = projection * view * vec4(frag_pos, 1.0);
}

"""

fragment_src = """
# version 330
in vec3 frag_pos;
in vec3 frag_normal;

out vec4 out_color;

uniform vec3 material_color;
uniform vec3 light_pos;
uniform vec3 view_pos;

void main()
{
    // Нормаль
    vec3 norm = normalize(frag_normal);

    // Вектор света
    vec3 light_dir = normalize(light_pos - frag_pos);

    // Диффузное освещение
    float diff = max(dot(norm, light_dir), 0.0);

    // Амбиентное освещение (фонарик в темноте)
    float ambient = 0.2;

    // Финальный цвет
    vec3 result = (ambient + diff) * material_color;
    out_color = vec4(result, 1.0);
}

"""

def compile_shader(source, shader_type):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)
    if glGetShaderiv(shader, GL_COMPILE_STATUS) != GL_TRUE:
        raise RuntimeError(glGetShaderInfoLog(shader))
    return shader

shader_program = glCreateProgram()
vertex_shader = compile_shader(vertex_src, GL_VERTEX_SHADER)
fragment_shader = compile_shader(fragment_src, GL_FRAGMENT_SHADER)


glAttachShader(shader_program, vertex_shader)
glAttachShader(shader_program, fragment_shader)
glLinkProgram(shader_program)

# ========== Матрицы ==========
model = pyrr.matrix44.create_identity(dtype=np.float32)
view = pyrr.matrix44.create_from_translation(pyrr.Vector3([0.0, 0.0, -8.0]), dtype=np.float32)
projection = pyrr.matrix44.create_perspective_projection(45.0, 800/600, 0.1, 100.0, dtype=np.float32)

glUseProgram(shader_program)
model_loc = glGetUniformLocation(shader_program, "model")
view_loc = glGetUniformLocation(shader_program, "view")
proj_loc = glGetUniformLocation(shader_program, "projection")
material_color_loc = glGetUniformLocation(shader_program, "material_color")

glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)
glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)


light_pos_loc = glGetUniformLocation(shader_program, "light_pos")
view_pos_loc = glGetUniformLocation(shader_program, "view_pos")

# ========== Цикл отрисовки ==========
while not glfw.window_should_close(window):
    glfw.poll_events()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0.2, 0.2, 0.2, 1.0)
    glUseProgram(shader_program)

    time = glfw.get_time()
    radius = 40

    camX = np.sin(time) * radius
    camZ = np.cos(time) * radius
    cam_pos = pyrr.Vector3([camX, 5.0, camZ])

    view = pyrr.matrix44.create_look_at(
        eye=cam_pos,
        target=pyrr.Vector3([0.0, 0.0, 0.0]),
        up=pyrr.Vector3([0.0, 1.0, 0.0]),
        dtype=np.float32
    )

    glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)

    # Положение света (можешь сделать его статичным или крутить вокруг объекта)
    glUniform3fv(light_pos_loc, 1, np.array([10.0, 10.0, 10.0], dtype=np.float32))
    # Положение камеры (для расчёта отражений, пока используется в будущем)
    glUniform3fv(view_pos_loc, 1, cam_pos)


    glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)

    # Получаем активный материал
    active_material_name = faces[0][1]
    material = materials.get(active_material_name, {})
    diffuse_color = material.get('Kd', [1.0, 1.0, 1.0])

    glUniform3fv(material_color_loc, 1, diffuse_color)

    glBindVertexArray(vao)
    glDrawArrays(GL_TRIANGLES, 0, len(vertex_data) // 6)

    glfw.swap_buffers(window)

glfw.terminate()
