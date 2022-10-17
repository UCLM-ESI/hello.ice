#!/usr/bin/python3 -u
# -*- mode:python; coding:utf-8; tab-width:4 -*-

from time import sleep

from gext import XApp, command, Recorder
from gext import mouse as m, keyboard as k

from gext.mouse import Mouse
from gext.keyboard import Keyboard

Keyboard.default_mode = Keyboard.MODE_NATURAL
Keyboard.default_wait = 1
Mouse.default_wait = 1


def click():
    m.click()


def new_connection():
    m.move(35, 87)
    click()
    m.move(788, 261)
    click()
    m.move(559, 432)
    click()
    m.move(297, 257)
    click()
    k.keys('IceGrid<Return>')
    m.move(267, 310)
    click()
    m.move(546, 436)
    click()
    m.move(324, 273)
    click()
    k.keys('tcp -h localhost -p 4061')
    m.move(554, 434)
    click()
    m.move(532, 246)
    click()
    k.keys('user')
    m.move(516, 274)
    click()
    k.keys('pass')
    m.move(664, 431)
    click()

    sleep(2)


def create_app():
    m.move(41, 54)
    m.click()
    m.move(38, 85)
    m.move(703, 91)
    m.move(701, 108)
    m.click()

#    m.move(38, 66)
#    click()
#    m.move(39, 96)
#    click()
#    m.move(700, 115)
#    click()
#    m.move(643, 208)
#    click()
#
    m.move(658, 204)
    click()
    k.keys('<Shift_L><Home><Delete>PrinterApp')
    m.move(774, 549)
    click()

    # ClientNode
    m.move(95, 211)
    click()
    m.right_click()
    m.move(208, 226)
    click()
    m.move(507, 203)
    click()
    k.keys('<Shift_L><Home><Delete>ClientNode')
    m.move(773, 549)
    click()

    # ServerNode
    m.move(118, 207)
    click()
    m.right_click()
    m.move(238, 220)
    click()
    m.move(570, 202)
    click()
    k.keys('<Shift_L><Home><Delete>ServerNode')
    m.move(761, 547)
    click()

    # IcePatch server
    m.move(167, 225)
    click()
    m.right_click()
    m.move(377, 323)
    click()
    m.move(827, 201)
    click()
    m.move(698, 239)
    click()
    m.move(737, 279)
    click()
    k.keys('<Shift_L><Home><Delete>/tmp/printer')
    m.move(772, 549)
    click()

    # IcePacth2 proxy
    m.move(100, 189)
    click()
    m.move(866, 429)
    click()
    m.move(853, 466)
    click()
    m.move(767, 544)
    click()


def create_server():
    m.move(161, 264)
    click()
    m.right_click()
    m.move(367, 316)
    click()
    m.move(593, 198)
    click()
    k.keys('<Shift_L><Home><Delete>PrinterServer')
    m.move(868, 235)
    m.drag_abs(870, 319)
    m.move(584, 298)
    click()
    k.keys('./Server.py')
    m.move(588, 361)
    click()
    k.keys('${application.distrib}')
    m.move(873, 335)
    m.drag_abs(871, 237)
    m.move(605, 328)
    click()
    click()
    click()
    k.keys('Ice.StdOut<Return>')
    m.move(731, 326)
    click()
    click()
    k.keys('${application.distrib}/server-out.txt<Return>')
    m.move(763, 544)
    click()


def create_server_adapter():
    m.move(201, 281)
    m.right_click()
    m.move(403, 290)
    click()
    m.move(624, 206)
    click()
    k.keys('<Shift_L><Home><Delete>PrinterAdapter')
    m.move(771, 539)
    click()


def create_client():
    m.move(160, 226)
    m.right_click()
    m.move(364, 270)
    click()
    m.move(598, 202)
    click()
    k.keys('<Shift_L><Home><Delete>PrinterClient')
    m.move(876, 228)
    m.drag_abs(869, 312)
    m.move(804, 308)
    click()
    k.keys('./Client.py')
    m.move(682, 364)
    click()
    k.keys('${application.distrib}')
    m.move(872, 370)
    m.drag_abs(870, 231)
    m.move(770, 538)
    click()


