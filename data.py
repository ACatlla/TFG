# -*- encoding: utf-8 -*-

import estructures
import comunicacio

"""
Mòdul data
==========

S'encarrega de la traducció de paquets a dades i de dades a paquets.

"""


# Conversió de dades

def data2int(v, len_tipus_param):
    """
    Conversor entre valors i representació hexadecimal del valor en un
    string. Si li passem un valor ens retorna el la seva representació
    hexadecimal en un string que te en compte la llargada del
    tipus de dada.

    :param int v: Valor que volem convertir
    :param int len_v_type: Llargada del tipus de dada
    :rtype: str corresponent a la conversió de valor

    >>> data2int(-1, 2) == '\xff\xff'
    True
    >>> data2int(-1, 4) == '\xff\xff\xff\xff'
    True
    >>> data2int(0xa0, 1) == '\xa0'
    True
    """
    str_value = ""
    for i in range(len_tipus_param):
        mascara = 0xff << (8*i)
        byte_value = (v & mascara) >> (8*i)
        str_value += chr(byte_value)
    return str_value


def str2int_unsigned(str_valor_param, len_tipus_param):
    """
    Conversor entre cadenes de caràcters i enters. Prenent cada caràcter com un
    byte. La cadena de caràcters representa un enter sense signe.

    :param int str_valor_param: Cadena de caràcters que codifica un enter sense signe
    :param int len_tipus_param: Llargada del tipus de paràmetre
    :rtype: int

    >>> str2int_unsigned('\xff',1)
    255
    >>> str2int_unsigned('\xff\xff',2)
    65535
    >>> str2int_unsigned('\xaa',1)
    170
    """
    acomulador = 0
    byte_index = range(len_tipus_param)
    byte_index.reverse()
    for i in byte_index:
        acomulador += ord(str_valor_param[i]) << (8 * i)
    return acomulador


def str2int_signed(str_valor_param, len_tipus_param):
    """
    Conversor entre cadenes de caràcters i enters. Prenent cada caràcter com un
    byte. La cadena de caràcters representa un enter amb signe.

    :param int str_valor_param: Cadena de caràcters que codifica un enter amb signe
    :param int len_tipus_param: Llargada del tipus de paràmetre
    :rtype: int

    >>> str2int_signed('\xff',1)
    -1
    >>> str2int_signed('\xff\xff',1)
    -1
    >>> str2int_signed('\xaa',1)
    -86
    """
    signed_mask = 0x80 << (8 * (len_tipus_param - 1))
    unsigned_mask = signed_mask - 1

    unsigned = str2int_unsigned(str_valor_param, len_tipus_param)

    return (unsigned & unsigned_mask) - (unsigned & signed_mask)


# Empaquetar/Desempaquetar

def dades2paquet(tx_data):
    """
    Passem un diccionari que conte 'tipus' i 'estructura'. La clau
    'tipus' te associat el tipus de paquet que es i la clau
    'estructura' te associat un diccionari que conte el nom dels
    paràmetres com a clau i el valor dels paràmetres com a valor.

    :param dict tx_data: Diccionari que conte l'identificador del tipus de paquet i l'estructura de les dades
    :rtype: str paquet corresponent a les dades de l'estructura

    >>> dades2paquet({'tipus': 'di', 'estructura': {'pitch': 0x1234, 'roll': 0x5678, 'yaw': 0x1234, 'thrust': 4321, 'ctrl': 0xB1B2, 'checksum': 0xAAAA}}) == 'di\x34\x12\x78\x56\x34\x12\x21\x43\xb1\xb2\xaa\xaa'
    True
    >>> dades2paquet({'tipus': '','estructura': ''})

    """
    paquet = ""
    tipus = tx_data['tipus']
    estructura = tx_data['estructura']
    for i in range(len(estructures.tx_structure[tipus][0])):
        nom_param = estructures.tx_structure[tipus][0][i]
        tipus_param = estructures.tx_structure[tipus][1][i]

        valor_param = estructura[nom_param]

        len_tipus_param = estructures.type_values[tipus_param]

        str_valor_param = data2int(valor_param, len_tipus_param)
        paquet += str_valor_param
    return tipus+paquet


def paquet2dades(rx_paquet):
    """
    Li passem un paquet i retorna l'identificador del paquet i un
    diccionari amb les dades extretes del paquet.

    :param dict tx_data: Diccionari que conte l'identificador del tipus de paquet i l'estructura de les dades
    :rtype: str paquet corresponent a les dades de l'estructura

    >>> paquet2dades('Ahsask')
    {'estructura': {}, 'tipus': 'No struct'}
    >>> paquet2dades('\x01\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff')
    {'estructura': {'temp_ADC': 4294967295, 'temp_gyro': 65535, 'acc_z': -1, 'pressure': -1, 'gyro_z': -1, 'gyro_x': -1, 'gyro_y': -1, 'acc_x': -1, 'mag_y': -1, 'mag_x': -1, 'acc_y': -1, 'mag_z': -1}, 'tipus': 'IMU_RAWDATA'}
    """
    codi_tipus = ord(rx_paquet[0])
    dades = rx_paquet[1:]

    if codi_tipus in estructures.descriptor2structure.keys():
        tipus = estructures.descriptor2structure[codi_tipus]

        estructura = {}
        for i in range(len(estructures.rx_structure[tipus][0])):
            nom_param = estructures.rx_structure[tipus][0][i]
            tipus_param = estructures.rx_structure[tipus][1][i]

            len_tipus_param = estructures.type_values[tipus_param]

            str_valor_param = dades[:len_tipus_param]
            dades = dades[len_tipus_param:]

            if 'u' in tipus_param:
                valor_param = str2int_unsigned(str_valor_param, len_tipus_param)
            else:
                valor_param = str2int_signed(str_valor_param, len_tipus_param)

            estructura[nom_param] = valor_param

        return {'tipus': tipus, 'estructura': estructura}
    else:
        return {'tipus': 'No struct', 'estructura': {}}


# Tx/Rx

def tx_data(tx_data):
    """
    Empaqueta les dades i les envia

    :param dict tx_data: Diccionari que conte l'identificador del tipus de paquet i l'estructura de les dades
    """
    tx_paquet = dades2paquet(tx_data)
    comunicacio.tx_paquet(tx_paquet)


def rx_data():
    """
    Demana un paquet el transforma en dades i el retorna
    Retorna un diccionari amb l'identificador del paquet i l'estructura de
    dades rebuda

    :rtype: dict
    """
    rx_paquet = comunicacio.rx_paquet()
    if rx_paquet:
        return paquet2dades(rx_paquet)
    else:
        return {}


def init():
    """
    Inicia el canal de comunicació
    Retorna True si s'ha pogut iniciar el canal de comunicació amb èxit

    :rtype: bool
    """
    return comunicacio.init()


def close():
    """
    Tenca el canal de comunicació
    """
    comunicacio.close()


if __name__ == "__main__":
    import doctest
    doctest.testmod()
