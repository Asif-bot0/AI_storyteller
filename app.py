import streamlit as st
from story_generator import generate_story_from_images, narrate_story
from PIL import Image

st.title("AI story generator from images")
st.markdown("Upload 1 to 10 images and choose a style and let AI write and narrate an story for you.")

with st.sidebar:
    st.header("Controls")

    # sidebar option to upload images
    uploaded_files = st.file_uploader(
        "upload your images...",
        type=["png", "jpg", "jpeg"],
        accept_multiple_files=True
    )

    # selecting a story style
    story_style = st.selectbox(
        "choose a style for the story...",
        ("Comedy","Thriller", "Fairy Tale", "Sci-Fi", "Mystery", "Adventure", "Morale")
    )

    # Button for the story
    generate_button = st.button("Generate Story and Narration", type="primary")


# Main Logic
if generate_button:
    if not uploaded_files:
        st.warning("please upload atleast 1 image.")
    elif len(uploaded_files) > 10:
        st.warning("please upload maximum of 10 images.")
    else:
        with st.spinner("AI is writing and narrating your story... This may take you moments."):
            try:
                pil_images= [Image.open(uploaded_file) for uploaded_file in uploaded_files]
                st.subheader("Your visual Inspiration:")
                image_columns= st.columns(len(pil_images))

                for i ,image in enumerate(pil_images):
                    with image_columns[i]:
                        st.image(image, use_container_width=True)

                generate_story = generate_story_from_images(pil_images, story_style)
                if "Error" in generate_story or "failed" in generate_story or "API key" in generate_story:
                    st.error(generate_story)
                else:
                    st.subheader(f"Your {story_style} story: ")
                    st.success(generate_story)

                st.subheader("Listen to your story:")
                audio_file = narrate_story(generate_story)
                if audio_file:
                    st.audio(audio_file, format="audio/mp3")

            except Exception as e:
                st.error(f"An Application error occurred {e}")
                