def deploy():
    m.move(121, 193)
    click()
    m.move(331, 90)
    click()
    m.move(113, 130)
    click()
    m.move(56, 213)
    click()
    m.move(56, 266)
    click()
    m.move(177, 63)
    click()
    m.move(153, 90)
    m.move(460, 91)
    click()
    m.move(456, 361)
    click()
    m.move(411, 357)
    click()
    m.move(158, 286)
    click()
    m.right_click()
    m.move(268, 300)
    click()


def run_server_and_client_with_proxy():
    m.move(163, 278)
    click()
    m.right_click()
    m.move(290, 448)
    click()
    m.move(535, 136)
    m.drag_abs(356, 515)
    m.move(355, 599)
    m.drag_abs(42, 595)
    m.move(130, 625)
    k.keys('<Control_L>c')
    m.move(229, 137)
    click()
    m.move(165, 267)
    click()
    m.move(870, 237)
    m.drag_abs(865, 322)
    m.move(679, 385)
    click()
    k.keys("<Home><Shift_L><End><Delete>")
    k.keys('"<Control_L>v"')
    m.move(766, 548)
    click()
    m.move(329, 91)
    click()
    m.move(121, 128)
    click()
    m.move(137, 250)
    click()
    m.right_click()
    m.move(175, 263)
    click()

    # close server stdout
    m.move(63, 540)
    click()
    m.move(94, 672)
    click()


def well_known_object():
    m.move(229, 128)
    click()
    m.move(218, 320)
    click()
    m.move(873, 245)
    m.drag_abs(860, 397)
    m.move(510, 318)
    click()
    click()
    click()
    k.keys('printer1<Return>')
    m.move(874, 450)
    m.drag_abs(875, 264)
    m.move(772, 542)
    click()
    m.move(186, 262)
    click()
    m.move(818, 390)
    click()
    m.move(818, 415)
    k.keys('<Shift_L><Home><Delete>printer1')
    m.move(870, 382)
    m.drag_abs(872, 262)
    m.move(768, 542)
    click()
    m.move(333, 92)
    click()
    m.move(119, 133)
    click()
    m.move(180, 284)
    m.right_click()
    m.move(291, 460)
    click()
    m.move(509, 143)
    m.drag_abs(319, 437)
    m.move(174, 245)
    click()
    m.right_click()
    m.move(195, 254)
    click()
    sleep(2)
    m.move(41, 459)
    click()
    m.move(96, 588)
    click()


def implicit_activation():
    m.move(207, 129)
    click()
    m.move(191, 301)
    click()
    m.move(868, 258)
    m.drag_abs(873, 415)
    m.move(847, 348)
    click()
    m.move(804, 404)
    click()
    m.move(873, 408)
    m.drag_abs(883, 230)
    m.move(765, 543)
    click()
    m.move(333, 90)
    click()
    m.move(129, 132)
    click()
    m.move(182, 248)
    m.right_click()
    m.move(282, 264)
    click()
    sleep(3)


def implicit_deactivation():
    m.move(238, 132)
    click()
    m.move(197, 303)
    click()
    m.move(601, 345)
    click()
    click()
    k.keys('Ice.ServerIdleTime')
    m.move(608, 344)
    k.keys('<Return>')
    m.move(786, 346)
    click()
    click()
    k.keys('5')
    m.move(771, 542)
    click()
    m.move(328, 93)
    click()
    m.move(109, 131)
    click()
    m.move(173, 246)
    m.right_click()
    m.move(266, 254)
    click()
    sleep(7)


command('rm /tmp/db/node1/distrib/PrinterApp/server-out.txt', expect_success=False)
command('rm -rf /home/david/.java/.userPrefs/IceGridGUI/Configurations')

icegridgui = XApp('icegridgui', title='IceGrid Admin')
icegridgui.wait_ready()

recorder = Recorder(width=940, height=640, output='icegrid.ogv')
sleep(5)

new_connection()
create_app()
create_server()
create_server_adapter()
create_client()

deploy()
run_server_and_client_with_proxy()

well_known_object()

implicit_activation()
implicit_deactivation()

recorder.terminate()

sleep(3)

icegridgui.terminate()
