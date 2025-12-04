# motokey
Binding hotkeys to phrases

Some specific keys send choosen phrases eg email address or paswd

On peut utiliser evdev.py pour intercepter W+F1 **même en console sans X11 ni Wayland**. Cad qu'il intervient AVANT X11 ou Wayland
Problème : on ne peut empêcher de re-emettre la touche interceptée que avec dev.grab() qui deonnecte tout le clavier : danger ...
