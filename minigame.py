def luo_kentta():
    """Palauttaa pienen 3x3-ruudukon ja aloituspisteen."""
    return {
        "koko": 3,
        "alku": (0, 0),
        "esteet": [(1, 1)],  # Ruutu, johon ei voi astua
    }


def tarkista_polku(reitti, kentta=None):
    """Tarkistaa, muodostaako pelaajan reitti kelvollisen Hamiltonin polun."""
    if kentta is None:
        kentta = luo_kentta()

    koko = kentta["koko"]
    esteet = set(kentta["esteet"])
    kaikki_ruudut = {
        (r, c)
        for r in range(koko)
        for c in range(koko)
        if (r, c) not in esteet
    }

    if not reitti or reitti[0] != kentta["alku"]:
        return False, "Reitin täytyy alkaa aloituspisteestä."

    # Tarkistetaan ettei samassa ruudussa käydä kahdesti
    if len(reitti) != len(set(reitti)):
        return False, "Samassa ruudussa ei saa käydä kahdesti."

    # Tarkistetaan että jokainen askel on sallittu (ylös, alas, vasen, oikea)
    for edellinen, nykyinen in zip(reitti, reitti[1:]):
        if nykyinen in esteet or nykyinen not in kaikki_ruudut:
            return False, "Reitti kulkee ruudukon ulkopuolelle tai esteeseen."
        etaisyys = abs(edellinen[0] - nykyinen[0]) + abs(edellinen[1] - nykyinen[1])
        if etaisyys != 1:
            return False, "Siirtymä saa olla vain yksi ruutu pysty- tai vaakasuunnassa."

    # Tarkistetaan onko kaikki vapaat ruudut kierretty
    if set(reitti) != kaikki_ruudut:
        return False, "Kaikkia ruutuja ei ole vielä kierretty."

    return True, "Onnittelut! Löysit Hamiltonin polun."s