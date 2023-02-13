import time
import random
import pygame



# initialisation de la taille de la fenêtre et de la fenêtre de jeu
taille_win = (800, 900)
taille_jeu = (taille_win[0], taille_win[0])
win = pygame.display.set_mode((taille_win))

# initialisation de variables
pygame.font.init()
font = pygame.font.SysFont('arial', 30)



def voisins(grille:list[list], x_case:int, y_case:int, taille:int)->int:
    """
    Hypothèse: 0<=x_case<taille et 0<=y_case<taille
               taille > 0
    Permet de compter le nombre de voisins d'une case.
    """
    # Vérification si la case n'est pas en dehors de la grille
    assert 0<=x_case<taille
    assert 0<=y_case<taille
    
    # Définit le nombre de voisins à 0 et la taille de la grille
    nb_voisins:int = 0
    taille_grille = len(grille)

    # Parcours la grille
    for i in range(-1,2):
        for j in range(-1,2):

            # Définit les voisins et les conditions
            x_voisines:int = x_case + i
            y_voisines:int = y_case + j
            not_coor_case:bool = [x_voisines, y_voisines] != [x_case, y_case]
            infe_taille:bool = y_voisines < taille_grille and x_voisines < taille_grille

            # Compte les voisins
            if x_voisines >= 0 and y_voisines >= 0 and infe_taille and not_coor_case:
                if grille[x_voisines][y_voisines] == 1:
                    nb_voisins += 1

    # Renvoi le nombre de voisins
    return nb_voisins



def vie(grille:list[list], nv_grille:list[list], x_case:list, y_case:list, taille)->None:
    """
    Hypothèse: 0<=x_case<10 et 0<=y_case<10
               taille > 0
    Applique les règles du jeu de la vie à la grille.
    """
    # Vérification si la case n'est pas en dehors de la grille
    assert 0<=x_case<taille
    assert 0<=y_case<taille

    # Définit nb_voisins
    nb_voisins = voisins(grille, x_case, y_case, taille)

    # La cellule meurt d'isolement (moins de 2 voisins)
    if grille[x_case][y_case] == 1 and nb_voisins < 2:
        nv_grille[x_case][y_case] = 0

    # La cellule survie à la prochaine itération (entre 2 et 3 voisins)
    elif grille[x_case][y_case] == 1 and 2 <= nb_voisins <= 3:
        nv_grille[x_case][y_case] = 1
    
    # La cellule meurt de d'étouffement (plus de 3 voisins)
    elif grille[x_case][y_case] == 1 and nb_voisins > 3:
        nv_grille[x_case][y_case] = 0

    # Une nouvelle cellule nait (3 voisins autour d'une cellule morte)
    elif grille[x_case][y_case] == 0 and nb_voisins == 3:
        nv_grille[x_case][y_case] = 1



def menu():
    """
    Affihage et gestion du menu
    """
    # Affichage de l'interface
    affiche('menu')

    # Running vérifie si je quitte le programme
    running = True

    # Boucle pygame
    while running:

        # Events
        for event in pygame.event.get():
            
            # Fermeture si ferme la page
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True

            # Clique de la souris
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                # Detection de l'appui sur les boutons
                try:

                    # Bouton JOUER
                    if taille_win[0]*1/6 < pos[0] < (taille_win[0]*1/6)+(taille_win[0]*4/6) and taille_win[0]*1/6 < pos[1] < (taille_win[1]*1/6)+(taille_win[1]*1/6):
                        return False

                    # Bouton QUITTER
                    if taille_win[0]*1/6 < pos[0] < (taille_win[0]*1/6)+(taille_win[0]*4/6) and taille_win[0]*3/6 < pos[1] < (taille_win[0]*4/6)+(taille_win[1]*1/6):
                        return True

                    # Bouton commandes
                    if 20 < pos[0] < 210 and taille_win[1]-42 < pos[1] < taille_win[1]-17:
                        menu_commandes()
                        affiche('menu')
                except:
                    pass



def menu_commandes():
    """
    Affichage et gestion du menu des contrôles
    """
    # Affichage de l'interface
    affiche('menu_commandes')

    # Running vérifie si je quitte le programme
    running = True

    # Boucle pygame
    while running:

        # Events
        for event in pygame.event.get():
            
            # Retour au menu si ferme la page
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True

            # Clique de la souris
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                # Detection de l'appui sur les boutons
                try:

                    # Bouton retour menu
                    if 20 < pos[0] < 210 and taille_win[1]-42 < pos[1] < taille_win[1]-17:
                        return True
                except:
                    pass



