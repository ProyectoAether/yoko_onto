import os
import __init__
from first_layer import knit
from multiprocessing import Process
import streamlit as st
import uuid
from py_query_cypher import query_neo4j_list, query_neo4j_str
from second_layer import neo2RDF


dict_erram = {}
st.set_page_config(
    page_title="YOKO ONtO",
    page_icon="🐜",
    layout="centered",
    menu_items={
        "Get Help": "https://github.com/ProyectoAether/knit",
        "Report a bug": "https://github.com/ProyectoAether/knit",
        "About": """The KHAOS research group has developed this application within the framework of the *Aether* project. Learn more about us and our lines of study in 
        https://khaos.uma.es/  and in https://aether.es/ """,
    },
)
st.write(
    """ 
# 🐜 YOKO ONtO: You only knit one ontology """
)
st.markdown(
    """
        <style>
        .css-15zrgzn {display: none}
        .css-eczf16 {display: none}
        .css-jn99sy {display: none}
        </style>
        """,
    unsafe_allow_html=True,
)

st.divider()

st.subheader(" Parameters Bioportal 🔬")
st.caption(
    " YOKO works thanks to the [KNIT](https://doi.org/10.1016/j.eswa.2023.120239) algorithm on the [Bioportal](https://bioportal.bioontology.org/) knowledge base to develop its potential, create or access your account and insert your API key below "
)


Bioportal_key = st.text_input("Bioportal ApiKey:", "", type="password")


st.subheader("Parameters Neo4j 💾")
st.caption(
    "YOKO uses Neo4j as its database. Download the docker image in the following [link](https://hub.docker.com/_/neo4j)"
)
user_neo = st.text_input("User Neo4j:", "", type="password")
pass_neo = st.text_input("Password Neo4j:", "", type="password")
url_neo4j = st.text_input("Url Neo4j:", "bolt://localhost:7687")
st.info("Please modify this field with your team's information", icon="ℹ️")


st.divider()

st.subheader("Optional parameters ⚙️")
st.caption(
    "These parameters are optional, YOKO has a default setting, however, you can modify it to improve the results at will. Here is some information about what they are and how you can use them:"
)
st.code(
    """
WC = Weight assigned to the ontology coverage criterion.
WA = Weight assigned to the ontology acceptance criterion.
WD = Weight assigned to the ontology detail criterion.
WS = Weight assigned to the ontology specialization criterion.
"""
)

col1, col2, col3, col4 = st.columns(4)
with col1:
    v_wc = st.text_input("WC:", "0.55")
    st.info("value in the range [0,1]", icon="ℹ️")

with col2:
    v_wa = st.text_input("WA:", "0.15")
    st.info("value in the range [0,1]", icon="ℹ️")

with col3:
    v_wd = st.text_input("WD:", "0.15")
    st.info("value in the range [0,1]", icon="ℹ️")

with col4:
    v_ws = st.text_input("WS:", "0.15")
    st.info("value in the range [0,1]", icon="ℹ️")

st.code(
    """
WhiteList -> If you want to USE one or several specific ontologies, 
            place the acronym here.
BlackList -> If you want to NOT USE one or several specific ontologies, 
            place the acronym here.
"""
)
p_WhiteList = st.text_input("WhiteList:", "")
st.info(
    """Please ensure the acronyms are correct and write them separated by commas without spaces between them. 

Example =NCIT,MESH,CODO""",
    icon="ℹ️",
)

if len(p_WhiteList) >= 1:
    v_WhiteList = p_WhiteList.split(",")
else:
    v_WhiteList = []

p_BlackList = st.text_input("BlackList:", "")
st.info(
    """Please ensure the acronyms are correct and write them separated by commas without spaces between them. 

Example =NCIT,MESH,CODO""",
    icon="ℹ️",
)

if len(p_BlackList) >= 1:
    v_BlackList = p_BlackList.split(",")
else:
    v_BlackList = []
st.divider()


st.title("KNIT Terms 🔍")
st.caption(
    "Write the key terms you want to represent in your future ontology. You can type as many as you want, separated by commas. The more terms you type, the longer the search will take. "
)
terms = st.text_input("Search terms:", "")
st.info(
    """Please ensure the search terms are correct; write them separated by commas and without spaces between them. 

Example =WATER,MRPS25,CEP135""",
    icon="ℹ️",
)


def t(hash1):

    sparql_service = "http://sparql.bioontology.org/sparql/"
    url = "https://data.bioontology.org"
    list_text = terms.split(",")

    wc = v_wc
    wa = v_wc
    wd = v_wc
    ws = v_wc
    WhiteList = v_WhiteList
    BlackList = v_BlackList
    api_k = Bioportal_key

    if len(list_text) <= 100:
        knit(
            sparql_service,
            url,
            list_text[0:100],
            api_k,
            url_neo4j,
            user_neo,
            pass_neo,
            wc,
            wa,
            wd,
            ws,
            WhiteList,
            BlackList,
            hash1,
        )

    else:
        st.write(
            "YOKO ONtO currently has a limitation of 100 terms per search, please try again with fewer terms."
        )


if (
    len(Bioportal_key) >= 30
    and len(terms) >= 1
    and len(user_neo) >= 1
    and len(pass_neo) >= 1
):
    col_go, col_stop = st.columns(2)

    if st.button("start KNIT"):
        hash1 = uuid.uuid4()
        print(hash1)
        if st.button("Kill Process"):
            st.error("KILL PROCESS!")
            st.stop()

        with st.spinner("Wait for it..."):
            t(str("a" + str(hash1).replace("-", "")))
            n = 1
            Name_Ontology = "output_ontology_test.owl"
            neo2RDF(
                url_neo4j,
                user_neo,
                pass_neo,
                Bioportal_key,
                "http://sparql.bioontology.org/sparql/",
                Name_Ontology,
                str("a" + str(hash1).replace("-", "")),
            )
        st.success("Done!")


else:
    bio, neo_user, neo_pass, term = st.columns(4)

    with bio:
        if len(Bioportal_key) <= 29:
            st.warning("Missing Bioportal Apikey", icon="🚨")

    with neo_user:
        if len(user_neo) <= 1:
            st.warning("Missing Neo4j User", icon="🧨")

    with neo_pass:
        if len(pass_neo) <= 1:
            st.warning("Missing Neo4j Password", icon="🔥")

    with term:
        if len(terms) <= 1:
            st.warning("Missing Search Terms", icon="🤖")

st.stop()
