# motokey
Binding hotkeys to phrases

Some specific keys send choosen phrases eg email address or paswd

On peut utiliser evdev.py pour intercepter W+F1 **même en console sans X11 ni Wayland**. Cad qu'il intervient AVANT X11 ou Wayland
Problème : on ne peut empêcher de re-emettre la touche interceptée que avec dev.grab() qui deonnecte tout le clavier : danger ...

# Solution avec autokeys :
  	   OK mais problème de sécurité avec le passwd en clair dans ~/.config/autokey/data/My Phrase/Fourth.txt
	   idee : avoir un script qui effacer ce fichier et qui est appelé regulièrement et un alias qui recrée le fichier (il faut se souvenir du passwd)
	   	- à la deconnexion de xfce
		- au halt
		- à la mise en veille

# Solution avec les raccourcis clavier de xfce:
  	   OK mais probème de sécutité car le passwd est en clair dans le sdipt xdotool
  	   il faut écrire un script qui utilise xdotool pour envoyer le passwd IL FAUT UN DELAI avant le xdotool type "maPhrase" AZERTY vs QWERTY
	   idee : avoir un script qui effacer ce fichier et qui est appelé regulièrement et un alias qui recrée le fichier (il faut se souvenir du passwd)
	   	- à la deconnexion de xfce
		- au halt
		- à la mise en veille
	OU desactivation des RACCOURCI CLAVIER EN CLI EFFECTUÉE dans un script