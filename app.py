import streamlit as st
from core import build_index

st.set_page_config(page_title="Nepali Doc Q&A", page_icon="📄")
st.title("📄 Nepal Law Document Search")
st.caption("Ask in English. Answers are passages from the source documents.")


@st.cache_resource
def get_index():
    return build_index()


store, n_chunks = get_index()
st.sidebar.write(f"Indexed chunks: **{n_chunks}**")
k = st.sidebar.slider("Results", 1, 5, 3)
threshold = st.sidebar.slider("Max distance (lower = stricter)", 0.5, 2.0, 1.2)

query = st.text_input("Your question")
if query:
    results = store.similarity_search_with_score(query, k=k)
    st.write(f"Top {len(results)} results retrieved.")
    good = [(d, s) for d, s in results if s <= threshold]
    if not good:
        st.warning("Nothing within the distance limit. Closest matches are shown below.")
    for doc, score in results:
        mark = "" if score <= threshold else " (above limit)"
        st.markdown(f"**{doc.metadata['source']}** · page {doc.metadata['page']} · distance {score:.2f}{mark}")
        st.info(doc.page_content)