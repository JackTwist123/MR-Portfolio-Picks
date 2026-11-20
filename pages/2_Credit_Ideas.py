"""Credit ideas: write-ups only, no P&L tracking. Shows whatever fields each idea file includes."""

import streamlit as st

import site_common as sc

sc.setup("Credit Ideas")
st.title("Credit Ideas")
st.write(
    "Bond and credit views, each dated with the levels at the time I published it. "
    "These aren't tracked for P&L."
)

ideas = sc.bond_ideas()
if not ideas:
    st.info("No credit ideas published yet.")
    sc.footer()
    st.stop()

SKIP = {"body", "file", "slug", "title", "headline", "status", "published", "closed"}

for idea in sorted(ideas, key=lambda i: sc.lib.to_date(i["published"]), reverse=True):
    published = sc.lib.to_date(idea["published"])
    status = str(idea.get("status", "active")).title()
    title = idea.get("title", idea["slug"])
    with st.expander(f"{title} · {published:%b %d, %Y} · {status}", expanded=False):
        if idea.get("headline"):
            st.markdown(f"**{idea['headline']}**")
        details = {k.replace("_", " ").title(): v for k, v in idea.items() if k not in SKIP and v not in (None, "")}
        if details:
            cols = st.columns(min(len(details), 4))
            for i, (k, v) in enumerate(details.items()):
                cols[i % len(cols)].metric(k, str(v))
        pitch, closing = sc.lib.split_closing_note(idea["body"])
        if closing:
            st.subheader("Closing note")
            st.markdown(closing)
            st.divider()
        st.markdown(pitch)

sc.footer()
