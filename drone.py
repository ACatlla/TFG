# -*- encoding: utf-8 -*-

import data
import checksum

"""
Mòdul Drone
===========

Implementació de la classe Drone. Ofereix les accions que podem aplicar-li.
"""


class Drone:

	def __init__(self):
		"""
		Inicialitza la comunicació. Inicialitza tots els pàrametres de control
		com a desactivats.
		"""
		data.init()
		self.ctrl = 0

	def __del__(self):
		"""
		Tanca la comunicació.
		"""
		data.close()

	def set_control(self, pitch=False, roll=False, yaw=False, thrust=False, height=True, gps=True):
		"""
		Permet definir quin són els paràmetres de comandament que estan activats.
		"""
		ctrl = 0
		if pitch:
			ctrl |= 0b00000001
		if roll:
			ctrl |= 0b00000010
		if yaw:
			ctrl |= 0b00000100
		if thrust:
			ctrl |= 0b00001000
		if height:
			ctrl |= 0b00010000
		if gps:
			ctrl |= 0b00100000
		self.ctrl = ctrl

	def estat(self):
		"""
		Consulta l'estat dels motors.
		Retorna True si els motors estan encesos i False si estan apagats.

		:rtype: bool
		"""
		# Consulta per comprovar si esta ences
		estructura_consulta = {'codi': 0x01}
		tx_data_consulta = {'tipus': 'p', 'estructura': estructura_consulta}
		data.tx_data(tx_data_consulta)

		encen = True
		rx_data_consulta = data.rx_data()
		if (rx_data_consulta['tipus'] == 'LL_STATUS') and (rx_data_consulta['estructura']['motors_on'] == 0x00):
			encen = False
		return encen

	def encen(self):
		"""
		Encén els motors.
		Retorna True si s'han encès els motors i False si no s'han encès.

		:rtype: bool
		"""
		estructura_encen = {'state': 1}
		tx_data_encen = {'tipus': 'm', 'estructura': estructura_encen}
		data.tx_data(tx_data_encen)
		return self.estat()

	def apaga(self):
		"""
		Apaga els motors del Drone.
		Retorna True si s'han apagat els motors i False si no s'han apagat.

		:rtype: bool
		"""
		estructura_apaga = {'state': 0}
		tx_data_apaga = {'tipus': 'm', 'estructura': estructura_apaga}
		data.tx_data(tx_data_apaga)
		return not self.estat()

	def comanda(self, pitch=0, roll=0, yaw=0, thrust=0):
		"""
		Envia una comanda de control al Drone.
		Retorna True si s'ha pogut enviar la comanda i False en cas contrari.

		:rtype: bool
		"""
		check = checksum.checksum([pitch, roll, yaw, thrust, self.ctrl])
		estructura = {'pitch': pitch, 'roll': roll, 'yaw': yaw, 'thrust': thrust, 'ctrl': self.ctrl, 'checksum': check}
		tx_data = {'tipus': 'di', 'estructura': estructura}
		data.tx_data(tx_data)
		rx_data = data.rx_data()
		return rx_data == 'OK'

	def consulta(self, codi):
		"""
		Envia una comanda de consulta al Drone.
		Retorna un diccionari amb el resultat de les dades consultades.
		Si no hi ha dades, retorna un diccionari buit.

		:rtype: dict
		"""
		estructura = {'codi': codi}
		tx_data = {'tipus': 'p', 'estructura': estructura}
		data.tx_data(tx_data)
		return data.rx_data()
