import streamlit as st
from google.oauth2 import service_account
import json
import uuid

credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcs_connections"]
)
fileid = str(uuid.uuid4())


def gen_image(text):
    PROJECT_ID = 'skeenan' # @param {type:"string"}
    LOCATION = 'us-central1'  # @param {type:"string"}

    import vertexai
    from vertexai.preview.vision_models import Image, ImageGenerationModel

    vertexai.init(project=PROJECT_ID, location=LOCATION, credentials=credentials)

    model = ImageGenerationModel.from_pretrained("imagegeneration@002")
    images1 = model.generate_images(
    prompt=text,
    # Optional:
    number_of_images=2,
    seed=1
    )

    images1[0].save(location="./{}1.png".format(fileid), include_generation_parameters=True)
    images1[1].save(location="./{}2.png".format(fileid), include_generation_parameters=True)

    st.image("./{}1.png".format(fileid))
    st.button("Vote for image 1")
    st.image("./{}2.png".format(fileid))
    st.button("Vote for image 2")


st.chat_message("user").write("Please upload a menu file")
menufile = st.file_uploader("Menu File", type=["json"])
if menufile is not None:
    bytes_data = menufile.getvalue()
    st.write(bytes_data)
    data = json.loads(bytes_data)
    menutext = """Generate an image for the following menu item: {item}
    for a restaurant with the following description: {description}
    """.format(item=data['items'][0], description=data['description'])
    gen_image(menutext)



