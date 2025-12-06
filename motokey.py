#!/usr/bin/env python3
import time,sys
from evdev import UInput, ecodes,list_devices,InputDevice

# --- Mapping AZERTY complet ---
KEYMAP = {
    # lettres minuscules
    'a': ecodes.KEY_Q, 'b': ecodes.KEY_B, 'c': ecodes.KEY_C, 'd': ecodes.KEY_D,
    'e': ecodes.KEY_E, 'f': ecodes.KEY_F, 'g': ecodes.KEY_G, 'h': ecodes.KEY_H,
    'i': ecodes.KEY_I, 'j': ecodes.KEY_J, 'k': ecodes.KEY_K, 'l': ecodes.KEY_L,
    'm': ecodes.KEY_SEMICOLON, 'n': ecodes.KEY_N, 'o': ecodes.KEY_O, 'p': ecodes.KEY_P,
    'q': ecodes.KEY_A, 'r': ecodes.KEY_R, 's': ecodes.KEY_S, 't': ecodes.KEY_T,
    'u': ecodes.KEY_U, 'v': ecodes.KEY_V, 'w': ecodes.KEY_Z, 'x': ecodes.KEY_X,
    'y': ecodes.KEY_Y, 'z': ecodes.KEY_W,

    # chiffres
    '0': ecodes.KEY_0, '1': ecodes.KEY_1, '2': ecodes.KEY_2, '3': ecodes.KEY_3,
    '4': ecodes.KEY_4, '5': ecodes.KEY_5, '6': ecodes.KEY_6, '7': ecodes.KEY_7,
    '8': ecodes.KEY_8, '9': ecodes.KEY_9,

    # caractères spéciaux
    ' ': ecodes.KEY_SPACE,
    '_': ecodes.KEY_8,       
    '=': ecodes.KEY_EQUAL,
    '#': ecodes.KEY_3,           # AltGr + 3
    '?': ecodes.KEY_M,       # Shift + ,
    '@': ecodes.KEY_0,           # AltGr + 0
    '.': ecodes.KEY_COMMA,
    ':': ecodes.KEY_DOT,         # Shift + .
    '<': ecodes.KEY_COMMA,       # Shift + ,
    '>': ecodes.KEY_DOT,         # Shift + .
    '~': ecodes.KEY_2,           # AltGr + 2
    '&': ecodes.KEY_1,           # Shift + 1
    '{': ecodes.KEY_4,           # AltGr + 4
    '}': ecodes.KEY_5,           # AltGr + 5
    '[': ecodes.KEY_5,           # Shift + 5
    ']': ecodes.KEY_RIGHTBRACE,  # AltGr nécessaire
    '\n': ecodes.KEY_ENTER,
}

# --- Lettres majuscules ---
for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
    KEYMAP[c] = KEYMAP[c.lower()]

# --- Modificateurs nécessaires ---
SPECIAL_MODIFIERS = {
    '0':'shift','1':'shift','2':'shift', '3':'shift','4':'shift','5':'shift',
    '6':'shift', '7':'shift', '8':'shift','9':'shift',
    '?': 'shift',
    '.':'shift',
    '&': 'shift',
    '@': 'altgr',
    '#': 'altgr',
    '~': 'altgr',
    '{': 'altgr',
    '}': 'altgr',
    '[': 'shift',
    ']': 'altgr',
}

# Majuscules nécessitent Shift
for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
    SPECIAL_MODIFIERS[c] = 'shift'

def keyboardSelection():
    """
    exit if no keyboard found
    ask is more than one keyboard found
    """
    # keyboards detection 
    devices = [InputDevice(path) for path in list_devices()]
    keyboards = []
    for device in devices:
       if  device.name.upper().find("KEYBOARD") == -1:
           continue
       if  device.name.upper().find("VIRTUAL") == -1:
           continue
       keyboards.append(device)
    if len(keyboards)==0:
       print("no keyboards found")
       exit(1)
    k = 0
    if len(keyboards)!=1:
        for i,k in enumerate(keyboards):
            print(f"{i=} {k.name=}")
        k= int(input("which one ? "))
    dev = keyboards[k]
    print(f"{dev=}")
    return dev

