
import streamlit as st
import hashlib
from dotenv import load_dotenv

from services.image_generator import generate_image
from services.image_describer import describe_image

load_dotenv()

st.set_page_config(
    page_title="AI Image Studio",
    page_icon="🎨",
    layout="wide"
)

st.title("🎨 AI Image Studio")
st.caption("Generate images with Grok and understand images with Groq.")

tab_generate, tab_describe = st.tabs([
    "✨ Text to Image",
    "🔍 Image to Description"
])


# --------------------------------
# FEATURE 1: TEXT TO IMAGE USING GROK
# --------------------------------

with tab_generate:

    st.subheader("Create an image from your words")

    prompt = st.text_area(
        "Describe the image you want",
        placeholder="Example: A cute dinosaur walking in a green forest",
        height=120
    )

    if st.button("Generate image", type="primary"):

        if not prompt.strip():
            st.warning("Please enter an image description.")

        else:
            with st.spinner("Grok is creating your image..."):

                try:
                    image_url = generate_image(prompt.strip())

                    st.session_state["generated_image_url"] = image_url

                except Exception as exc:
                    st.error(f"Image generation failed: {exc}")

    if st.session_state.get("generated_image_url"):

        st.image(
            st.session_state["generated_image_url"],
            caption="Generated with Grok",
            use_container_width=True
        )


# --------------------------------
# FEATURE 2: IMAGE DESCRIPTION USING GROQ
# --------------------------------

with tab_describe:

    st.subheader("Upload an image and ask questions")

    uploaded_file = st.file_uploader(
        "Choose an image",
        type=["png", "jpg", "jpeg", "webp"]
    )

    if uploaded_file:

        image_bytes = uploaded_file.getvalue()
        image_mime = uploaded_file.type

        # Identify the uploaded image
        image_id = hashlib.sha256(image_bytes).hexdigest()

        # Reset chat only when a different image is uploaded
        if st.session_state.get("current_image_id") != image_id:

            st.session_state["current_image_id"] = image_id
            st.session_state["image_bytes"] = image_bytes
            st.session_state["image_mime"] = image_mime
            st.session_state["chat_history"] = []
            st.session_state["image_description"] = None

        st.image(
            st.session_state["image_bytes"],
            caption="Your uploaded image",
            use_container_width=True
        )

        # Short image description
        if st.button("Generate short description"):

            with st.spinner("Groq is analyzing your image..."):

                try:
                    description = describe_image(
                        st.session_state["image_bytes"],
                        st.session_state["image_mime"],
                        "Describe this image in 2 to 3 short bullet points. Use simple language."
                    )

                    st.session_state["image_description"] = description

                except Exception as exc:
                    st.error(f"Description failed: {exc}")

        # Display short description
        if st.session_state.get("image_description"):

            st.markdown("### Image Description")
            st.markdown(st.session_state["image_description"])

        st.divider()

        # Chat section
        st.markdown("### 💬 Ask anything about this image")

        st.caption(
            "You can ask multiple questions about the same uploaded image."
        )

        # Display previous questions and answers
        for message in st.session_state.get("chat_history", []):

            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Ask a new question
        question = st.chat_input(
            "Ask a question about your image..."
        )

        if question:

            # Display user question
            st.session_state["chat_history"].append({
                "role": "user",
                "content": question
            })

            with st.chat_message("user"):
                st.markdown(question)

            # Get answer from Groq
            with st.chat_message("assistant"):

                with st.spinner("Groq is thinking..."):

                    try:
                        answer = describe_image(
                            st.session_state["image_bytes"],
                            st.session_state["image_mime"],
                            question
                        )

                        st.markdown(answer)

                        st.session_state["chat_history"].append({
                            "role": "assistant",
                            "content": answer
                        })

                    except Exception as exc:

                        st.error(f"Unable to answer: {exc}")

                        st.session_state["chat_history"].pop()


st.divider()

st.caption(
    "Grok generates images. Groq describes uploaded images and answers questions."
)
