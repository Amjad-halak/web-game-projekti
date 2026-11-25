import json
import os
from flask import Flask, render_template, request, jsonify
import minigame

app = Flask(__name__)
TIEDOSTO = "data/scores.json"


def lue_pisteet():
    if not os.path.exists(TIEDOSTO):
        return {"players": []}
    with open(TIEDOSTO, "r", encoding="utf-8") as f:
        return json.load(f)


def tallenna_pisteet(data):
    if not os.path.exists("data"):
        os.mkdir("data")
    with open(TIEDOSTO, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/player", methods=["POST"])
def aseta_pelaaja():
    tiedot = request.get_json()
    nimi = tiedot.get("nickname", "").strip()
    avatar = tiedot.get("avatar", "avatar1")

    if nimi == "":
        return jsonify({"error": "Nimimerkki puuttuu"}), 400

    data = lue_pisteet()

    for pelaaja in data["players"]:
        if pelaaja["nickname"].lower() == nimi.lower():
            pelaaja["avatar"] = avatar
            tallenna_pisteet(data)
            return jsonify(pelaaja)

    uusi_pelaaja = {
        "nickname": nimi,
        "avatar": avatar,
        "total_score": 0,
        "games": {
            "game1": {"best_score": 0, "played": 0},
            "game2": {"best_score": 0, "played": 0}
        }
    }
    data["players"].append(uusi_pelaaja)
    tallenna_pisteet(data)
    return jsonify(uusi_pelaaja), 201


@app.route("/api/score", methods=["POST"])
def lisaa_pisteet():
    tiedot = request.get_json()
    nimi = tiedot.get("nickname", "").strip()
    peli = tiedot.get("game", "game1")
    vaikeustaso = tiedot.get("difficulty", "easy").lower()
    voitti = tiedot.get("won", False)

    saadut_pisteet = 0
    if voitti:
        if vaikeustaso == "easy":
            saadut_pisteet = 10
        elif vaikeustaso == "medium":
            saadut_pisteet = 20
        elif vaikeustaso == "hard":
            saadut_pisteet = 30

    data = lue_pisteet()

    for pelaaja in data["players"]:
        if pelaaja["nickname"].lower() == nimi.lower():
            # Lisätään pisteet kokonaispottiin
            pelaaja["total_score"] += saadut_pisteet

            # Päivitetään pelikohtaiset tilastot
            if peli not in pelaaja["games"]:
                pelaaja["games"][peli] = {"best_score": 0, "played": 0}

            pelaaja["games"][peli]["played"] += 1
            if saadut_pisteet > pelaaja["games"][peli]["best_score"]:
                pelaaja["games"][peli]["best_score"] = saadut_pisteet

            tallenna_pisteet(data)
            return jsonify({
                "earned": saadut_pisteet,
                "total_score": pelaaja["total_score"],
                "game_stats": pelaaja["games"][peli]
            })

    return jsonify({"error": "Pelaajaa ei löytynyt"}), 404


@app.route("/api/leaderboard", methods=["GET"])
def hae_pistetaulukko():
    data = lue_pisteet()
    pelaajat = data["players"]
    pelaajat.sort(key=lambda p: p["total_score"], reverse=True)
    return jsonify(pelaajat[:10])

@app.route("/api/minigame/kentta", methods=["GET"])
def hae_minigame_kentta():
    kentta = minigame.luo_kentta()
    return jsonify({
        "koko": kentta["koko"],
        "alku": list(kentta["alku"]),
        "esteet": [list(e) for e in kentta["esteet"]],
    })


@app.route("/api/minigame/tarkista", methods=["POST"])
def tarkista_minigame_reitti():
    data = request.get_json() or {}
    raaka_reitti = data.get("reitti", [])
    reitti = [tuple(p) for p in raaka_reitti]

    ok, viesti = minigame.tarkista_polku(reitti)
    return jsonify({"ok": ok, "viesti": viesti})
if __name__ == "__main__":
    app.run(debug=True)