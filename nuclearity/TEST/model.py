import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from pywavefront import Wavefront

# Initialize GLFW
if not glfw.init():
    raise Exception("GLFW could not be initialized!")

# Create a windowed mode window and its OpenGL context
window = glfw.create_window(800, 600, "Render Model", None, None)
if not window:
    glfw.terminate()
    raise Exception("GLFW window could not be created!")

# Make the window's context current
glfw.make_context_current(window)

# Load the model and material
model = Wavefront('TEST\\model.obj', create_materials=True, collect_faces=True)


glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluPerspective(45, 800/600, 0.1, 100)
glMatrixMode(GL_MODELVIEW)


# Main render loop
while not glfw.window_should_close(window):
    # Clear the screen
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)




    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 5, 20,  # камера позади и чуть сверху
          0, 0, 0,   # смотрим в центр сцены
          0, 1, 0)   # вверх по Y



    glPushMatrix()
    glScalef(0.1, 0.1, 0.1)
    glRotatef(glfw.get_time() * 50, 0, 1, 0)  # Rotate the model over time

    print(model.vertices[:10])  # Посмотри, где реально точки
    

    # Пробуем использовать структуру mesh.faces для доступа к вершинам
    for mesh in model.meshes.values():  # Используем mesh_dict, а не mesh_list
        glBegin(GL_TRIANGLES)
        for face in mesh.faces:
            for vertex_i in face:
                # Получаем координаты вершин из индексов
                vertex = model.vertices[vertex_i]
                material = mesh.material
                glColor3f(*material.diffuse[:3])  # Use the diffuse color of the material
                glVertex3f(*vertex)

    glEnd()

    glPopMatrix()

    # Swap front and back buffers
    glfw.swap_buffers(window)

    # Poll for and process events
    glfw.poll_events()

# Clean up and terminate GLFW
glfw.terminate()