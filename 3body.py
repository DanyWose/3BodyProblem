import pygame
import pygame_gui
import numpy as np
from scipy.integrate import odeint

Gr = 6.67 * 10**-11
m1, m2, m3 = 10**10, 10**10, 10**10

def dist(x1,y1,x2,y2):
    vec_x = np.array([x1,y1])
    vec_y = np.array([x2,y2])
    vec = vec_y - vec_x
    r_xy = np.sqrt(np.dot(vec,vec))

    return r_xy, vec

def deriv(z, t, m1, m2, m3, G):
    x1, y1, vx1, vy1, x2, y2, vx2, vy2, x3, y3, vx3, vy3 = z
    d12 = dist(x1,y1,x2,y2)
    d13 = dist(x1,y1,x3,y3)
    d21 = dist(x2,y2,x1,y1)
    d23 = dist(x2,y2,x3,y3)
    d31 = dist(x3,y3,x1,y1)
    d32 = dist(x3,y3,x2,y2)

    x1dot = vx1
    a1x = G*(m2/(d12[0]**2)*d12[1][0]+m3/(d13[0]**2)*d13[1][0])
    y1dot = vy1
    a1y = G*(m2/(d12[0]**2)*d12[1][1]+m3/(d13[0]**2)*d13[1][1])
    x2dot = vx2
    a2x = G*(m1/(d21[0]**2)*d21[1][0]+m3/(d23[0]**2)*d23[1][0])
    y2dot = vy2
    a2y = G*(m1/(d21[0]**2)*d21[1][1]+m3/(d23[0]**2)*d23[1][1])
    x3dot = vx3
    a3x = G*(m1/(d31[0]**2)*d31[1][0]+m2/(d32[0]**2)*d32[1][0])
    y3dot = vy3
    a3y = G*(m1/(d31[0]**2)*d31[1][1]+m2/(d32[0]**2)*d32[1][1])
    
    return x1dot,y1dot,a1x,a1y,x2dot,y2dot,a2x,a2y,x3dot,y3dot,a3x,a3y

t = np.linspace(0, 10000, 3000)

pygame.init()
display = (1600, 900)
screen = pygame.display.set_mode(display)

# Crear un objeto UIManager para administrar los widgets de la interfaz de usuario
ui_manager = pygame_gui.UIManager((1600, 900))

# Crear un widget de campo de texto
# Crear campos de texto interactivos
pos_x1_input = pygame_gui.elements  .UITextEntryLine(relative_rect=pygame.Rect((10, 60), (60, 30)),
                                       manager=ui_manager)
pos_y1_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((10, 90), (60, 30)),
                                       manager=ui_manager)
pos_x2_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((10, 120), (60, 30)),
                                       manager=ui_manager)
pos_y2_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((10, 150), (60, 30)),
                                       manager=ui_manager)
pos_x3_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((10, 180), (60, 30)),
                                       manager=ui_manager)
pos_y3_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((10, 210), (60, 30)),
                                       manager=ui_manager)

StartButton = pygame.Rect(10,500,300,300)


