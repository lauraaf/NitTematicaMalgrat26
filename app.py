import streamlit as st
import random

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

PARTICIPANTS = NOIS + NOIES


# =========================================================
# FUNCIONS
# =========================================================

def generar_sorteig():
    """
    Cada noi rep una noia.
    Cada noia rep un noi.
    No hi ha parelles recíproques.
    Les repeticions de les noies són equilibrades.
    """

    # -----------------------------
    # NOIS -> NOIES
    # -----------------------------

    noies_assignades = NOIES.copy()

    # Com tenim 6 nois i 4 noies,
    # dues noies apareixeran dues vegades.
    extres = random.sample(
        NOIES,
        len(NOIS) - len(NOIES)
    )

    noies_assignades.extend(extres)

    random.shuffle(noies_assignades)

    sorteig_nois = dict(
        zip(NOIS, noies_assignades)
    )

    # -----------------------------
    # NOIES -> NOIS
    # -----------------------------

    while True:

        nois_assignats = random.sample(
            NOIS,
            len(NOIES)
        )

        sorteig_noies = dict(
            zip(NOIES, nois_assignats)
        )

        # Comprovem que no hi hagi
        # cap parella recíproca.
        reciproc = False

        for noia, noi in sorteig_noies.items():

            if sorteig_nois[noi] == noia:
                reciproc = True
                break

        if not reciproc:
            break

    sorteig = {}

    sorteig.update(sorteig_nois)
    sorteig.update(sorteig_noies)

    return sorteig


def obtenir_sorteig():
    """
    Llegeix el sorteig guardat als secrets.
    """

    if "sorteig" not in st.secrets:
        return None

    if not st.secrets["sorteig"].get("actiu", False):
        return None

    resultat = {}

    for persona in PARTICIPANTS:

        if persona in st.secrets["sorteig"]:
            resultat[persona] = st.secrets["sorteig"][persona]

    if len(resultat) != len(PARTICIPANTS):
        return None

    return resultat


# =========================================================
# CAPÇALERA
# =========================================================

st.title("🎭 Nit Temàtica Malgrat '26")

st.write(
    "Introdueix el teu nom i el teu PIN per descobrir "
    "de qui t'hauràs de vestir 👀"
)

st.divider()


# =========================================================
# CONSULTAR RESULTAT
# =========================================================

st.subheader("🎟️ Descobreix qui t'ha tocat")

persona = st.selectbox(
    "Qui ets?",
    ["Selecciona el teu nom"] + PARTICIPANTS
)

pin = st.text_input(
    "PIN",
    type="password",
    max_chars=4,
    placeholder="••••"
)

if st.button(
    "🎭 Descobrir el meu resultat",
    use_container_width=True
):

    if persona == "Selecciona el teu nom":

        st.warning(
            "Selecciona primer el teu nom."
        )

    elif pin != str(st.secrets["pins"][persona]):

        st.error(
            "❌ El PIN no és correcte."
        )

    else:

        sorteig = obtenir_sorteig()

        if sorteig is None:

            st.info(
                "⏳ El sorteig encara no s'ha fet."
            )

        else:

            resultat = sorteig[persona]

            st.balloons()

            st.markdown(
                f"""
                ### 🎉 {persona}, t'ha tocat...

                # 🎭 {resultat}
                """
            )

            st.info(
                "🤫 Guarda el secret!"
            )


# =========================================================
# ZONA ADMIN
# =========================================================

st.divider()

with st.expander("⚙️ Administrador"):

    password = st.text_input(
        "Contrasenya d'administrador",
        type="password",
        key="admin_password"
    )

    if password:

        if password != st.secrets["admin_password"]:

            st.error(
                "Contrasenya incorrecta."
            )

        else:

            st.success(
                "🔓 Mode administrador"
            )

            sorteig_actual = obtenir_sorteig()

            if sorteig_actual:

                st.success(
                    "✅ El sorteig està actiu."
                )

                st.write("### Resultats actuals")

                st.write("**👦 Nois**")

                for noi in NOIS:
                    st.write(
                        f"{noi} → {sorteig_actual[noi]}"
                    )

                st.write("**👧 Noies**")

                for noia in NOIES:
                    st.write(
                        f"{noia} → {sorteig_actual[noia]}"
                    )

            else:

                st.info(
                    "Encara no hi ha cap sorteig actiu."
                )

                if st.button(
                    "🎲 Generar sorteig",
                    use_container_width=True
                ):

                    nou_sorteig = generar_sorteig()

                    st.session_state[
                        "nou_sorteig"
                    ] = nou_sorteig

            # ---------------------------------------------
            # MOSTRAR SORTEIG GENERAT
            # ---------------------------------------------

            if "nou_sorteig" in st.session_state:

                nou_sorteig = st.session_state[
                    "nou_sorteig"
                ]

                st.success(
                    "🎉 Sorteig generat!"
                )

                st.write(
                    "Comprova'l i copia el bloc de sota "
                    "als Secrets de Streamlit."
                )

                st.write("### 👦 Nois")

                for noi in NOIS:
                    st.write(
                        f"**{noi}** → "
                        f"{nou_sorteig[noi]}"
                    )

                st.write("### 👧 Noies")

                for noia in NOIES:
                    st.write(
                        f"**{noia}** → "
                        f"{nou_sorteig[noia]}"
                    )

                secrets_text = """
[sorteig]
actiu = true
"""

                for persona in PARTICIPANTS:

                    secrets_text += (
                        f'"{persona}" = '
                        f'"{nou_sorteig[persona]}"\n'
                    )

                st.code(
                    secrets_text,
                    language="toml"
                )