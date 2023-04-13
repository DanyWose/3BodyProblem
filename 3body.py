import pygame
import pygame_gui
import numpy as np
from scipy.integrate import odeint

Gr = 6.67 * 10**-11
m1, m2, m3 = 10**10, 10**10, 10**10

# Make a class for the 3 bodies and initialize the objects inside the window in a preset coordinate
class Body:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x-10, self.y-10, 20, 20)
        self.color = color
        self.drag = False

Circle1 = Body(550,600,(255,0,0))
Circle2 = Body(800,200,(0,255,0))
Circle3 = Body(1050,600,(0,0,255))

# Calculates the distance between two points and the vector going from point 1 to point 2
def dist(x1,y1,x2,y2):
    vec_x = np.array([x1,y1])
    vec_y = np.array([x2,y2])
    vec = vec_y - vec_x
    r_xy = np.sqrt(np.dot(vec,vec))

    return r_xy, vec

# Creates the data for solving the ODEs basend on the motion equations
def deriv(z, t, m1, m2, m3, G):
    x1, y1, vx1, vy1, x2, y2, vx2, vy2, x3, y3, vx3, vy3 = z
    d12 = dist(x1,y1,x2,y2)
    d13 = dist(x1,y1,x3,y3)
    d23 = dist(x2,y2,x3,y3)

    x1dot = vx1
    a1x = G*(m2/(d12[0]**2)*d12[1][0]+m3/(d13[0]**2)*d13[1][0])
    y1dot = vy1
    a1y = G*(m2/(d12[0]**2)*d12[1][1]+m3/(d13[0]**2)*d13[1][1])
    x2dot = vx2
    a2x = G*(m1/(d12[0]**2)*-(d12[1][0])+m3/(d23[0]**2)*d23[1][0])
    y2dot = vy2
    a2y = G*(m1/(d12[0]**2)*(-d12[1][1])+m3/(d23[0]**2)*d23[1][1])
    x3dot = vx3
    a3x = G*(m1/(d13[0]**2)*(-d13[1][0])+m2/(d23[0]**2)*(-d23[1][0]))
    y3dot = vy3
    a3y = G*(m1/(d13[0]**2)*(-d13[1][1])+m2/(d23[0]**2)*(-d23[1][1]))
    
    return x1dot,y1dot,a1x,a1y,x2dot,y2dot,a2x,a2y,x3dot,y3dot,a3x,a3y

# Calculates the simulation
def simulate(x_1,y_1,x_2,y_2,x_3,y_3):
    z0 = np.array([x_1,y_1,0,0,x_2,y_2,0,0,x_3,y_3,0,0])
    t = np.linspace(0,10000,3000)
    z = odeint(deriv, z0, t, args = (m1, m2, m3, Gr))
    return z

pygame.init()
display = (1600, 900)
screen = pygame.display.set_mode(display)

# Crear un objeto UIManager para administrar los widgets de la interfaz de usuario
ui_manager = pygame_gui.UIManager((1600, 900))

# Crear un widget de campo de texto
# Crear campos de texto interactivos
pos_x1_input = pygame_gui.elements  .UITextEntryLine(relative_rect=pygame.Rect((10, 60), (60, 30)),
                                       manager=ui_manager)
pos_x1_input.set_text(str(Circle1.x))
pos_y1_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((10, 90), (60, 30)),
                                       manager=ui_manager)
pos_y1_input.set_text(str(Circle1.y))
pos_x2_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((10, 120), (60, 30)),
                                       manager=ui_manager)
pos_x2_input.set_text(str(Circle2.x))
pos_y2_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((10, 150), (60, 30)),
                                       manager=ui_manager)
pos_y2_input.set_text(str(Circle2.y))
pos_x3_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((10, 180), (60, 30)),
                                       manager=ui_manager)
pos_x3_input.set_text(str(Circle3.x))
pos_y3_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((10, 210), (60, 30)),
                                       manager=ui_manager)
pos_y3_input.set_text(str(Circle3.y))