def choix_case(grille:list, taille:int, taille_jeu:list, taille_win:list):
    """
    Hypothèse: taille > 0
               taille_jeu > 0
               taille_win > 0
    Donne le choix des cases à cocher à l'utilisateur en début de partie.
    """
    #
    taille_case = taille_jeu[0] / taille

    # Affichage de l'interface
    affiche('choix_case', grille, taille)

    # Running vérifie si je quitte le programme
    running = True  

    # Boucle pygame
    while running:

        # Events
        for event in pygame.event.get():
            
            # Fermeture si ferme la page
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True
            
            # Clique de la souris
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                x = int(pos[0]//taille_case)
                y = int(pos[1]//taille_case)

                # coche/décoche les cases cliquées
                try:
                    # Si 0 alors cliqué
                    if grille[x][y] == 0:
                        pygame.draw.rect(win, (0,0,0), [x*taille_case, y*taille_case, taille_case-1, taille_case-1])
                        grille[x][y] = 1
                        affiche('choix_case', grille, taille)
                    
                    # Si 1 alors décliqué
                    else:
                        pygame.draw.rect(win, (255,255,255), [x*taille_case, y*taille_case, taille_case-1, taille_case-1])
                        grille[x][y] = 0
                        affiche('choix_case', grille, taille)
                except:
                    pass

                # Lance la partie
                if 0 < pos[0] < taille_win[0] and taille_jeu[1] < pos[1] < taille_win[1]:
                    return



def affiche(mode:str, grille:list[list]=[], taille:int=0)->None:
    """
    Hypothèse: taille > 0
    Affiche la grille de jeu.
    """
    # Vérification pour les modes 'play', 'pause' et 'choix_case' qui utilisent la grille
    if mode in ['play', 'pause', 'choix_case']:

        # Créé la grille
        win.fill((0,0,0))
        taille_case = taille_jeu[0] / taille
        for x in range(taille):
            for y in range(taille):
                # peint la case (x,y) en noir si grille[x][y] vaut 1
                if grille[x][y] == 1:
                    pygame.draw.rect(win, (0,0,0), [x*taille_case, y*taille_case, taille_case-1, taille_case-1])
                # peint la case (x,y) en blanc si grille[x][y] vaut 0
                else:
                    pygame.draw.rect(win, (255,255,255), [x*taille_case, y*taille_case, taille_case-1, taille_case-1])
        
        # Prépare l'affichage en mode play
        if mode == 'play':
            # Bouton pause
            pygame.draw.rect(win, (255,255,255), [0, taille_jeu[0], taille_win[0], taille_win[1]-taille_jeu[1]])
            pygame.draw.rect(win, (230,230,230), [0, taille_jeu[0], taille_win[0], taille_win[1]-taille_jeu[1]], 10)
            # Texte
            texte_pause = font.render('PAUSE', True, (0, 0, 0))

            # Affichage de l'interface
            win.blit(texte_pause, ((taille_win[0]/2)-40, (taille_jeu[1]+int(taille_win[1]-taille_jeu[1])//2)-20))
            pygame.display.flip()

        # Prépare l'affichage en mode pause
        if mode == 'pause':
            # Bouton retour
            pygame.draw.rect(win, (255,255,255), [0, taille_jeu[0], taille_win[0]*1/3, taille_win[1]-taille_jeu[1]])
            pygame.draw.rect(win, (230,230,230), [0, taille_jeu[0], taille_win[0]*1/3, taille_win[1]-taille_jeu[1]], 10)
            # Bouton play
            pygame.draw.rect(win, (255,255,255), [taille_win[0]*1/3, taille_jeu[0], taille_win[0]*1/3, taille_win[1]-taille_jeu[1]])
            pygame.draw.rect(win, (230,230,230), [taille_win[0]*1/3, taille_jeu[0], taille_win[0]*1/3, taille_win[1]-taille_jeu[1]], 10)
            # Bouton avance
            pygame.draw.rect(win, (255,255,255), [taille_win[0]*2/3, taille_jeu[0], taille_win[0]*1/3, taille_win[1]-taille_jeu[1]])
            pygame.draw.rect(win, (230,230,230), [taille_win[0]*2/3, taille_jeu[0], taille_win[0]*1/3, taille_win[1]-taille_jeu[1]], 10)
            # Texte
            texte_play = font.render('PLAY', True, (0, 0, 0))
            texte_recule = font.render('<<', True, (0, 0, 0))
            texte_avance = font.render('>>', True, (0, 0, 0))
            
            # Affichage de l'interface
            win.blit(texte_play, ((taille_win[0]/2)-30, (taille_jeu[1]+int(taille_win[1]-taille_jeu[1])//2)-20))
            win.blit(texte_recule, ((taille_win[0]*1/6)-15, (taille_jeu[1]+int(taille_win[1]-taille_jeu[1])//2)-20))
            win.blit(texte_avance, ((taille_win[0]*5/6)-15, (taille_jeu[1]+int(taille_win[1]-taille_jeu[1])//2)-20))
            pygame.display.flip()
            

        # Prépare l'affichage en mode choix de case
        if mode == 'choix_case':
            # Bouton play
            pygame.draw.rect(win, (255,255,255), [0, taille_jeu[0], taille_win[0], taille_win[1]-taille_jeu[1]])
            pygame.draw.rect(win, (230,230,230), [0, taille_jeu[0], taille_win[0], taille_win[1]-taille_jeu[1]], 10)
            texte_play = font.render('PLAY', True, (0, 0, 0))
            
            # Affichage de l'interface
            win.blit(texte_play, ((taille_win[0]/2)-30, (taille_jeu[1]+int(taille_win[1]-taille_jeu[1])//2)-20))
            pygame.display.flip()
    else:
        # Prépare l'affichage en mode menu
        if mode == 'menu':
            # Fond
            win.fill((255,255,255))
            pygame.draw.rect(win, (230,230,230), [0, 0, taille_win[0], taille_win[1]], 10)
            # Bouton JOUE
            pygame.draw.rect(win, (200,255,200), [taille_win[0]*1/6, taille_win[1]*1/6, taille_win[0]*4/6, taille_win[1]*1/6])
            pygame.draw.rect(win, (150,255,150), [taille_win[0]*1/6, taille_win[1]*1/6, taille_win[0]*4/6, taille_win[1]*1/6], 10)
            texte_jouer = font.render('JOUER', True, (0, 0, 0))
            win.blit(texte_jouer, ((taille_win[0]/2)-30, ((taille_win[1]*1/6)+taille_win[1]*1/12)-20))
            # Bouton QUITTER
            pygame.draw.rect(win, (255,200,200), [taille_win[0]*1/6, taille_win[1]*3/6, taille_win[0]*4/6, taille_win[1]*1/6])
            pygame.draw.rect(win, (255,150,150), [taille_win[0]*1/6, taille_win[1]*3/6, taille_win[0]*4/6, taille_win[1]*1/6], 10)
            texte_quitter = font.render('QUITTER', True, (0, 0, 0))
            win.blit(texte_quitter, ((taille_win[0]/2)-60, ((taille_win[1]*3/6)+taille_win[1]*1/12)-20))
            # Bonton commandes
            texte_quitter = font.render('Commandes', True, (0, 0, 255))
            win.blit(texte_quitter, (20, taille_win[1]-50))
            # Texte version
            texte_version = font.render('Jeu de la vie', False, (0, 0, 0))
            win.blit(texte_version, (taille_win[0]-155, ((taille_win[1])-80)))
            texte_version = font.render('(v1.0)', False, (0, 0, 0))
            win.blit(texte_version, (taille_win[0]-80, ((taille_win[1])-50)))
    
            # Affichage de l'interface
            pygame.display.flip()
        
        # Prépare l'affichage en mode menu des commandes
        if mode == 'menu_commandes':
            # Fond
            win.fill((255,255,255))
            pygame.draw.rect(win, (230,230,230), [0, 0, taille_win[0], taille_win[1]], 10)
            # Texte commandes
            texte_commandes1 = font.render('Barre espace : play/stop', True, (0, 0, 0))
            win.blit(texte_commandes1, (taille_win[0]*1/12, taille_win[1]*1/12))
            texte_commandes2 = font.render('Flèche gauche : retour en arrière', True, (0, 0, 0))
            win.blit(texte_commandes2, (taille_win[0]*1/12, taille_win[1]*2/12))
            texte_commandes3 = font.render('Flèche droite : aller en avant', True, (0, 0, 0))
            win.blit(texte_commandes3, (taille_win[0]*1/12, taille_win[1]*3/12))
            texte_commandes4 = font.render('Echap : quitter', True, (0, 0, 0))
            win.blit(texte_commandes4, (taille_win[0]*1/12, taille_win[1]*4/12))
            # Bonton retour au menu
            texte_quitter = font.render('retour au menu', True, (255, 0, 0))
            win.blit(texte_quitter, (20, taille_win[1]-50))

            # Affichage de l'interface
            pygame.display.flip()



def jeu(taille:int, randome:bool):
    """
    Hypothèse: taille > 0
               aléatoire : random = True
               manuel : random = False
    Simule le jeu de la vie.
    """
    # Affiche le menu, si True quitte le jeu
    if menu() is True:
        quit()

    # Création des grilles
    if randome == True:
        grille = [[random.randint(0,1) for i in range(taille)] for j in range(taille)]
    else:
        grille = [[0 for i in range(taille)] for j in range(taille)]
    historique_grille = []
    nv_grille = grille

    iterations = 0
    # Choix des cases + quitte si return True
    if choix_case(grille, taille, taille_jeu, taille_win) is True:
        jeu(taille, randome)

    #Initialisation des variables pour pygame
    running = True
    pause = False

    # Boucle de jeu tant que running est vrai
    while running:

        # Events
        for event in pygame.event.get():
            # Fermeture si ferme la page
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            
            # Un bouton de la souris a été pressé
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                
                # Si le jeu est en pause
                if pause:
                    # Retour en arrière
                    if 0 < pos[0] < taille_win[0]*1/3 and taille_jeu[1] < pos[1] < taille_win[1]:
                        try:
                            # Affiche la grille
                            affiche('pause', historique_grille[-1], taille)
                            # Créé la nouvelle grille et met à jour l'itération
                            grille = historique_grille.pop()
                            iterations -= 1
                            # Affiche l'itération
                            print(iterations)
                        except:
                            print('Vous ne pouvez pas aller plus en arrière !')
                    
                    # Va en avant
                    if taille_jeu[0]*2/3 < pos[0] < taille_win[0] and taille_jeu[1] < pos[1] < taille_win[1]:
                        # Stock la grille dans l'historique
                        historique_grille.append(grille)
                        # Fait avancer le jeu de la vie
                        nv_grille = [[0 for i in range(taille)] for i in range(taille)]
                        for x in range(len(grille)):
                            for y in range(len(grille)):
                                vie(grille, nv_grille, x, y, taille)
                        # Créé la nouvelle grille, met à jour l'itération et temporise
                        grille = nv_grille
                        iterations += 1
                        # Affiche l'itération et la grille
                        print(iterations)
                        affiche('pause', grille, taille)
                    



                    # Pause
                    if taille_jeu[0]*1/3 < pos[0] < taille_win[0]*2/3 and taille_jeu[1] < pos[1] < taille_win[1]:
                        pause = False
                        print('play')
                
                # Si le jeu n'est pas en pause
                else:
                    # Pause
                    if 0 < pos[0] < taille_win[0] and taille_jeu[1] < pos[1] < taille_win[1]:
                        pause = True
                        print('stop')
                        affiche('pause', grille, taille)

            # Une touche du clavier a été pressée
            if event.type == pygame.KEYDOWN:
                # Si le jeu est en pause
                if pause:
                    # Retour en arrière
                    if event.key == pygame.K_LEFT:
                        try:
                            # Affiche la grille
                            affiche('pause', historique_grille[-1], taille)
                            # Créé la nouvelle grille et met à jour l'itération
                            grille = historique_grille.pop()
                            iterations -= 1
                            # Affiche l'itération
                            print(iterations)
                        except:
                            print('Vous ne pouvez pas aller plus en arrière !')
                    
                    # Va en avant
                    if event.key == pygame.K_RIGHT:
                        # Stock la grille dans l'historique
                        historique_grille.append(grille)
                        # Fait avancer le jeu de la vie
                        nv_grille = [[0 for i in range(taille)] for i in range(taille)]
                        for x in range(len(grille)):
                            for y in range(len(grille)):
                                vie(grille, nv_grille, x, y, taille)
                        # Créé la nouvelle grille, met à jour l'itération et temporise
                        grille = nv_grille
                        iterations += 1
                        # Affiche l'itération et la grille
                        print(iterations)
                        affiche('pause', grille, taille)
                    
                    # Pause
                    if event.key == pygame.K_SPACE:
                        pause = False
                        print('play')
               
                # Si le jeu n'est pas en pause
                else:
                    # Pause
                    if event.key == pygame.K_SPACE:
                        pause = True
                        print('stop')
                        affiche('pause', grille, taille)



        # Si le programme n'est pas en pause
        if not pause:
            # Stock la grille dans l'historique
            historique_grille.append(grille)
            # Fait avancer le jeu de la vie
            nv_grille = [[0 for i in range(taille)] for i in range(taille)]
            for x in range(len(grille)):
                for y in range(len(grille)):
                    vie(grille, nv_grille, x, y, taille)
            # Créé la nouvelle grille et met à jour l'itération
            grille = nv_grille
            iterations += 1
            # Affiche l'itération et la grille
            print(iterations)
            affiche('play', grille, taille)
            # Temporise
            time.sleep(0.1)

    # Retour en arrière à la fermeture
    for i in range(len(historique_grille)-2, -1, -1):
        # Quitte le programme si rappui sur croix
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        # Affiche l'historique de la fin au début
        affiche('play', historique_grille[i], taille)
        time.sleep(0.01)
    
    # Affiche le menu
    jeu(taille, randome)
        


jeu(50, False)



pygame.quit()
quit()