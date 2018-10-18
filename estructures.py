# -*- encoding: utf-8 -*-

"""
Mòdul estructures
=================

Mòdul en el que es defineixen les diferents estructures de recepció i
de transmissió utilitzades en el protocol sèrie.

Type values
-----------

Definició de la llargada dels diferents tipus de dades.

 :Char: 1 Byte
 :Unsigned Char: 1 Byte
 :Short: 2 Byte
 :Unsigned Short: 2 Byte
 :Integer: 4 Bytes
 :Unsigned Int: 4 Bytes


Rx descriptor
-------------

Diccionari on es defineix la relació entre el nom del tipus de paquet
a rebre i el codi que es rep. Aquest identificador es troba a
l'estructura enviada des del drone al computador. En aquest tipus de
paquets s'envia les dades de les variables de telemetria del drone.


Tx descriptor
-------------

Diccionari on es defineix la relació entre el nom del tipus de paquet
de telemetria que volem consultar i el bit al que correspon del byte
de petició que s'envia. Aquest codi el trobem en els missatges de
petició de paquets de telemetria que s'envien des del computador al
drone.


Rx structure
------------

Diccionari que conté la relació del tx_descriptor del paquet rebut i
l'estructura de dades segons el tipus de paquet. El valor d'aquest
diccionari és una tupla de dues llistes. La primera llista conté el
nom de les variables i la segona llista conté el tipus de variable que
és. Durant la definició d'aquestes estructures s'ha tingut en compte
l'ordre de les variables per tal de que concordin amb la posició del
valor de les variables a l'estructura del paquet rebut i de la mateixa
manera coincideixi el tipus de variable que s'utilitzarà per
determinar la llargada de la mateixa.


Tx structure
------------

És simètric a rx_structure. En aquest cas només és contempla una
estructura d'enviament de dades. El cas de les dades de control.


Descriptor to structure
-----------------------

Diccionari que defineix la relació entre el codi de rx_descriptor
rebut i el nom de tx_descriptor que s'ha fet la petició. S'utilitzà per
poder conèixer l'estructura associada ala paquets que rebem.

"""


# TYPE_VALUES --------------------------------------------------------

type_values = {}

type_values['c'] = 1
type_values['uc'] = 1
type_values['s'] = 2
type_values['us'] = 2
type_values['i'] = 4
type_values['ui'] = 4


# RX_DESCRIPTOR ------------------------------------------------------

rx_descriptor = {}

rx_descriptor[0x01] = "PD_IMURAWDATA"
rx_descriptor[0x02] = "PD_LLSTATUS"
rx_descriptor[0x03] = "PD_IMUCALCDATA"
rx_descriptor[0x04] = "PD_HLSTATUS"
rx_descriptor[0x05] = "PD_DEBUGDATA"
rx_descriptor[0x11] = "PD_CTRLOUT"
rx_descriptor[0x12] = "PD_FLIGHTPARAMS"
rx_descriptor[0x13] = "PD_CTRLCOMMANDS"
rx_descriptor[0x14] = "PD_CTRLINTERNAL"
rx_descriptor[0x15] = "PD_RCDATA"
rx_descriptor[0x16] = "PD_CTRLSTATUS"
rx_descriptor[0x17] = "PD_CTRLINPUT"
rx_descriptor[0x18] = "PD_CTRLFALCON"
rx_descriptor[0x20] = "PD_WAYPOINT"
rx_descriptor[0x21] = "PD_CURRENTWAY"
rx_descriptor[0x22] = "PD_NMEADATA"
rx_descriptor[0x23] = "PD_GPSDATA"
rx_descriptor[0x24] = "PD_SINGLEWAYPOINT"
rx_descriptor[0x25] = "PD_GOTOCOMMAND"
rx_descriptor[0x26] = "PD_LAUNCHCOMMAND"
rx_descriptor[0x27] = "PD_LANDCOMMAND"
rx_descriptor[0x28] = "PD_HOMECOMMAND"
rx_descriptor[0x29] = "PD_GPSDATA_ADVANCED"


# TX_DESCRIPTOR ------------------------------------------------------

tx_descriptor = {}

tx_descriptor[0x0001] = "LL_STATUS"
tx_descriptor[0x0002] = "IMU_RAWDATA"
tx_descriptor[0x0004] = "IMU_CALCDATA"
tx_descriptor[0x0008] = "RC_DATA"
tx_descriptor[0x0010] = "CONTROLLER_OUTPUT"
tx_descriptor[0x0080] = "GPS_DATA"
#Don't have struct
tx_descriptor[0x0100] = "CURRENT_WAY"
tx_descriptor[0x0200] = "GPS_DATA_ADVANCED"
#Don't have struct
tx_descriptor[0x0800] = "CAM_DATA"


