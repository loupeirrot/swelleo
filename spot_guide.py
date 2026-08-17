#!/usr/bin/env python3
"""Contenu éditorial par spot, rendu sur les fiches /spots/<slug>/.

Source : notes de terrain + recherches croisées (offices de tourisme, guides locaux).
Champs par spot :
  intro      — ce qui fait le spot (paragraphe d'accroche)
  conditions — quand ça marche vraiment / quand c'est nul
  niveau     — pour qui, quel type de planche
  dangers    — les pièges
  acces      — parking, accès, affluence
  astuce     — le réflexe local
"""

SPOT_GUIDE = {
    "la-nord-hossegor": {
        "intro": "Beach break mythique d'Hossegor, réputé pour ses vagues rapides, puissantes et creuses. Le banc peut produire des barrels de très haut niveau, et le Gouf de Capbreton — canyon sous-marin qui vient mourir juste devant la plage — contribue à concentrer l'énergie de la houle.",
        "conditions": "Meilleur avec une houle d'Ouest à Nord-Ouest et un vent d'Est (offshore). La qualité dépend énormément du banc du moment et de la marée. C'est nul quand la houle est mal orientée ou que le vent bascule onshore : le spot ferme et devient un mur d'écume.",
        "niveau": "Confirmé à expert dès que ça pousse. Shortboard principalement. Les petites conditions peuvent convenir à un niveau intermédiaire, mais ce n'est pas un spot d'apprentissage.",
        "dangers": "Rouleaux de bord, courants d'arrachement et bancs qui changent vite. Shore-break puissant et faible profondeur quand ça creuse. Affluence importante et niveau élevé dans l'eau.",
        "acces": "Accès depuis le front de mer d'Hossegor, parkings urbains à proximité. Forte affluence en saison : viser tôt le matin ou hors saison.",
        "astuce": "Regarder plusieurs séries avant de se mettre à l'eau : à Hossegor, le banc qui paraît parfait depuis la plage peut fermer quelques dizaines de mètres plus loin.",
    },
    "la-graviere-hossegor": {
        "intro": "L'un des beach breaks les plus célèbres d'Europe : vague très rapide, creuse et puissante, avec de vrais tubes qui déferlent près du bord. La plage est proche de la place des Landais mais garde une configuration de spot de surf pur.",
        "conditions": "Houle de Nord-Ouest et vent d'Est : les conditions de référence. Elle devient vraiment intéressante avec une houle consistante ; les petites conditions restent surfables mais lui font perdre tout son intérêt.",
        "niveau": "Confirmé à expert — débutants s'abstenir. La vague déferle vite, dans peu d'eau. Shortboard ou bodyboard plutôt que longboard quand le spot fonctionne.",
        "dangers": "Rouleaux de bord très puissants, courants d'arrachement, faible profondeur. Le piège classique est de sous-estimer la vitesse de la vague et la violence du shore-break. Spot fréquenté par des surfeurs expérimentés.",
        "acces": "Accès direct depuis Hossegor, proche des commerces de la place des Landais. Plage surveillée en saison.",
        "astuce": "Si La Gravière paraît trop grosse ou trop fermée, ne pas insister : regarder les spots voisins avant de se mettre à l'eau.",
    },
    "les-estagnots-seignosse": {
        "intro": "Beach break à bancs de sable très réputé, capable de produire de longues parois à marée basse et des vagues creuses et rapides à marée haute. L'un des spots les plus constants de Seignosse, avec droites et gauches.",
        "conditions": "Houle d'Ouest à Nord-Ouest — idéalement NO — et vent d'Est à Est-Sud-Est. Fonctionne à toutes les marées : marée basse donne des murs plus longs, marée haute un shore-break plus creux et parfois brutal. Automne et hiver (septembre à février) pour la meilleure régularité.",
        "niveau": "Intermédiaire à expert selon la taille. Accessible aux débutants seulement dans de petites conditions et sur les pics adaptés. Shortboard, fish et bodyboard ; longboard possible quand c'est petit.",
        "dangers": "Baïnes, courants d'arrachement et dérive latérale, qui deviennent très forts avec la taille. Shore-break potentiellement violent à marée haute. Spot souvent très fréquenté.",
        "acces": "Grand parking gratuit dans les dunes, accès très court à la plage. Écoles de surf, restauration, sanitaires et poste de secours sur place. En été, arriver tôt : le stationnement est très demandé.",
        "astuce": "Quand le spot est plein, marcher quelques centaines de mètres change complètement la qualité du pic et la densité. Mieux vaut chercher le banc qui fonctionne que s'accrocher au pic principal.",
    },
    "santocha-capbreton": {
        "intro": "Beach break sur sable, multi-pics avec droites et gauches. Le Gouf de Capbreton influence la bathymétrie et les bancs : le spot atténue une partie des grosses houles tout en restant assez régulier.",
        "conditions": "Pour débuter : 0,5 à 1 m, vent faible ou offshore d'Est, mi-marée. Pour les confirmés : 1 à 2 m et plus, vent d'Est à Nord-Est, plutôt de basse à mi-marée montante. Automne-hiver nettement plus consistant.",
        "niveau": "Tous niveaux selon les conditions. Très bon choix pour débutants et intermédiaires dans les petites tailles. Shortboard, fish et longboard selon le banc.",
        "dangers": "Fond sableux, mais baïnes et courants présents, et baigneurs en été. La dérive peut devenir importante quand la houle monte. Le vrai risque est de choisir un pic trop gros pour son niveau.",
        "acces": "Parking gratuit à proximité, mais vite plein en été. Accès facile à pied ou à vélo depuis Capbreton. Le matin est conseillé pour éviter la foule ; surveillance en saison.",
        "astuce": "Le spot est multi-pics : ne pas se focaliser sur le premier pic visible depuis l'accès. Quelques dizaines de mètres suffisent souvent à trouver une vague bien plus adaptée.",
    },
    "la-piste-capbreton": {
        "intro": "Beach break puissant de Capbreton, réputé pour ses tubes. La vague gagne en taille et en puissance en allant vers le sud : les gros jours, elle rivalise avec les spots majeurs d'Hossegor.",
        "conditions": "Meilleure avec une houle consistante, environ 1 à 2 m et plus selon le banc, plutôt à marée basse, avec un vent d'Est offshore. Quand la houle devient trop grosse ou que les bancs ferment, le spot devient très difficile.",
        "niveau": "Intermédiaire à expert, confirmé dès que la houle est importante. Shortboard ou bodyboard. Pas un spot d'apprentissage.",
        "dangers": "Courants, baïnes, shore-break et vagues creuses puissantes. Les bancs sont irréguliers et la taille augmente vers le sud.",
        "acces": "Parking gratuit à proximité, capacité limitée en saison. Accès court depuis la route. Tôt le matin ou hors saison pour éviter le monde.",
        "astuce": "Regarder la plage vers le sud avant de choisir son pic : quelques centaines de mètres font une grosse différence de taille et de puissance.",
    },
    "cote-des-basques-biarritz": {
        "intro": "Spot historique, considéré comme le berceau du surf en France. Grande plage de sable encaissée entre les falaises ; la partie nord, plus douce, est le terrain de jeu des longboarders.",
        "conditions": "Petites à moyennes houles de Nord-Ouest à Ouest, vent d'Est à Sud-Est. Le spot fonctionne jusqu'à environ trois quarts de marée : la plage disparaît complètement à marée haute, en particulier avec des coefficients supérieurs à 45. L'automne, de septembre à novembre, est souvent la meilleure période.",
        "niveau": "Débutant à intermédiaire sur petites conditions, confirmé quand la houle grossit. Longboard très adapté dans la partie nord ; shortboard quand les vagues prennent de la puissance.",
        "dangers": "La plage disparaît à marée haute : surveiller impérativement son heure de sortie. Affluence importante l'été, nombreux débutants, et quelques rochers dans la partie sud.",
        "acces": "Parking de plage difficile en saison. Le parking en haut de la falaise, avenue Beau Rivage, est une bonne option, avec descente à pied par le chemin en lacets. Surveillance de mai à septembre.",
        "astuce": "Le nord de la plage est le meilleur point de départ pour une session tranquille en petite houle. Attention au piège de la session qui commence bien : la marée monte vite et la plage disparaît.",
    },
    "les-cavaliers-anglet": {
        "intro": "Beach break majeur d'Anglet, connu pour ses A-frames rapides et creux, avec gauches et droites. Les digues et la proximité de l'Adour structurent les bancs de sable.",
        "conditions": "Houle d'Ouest à Nord-Ouest — idéalement NO à ONO — et vent d'Est. Le spot supporte mieux un léger Nord-Ouest qu'Hossegor. Marée moyenne idéale. Il devient vraiment intéressant à taille solide.",
        "niveau": "Intermédiaire à expert quand ça pousse. Shortboard principalement ; longboard possible sur les petites conditions et les pics plus doux d'Anglet.",
        "dangers": "Courants et dérive latérale, surtout avec la taille. Pics puissants, foule sur les meilleurs bancs et niveau élevé : observer avant de se placer et respecter les priorités.",
        "acces": "Accès urbain facile, parkings autour du secteur des Cavaliers. Affluence importante sur les bons jours et en été ; venir tôt facilite nettement le stationnement.",
        "astuce": "Anglet permet de changer de pic rapidement : si Les Cavaliers est trop gros ou trop venté, regarder les plages voisines avant de renoncer. Toute la côte se lit depuis les hauteurs.",
    },
    "hendaye": {
        "intro": "Grande baie très abritée par le cap du Figuier, orientée au nord : c'est LE spot de repli du Pays Basque. Fond sableux et pente progressive, avec plusieurs zones — Sokoburu, Casino, Digue — qui permettent d'adapter la session.",
        "conditions": "Fonctionne à toutes les marées. Une houle de Nord-Ouest moyenne à grosse peut rentrer alors que le reste de la côte est saturé ; vent de Sud favorable. Les petites houles donnent des vagues douces, parfaites pour débuter.",
        "niveau": "Débutant à intermédiaire. Excellent spot d'apprentissage et de perfectionnement. Longboard très adapté dans les petites conditions, shortboard quand la houle rentre.",
        "dangers": "Beaucoup moins de baïnes dangereuses que sur les plages landaises, mais un courant latéral est possible avec les entrées maritimes d'Ouest. Rochers à l'est, autour des Deux Jumeaux. Forte présence des écoles de surf.",
        "acces": "Accès très facile depuis la ville et le front de mer. Parkings payants le long du front de mer, très chargés en été : arriver tôt ou hors saison.",
        "astuce": "Quand la côte basque est trop grosse, Hendaye est le premier réflexe : la baie filtre fortement la houle. Le secteur Casino/Digue convient aux débutants ; Valencia fonctionne davantage à basse et mi-marée pour les intermédiaires.",
    },
    "lacanau-ocean": {
        "intro": "Long beach break de près de 14 km, avec une succession de bancs de sable et de digues qui structurent des pics droits et gauches. Le spot central est le cœur historique du surf à Lacanau et accueille des compétitions professionnelles depuis des décennies.",
        "conditions": "Houle d'Ouest à Nord-Ouest et vent d'Est. Fonctionne à toutes les marées, mais les bancs changent beaucoup : à marée basse, vagues plus rapides et creuses sur les bancs externes ; à montante, sections plus courtes et plus proches du bord. Automne-hiver (octobre à février) pour la régularité.",
        "niveau": "Débutant à expert selon le secteur et la taille. La plage centrale convient aux débutants dans de petites conditions ; les bancs nord sont plus creux et puissants.",
        "dangers": "Courants d'arrachement, notamment près des digues et des chenaux. Bancs très mobiles : une zone parfaite un jour peut être mauvaise le lendemain. Forte affluence l'été au centre.",
        "acces": "Accès simple, infrastructures nombreuses au centre : parkings, commerces, écoles, surveillance. En été, arriver tôt. Les secteurs nord et sud demandent parfois une marche depuis les parkings.",
        "astuce": "Ne pas considérer Lacanau comme un seul spot : regarder plusieurs centaines de mètres de côte avant de choisir. Les bancs sont très différents entre le centre, le nord et le sud.",
    },
    "le-porge-ocean": {
        "intro": "Très longue plage sauvage d'environ 13 km, avec une succession de bancs de sable. Le caractère naturel du littoral permet de chercher son pic, mais les bancs sont réputés particulièrement capricieux.",
        "conditions": "Beach break très exposé : le choix se fait selon le banc du jour, avec un vent offshore d'Est. Après une grosse houle, certains bancs peuvent complètement fermer.",
        "niveau": "Plutôt intermédiaire à confirmé, surtout parce qu'il faut savoir lire les bancs et les courants. Débutant uniquement dans de petites conditions et dans la zone surveillée.",
        "dangers": "Baïnes et courants d'arrachement : c'est le vrai sujet de sécurité du secteur. Les bancs irréguliers rendent la lecture difficile et l'océan reste très exposé.",
        "acces": "Accès par Le Porge-Océan, avec parkings et accès aménagés ; la plage du Gressier est le principal point d'information. Affluence autour des accès principaux en été.",
        "astuce": "La meilleure astuce ici, c'est de marcher : 13 km de plage permettent de sortir de la zone fréquentée. Toujours repérer les baïnes avant d'entrer, et privilégier la zone surveillée en saison.",
    },
    "cap-ferret": {
        "intro": "Ce n'est pas un spot mais une longue côte atlantique ponctuée d'accès : Grand Crohot, Truc Vert, Petit Crohot. Des beach breaks sur sable, aux bancs mobiles, souvent capables de produire des A-frames et de belles sections creuses.",
        "conditions": "Au Grand Crohot : houle d'Ouest à Nord-Ouest, vent d'Est, et fonctionnement à plusieurs marées selon le banc. Automne-hiver plus régulier. Au-delà d'environ 2 m, les bancs externes peuvent fermer.",
        "niveau": "Débutant à confirmé selon la taille et le pic. Les petites houles estivales conviennent aux débutants ; dès que ça creuse, niveau intermédiaire minimum.",
        "dangers": "Baïnes et courants d'arrachement, bancs très irréguliers et changements fréquents. Le Grand Crohot est particulièrement fréquenté le week-end et en été.",
        "acces": "Grand Crohot : grand parking derrière la dune, puis environ 5 minutes à pied sur les caillebotis. Truc Vert et les autres accès demandent davantage de marche.",
        "astuce": "Ici, trouver le bon banc compte plus que suivre une règle de marée. Regarder plusieurs pics depuis la dune avant de choisir, et ne pas hésiter à marcher quelques centaines de mètres.",
    },
    "la-sauzaie-bretignolles": {
        "intro": "Spot de reef rocheux emblématique de Vendée, célèbre pour ses vagues rapides, puissantes et creuses. C'est un spot de compétition, capable de produire de très gros barrels sur le bon swell.",
        "conditions": "Houle consistante et propre, vent d'Est à Nord-Est offshore. La marée haute à montante est généralement privilégiée, car de nombreux rochers découvrent à basse mer — ce qui augmente nettement le risque sur le reef.",
        "niveau": "Intermédiaire à expert, clairement réservé aux surfeurs à l'aise sur un reef peu profond dès que ça pousse. Shortboard principalement.",
        "dangers": "Rochers, reef peu profond, take-off rapide et sections qui ferment. À marée basse, de nombreux rochers découvrent. Pic très compétitif et forte densité sur les bons swells.",
        "acces": "Accès par la Corniche, avec un point de vue depuis l'esplanade puis une descente vers la crique. Plage surveillée en juillet-août.",
        "astuce": "Observer longtemps depuis la Corniche avant d'aller à l'eau : le pic se déplace et certaines sections, notamment vers le « Killer », deviennent très peu profondes. Respect strict des priorités.",
    },
    "les-conches-longeville": {
        "intro": "Large beach break de la côte vendéenne, avec des pics en A-frame et des bancs de sable mobiles. Le secteur est surtout connu pour sa proximité avec Bud Bud, au sud, réputé pour ses vagues creuses.",
        "conditions": "Houles de Sud-Ouest à Nord-Ouest, vent de Nord-Est offshore. Fonctionne à toutes les marées selon les bancs, avec une saison plus régulière de septembre à juin. L'été est souvent plus calme.",
        "niveau": "Débutant à intermédiaire sur petites conditions ; intermédiaire recommandé quand les vagues deviennent creuses et puissantes. École de surf sur place.",
        "dangers": "Bancs de sable mobiles et quelques dangers immergés à marée basse. Affluence possible sur les bons jours, mais la plage est longue.",
        "acces": "Grand parking gratuit à l'accès n°13, avec accès direct à la plage. Poste de secours et surveillance de mi-juin à mi-septembre. Arriver tôt pendant les vacances.",
        "astuce": "Pour une session plus engagée, longer vers le sud jusqu'au secteur de Bud Bud. Les meilleures conditions sont généralement hors plein été, quand les houles atlantiques sont plus consistantes.",
    },
    "la-torche": {
        "intro": "Beach break très exposé et très consistant de la baie d'Audierne, avec un long banc de sable capable de produire gauches et droites ; certaines sections déroulent sur une grande distance.",
        "conditions": "Houles d'Ouest à Nord-Ouest, vent d'Est à Sud-Est offshore. Fonctionne à toutes les marées, avec un automne-hiver nettement plus régulier. Sur les grosses houles, le courant devient très fort et des sections ferment.",
        "niveau": "Intermédiaire à confirmé. Accessible aux débutants dans de petites conditions, mais l'exposition et le courant rendent le spot moins tolérant que les plages abritées.",
        "dangers": "Courants parfois puissants, bancs changeants et rochers par endroits. Affluence importante les bons week-ends et en été. Toujours observer les courants avant d'entrer.",
        "acces": "Accès facile et nombreux parkings. La pointe est très fréquentée en saison. Matin tôt ou semaine hors vacances pour éviter la foule.",
        "astuce": "La Torche peut être excellente quand d'autres spots bretons ne marchent pas, mais il faut accepter de bouger sur la plage pour trouver le banc qui tient. Les jours solides, repérer le courant de sortie avant tout.",
    },
    "la-palue-crozon": {
        "intro": "Grande plage très exposée de la presqu'île de Crozon : un beach break sur sable, encadré par des zones rocheuses. Connue pour ses vagues et ses courants nettement plus exigeants que les spots abrités de la baie.",
        "conditions": "Plutôt un spot d'automne et d'hiver, quand les houles atlantiques sont consistantes. Les conditions dépendent fortement de la taille et de la direction de houle : c'est un spot qui se juge sur place.",
        "niveau": "Intermédiaire à expert. Débutants déconseillés dès que la houle est présente : mieux vaut aller apprendre à Morgat ou à l'Aber.",
        "dangers": "Courants réputés difficiles, rochers aux extrémités et récifs parfois peu visibles selon le niveau d'eau. Des obstacles sont également signalés dans la partie sud. La sécurité est le vrai sujet du spot.",
        "acces": "Accès routier puis marche jusqu'à la plage. Parking disponible, mais peu d'infrastructures directement sur place.",
        "astuce": "Vérifier plusieurs spots de Crozon avant de choisir La Palue : si elle est trop exposée, Morgat ou l'Aber offrent une solution beaucoup plus tolérante. Ne jamais entrer sans avoir repéré le courant et les rochers.",
    },
}