def send_char(c):
    if c.isupper():
        ui.write(ecodes.EV_KEY, ecodes.KEY_LEFTSHIFT, 1)
        ui.write(ecodes.EV_KEY, KEYMAP[c.lower()], 1)
        ui.write(ecodes.EV_KEY, KEYMAP[c.lower()], 0)
        ui.write(ecodes.EV_KEY, ecodes.KEY_LEFTSHIFT, 0)
    elif c in SPECIAL_MODIFIERS:
        mod = SPECIAL_MODIFIERS[c]
        if mod == 'shift':
            ui.write(ecodes.EV_KEY, ecodes.KEY_LEFTSHIFT, 1)
            ui.write(ecodes.EV_KEY, KEYMAP[c], 1)
            ui.write(ecodes.EV_KEY, KEYMAP[c], 0)
            ui.write(ecodes.EV_KEY, ecodes.KEY_LEFTSHIFT, 0)
        elif mod == 'altgr':
            ui.write(ecodes.EV_KEY, ecodes.KEY_RIGHTALT, 1)
            ui.write(ecodes.EV_KEY, KEYMAP[c], 1)
            ui.write(ecodes.EV_KEY, KEYMAP[c], 0)
            ui.write(ecodes.EV_KEY, ecodes.KEY_RIGHTALT, 0)
    else:
        ui.write(ecodes.EV_KEY, KEYMAP[c], 1)
        ui.write(ecodes.EV_KEY, KEYMAP[c], 0)
    ui.syn()
    time.sleep(0.01)

def send_text(text):
    for c in text:
        send_char(c)

# --- Crée le clavier virtuel ---
ui = UInput({ecodes.EV_KEY: list(KEYMAP.values()) + [ecodes.KEY_LEFTSHIFT, ecodes.KEY_RIGHTALT]}, name="virtual_keyboard")

# print("ds 3 sec je balance la puree")
# time.sleep(3)  # laisser le temps de placer le curseur
# send_text("1changed1")
# sys.exit(1)

dev = keyboardSelection()

# --- Exemple ---
# time.sleep(1)
# send_text("1Changed1_")
# send_char('\n')  # Enter
# import sys
# send_text("1changed1")
# send_char('\n')  # Enter
# send_text("jeanchristian@anglesdauriac.fr")
# send_char('\n')  # Enter
# send_text("E#e7o=p_u?")
# send_char('\n')  # Enter
# send_text("myriam@anglesdauriac.fr")
#########################################

# On garde en mémoire l'état courant des touches
keys_down = set()
for event in dev.read_loop():
   if event.type != ecodes.EV_KEY:
      # print(f"quite {event.type=} != {ecodes.EV_KEY=}")
      continue
   code = event.code     # keycode Linux (ex: 17 pour KEY_W)
   val = event.value       # 1=down, 0=up, 2=autorepeat
   if val==0: # on relache
      keys_down.remove(code)
   elif val==1: # on enfonce
      keys_down.add(code)
   if not (125 in keys_down):
      # print(f"quitte car 125 not in {keys_down=}")
      continue
   if val==2 or val==0:
      # print(f"quite car {val=}")
      continue
   if code==59: #      print(f"treating W+F1")
      send_text("1Changed1_")
   elif code==60: #      print(f"treating W+F2")
      send_text("1changed1")
   elif code==61: #      print(f"treating W+F3")
      send_text("jeanchristian@anglesdauriac.fr")
   elif code==62: #      print(f"treating W+F4")
      send_text("E#e7o=p_u?")
   elif code==63: #       print(f"treating W+F5")
      send_text("myriam@anglesdauriac.fr")
#   else:      print(f"rien car {code=}")
