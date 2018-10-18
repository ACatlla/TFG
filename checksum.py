# -*- encoding: utf-8 -*-

"""
Mòdul checksum
==============

Aquest mòdul implementa la comprovació i generació de checksum.
"""


def checksum(llista_dades):
    """
    Calcula el checksum corresponent dels elements d'una llista de
    dades.

    :param list llista_dades: Llista de dades a calcular checksum
    :rtype: int valor de checksum corresponent

    >>> hex(checksum([]))
    '0xaaaa'
    >>> hex(checksum([0]))
    '0xaaaa'
    >>> hex(checksum([1]))
    '0xaaab'
    """
    checksum = 0xAAAA
    for dada in llista_dades:
        checksum += dada
        checksum &= 0xffff
    return checksum


def check_checksum(llista_dades, checksum):
    """
    Comprova si el checksum és correcte. Retorna True si aquest és
    correcte o retorna False en cas contrari.

    :param list llista_dades: Llista de dades a verificar el checksum
    :param int checksum: Checksum a verificar
    :rtype: bool

    >>> check_checksum([0], '0xaaaa')
    True
    >>> checksum([1], '0xaaab')
    True
    >>> checksum([1], '0xaaaa')
    False
    """
    return checksum(llista_dades) == checksum
