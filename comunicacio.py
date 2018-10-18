# -*- encoding: utf-8 -*-

import serial
import crc16


"""
Mòdul comunicació
=================

S'encarrega de la gestió de mes baix nivell del protocol de comunicació.
"""


# Comprovacions ------------------------------------------------------

def check_start_end(frame):
    """
    Verifica que la trama contingui la inicialització i finalització
    de trama definides al protocol.
    Retorna True si la trama conté la inicialització i finalització
    correcte i False en cas contrari.

    :param str frame: Cadena de caràcters que forma una trama
    :rtype: bool
    """
    frame_init = frame.find(">*>")
    frame_end = frame.find("<#<")
    if frame_init != -1 and frame_end != -1:
        return True
    else:
        return False


def check_len(frame):
    """
    Verifica que el camp de llargada de paquet que conté la trama
    correspongui amb la llargada real del paquet.
    Retorna True si la llargada del paquet coincideix amb el valor
    del camp llargada i False en cas contrari.

    :param str frame: Cadena de caràcters corresponent a una trama
    :rtype: bool
    """

    frame_len_data = ord(frame[3])+ord(frame[4])
    frame_data = frame[6:-5]
    if frame_len_data == len(frame_data):
        return True
    else:
        return False


def check_frame(frame):
    """
    Verifica que la llargada del paquet de la trama sigui correcte i
    que el format de la trama sigui l'adequat.
    Retorna True si es compleix que la llargada de la trama és
    correcte i alhora el frmat de la trama també ho és.
    En cas de que alguna de les dues comprovacions sigui errònia
    retorna False.

    :param str frame: Cadena de caràcters corresponent a una trama
    :rtype: bool
    """
    crc = ord(frame[-5])+ord(frame[-4])
    return check_start_end(frame) and check_len(frame) and crc16.check_crc16(frame, crc)


# Frame API Functions ------------------------------------------------

def init():
    """
    Inicialitza la comunicació. Retorna True si s'ha pogut inicialitzar
    la comunicació i False en cas contrari.

    :rtype: bool

    """
    global ser
    try:
        ser = serial.Serial('/dev/ttyUSB0', 57600, timeout=0.5)
    except:
        return False
    else:
        return True


def close():
    """
    Tenca la comunicació.
    """
    global ser
    ser.close()


# New -----------------------------------------------------

def tx_paquet(tx_paquet):
    """
    Permet la funcionalitat d'enviament d'un paquet.
    Afegeix els camps necessaris per convertir el paquet en
    trama i envia la trama.

    :param str tx_paquet:
    """
    global ser
    frame = ">*>{tx_paquet}<#<".format(tx_paquet=tx_paquet)
    ser.write(frame)


def rx_paquet():
    """
    Permet la funcionalitat de recepció d'un paquet o una
    confirmació.
    Espera a llegir una trama o confirmació i verifica que
    aquesta no sigui corrupte.
    Si la trama és vàlida extreu el paquet que conté. Pot
    retornar un paquet, un OK si és una confirmació o un str
    buit si la trama és corrupte.

    :rtype: str
    """
    global ser
    frame = ""

    while True:
        caracter = ser.read()
        frame += caracter
        if caracter == '':
            return ''
        elif frame[-3:] == "<#<":
            if check_frame(frame):
                frame_init = frame.find('>*>')
                frame_end = frame.find('<#<')
                # Te en compte frame_init(3B) + frame_len_data(2B) = (5B) i frame_crc(2B)
                rx_paquet = frame[frame_init+5:frame_end-2]
                return rx_paquet
            else:
                return ''
        elif frame[-5:] == ">a\x17a<":
            return 'OK'
