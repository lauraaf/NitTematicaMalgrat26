import streamlit as st
import random
import json
import os

# =========================================================
# CONFIGURACIÓ
# =========================================================

st.set_page_config(
    page_title="Nit Temàtica Malgrat '26",
    page_icon="🎭",
    layout="centered"
)

NOIS = ["Barat", "Pau", "Pol", "Oriol", "Macià", "Roc"]
NOIES = ["Laura", "Clàudia", "Lidia", "Caty"]

# De moment posem PINs manualment.
# Després els podem generar automàticament des de la zona admin.
PINS = {
    "Barat": "4821",
    "Pau": "7354",
    "Pol": "2196",
    "Oriol": "8642",
    "Macià": "3517",
    "Roc": "9273",
    "Laura": "6048",
    "Clàudia": "1735",
    "Lidia": "5489",
    "Caty": "3164"
}

ADMIN_PASSWORD = "malgrat26"

FITXER_SORTEIG = "sorteig.json"


# =========================================================
# FUNCIONS
# =========================================================

def guardar_sorteig(sorteig):
    """Guarda el sorteig en un fitxer JSON."""

    with open(FITXER_SORTEIG, "w", encoding="utf-8") as fitxer:
        json.dump(
            sorteig,
            fitxer,
            ensure_ascii=False,
            indent=4
        )


def carregar_sorteig():
    """Carrega el sorteig si ja existeix."""

    if not os.path.exists(FITXER_SORTEIG):
        return None

    with open(FITXER_SORTEIG, "r", encoding="utf-8") as fitxer:
        return json.load(fitxer)


def generar_sorteig():
    """
    Genera el sorteig.

    - Cada noi rep una noia.
    - Cada noia rep un noi.
    - Els sortejos són independents.
    - Les noies es reparteixen de manera equilibrada.
    - S'eviten parelles recíproques.
    """

    # -----------------------------------------------------
    # NOIS -> NOIES
    # -----------------------------------------------------

    # Tenim 6 nois i 4 noies.
    # Creem una llista equilibrada:
    #
    # 4 noies apareixen una vegada
    # + 2 noies apareixen una segona vegada

    noies_assignades = NOIES.copy()

    noies_extra = random.sample(
        NOIES,
        len(NOIS) - len(NOIES)
    )

    noies_assignades.extend(noies_extra)

    random.shuffle(noies_assignades)

    sorteig_nois = {}

    for noi, noia in zip(NOIS, noies_assignades):
        sorteig_nois[noi] = noia

    # -----------------------------------------------------
    # NOIES -> NOIS
    # -----------------------------------------------------
    #
    # Volem que:
    #
    # Laura -> X
    #
    # però si X -> Laura,
    # NO volem Laura -> X.
    #
    # Així evitem parelles recíproques.
    # -----------------------------------------------------

    intents = 0

    while True:

        intents += 1

        # Cada noia tindrà un noi diferent
        nois_assignats = random.sample(
            NOIS,
            len(NOIES)
        )

        sorteig_noies = dict(
            zip(NOIES, nois_assignats)
        )

        reciproc = False

        for noia, noi in sorteig_noies.items():

            if sorteig_nois[noi] == noia:
                reciproc = True
                break

        if not reciproc:
            break

        # Protecció per si alguna cosa estranya passés
        if intents > 10000:
            raise Exception(
                "No s'ha pogut generar un sorteig vàlid."
            )

    # Unim els dos sortejos

    sorteig = {}

    sorteig.update(sorteig_nois)
    sorteig.update(sorteig_noies)

    return sorteig


# =========================================================
# INTERFÍCIE
# =========================================================

st.title("🎭 Nit Temàtica Malgrat '26")

st.write(
    "Descobreix de qui t'hauràs de vestir aquesta nit 👀"
)

st.divider()


# =========================================================
# CONSULTAR RESULTAT
# =========================================================

st.subheader("🎟️ Consulta el teu sorteig")

participants = NOIS + NOIES

persona = st.selectbox(
    "Qui ets?",
    ["Selecciona el teu nom"] + participants
)

pin = st.text_input(
    "Introdueix el teu PIN",
    type="password",
    max_chars=4
)

if st.button(
    "👀 Descobrir qui m'ha tocat",
    use_container_width=True
):

    sorteig = carregar_sorteig()

    if persona == "Selecciona el teu nom":

        st.warning(
            "Selecciona primer el teu nom."
        )

    elif pin != PINS[persona]:

        st.error(
            "❌ El PIN no és correcte."
        )

    elif sorteig is None:

        st.warning(
            "⏳ Encara no s'ha fet el sorteig."
        )

    else:

        resultat = sorteig[persona]

        st.balloons()

        st.success(
            f"🎉 **{persona}**, t'ha tocat..."
        )

        st.markdown(
            f"""
            ## 🎭 {resultat}
            """
        )

        st.info(
            "🤫 No ho expliquis als altres!"
        )


# =========================================================
# ZONA ADMIN
# =========================================================

st.divider()

with st.expander("🔐 Zona administrador"):

    password = st.text_input(
        "Contrasenya d'administrador",
        type="password"
    )

    if password == ADMIN_PASSWORD:

        st.success("Administrador identificat.")

        sorteig_actual = carregar_sorteig()

        if sorteig_actual is None:

            st.info(
                "Encara no s'ha fet cap sorteig."
            )

        else:

            st.warning(
                "⚠️ Ja existeix un sorteig."
            )

        if st.button(
            "🎲 Fer un nou sorteig",
            use_container_width=True
        ):

            nou_sorteig = generar_sorteig()

            guardar_sorteig(nou_sorteig)

            st.success(
                "✅ Sorteig realitzat correctament!"
            )

            st.rerun()

        # -------------------------------------------------
        # RESULTATS ADMIN
        # -------------------------------------------------

        sorteig_actual = carregar_sorteig()

        if sorteig_actual:

            st.subheader("👑 Resultats del sorteig")

            st.caption(
                "Aquesta informació només apareix a la zona administrador."
            )

            st.write("### 👦 Nois")

            for noi in NOIS:

                st.write(
                    f"**{noi}** → {sorteig_actual[noi]}"
                )

            st.write("### 👧 Noies")

            for noia in NOIES:

                st.write(
                    f"**{noia}** → {sorteig_actual[noia]}"
                )

            st.divider()

            st.write("### 🔑 PINs")

            for persona_nom, persona_pin in PINS.items():

                st.write(
                    f"**{persona_nom}:** `{persona_pin}`"
                )

    elif password:

        st.error(
            "Contrasenya incorrecta."
        )