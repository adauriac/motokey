from evdev import InputDevice, UInput, categorize, ecodes

dev = InputDevice('/dev/input/event3')  # Adapter le device
ui = UInput()                           # Device virtuel
dev.grab()                               # Empêche les événements natifs

modifiers = {
    'LEFTMETA': False,
    'RIGHTMETA': False,
}

KEYCODES = ["KEY_F1","KEY_F2","KEY_F3","KEY_F4","KEY_F5"]
try:
    for event in dev.read_loop():
        if event.type == ecodes.EV_KEY:
            key = categorize(event)
            if key.keystate==2:
                continue
            # Mise à jour de l’état des touches Super
            if key.keycode == 'KEY_LEFTMETA':
                modifiers['LEFTMETA'] = (key.keystate == key.key_down)
            if key.keycode == 'KEY_RIGHTMETA':
                modifiers['RIGHTMETA'] = (key.keystate == key.key_down)
            # Détection de Super + F1
            if key.keycode in KEYCODES and key.keystate == key.key_down:
                if modifiers['LEFTMETA'] or modifiers['RIGHTMETA']:
                    print(f"SUPER + {key.keycode} capturé (bloqué).")
                    continue  # NE PAS réémettre ⇒ bloque l’événement natif
                else:
                    print("sans W ")
        # Réémettre tout ce qui n’est pas bloqué
        ui.write_event(event)

finally:
    dev.ungrab()
    ui.close()
