from evdev import InputDevice, UInput, categorize, ecodes

dev = InputDevice('/dev/input/event3')  # Adapter le device
ui = UInput()                           # Device virtuel
# dev.grab()                               # Empêche les événements natifs

modifiers = {
    'LEFTMETA': False,
    'RIGHTMETA': False,
}

try:
    for event in dev.read_loop():
        if event.type == ecodes.EV_KEY:
            key = categorize(event)
            if key.keystate==2:
                continue
            # print(f"{key.keycode=}")
            # continue
            # Mise à jour de l’état des touches Super
            if key.keycode == 'KEY_LEFTMETA':
                modifiers['LEFTMETA'] = (key.keystate == key.key_down)

            if key.keycode == 'KEY_RIGHTMETA':
                modifiers['RIGHTMETA'] = (key.keystate == key.key_down)

            if modifiers['LEFTMETA']:
                print("WITH W")
            # Détection de Super + F1
            if key.keycode == 'KEY_F1' and key.keystate == key.key_down:
                print("KEY_F1 enfoncée")
                if modifiers['LEFTMETA'] or modifiers['RIGHTMETA']:
                    print("SUPER + F1 capturé (bloqué).")
                    # envoyer votre string ici
                    continue  # NE PAS réémettre ⇒ bloque l’événement natif
                else:
                    print("sans W ")
        # Réémettre tout ce qui n’est pas bloqué
        ui.write_event(event)

finally:
    dev.ungrab()
    ui.close()