StartButton = pygame.Rect(10,500,300,300)

i = None
# Variable para detectar si se está arrastrando el rectángulo
while True:
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if StartButton.collidepoint(pygame.mouse.get_pos()) and not isinstance(i, int):
                i = 0
            if not str(i).isdigit():
                if Circle1.rect.collidepoint(event.pos):
                    Circle1.drag = True
                    i = "idk"
            if not str(i).isdigit():
                if Circle2.rect.collidepoint(event.pos):
                    Circle2.drag = True
                    i = "idk"
            if not str(i).isdigit():
                if Circle3.rect.collidepoint(event.pos):
                    Circle3.drag = True
                    i = "idk"
        elif event.type == pygame.MOUSEBUTTONUP:
            # Cuando se suelta el botón del ratón, deja de arrastrar el rectángulo
                if Circle1.drag == True:
                    Circle1.drag = False
                if Circle2.drag == True:
                    Circle2.drag = False
                if Circle3.drag == True:
                    Circle3.drag = False
        
                    
        # Actualizar el GUI
        ui_manager.process_events(event)
    
    # Renderizar el GUI encima de la ventana de Pygame
    ui_manager.draw_ui(screen)

    # Dibujar cuerpos
    if isinstance(i, int):
        # Creo la simulación a partir de los datos iniciales
        if i == 0:
            z = simulate(Circle1.x,Circle1.y,Circle2.x,Circle2.y,Circle3.x,Circle3.y)
            x1, y1 = z[:,0], z[:,1]
            x2, y2 = z[:,4], z[:,5]
            x3, y3 = z[:,8], z[:,9]
            i += 1
        elif i > 0:
            pygame.draw.circle(screen,(255,0,0),(x1[i],y1[i]),10)
            pygame.draw.circle(screen,(0,255,0),(x2[i],y2[i]),10)
            pygame.draw.circle(screen,(0,0,255),(x3[i],y3[i]),10)
            i += 1       
    else:
        pygame.draw.rect(screen, (255, 255, 255), StartButton)

        if Circle1.drag:
                Circle1.rect.x, Circle1.rect.y = np.array(pygame.mouse.get_pos()) - 10
                Circle1.x, Circle1.y = pygame.mouse.get_pos()
                pos_x1_input.set_text(str(int(pygame.mouse.get_pos()[0])))
                pos_y1_input.set_text(str(int(pygame.mouse.get_pos()[1])))

        if Circle2.drag:
                Circle2.rect.x, Circle2.rect.y = np.array(pygame.mouse.get_pos()) - 10
                Circle2.x, Circle2.y = pygame.mouse.get_pos()
                pos_x2_input.set_text(str(int(pygame.mouse.get_pos()[0])))
                pos_y2_input.set_text(str(int(pygame.mouse.get_pos()[1])))

        if Circle3.drag:
                Circle3.rect.x, Circle3.rect.y = np.array(pygame.mouse.get_pos()) - 10
                Circle3.x, Circle3.y = pygame.mouse.get_pos()
                pos_x3_input.set_text(str(int(pygame.mouse.get_pos()[0])))
                pos_y3_input.set_text(str(int(pygame.mouse.get_pos()[1])))

        # Allows you to drag only one body
        if Circle3.rect.colliderect(Circle2.rect) and Circle3.drag:
            Circle2.drag = False

        if Circle3.rect.colliderect(Circle1.rect) and Circle3.drag:
            Circle1.drag = False

        if Circle2.rect.colliderect(Circle1.rect) and Circle2.drag:
            Circle1.drag = False

        pygame.draw.circle(screen,(255,0,0),(Circle1.x,Circle1.y),10)
        pygame.draw.circle(screen,(0,255,0),(Circle2.x,Circle2.y),10)
        pygame.draw.circle(screen,(0,0,255),(Circle3.x,Circle3.y),10)
        
    

    # Actualizar el GUI
    ui_manager.update(pygame.time.get_ticks())

    
    pygame.display.flip()
    pygame.time.wait(10)


