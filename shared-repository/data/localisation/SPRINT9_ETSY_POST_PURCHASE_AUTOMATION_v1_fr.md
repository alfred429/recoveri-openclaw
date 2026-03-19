# RecoveriStudio — Automatisation Post-Achat
## Version 1.0 | 18 Mars 2026 | Session 11
## Statut : BOUGUE — À revoir par le responsable
## Objectif : Message proactif pour éliminer les tickets de support Bucket A et B avant qu’ils n’apparaissent

---

## Qu’est-ce que C’est

Un message proactif envoyé à chaque acheteur après l’achat. Etsy permet aux vendeurs d’envoyer un message automatique par commande. Ce message :

1. Remercie le client
2. Lui fournit les instructions de téléchargement (évite les tickets Bucket A)
3. Explique ce qu’il a acheté et comment l’utiliser (évite les tickets Bucket B)
4. Propose un canal de support (détecte tout autre problème au plus tôt)
5. Encourage l’engagement futur (liste d’emails, achats répétés)

---

## Modèle de Message Post-Achat

### Configuration dans : Etsy > Boutique Manager > Paramètres > Informations et Apparence > Message aux Acheteurs

```
Merci pour votre achat sur RecoveriStudio !

VOS FICHIERS SONT PRÊTS À ÊTRE TÉLÉCHARGÉS

1. Consultez votre boîte email pour obtenir le lien de téléchargement d’Etsy
2. Ou allez à : Votre Compte > Achats > trouvez cette commande > cliquez sur "Télécharger les fichiers"
3. Les liens de téléchargement sont valables pendant 30 jours

Si vous avez payé avec PayPal, cela peut prendre quelques minutes supplémentaires - vérifiez votre dossier "Spam" si nécessaire.

CE QU'IL Y A DENTRE

Votre téléchargement contient : [cette section affichera automatiquement la description de la fiche Etsy]

Si les fichiers sont dans un dossier ZIP :
- Windows : cliquez droit > "Extraire tout"
- Mac : double-cliquez pour une extraction automatique

BESOIN D'AIDE ?

Répondez à ce message et nous vous répondrons dans les 2 heures. Nous sommes là pour les problèmes de téléchargement, les questions de compatibilité, ou tout autre besoin.

Profitez de vos nouveaux outils !
— L'Équipe RecoveriStudio
```

---

## Notes de Configuration Etsy

*   Etsy "Message aux Acheteurs" est envoyé automatiquement avec chaque confirmation de commande
*   Il s’agit du MÊME message pour tous les produits (vous ne pouvez pas le personnaliser par fiche)
*   Gardez-le suffisamment générique pour fonctionner avec n’importe quel type de produit
*   Longueur maximale : 2 000 caractères (le modèle ci-dessus est d’environ 850)
*   Le message apparaît dans la boîte de réception des messages Etsy du client

---

## Améliorations Futures (non incluses pour le moment – après les premières ventes)

### Phase 2 – Capture de la Liste d’Emails (lorsque recoveri.io sera en ligne)

Ajouter au message post-achat :

```
OFFRE EXCLUSIVE

Rejoignez notre liste d’emails pour bénéficier d’une réduction de 20 % sur votre prochaine commande :
recoveri.io/exclusive

Vous bénéficierez également d’un accès anticipé aux nouveaux produits et de ressources gratuites.
```

Cela est conforme aux règles d’Etsy : vous ne les envoyez pas d’emails, vous les invitez volontairement à s’inscrire via votre propre site web.

### Phase 3 – Téléchargement PDF de Suivi

Inclure un PDF d’une page dans chaque ZIP de produit contenant :

*   Instructions de téléchargement et de configuration avec captures d’écran
*   FAQ pour ce type de produit spécifique
*   Lien vers recoveri.io pour les ressources
*   Informations de contact pour le support

Ce PDF agit comme une "couche de prévention in-product" : le client le voit même s’il saute le message d’Etsy.

---

## Impact de la Prévention

| Bucket | Comment cela évite les tickets de support |
|---|---|
| A – Téléchargement et Accès | Les étapes 1-3 couvrent le téléchargement, l’extraction ZIP, le délai PayPal |
| B – Compréhension du produit | La section "Ce qu'il y a dedans" + la description du fichier |
| A + B combinés | "Besoin d'aide ?" détecte tout ce que les instructions ont manqué, AVANT que le client ne se frustre |

Objectif : réduire les tickets Bucket A de 40-50 % au cours du premier mois.

---

*Automatisation Post-Achat v1 | Session 11 | 18 Mars 2026*
*Aligné à : Cadre CS v2 Contrôles de Prévention, Compétence 132 Stratégie de Marque v1 (phase 2 de capture d’emails)*