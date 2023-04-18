import sys
import pygame
import pygame_gui
import numpy as np
from scipy.integrate import odeint
from button import Button

pygame.init()
display = (1920, 1080)
screen = pygame.display.set_mode(display, pygame.FULLSCREEN)

Gr = 6.67 * 10**-11
m1, m2, m3 = 10**10, 10**10, 10**10

# Colours
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)


# Make a class for the 3 bodies and initialize the objects inside the window in a preset coordinate
class Body:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x-10, self.y-10, 20, 20)
        self.color = color
        self.drag = False

Circle1 = Body(400,300,red)
Circle2 = Body(800,200,green)
Circle3 = Body(1050,600,blue)

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

# Font
def get_font(size):
    return pygame.font.SysFont(None, size)

# Play
def play():
    start_button = Button(image=None, pos=(100,790), text_input="START", font=get_font(50), 
                          base_color="#d7fcd4", hovering_color="white")


    # Crear un objeto UIManager para administrar los widgets de la interfaz de usuario
    ui_manager = pygame_gui.UIManager((1920, 1080))

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
    i = None
    # Variable para detectar si se está arrastrando el rectángulo
    while True:
        screen.fill("black")

        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_TEXT_ENTRY_CHANGED:
                    # Actualizar las coordenadas de la esfera con los valores de los campos de texto
                    # Posición inicial cuerpo rojo
                    if pos_x1_input.get_text().isdigit():
                        Circle1.x = float(pos_x1_input.get_text())
                        Circle1.rect.x = float(pos_x1_input.get_text())
                    elif len(pos_x1_input.get_text()) > 1:
                        if pos_x1_input.get_text()[0] == "-" and pos_x1_input.get_text()[1:].isdigit():
                            Circle1.x = float(pos_x1_input.get_text())
                            Circle1.rect.x = float(pos_x1_input.get_text())
                    elif pos_x1_input.get_text() == "":
                        Circle1.x = 0.0
                        Circle1.rect.x = 0.0
                    if pos_y1_input.get_text().isdigit():
                        Circle1.y = float(pos_y1_input.get_text())
                        Circle1.rect.y = float(pos_y1_input.get_text())
                    elif len(pos_y1_input.get_text()) > 1:
                        if pos_y1_input.get_text()[0] == "-" and pos_y1_input.get_text()[1:].isdigit():
                            Circle1.y = float(pos_y1_input.get_text())
                            Circle1.rect.y = float(pos_y1_input.get_text())
                    elif pos_y1_input.get_text() == "":
                        Circle1.y = 0.0
                        Circle1.rect.y = 0.0

                    # Posición inicial cuerpo verde
                    if pos_x2_input.get_text().isdigit():
                        Circle2.x = float(pos_x2_input.get_text())
                        Circle2.rect.x = float(pos_x2_input.get_text())
                    elif len(pos_x2_input.get_text()) > 1:
                        if pos_x2_input.get_text()[0] == "-" and pos_x2_input.get_text()[1:].isdigit():
                            Circle2.x = float(pos_x2_input.get_text())
                            Circle2.rect.x = float(pos_x2_input.get_text())
                    elif pos_x2_input.get_text() == "":
                        Circle2.x = 0.0
                        Circle2.rect.x = 0.0
                    if pos_y2_input.get_text().isdigit():
                        Circle2.y = float(pos_y2_input.get_text())
                        Circle2.rect.y = float(pos_y2_input.get_text())
                    elif len(pos_y2_input.get_text()) > 1:
                        if pos_y2_input.get_text()[0] == "-" and pos_y2_input.get_text()[1:].isdigit():
                            Circle2.y = float(pos_y2_input.get_text())
                            Circle2.rect.y = float(pos_y2_input.get_text())
                    elif pos_y2_input.get_text() == "":
                        Circle2.y = 0.0
                        Circle2.rect.y = 0.0

                    # Posición inicial cuerpo azul
                    if pos_x3_input.get_text().isdigit():
                        Circle3.x = float(pos_x3_input.get_text())
                        Circle3.rect.x = float(pos_x3_input.get_text())
                    elif len(pos_x3_input.get_text()) > 1:
                        if pos_x3_input.get_text()[0] == "-" and pos_x3_input.get_text()[1:].isdigit():
                            Circle3.x = float(pos_x3_input.get_text())
                            Circle3.rect.x = float(pos_x3_input.get_text())
                    elif pos_x3_input.get_text() == "":
                        Circle3.x = 0.0
                        Circle3.rect.x = 0.0
                    if pos_y3_input.get_text().isdigit():
                        Circle3.y = float(pos_y3_input.get_text())
                        Circle3.rect.y = float(pos_y3_input.get_text())
                    elif len(pos_y3_input.get_text()) > 1:
                        if pos_y3_input.get_text()[0] == "-" and pos_y3_input.get_text()[1:].isdigit():
                            Circle3.y = float(pos_y3_input.get_text())
                            Circle3.rect.y = float(pos_y3_input.get_text())
                    elif pos_y3_input.get_text() == "":
                        Circle3.y = 0.0
                        Circle3.rect.y = 0.0

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.checkForInput(mouse_pos) and not isinstance(i, int):
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
            start_button.changeColor(mouse_pos)
            start_button.update(screen)

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

            pygame.draw.circle(screen,red,(Circle1.x,Circle1.y),10)
            pygame.draw.circle(screen,green,(Circle2.x,Circle2.y),10)
            pygame.draw.circle(screen,blue,(Circle3.x,Circle3.y),10)
            
        # Actualizar el GUI
        ui_manager.update(pygame.time.get_ticks())
        
        pygame.display.update()
        pygame.time.wait(10)

# Options
def options():
    return

# Main menu
def main_menu():
    play_button = Button(image=None, pos=(960, 390), text_input="PLAY", font=get_font(50), 
                         base_color="#d7fcd4", hovering_color="White")
    options_button = Button(image=None, pos=(960, 540), text_input="OPTIONS", font=get_font(50), 
                         base_color="#d7fcd4", hovering_color="White")
    exit_button = Button(image=None, pos=(960, 690), text_input="EXIT", font=get_font(50), 
                         base_color="#d7fcd4", hovering_color="White")

    while True:
        screen.fill(black)

        mouse_pos = pygame.mouse.get_pos()

        for button in [play_button, options_button, exit_button]:
            button.changeColor(mouse_pos)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.checkForInput(mouse_pos):
                    play()
                if options_button.checkForInput(mouse_pos):
                    options()
                if exit_button.checkForInput(mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


if __name__ == "__main__":
    main_menu()
