# Import de la classe Flask du module flask
from flask import Flask, render_template, session, redirect
# Import de la liste questions
from questions import questions
import os
# Création d'une instance de la classe Flask = notre app
app = Flask("Ma première App")
# On crée notre clef de sécurité de 24 octets avec urandom (valeur aléatoire)
app.secret_key = os.urandom(24)



# On crée notre premier qui sera l'URL racine /, la fonction index sera appelée
# On renvoit ce que la fonction index renvoie.
@app.route("/")
def index():
    session["numero_question"] = 0
    session["score"] = { "Pikachu" :0, "Mew": 0, "Salamèche": 0,"Carapuce": 0}
    return render_template("index.html")


# route pour la seconde page
@app.route("/question")
def question():
    # On accède à la variable globale questions
    global questions

    # On récupère le cookie question qui nous permet de sevoir à quelle question on est
    numero = session["numero_question"]
    # On vérifie s'il reste des questions
    if numero < len(questions):
        # On récupère l'énoncé de la question
        enonce_question = questions[numero]["enonce"]
        # On crée une copie de notre dictionnaire contenant la question et les reponses
        question_copy = questions[numero].copy()
        # On supprime l'enoncé de la question
        question_copy.pop("enonce")
        # On récupère les réponses sous forme de liste
        reponses = list(question_copy.values())
        # On récupère également les clefs pour les scores
        clefs = list(question_copy.keys())
        # On stocke l'ordre des clefs dans un cookie pour le comptage des scores
        session["clefs"] = clefs
        # On affiche notre page question.html
        return render_template("question.html", question = enonce_question, reponses = reponses)
    else:
        # On trie le score de manière décroissante
        score_trie = sorted(session["score"], key = session["score"].get ,reverse = True)
        # On récupère le vainqueur
        vainqueur = score_trie[0]
        return render_template("resultat.html", vainqueur = vainqueur)

# On crée notre route reponse
@app.route("/reponse/<numero>")
def reponse(numero):
    # On incrémente numéro question pour passer à la questions suivante
    session["numero_question"] += 1
    # On sélectionne le personnage dont la réponse a été sélectionnée avec le dico des clefs
    personnage = session["clefs"][int(numero)]
    # On incrémente les scores selon le personnage
    session["score"][personnage] += 1
    return redirect("/question")




# Execution de l'application
# host='0.0.0.0' -> le serveur Flask ecoute sur toutes les adresses IP
# port = 81 -> port d'écoute de l'app avec lequel on accède à l
app.run(host='0.0.0.0', port = 81)






