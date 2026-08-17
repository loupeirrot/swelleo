#!/usr/bin/env python3
"""Contenu éditorial par spot, rendu sur les fiches /spots/<slug>/.

Champs par spot :
  intro      — ce qui fait le spot
  conditions — quand ça marche, quand ça ne marche pas
  niveau     — pour qui
  dangers    — les pièges
  acces      — parking, accès, affluence
  astuce     — le réflexe à avoir sur place
"""

SPOT_GUIDE = {
    "la-nord-hossegor": {
        "intro": "La Nord, c'est la vague qui a fait la réputation d'Hossegor. Un beach break qui creuse vite et qui tape fort. Le Gouf de Capbreton, ce canyon sous-marin qui vient mourir juste devant la plage, concentre l'énergie de la houle. C'est ce qui explique qu'on y trouve des tubes qu'on ne voit nulle part ailleurs sur la côte landaise.",
        "conditions": "Il faut une houle d'ouest à nord-ouest et un vent d'est pour tenir la vague ouverte. Après, tout dépend du banc du moment : le même swell peut donner une session mémorable une semaine, et des séries qui ferment la suivante. Dès que le vent bascule onshore, c'est plié.",
        "niveau": "Pas un spot où l'on apprend. Dès que ça pousse, il faut être à l'aise au take-off et savoir gérer un shore break qui ne pardonne rien. En petites conditions, un bon intermédiaire s'en sort. Shortboard dans la quasi-totalité des cas.",
        "dangers": "Rouleaux de bord, courants d'arrachement, et des bancs qui bougent d'une marée à l'autre. Quand ça creuse, il reste très peu d'eau sous la vague. Ajoutez du monde au line-up et un niveau général élevé : la place ne se donne pas.",
        "acces": "Accès par le front de mer d'Hossegor, parkings de ville à proximité. En juillet-août c'est saturé. Tôt le matin ou hors saison, c'est une autre histoire.",
        "astuce": "Regardez passer plusieurs séries avant d'y aller. À Hossegor, le pic qui paraît parfait depuis la plage peut fermer complètement trente mètres plus loin.",
    },
    "la-graviere-hossegor": {
        "intro": "Peu de vagues en Europe ont autant de réputation que La Gravière. Elle déferle vite, dans très peu d'eau, et tube presque au bord. La plage est à deux pas de la place des Landais, ce qui donne un contraste bizarre entre les terrasses et ce qui se passe à l'eau.",
        "conditions": "Houle de nord-ouest, vent d'est : c'est la combinaison qui la fait marcher. Il lui faut de la houle consistante pour montrer ce qu'elle sait faire. En petit, elle reste surfable mais perd tout son intérêt.",
        "niveau": "Confirmés et experts. La mairie elle-même déconseille le spot aux débutants, et ce n'est pas un excès de prudence : la vague casse trop vite et trop près du bord. Shortboard ou bodyboard quand ça fonctionne, le longboard n'a pas sa place.",
        "dangers": "Le shore break est le vrai sujet. Il envoie des gens à l'hôpital chaque année. Ajoutez les courants d'arrachement et une profondeur ridicule au moment du take-off. L'erreur classique, c'est de sous-estimer la vitesse de la vague depuis la plage.",
        "acces": "Accès direct depuis Hossegor, commerces et restaurants juste derrière. Plage surveillée en saison.",
        "astuce": "Si elle paraît trop grosse ou trop fermée, n'insistez pas. Les spots voisins tournent souvent mieux le même jour, et il n'y a rien à prouver.",
    },
    "les-estagnots-seignosse": {
        "intro": "Les Estagnots, c'est le compromis qui marche souvent quand les autres spots landais sont trop capricieux. Des bancs de sable qui donnent de longues parois à marée basse, et une vague plus creuse quand la mer remonte. Droites et gauches, selon le banc que vous choisissez.",
        "conditions": "Houle d'ouest à nord-ouest, le nord-ouest étant le meilleur, avec un vent d'est ou est-sud-est. Ça tourne à toutes les marées, mais pas de la même façon : basse mer donne des murs plus longs, pleine mer un shore break plus sec, parfois brutal. La régularité arrive avec l'automne, de septembre à février.",
        "niveau": "Intermédiaire à expert selon la taille. Un débutant peut y aller en petit, à condition de choisir le bon pic et d'éviter les jours de foule. Shortboard et fish la plupart du temps, longboard possible quand c'est plat.",
        "dangers": "Baïnes, courants d'arrachement et dérive latérale, qui montent vite en puissance avec la taille. À marée haute, le shore break peut surprendre. Le spot est souvent chargé.",
        "acces": "Grand parking gratuit dans les dunes, la plage est à cinquante mètres. Écoles de surf, snack, sanitaires, poste de secours. L'été, le parking se remplit tôt.",
        "astuce": "Quand le pic principal est bondé, marchez. Deux ou trois cents mètres suffisent souvent à trouver un banc équivalent avec quatre personnes dessus au lieu de quarante.",
    },
    "santocha-capbreton": {
        "intro": "Santocha est un multi-pics sur sable, avec des droites et des gauches réparties le long de la plage. Le Gouf de Capbreton joue ici en votre faveur : il absorbe une partie des grosses houles, ce qui rend le spot plus abordable que ses voisins du nord tout en restant régulier.",
        "conditions": "Pour débuter, visez 0,5 à 1 m avec un vent faible ou offshore d'est, autour de la mi-marée. Pour les confirmés, ça devient intéressant à partir d'1 m, vent d'est ou nord-est, plutôt de basse à mi-marée montante. L'automne et l'hiver sont nettement plus consistants.",
        "niveau": "Un des rares spots landais où tous les niveaux trouvent leur compte, à condition de choisir son pic. En petit, c'est un très bon terrain d'apprentissage. Shortboard, fish ou longboard, ça dépend du jour.",
        "dangers": "Fond de sable, donc pas de rochers, mais des baïnes bien présentes et des baigneurs partout en été. La dérive devient sérieuse quand la houle monte. Le principal risque reste de se mettre sur un pic trop gros pour soi.",
        "acces": "Parking gratuit juste à côté, plein très tôt en été. On y va facilement à pied ou à vélo depuis Capbreton. Surveillance en saison.",
        "astuce": "Ne vous arrêtez pas au premier pic visible depuis l'accès. Le spot en compte plusieurs, et quelques dizaines de mètres changent complètement le type de vague.",
    },
    "la-piste-capbreton": {
        "intro": "La Piste, c'est le spot puissant de Capbreton, celui qui tube. Particularité : la vague grossit à mesure qu'on descend vers le sud. Les gros jours, la partie basse n'a rien à envier aux spots d'Hossegor.",
        "conditions": "Elle demande de la houle consistante, disons 1 à 2 m selon le banc, plutôt à marée basse, avec un vent d'est. Passé une certaine taille, ou quand les bancs se referment, ça devient rapidement ingérable.",
        "niveau": "Intermédiaire à expert, et clairement expert dès que la houle rentre pour de bon. Shortboard ou bodyboard. Ce n'est pas un endroit où l'on progresse doucement.",
        "dangers": "Courants, baïnes, shore break, et des vagues creuses qui envoient au fond. Les bancs sont irréguliers d'une année sur l'autre.",
        "acces": "Parking gratuit à proximité mais capacité limitée en saison. L'accès depuis la route est court.",
        "astuce": "Avant de choisir votre pic, remontez la plage du regard vers le sud. Deux cents mètres peuvent faire la différence entre une session agréable et une séance de nettoyage.",
    },
    "cote-des-basques-biarritz": {
        "intro": "C'est ici que le surf a démarré en France, dans les années cinquante. Une grande plage de sable coincée entre les falaises, avec une partie nord plus douce où les longboards se retrouvent. L'endroit a gardé quelque chose de son époque.",
        "conditions": "Petites à moyennes houles de nord-ouest ou d'ouest, vent d'est à sud-est. Le détail qui compte : la plage disparaît complètement à marée haute, surtout au-delà de 45 de coefficient. Le spot tourne donc jusqu'aux trois quarts de marée, pas au-delà. L'automne, de septembre à novembre, est la meilleure période.",
        "niveau": "Débutant et intermédiaire en petit, confirmé quand ça grossit. Le longboard est chez lui dans la partie nord. Shortboard quand la houle prend de la puissance.",
        "dangers": "Le vrai piège n'est pas la vague, c'est la marée. La plage se referme et on peut se retrouver coincé contre la falaise. Surveillez l'heure. Beaucoup de débutants à l'eau l'été, et quelques rochers dans la partie sud.",
        "acces": "Le parking de la plage est difficile en saison. Celui du haut de la falaise, avenue Beau Rivage, est plus fiable, avec une descente à pied par le chemin en lacets. Surveillance de mai à septembre.",
        "astuce": "Commencez par le nord de la plage en petite houle, c'est là que c'est le plus tranquille. Et ne vous laissez pas piéger par une session qui démarre bien : la mer monte vite ici.",
    },
    "les-cavaliers-anglet": {
        "intro": "Les Cavaliers est le spot sérieux d'Anglet. Des A-frames rapides, gauches et droites, avec des bancs structurés par les digues et par l'embouchure de l'Adour juste à côté.",
        "conditions": "Houle d'ouest à nord-ouest, le nord-ouest ou ouest-nord-ouest en tête, avec un vent d'est. Il encaisse mieux qu'Hossegor un léger nord-ouest, ce qui en fait une bonne option les jours de vent tournant. Marée moyenne. Il prend toute sa dimension quand la houle est solide.",
        "niveau": "Intermédiaire à expert quand ça pousse. Shortboard principalement. Pour du longboard, les pics plus doux d'Anglet feront mieux l'affaire.",
        "dangers": "Courants et dérive latérale qui augmentent avec la taille. Le pic est puissant et disputé : observez cinq minutes avant de vous placer, et respectez les priorités. Le niveau à l'eau est élevé les bons jours.",
        "acces": "Accès urbain simple, parkings autour du secteur. Ça se remplit vite les bons jours et tout l'été. Venir tôt règle le problème.",
        "astuce": "Anglet a l'avantage d'aligner les plages les unes après les autres. Si Les Cavaliers est trop gros ou trop venté, cinq minutes de voiture suffisent à trouver mieux.",
    },
    "hendaye": {
        "intro": "Hendaye est la solution de repli du Pays Basque, et tout le monde le sait. La baie est protégée par le cap du Figuier et orientée au nord, ce qui filtre énormément. Fond de sable, pente douce, et plusieurs secteurs (Sokoburu, le Casino, la Digue) qui permettent d'adapter la session au niveau.",
        "conditions": "Ça marche à toutes les marées. L'intérêt principal : quand une grosse houle de nord-ouest sature toute la côte, ici ça reste surfable. Vent de sud favorable. Les petites houles donnent des vagues douces, parfaites pour progresser.",
        "niveau": "Débutant à intermédiaire. C'est probablement le meilleur endroit du Pays Basque pour apprendre. Longboard idéal en petit, shortboard dès que la houle rentre vraiment.",
        "dangers": "Beaucoup moins de baïnes que sur les plages landaises, ce qui explique sa réputation de spot sûr. Un courant latéral peut se lever avec les entrées maritimes d'ouest. Rochers à l'est, du côté des Deux Jumeaux. Les écoles de surf occupent une bonne partie du plan d'eau en saison.",
        "acces": "Accès très simple depuis la ville et le front de mer. Parkings payants le long de la plage, saturés en été.",
        "astuce": "Le réflexe à retenir : quand la côte basque est trop grosse, on vient ici. Casino et Digue pour les débutants, Valencia à basse et mi-marée pour ceux qui cherchent un peu plus de vague.",
    },
    "lacanau-ocean": {
        "intro": "Quatorze kilomètres de plage, une succession de bancs de sable et des digues qui structurent les pics. Le centre est le cœur historique du surf à Lacanau, avec une compétition professionnelle qui s'y tient depuis les années quatre-vingt.",
        "conditions": "Houle d'ouest à nord-ouest, vent d'est. Toutes les marées fonctionnent, mais différemment : à basse mer, les bancs extérieurs donnent des vagues rapides et creuses ; à montante, les sections raccourcissent et se rapprochent du bord. La bonne saison va d'octobre à février.",
        "niveau": "Du débutant à l'expert, tout dépend du secteur. La plage centrale convient à l'apprentissage en petit. Les bancs nord sont plus creux et plus exigeants.",
        "dangers": "Courants d'arrachement, en particulier près des digues et des chenaux. Les bancs bougent énormément : un endroit parfait en octobre peut être inutilisable en décembre. Beaucoup de monde au centre l'été.",
        "acces": "Tout est là au centre : parkings, commerces, écoles, surveillance. Les secteurs nord et sud demandent parfois de marcher un peu depuis le parking.",
        "astuce": "Ne traitez pas Lacanau comme un spot unique. Faites quelques centaines de mètres à pied et comparez avant de vous décider, les bancs n'ont souvent rien à voir entre le centre et le nord.",
    },
    "le-porge-ocean": {
        "intro": "Treize kilomètres de plage sauvage, sans grand-chose derrière la dune. Les bancs y sont réputés capricieux, ce qui est à la fois le défaut et l'intérêt du coin : personne ne peut vous dire à l'avance où ça va marcher.",
        "conditions": "Beach break très exposé. Le choix se fait sur place, en fonction du banc du jour et avec un vent d'est. Après un gros coup de houle, certains bancs se referment complètement pendant des semaines.",
        "niveau": "Plutôt intermédiaire à confirmé, moins pour la difficulté de la vague que pour la lecture du plan d'eau. Un débutant devrait s'en tenir aux petites conditions et à la zone surveillée.",
        "dangers": "Les baïnes sont le sujet numéro un ici, et elles ont fait des victimes. Les bancs irréguliers compliquent la lecture. Pas d'obstacle fixe, mais un océan qui ne pardonne pas l'imprudence.",
        "acces": "Accès par Le Porge-Océan, avec parkings et cheminements aménagés. La plage du Gressier sert de point d'information principal. L'affluence se concentre autour des accès.",
        "astuce": "La seule vraie astuce ici, c'est de marcher. Treize kilomètres de côte, et presque tout le monde reste dans les trois cents mètres autour du parking.",
    },
    "cap-ferret": {
        "intro": "Parler du Cap Ferret comme d'un spot n'a pas vraiment de sens. C'est une côte entière avec plusieurs accès : Grand Crohot, Truc Vert, Petit Crohot. Des beach breaks sur sable, des bancs mobiles, et de bons A-frames quand tout s'aligne.",
        "conditions": "Au Grand Crohot, comptez sur une houle d'ouest à nord-ouest et un vent d'est. Plusieurs marées fonctionnent selon le banc, et c'est justement pour ça qu'aucune règle fixe ne tient ici. L'automne et l'hiver sont plus réguliers. Au-delà de 2 m, les bancs extérieurs ont tendance à fermer.",
        "niveau": "Du débutant au confirmé selon le pic et la taille. Les petites houles d'été conviennent à l'apprentissage. Dès que ça creuse, il faut un vrai niveau intermédiaire.",
        "dangers": "Baïnes et courants d'arrachement, avec des bancs qui changent souvent. Le Grand Crohot est très fréquenté le week-end et en été.",
        "acces": "Au Grand Crohot, grand parking derrière la dune puis cinq minutes de caillebotis. Truc Vert et les autres accès demandent davantage de marche.",
        "astuce": "Montez sur la dune et regardez plusieurs pics avant de descendre. Trouver le bon banc compte bien plus ici que respecter une règle de marée.",
    },
    "la-sauzaie-bretignolles": {
        "intro": "La Sauzaie est le spot de reef de référence en Vendée. Une vague rapide et creuse qui casse sur du rocher, capable de sortir de vrais barrels quand le swell est propre. C'est aussi un spot de compétition, ce qui se sent au line-up.",
        "conditions": "Il lui faut une houle consistante et propre, avec un vent d'est ou nord-est. On privilégie la marée haute ou montante, tout simplement parce qu'à basse mer une bonne partie du reef découvre.",
        "niveau": "Intermédiaire à expert, et seulement si vous êtes à l'aise au-dessus d'un fond dur. Shortboard. Un take-off raté ne se termine pas dans le sable.",
        "dangers": "Le rocher, avant tout. Peu de fond, take-off rapide, sections qui ferment. À marée basse, les cailloux sortent franchement. Le pic est disputé et le respect des priorités n'est pas négociable.",
        "acces": "Accès par la Corniche : on observe depuis l'esplanade, puis on descend vers la crique. Plage surveillée en juillet et août.",
        "astuce": "Prenez le temps de regarder depuis la Corniche, vraiment. Le pic se déplace et certaines sections, notamment vers le Killer, deviennent très peu profondes selon la marée.",
    },
    "les-conches-longeville": {
        "intro": "Un large beach break vendéen, avec des A-frames et des bancs qui se déplacent au fil des saisons. Le secteur est surtout connu par ce qui se trouve juste au sud : Bud Bud, et ses vagues nettement plus creuses.",
        "conditions": "Houles de sud-ouest à nord-ouest, vent de nord-est. Toutes les marées peuvent donner quelque chose selon les bancs. La saison utile va de septembre à juin, l'été étant souvent trop calme.",
        "niveau": "Débutant à intermédiaire en petit. Dès que les vagues creusent, mieux vaut avoir un vrai niveau intermédiaire. Une école de surf est installée sur place.",
        "dangers": "Bancs mobiles et quelques obstacles immergés à marée basse. La plage est longue, donc la foule se dilue vite même les bons jours.",
        "acces": "Grand parking gratuit à l'accès numéro 13, plage juste derrière. Poste de secours de mi-juin à mi-septembre.",
        "astuce": "Pour une session plus engagée, longez vers le sud jusqu'au secteur de Bud Bud. Et visez hors plein été : c'est là que les houles atlantiques arrivent vraiment.",
    },
    "la-torche": {
        "intro": "La Torche capte tout. C'est le spot le plus exposé de la baie d'Audierne, avec un long banc de sable qui donne des gauches et des droites, et parfois des sections qui déroulent sur une bonne distance. Quand rien ne marche en Bretagne, il reste souvent quelque chose ici.",
        "conditions": "Houles d'ouest à nord-ouest, vent d'est à sud-est. Toutes les marées passent, avec un automne et un hiver bien plus réguliers. Sur les grosses houles, le courant devient franchement fort et une partie des sections ferment.",
        "niveau": "Intermédiaire à confirmé. Un débutant peut y aller en petit, mais l'exposition et le courant rendent l'endroit moins indulgent qu'une plage abritée.",
        "dangers": "Le courant est le vrai sujet, notamment vers le nord de la plage. Ajoutez des bancs changeants et des rochers par endroits. Observez toujours où part l'eau avant d'entrer.",
        "acces": "Accès facile et parkings nombreux. La pointe est très fréquentée en saison.",
        "astuce": "Acceptez de marcher le long de la plage pour trouver le banc qui tient. Les jours solides, repérez d'abord le courant de sortie : il vous fera gagner beaucoup d'énergie.",
    },
    "la-palue-crozon": {
        "intro": "La Palue est une grande plage exposée de la presqu'île de Crozon, encadrée par des zones rocheuses. Beach break sur sable, mais avec des courants d'une autre catégorie que les plages abritées de la rade. C'est un endroit magnifique et exigeant.",
        "conditions": "Un spot d'automne et d'hiver, quand les houles atlantiques deviennent consistantes. Les conditions se jugent sur place : la taille et la direction changent complètement la physionomie de la plage d'un jour à l'autre.",
        "niveau": "Intermédiaire à expert. Dès qu'il y a de la houle, ce n'est pas un endroit pour apprendre. Morgat ou l'Aber remplissent bien mieux ce rôle.",
        "dangers": "Les courants ont une réputation solide, et elle est méritée. Rochers aux deux extrémités, récifs pas toujours visibles selon le niveau d'eau, et des obstacles signalés dans la partie sud. Ici, la sécurité passe avant la session.",
        "acces": "Route puis marche jusqu'à la plage. Parking disponible, mais aucune infrastructure une fois sur le sable.",
        "astuce": "Faites le tour des spots de Crozon avant de vous décider. Si La Palue est trop exposée, Morgat ou l'Aber offrent une alternative bien plus tolérante le même jour.",
    },
}
