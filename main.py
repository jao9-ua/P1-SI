import pygame
import tkinter
from tkinter import *
from tkinter.simpledialog import *
from tkinter import messagebox as MessageBox
from tablero import *
from dominio import *
from pygame.locals import *

GREY=(190, 190, 190)
NEGRO=(100,100, 100)
BLANCO=(255, 255, 255)

MARGEN=5 #ancho del borde entre celdas
MARGEN_INFERIOR=60 #altura del margen inferior entre la cuadrícula y la ventana
TAM=60  #tamaño de la celda
FILS=5 # número de filas del crucigrama
COLS=6 # número de columnas del crucigrama

LLENA='*' 
VACIA='-'

#########################################################################
# Detecta si se pulsa el botón de FC
######################################################################### 
def pulsaBotonFC(pos, anchoVentana, altoVentana):
    if pos[0]>=anchoVentana//4-25 and pos[0]<=anchoVentana//4+25 and pos[1]>=altoVentana-45 and pos[1]<=altoVentana-19:
        return True
    else:
        return False
    
######################################################################### 
# Detecta si se pulsa el botón de AC3
######################################################################### 
def pulsaBotonAC3(pos, anchoVentana, altoVentana):
    if pos[0]>=3*(anchoVentana//4)-25 and pos[0]<=3*(anchoVentana//4)+25 and pos[1]>=altoVentana-45 and pos[1]<=altoVentana-19:
        return True
    else:
        return False
    
######################################################################### 
# Detecta si se pulsa el botón de reset
######################################################################### 
def pulsaBotonReset(pos, anchoVentana, altoVentana):
    if pos[0]>=(anchoVentana//2)-25 and pos[0]<=(anchoVentana//2)+25 and pos[1]>=altoVentana-45 and pos[1]<=altoVentana-19:
        return True
    else:
        return False
    
######################################################################### 
# Detecta si el ratón se pulsa en la cuadrícula
######################################################################### 
def inTablero(pos):
    if pos[0]>=MARGEN and pos[0]<=(TAM+MARGEN)*COLS+MARGEN and pos[1]>=MARGEN and pos[1]<=(TAM+MARGEN)*FILS+MARGEN:        
        return True
    else:
        return False
    
######################################################################### 
# Busca posición de palabras de longitud tam en el almacen
######################################################################### 
def busca(almacen, tam):
    enc=False
    pos=-1
    i=0
    while i<len(almacen) and enc==False:
        if almacen[i].tam==tam: 
            pos=i
            enc=True
        i=i+1
    return pos
    
######################################################################### 
# Crea un almacen de palabras
######################################################################### 
def creaAlmacen():
    f= open('d0.txt', 'r', encoding="utf-8")
    lista=f.read()
    f.close()
    listaPal=lista.split()
    almacen=[]
   
    for pal in listaPal:        
        pos=busca(almacen, len(pal)) 
        if pos==-1: #no existen palabras de esa longitud
            dom=Dominio(len(pal))
            dom.addPal(pal.upper())            
            almacen.append(dom)
        elif pal.upper() not in almacen[pos].lista: #añade la palabra si no está duplicada        
            almacen[pos].addPal(pal.upper())           
    
    return almacen

######################################################################### 
# Imprime el contenido del almacen
######################################################################### 
def imprimeAlmacen(almacen):
    for dom in almacen:
        print (dom.tam)
        lista=dom.getLista()
        for pal in lista:
            print (pal, end=" ")
        print()

class Variable:
    def __init__(self, nombre, fila, columna, longitud, orientacion):
        self.nombre = nombre
        self.fila = fila
        self.columna = columna
        self.longitud = longitud
        self.orientacion = orientacion
        self.dominio = []

    def setDominio(self, dominio):
        self.dominio = dominio

    def __str__(self):
        return f"Variable({self.nombre}, ({self.fila}, {self.columna}), {self.longitud}, {self.orientacion}, {self.dominio})"

def crearVariables(tablero):
    variables = []  # Lista para almacenar las variables
    fila_inicio = None
    columna_inicio = None
    tamano = None
    direccion = None

    for fila in range(tablero.getAlto()):
        for columna in range(tablero.getAncho()):
            celda = tablero.getCelda(fila, columna)
            if celda == VACIA:
                if columna == 0 or tablero.getCelda(fila, columna-1) == LLENA:
                    # Inicio de una nueva variable
                    fila_inicio = fila
                    columna_inicio = columna
                    tamano = 1
                    while columna + tamano < tablero.getAncho() and tablero.getCelda(fila, columna + tamano) == VACIA:
                        tamano += 1
                    direccion = 'horizontal'
                elif fila == 0 or tablero.getCelda(fila-1, columna) == LLENA:
                    fila_inicio = fila
                    columna_inicio = columna
                    tamano = 1
                    while fila + tamano < tablero.getAlto() and tablero.getCelda(fila + tamano, columna) == VACIA:
                        tamano += 1
                    direccion = 'vertical'
            elif celda == LLENA and tamano is not None:
                # Fin de la variable
                dominio = []  # Aquí deberás determinar qué palabras en el almacén tienen el tamaño correcto
                nueva_variable = Variable(fila_inicio, columna_inicio, tamano, dominio, direccion)
                variables.append(nueva_variable)
                tamano = None

    return variables

def identificarVariables(tablero, almacen):
    variables = []
    var_id = 0
    
    # Horizontal variables
    for fil in range(FILS):
        col = 0
        while col < COLS:
            # Comienza si la celda está vacía o contiene una letra
            if tablero.getCelda(fil, col) == VACIA or tablero.getCelda(fil, col).isalpha():
                start_col = col
                valid = True
                palabra = ""
                
                # Extiende hacia la derecha mientras las condiciones sean apropiadas
                while col < COLS and (tablero.getCelda(fil, col) == VACIA or tablero.getCelda(fil, col).isalpha()):
                    palabra += tablero.getCelda(fil, col) if tablero.getCelda(fil, col) != VACIA else ' '
                    col += 1
                
                # Verifica la longitud de la palabra y si es válida
                if col - start_col > 1:
                    var = Variable(f"V{var_id}", fil, start_col, col - start_col, 'H')
                    pos = busca(almacen, col - start_col)
                    if pos != -1:
                        # Filtra dominio para incluir solo palabras que coincidan con las letras introducidas
                        filtered_domain = [word for word in almacen[pos].getLista() if all((c == ' ' or c == word[i]) for i, c in enumerate(palabra) if i < len(word))]
                        if filtered_domain:
                            var.setDominio(filtered_domain)
                            variables.append(var)
                            var_id += 1
            col += 1
    
    # Vertical variables
    for col in range(COLS):
        fil = 0
        while fil < FILS:
            if tablero.getCelda(fil, col) == VACIA or tablero.getCelda(fil, col).isalpha():
                start_fil = fil
                valid = True
                palabra = ""
                
                # Extiende hacia abajo mientras las condiciones sean apropiadas
                while fil < FILS and (tablero.getCelda(fil, col) == VACIA or tablero.getCelda(fil, col).isalpha()):
                    palabra += tablero.getCelda(fil, col) if tablero.getCelda(fil, col) != VACIA else ' '
                    fil += 1
                
                # Verifica la longitud de la palabra y si es válida
                if fil - start_fil > 1:
                    var = Variable(f"V{var_id}", start_fil, col, fil - start_fil, 'V')
                    pos = busca(almacen, fil - start_fil)
                    if pos != -1:
                        # Filtra dominio para incluir solo palabras que coincidan con las letras introducidas
                        filtered_domain = [word for word in almacen[pos].getLista() if all((c == ' ' or c == word[i]) for i, c in enumerate(palabra) if i < len(word))]
                        if filtered_domain:
                            var.setDominio(filtered_domain)
                            variables.append(var)
                            var_id += 1
            fil += 1
    
    return variables


def forwardChecking(tablero, variables, almacen):
    if not variables:
        return True
    
    variable = variables[0]
    for palabra in variable.dominio:
        if consistent(tablero, variable, palabra, almacen):
            assign(tablero, variable, palabra)
            
            if forwardChecking(tablero, variables[1:], almacen):
                
                return True
            unassign(tablero, variable, palabra)
    return False

def consistent(tablero, variable, palabra, almacen):
    for i, char in enumerate(palabra):
        # Establecer las coordenadas basadas en la orientación de la palabra
        fil, col = (variable.fila + i, variable.columna) if variable.orientacion == 'V' else (variable.fila, variable.columna + i)

        # Verificar que la letra actual encaje en el tablero
        if tablero.getCelda(fil, col) not in [VACIA, char]:
            return False

        # Verificación de palabras horizontales y verticales para cada letra
        if not palabra_valida(tablero, fil, col, 'H', almacen):
            return False
        if not palabra_valida(tablero, fil, col, 'V', almacen):
            return False

    return True

def palabra_valida(tablero, fila, columna, orientacion, almacen):
    # Encuentra el inicio y el final de la palabra en la orientación especificada
    if orientacion == 'H':
        inicio = columna
        while inicio > 0 and tablero.getCelda(fila, inicio - 1) != LLENA:
            inicio -= 1
        final = columna
        while final < tablero.getAncho() - 1 and tablero.getCelda(fila, final + 1) != LLENA:
            final += 1
    else:
        inicio = fila
        while inicio > 0 and tablero.getCelda(inicio - 1, columna) != LLENA:
            inicio -= 1
        final = fila
        while final < tablero.getAlto() - 1 and tablero.getCelda(final + 1, columna) != LLENA:
            final += 1

    # Formar la palabra
    palabra = ''.join(tablero.getCelda(inicio + k, columna) if orientacion == 'V' else tablero.getCelda(fila, inicio + k) for k in range(final - inicio + 1))
    
    # Comprobar si la palabra formada es válida
    if '-' in palabra:  # Si hay celdas sin asignar en la palabra formada, ignorar
        return True
    return any(palabra == p for dom in almacen for p in dom.getLista() if dom.tam == len(palabra))


def assign(tablero, variable, palabra):
    for i, char in enumerate(palabra):
        
        if variable.orientacion == 'H':
            tablero.setCelda(variable.fila, variable.columna + i, char)
        else:
            tablero.setCelda(variable.fila + i, variable.columna, char)
    

def unassign(tablero, variable, palabra):
    for i, char in enumerate(palabra):
        if variable.orientacion == 'H':
            tablero.setCelda(variable.fila, variable.columna + i, VACIA)
        else:
            tablero.setCelda(variable.fila + i, variable.columna, VACIA)

def imprimirTablero(tablero):
    print("Estado final del tablero:")
    for fila in range(tablero.getAlto()):
        for col in range(tablero.getAncho()):
            print(tablero.getCelda(fila, col), end=" ")
        print()

def ac3(tablero, variables, almacen):
    print("DOMINIOS ANTES DEL AC3")
    for variable in variables:
        print(f"Nombre {variable.nombre} Posición {variable.fila} {variable.columna} Tipo: {variable.orientacion} Dominio: {variable.dominio}")
    
    # Inicializa la cola de arcos con todas las aristas del grafo de restricciones
    queue = [(vi, vj) for vi in variables for vj in variables if vi != vj and are_neighbors(vi, vj)]
    
    while queue:
        (vk, vm) = queue.pop(0)
        cambio = False
        if revise(tablero, vk, vm, almacen):
            if not vk.dominio:
                return False  # Si el dominio se queda vacío, no hay solución
            cambio = True
        if cambio:
            for vr in variables:
                if vr != vk and are_neighbors(vr, vk):
                    queue.append((vr, vk))
    
    print("\nDOMINIOS DESPUÉS DEL AC3")
    for variable in variables:
        print(f"Nombre {variable.nombre} Posición {variable.fila} {variable.columna} Tipo: {variable.orientacion} Dominio: {variable.dominio}")
    
    return True

def are_neighbors(vi, vj):
    # Determina si dos variables son vecinos (comparten al menos una celda)
    if vi.orientacion == 'H':
        cells_vi = [(vi.fila, vi.columna + i) for i in range(vi.longitud)]
    else:
        cells_vi = [(vi.fila + i, vi.columna) for i in range(vi.longitud)]
    
    if vj.orientacion == 'H':
        cells_vj = [(vj.fila, vj.columna + i) for i in range(vj.longitud)]
    else:
        cells_vj = [(vj.fila + i, vj.columna) for i in range(vj.longitud)]
    
    return bool(set(cells_vi) & set(cells_vj))

def revise(tablero, vi, vj, almacen):
    revised = False
    for x in vi.dominio[:]:
        if not any(is_arc_consistent(tablero, vi, x, vj, y, almacen) for y in vj.dominio):
            vi.dominio.remove(x)
            revised = True
    return revised

def is_arc_consistent(tablero, variable1, palabra1, variable2, palabra2, almacen):
    if variable1.orientacion == 'H':
        cells1 = [(variable1.fila, variable1.columna + i) for i in range(variable1.longitud)]
    else:
        cells1 = [(variable1.fila + i, variable1.columna) for i in range(variable1.longitud)]
    
    if variable2.orientacion == 'H':
        cells2 = [(variable2.fila, variable2.columna + i) for i in range(variable2.longitud)]
    else:
        cells2 = [(variable2.fila + i, variable2.columna) for i in range(variable2.longitud)]
    
    for (fil1, col1) in cells1:
        if (fil1, col1) in cells2:
            i = cells1.index((fil1, col1))
            j = cells2.index((fil1, col1))
            if palabra1[i] != palabra2[j]:
                return False
    
    return True

#########################################################################  
# Principal
#########################################################################
def main():
    root= tkinter.Tk() #para eliminar la ventana de Tkinter
    root.withdraw() #se cierra
    pygame.init()
    
    reloj=pygame.time.Clock()
    
    anchoVentana=COLS*(TAM+MARGEN)+MARGEN
    altoVentana= MARGEN_INFERIOR+FILS*(TAM+MARGEN)+MARGEN
    
    dimension=[anchoVentana,altoVentana]
    screen=pygame.display.set_mode(dimension) 
    pygame.display.set_caption("Practica 1: Crucigrama")
    
    botonFC=pygame.image.load("botonFC.png").convert()
    botonFC=pygame.transform.scale(botonFC,[50, 30])
    
    botonAC3=pygame.image.load("botonAC3.png").convert()
    botonAC3=pygame.transform.scale(botonAC3,[50, 30])
    
    botonReset=pygame.image.load("botonReset.png").convert()
    botonReset=pygame.image.load("botonReset.png").convert()
    botonReset=pygame.transform.scale(botonReset,[50,30])
    
    almacen=creaAlmacen()
    game_over=False
    tablero=Tablero(FILS, COLS)
    ac3_executed = False 
    
    while not game_over:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:               
                game_over=True
            if event.type==pygame.MOUSEBUTTONUP:                
                #obtener posición y calcular coordenadas matriciales                               
                pos=pygame.mouse.get_pos()                
                if pulsaBotonFC(pos, anchoVentana, altoVentana):
                    print("FC")
                    if not ac3_executed:
                        variables = identificarVariables(tablero, almacen)
                        print("No AC3")
                    res = forwardChecking(tablero, variables, almacen)
                    if not res:
                        MessageBox.showwarning("Alerta", "No hay solución")                                 
                elif pulsaBotonAC3(pos, anchoVentana, altoVentana):                    
                    print("AC3")
                    variables = identificarVariables(tablero, almacen)
                    if ac3(tablero, variables, almacen):
                        MessageBox.showinfo("AC3 Result", "AC3 completed successfully. Domains have been reduced.")
                        ac3_executed = True
                    else:
                        MessageBox.showwarning("AC3 Result", "No solution found.")
                elif pulsaBotonReset(pos, anchoVentana, altoVentana):                   
                    tablero.reset()
                elif inTablero(pos):
                    colDestino=pos[0]//(TAM+MARGEN)
                    filDestino=pos[1]//(TAM+MARGEN)                    
                    if event.button==1: #botón izquierdo
                        if tablero.getCelda(filDestino, colDestino)==VACIA:
                            tablero.setCelda(filDestino, colDestino, LLENA)
                        else:
                            tablero.setCelda(filDestino, colDestino, VACIA)
                    elif event.button==3: #botón derecho
                        c=askstring('Entrada', 'Introduce carácter')
                        tablero.setCelda(filDestino, colDestino, c.upper())   
            
        ##código de dibujo        
        #limpiar pantalla
        screen.fill(NEGRO)
        pygame.draw.rect(screen, GREY, [0, 0, COLS*(TAM+MARGEN)+MARGEN, altoVentana],0)
        for fil in range(tablero.getAlto()):
            for col in range(tablero.getAncho()):
                if tablero.getCelda(fil, col)==VACIA: 
                    pygame.draw.rect(screen, BLANCO, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)
                elif tablero.getCelda(fil, col)==LLENA: 
                    pygame.draw.rect(screen, NEGRO, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)
                else: #dibujar letra                    
                    pygame.draw.rect(screen, BLANCO, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)
                    fuente= pygame.font.Font(None, 70)
                    texto= fuente.render(tablero.getCelda(fil, col), True, NEGRO)            
                    screen.blit(texto, [(TAM+MARGEN)*col+MARGEN+15, (TAM+MARGEN)*fil+MARGEN+5])             
        #pintar botones        
        screen.blit(botonFC, [anchoVentana//4-25, altoVentana-45])
        screen.blit(botonAC3, [3*(anchoVentana//4)-25, altoVentana-45])
        screen.blit(botonReset, [anchoVentana//2-25, altoVentana-45])
        #actualizar pantalla
        pygame.display.flip()
        reloj.tick(40)
        if game_over==True: #retardo cuando se cierra la ventana
            pygame.time.wait(1000)
 
if __name__=="__main__":
    main()
 