draw1 = [False,False]
draw2 = [False,False]
draw3 = [False,False]
dragging1 = False
dragging2 = False
dragging3 = False
i = None
# Variable para detectar si se está arrastrando el rectángulo
while True:
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_TEXT_ENTRY_CHANGED:
                # Actualizar las coordenadas de la esfera con los valores de los campos de texto
                # Posición inicial cuerpo rojo
                if pos_x1_input.get_text().isdigit():
                    x_1 = float(pos_x1_input.get_text())
                    draw1[0] = True
                elif len(pos_x1_input.get_text()) > 1:
                    if pos_x1_input.get_text()[0] == "-" and pos_x1_input.get_text()[1:].isdigit():
                        x_1 = float(pos_x1_input.get_text())
                        draw1[0] = True
                elif pos_x1_input.get_text() == "":
                    x_1 = 0.0
                    draw1[0] = True
                if pos_y1_input.get_text().isdigit():
                    y_1 = float(pos_y1_input.get_text())
                    draw1[1] = True
                elif len(pos_y1_input.get_text()) > 1:
                    if pos_y1_input.get_text()[0] == "-" and pos_y1_input.get_text()[1:].isdigit():
                        y_1 = float(pos_y1_input.get_text())
                        draw1[1] = True
                elif pos_y1_input.get_text() == "":
                    y_1 = 0.0
                    draw1[1] = True

                # Posición inicial cuerpo verde
                if pos_x2_input.get_text().isdigit():
                    x_2 = float(pos_x2_input.get_text())
                    draw2[0] = True
                elif len(pos_x2_input.get_text()) > 1:
                    if pos_x2_input.get_text()[0] == "-" and pos_x2_input.get_text()[1:].isdigit():
                        x_2 = float(pos_x2_input.get_text())
                        draw2[0] = True
                elif pos_x2_input.get_text() == "":
                    x_2 = 0.0
                    draw2[0] = True
                if pos_y2_input.get_text().isdigit():
                    y_2 = float(pos_y2_input.get_text())
                    draw2[1] = True
                elif len(pos_y2_input.get_text()) > 1:
                    if pos_y2_input.get_text()[0] == "-" and pos_y2_input.get_text()[1:].isdigit():
                        y_2 = float(pos_y2_input.get_text())
                        draw2[1] = True
                elif pos_y2_input.get_text() == "":
                    y_2 = 0.0
                    draw2[1] = True

                # Posición inicial cuerpo azul
                if pos_x3_input.get_text().isdigit():
                    x_3 = float(pos_x3_input.get_text())
                    draw3[0] = True
                elif len(pos_x3_input.get_text()) > 1:
                    if pos_x3_input.get_text()[0] == "-" and pos_x3_input.get_text()[1:].isdigit():
                        x_3 = float(pos_x3_input.get_text())
                        draw3[0] = True
                elif pos_x3_input.get_text() == "":
                    x_3 = 0.0
                    draw3[0] = True
                if pos_y3_input.get_text().isdigit():
                    y_3 = float(pos_y3_input.get_text())
                    draw3[1] = True
                elif len(pos_y3_input.get_text()) > 1:
                    if pos_y3_input.get_text()[0] == "-" and pos_y3_input.get_text()[1:].isdigit():
                        y_3 = float(pos_y3_input.get_text())
                        draw3[1] = True
                elif pos_y3_input.get_text() == "":
                    y_3 = 0.0
                    draw3[1] = True

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if StartButton.collidepoint(pygame.mouse.get_pos()) and draw1 == [True,True] and draw2 == [True,True] and draw3 == [True,True] and not isinstance(i, int):
                i = 0
            if draw1 == [True,True] and not str(i).isdigit():
                if Circle1.collidepoint(event.pos):
                    dragging1 = True
                    i = "chupala"
            if draw2 == [True,True] and not str(i).isdigit():
                if Circle2.collidepoint(event.pos):
                    dragging2 = True
                    i = "chupala"
            if draw3 == [True,True] and not str(i).isdigit():
                if Circle3.collidepoint(event.pos):
                    dragging3 = True
                    i = "chupala"
        elif event.type == pygame.MOUSEBUTTONUP:
            # Cuando se suelta el botón del ratón, deja de arrastrar el rectángulo
                if dragging1 == True:
                    dragging1 = False
                if dragging2 == True:
                    dragging2 = False
                if dragging3 == True:
                    dragging3 = False
        
                    
        # Actualizar el GUI
        ui_manager.process_events(event)
    
    # Renderizar el GUI encima de la ventana de Pygame
    ui_manager.draw_ui(screen)

    # Condiciones iniciales
    if draw1 == [True,True] and not isinstance(i,int):
        pygame.draw.circle(screen,(255,0,0),(x_1,y_1),10)
        Circle1 = pygame.Rect(x_1-5,y_1-5,10,10)
    if draw2 == [True,True] and not isinstance(i,int):
        pygame.draw.circle(screen,(0,255,0),(x_2,y_2),10)
        Circle2 = pygame.Rect(x_2-5,y_2-5,10,10)
    if draw3 == [True,True] and not isinstance(i,int):
        pygame.draw.circle(screen,(0,0,255),(x_3,y_3),10)
        Circle3 = pygame.Rect(x_3-5,y_3-5,10,10)

    # Dibujar cuerpos
    if isinstance(i, int):
        # Creo la simulación a partir de los datos iniciales
        if i == 0:
            z0 = np.array([x_1,y_1,0,0,x_2,y_2,0,0,x_3,y_3,0,0])
            t = np.linspace(0,100000,30000)
            z = odeint(deriv, z0, t, args = (m1, m2, m3, Gr))
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
        if dragging1:
                Circle1.x, Circle1.y = pygame.mouse.get_pos()
                x_1, y_1 = int(pygame.mouse.get_pos()[0]), int(pygame.mouse.get_pos()[1])
                pos_x1_input.set_text(str(int(pygame.mouse.get_pos()[0])))
                pos_y1_input.set_text(str(int(pygame.mouse.get_pos()[1])))
        if dragging2:
                Circle2.x, Circle2.y = pygame.mouse.get_pos()
                x_2, y_2 = int(pygame.mouse.get_pos()[0]), int(pygame.mouse.get_pos()[1])
                pos_x2_input.set_text(str(int(pygame.mouse.get_pos()[0])))
                pos_y2_input.set_text(str(int(pygame.mouse.get_pos()[1])))
        if dragging3:
                Circle3.x, Circle3.y = pygame.mouse.get_pos()
                x_3, y_3 = int(pygame.mouse.get_pos()[0]), int(pygame.mouse.get_pos()[1])
                pos_x3_input.set_text(str(int(pygame.mouse.get_pos()[0])))
                pos_y3_input.set_text(str(int(pygame.mouse.get_pos()[1])))
    
    # Actualizar el GUI
    ui_manager.update(pygame.time.get_ticks()/100)

    
    pygame.display.flip()
    pygame.time.wait(10)


