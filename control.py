# -*- encoding: utf-8 -*-

import drone
import time
import Leap
import sys

"""
Mòdul control
=============

Mòdul que implementa l'objecte Control que és l'encarregat de controlar i
fusionar les dades d'entrada del Leap Motion amb les dades de control del UAV
"""


class Control(Leap.Listener, drone.Drone):

    def __init__(self):
        """
        Inicialitza les variables d'estat de l'objecte
        """
        Leap.Listener.__init__(self)
        drone.Drone.__init__(self)
        self.ultim_enviament = time.time()
        self.state = 0
        self.set_control(
            pitch=True,
            roll=True,
            yaw=False,
            thrust=True,
            height=True,
            gps=True)

    # Tractament

    def normalitza(self, pitch=0, roll=0, yaw=0, thrust=0):
        """
        Normalització dels rangs del Leap motion als rangs de control del UAV
        Retorna una tupla de (pitch, roll, yaw, thrust) amb els rangs adequats

        :param int pitch: Valor de pitch en el rang del Leap Motion
        :param int roll: Valor de roll en el rang del Leap Motion
        :param int yaw: Valor de yaw en el rang del Leap Motion
        :param int thrust: Valor de thrust en el rang del Leap Motion
        :rtype: tupla
        """
        if pitch > 1:
            pitch = 1
        elif pitch < -1:
            pitch = -1

        if roll > 1:
            roll = 1
        elif roll < -1:
            roll = -1

        if yaw > 1:
            yaw = 1
        elif yaw < -1:
            yaw = -1

        # Regió 100 - 300cm
        thrust = (thrust - 100.0)/200.0
        if thrust > 1:
            thrust = 1
        elif thrust < -1:
            thrust = -1

        ponderacio = 0.5

        pitch = int(pitch * 2047.0 * ponderacio)
        if pitch > 2047:
            pitch = 2047
        elif pitch < -2047:
            pitch = -2047

        roll = int(roll * -2047.0 * ponderacio)
        if roll > 2047:
            roll = 2047
        elif roll < -2047:
            roll = -2047

        yaw = int(yaw * 2047.0 * ponderacio)
        if yaw > 2047:
            yaw = 2047
        elif yaw < -2047:
            yaw = -2047

        thrust = int(thrust * 4094)
        if thrust > 2047 + int(2047 * ponderacio):
            thrust = 2047 + int(2047 * ponderacio)
        elif thrust < 0:
            thrust = 0

        return (pitch, roll, yaw, thrust)

#    d ef filtre_control(pitch, roll, yaw, thrust):
#        return (pitch, roll, yaw, thrust)

    # Events

    def on_init(self, controller):
        """
        Callback associat a la inicialització del controlador de Leap Motion
        """
        print "Initialized"

    def on_connect(self, controller):
        """
        Callback associat a la connexió del Leap Motion
        """
        print "Connected"

    def on_disconnect(self, controller):
        """
        Callback associat a la desconnexió del Leap Motion
        """
        print "Disconnected"

    def on_exit(self, controller):
        """
        Callback associat a la sortida del controlador de Leap Motion
        """
        print "Exited"

    def on_frame(self, controller):
        """
        Callback associat a la recepció d'una trama del Leap Motion
        S'encarrega de gestionar la comunicació entre les dades rebudes del
        Leap Motion i les dades de control del UAV.
        Implementa la màquina d'estats que s'encarrega de la gestió del UAV.
        """
        frame = controller.frame()

        if not frame.hands.is_empty:
            # Get the first hand
            hand = frame.hands[0]

            pitch, roll, yaw, thrust = self.normalitza(
                hand.direction.pitch,
                hand.palm_normal.roll,
                hand.direction.yaw,
                hand.palm_position.y)

            if len(hand.fingers) == 0 and self.state == 1:
                print "Apaga ----------------------------------------"
                self.state = 0
                self.apaga()

            elif len(hand.fingers) == 5 and self.state == 0:
                print "Encen ----------------------------------------"
                self.state = 1
                self.encen()

            elif self.state == 1:
                ara = time.time()
                if ara - self.ultim_enviament > 0.075:
                    self.ultim_enviament = ara

                    if len(hand.fingers) == 1:
#                        pitch, roll, yaw, thrust = self.filtre_control(pitch, roll, yaw, thrust)
                        print "Mode control"
                    else:
                        print "Mode lliure"

                    self.comanda(pitch=pitch, roll=roll, yaw=yaw, thrust=thrust)

                    print 'Pitch: ', pitch
                    print 'Roll: ', roll
                    print 'Yaw: ', yaw
                    print 'Thrust: ', thrust
                    print '-----------------------'


def main():
    """
    Funció principal del programa de control.
    Inicialitza els diferents mòduls i permet una iniciar la lectura de dades
    del Leap Motion i transmissió de control del UAV
    Un cop iniciada es manté encesa fins que és premi la tecla enter per sortir
    dl programa.
    """
    # Create a sample listener and controller
    listener = Control()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    sys.stdin.readline()

    # Remove the sample listener when done
    controller.remove_listener(listener)


if __name__ == "__main__":
    main()