# RX_STRUCTURE -------------------------------------------------------

rx_structure = {}

names = [
    "battery_voltage_1",
    "battery_voltage_2",
    "status",
    "cpu_load",
    "compass_enabled",
    "chksum_error",
    "flying",
    "motors_on",
    "flightMode",
    "up_time"]
types = ['s', 's', 's', 's', 'c', 'c', 'c', 'c', 's', 's']
rx_structure["LL_STATUS"] = (names, types)


names = [
    "pressure",
    "gyro_x",
    "gyro_y",
    "gyro_z",
    "mag_x",
    "mag_y",
    "mag_z",
    "acc_x",
    "acc_y",
    "acc_z",
    "temp_gyro",
    "temp_ADC"]
types = ['i', 's', 's', 's', 's', 's', 's', 's', 's', 's', 'us', 'ui']
rx_structure["IMU_RAWDATA"] = (names, types)


names = [
    "angle_nick",
    "angle_roll",
    "angle_yaw",
    "angvel_nick",
    "angvel_roll",
    "angvel_yaw",
    "acc_x_calib",
    "acc_y_calib",
    "acc_z_calib",
    "acc_x",
    "acc_y",
    "acc_z",
    "acc_angle_nick",
    "acc_angle_roll",
    "acc_absolute_value",
    "Hx",
    "Hy",
    "Hz",
    "mag_heading",
    "speed_x",
    "speed_y",
    "speed_z",
    "height",
    "dheight",
    "dheight_reference",
    "height_reference"]
types = [
    'i',
    'i',
    'i',
    'i',
    'i',
    'i',
    's',
    's',
    's',
    's',
    's',
    's',
    'i',
    'i',
    'i',
    'i',
    'i',
    'i',
    'i',
    'i',
    'i',
    'i',
    'i',
    'i',
    'i',
    'i']
rx_structure["IMU_CALCDATA"] = (names, types)


names = [
    "latitude",
    "longitude",
    "height",
    "speed_x",
    "speed_y",
    "heading",
    "horizontal_accuracy",
    "vertical_accuracy",
    "speed_accuracy",
    "numSV",
    "status"]
types = ['i', 'i', 'i', 'i', 'i', 'i', 'ui', 'ui', 'ui', 'ui', 'i']
rx_structure["GPS_DATA"] = (names, types)


names = [
    "latitude",
    "longitude",
    "height",
    "speed_x",
    "speed_y",
    "heading",
    "horizontal_accuracy",
    "vertical_accuracy",
    "speed_accuracy",
    "numSV",
    "status",
    "latitude_best_estimate",
    "longitude_best_estimate",
    "speed_x_best_estimate",
    "speed_y_best_estimate"]
types = [
    'i',
    'i',
    'i',
    'i',
    'i',
    'i',
    'ui',
    'ui',
    'ui',
    'ui',
    'i',
    'i',
    'i',
    'i',
    'i']
rx_structure["GPS_DATA_ADVANCED"] = (names, types)


names = ["channels_in8", "channels_out8", "lock"]
types = ['us', 'us', 'uc']
rx_structure["RC_DATA"] = (names, types)


names = ["nick", "roll", " yaw", "thrust"]
types = ['i', 'i', 'i', 'i']
rx_structure["CONTROLLER_OUTPUT"] = (names, types)


# TX_STRUCTURE -------------------------------------------------------

tx_structure = {}

#CTRL_INPUT
names = ["pitch", "roll", "yaw", "thrust", "ctrl", "checksum"]
types = ['s', 's', 's', 's', 's', 's']
tx_structure["di"] = (names, types)

#CONSULT
names = ["codi"]
types = ['us']
tx_structure["p"] = (names, types)

#SWITCH_ON
names = ["state"]
types = ['uc']
tx_structure["m"] = (names, types)

# DESCRIPTOR TO STRUCTURE --------------------------------------------

descriptor2structure = {}

descriptor2structure[0x01] = "IMU_RAWDATA"
descriptor2structure[0x02] = "LL_STATUS"
descriptor2structure[0x03] = "IMU_CALCDATA"
descriptor2structure[0x11] = "CONTROLLER_OUTPUT"
descriptor2structure[0x15] = "RC_DATA"
descriptor2structure[0x23] = "GPS_DATA"
descriptor2structure[0x29] = "GPS_DATA_ADVANCED"
