import streamlit as st
import requests

# Function to fetch images from Pexels API
def fetch_pexels_images(topic, api_key, num_images=5):
    url = "https://api.pexels.com/v1/search"
    headers = {
        "Authorization": api_key
    }
    params = {
        "query": topic,
        "per_page": num_images
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        images = []
        for photo in data.get('photos', []):
            image_url = photo.get('src', {}).get('large')
            if image_url:
                images.append(image_url)
        return images
    else:
        st.error(f"Error: {response.status_code}")
        return []

# Streamlit App
def main():
    st.title("Image Fetcher App 🖼")
    st.write("Fetch relevant images based on a topic using the Pexels API.")

    # Input fields
    api_key = st.text_input("Enter your Pexels API Key", type="password")
    topic = st.text_input("Enter a topic (e.g., mountains, cats, etc.)")
    num_images = st.slider("Number of images to fetch", 1, 10, 5)

    # Fetch images button
    if st.button("Fetch Images"):
        if api_key and topic:
            with st.spinner("Fetching images..."):
                images = fetch_pexels_images(topic, api_key, num_images)
                if images:
                    st.success(f"Found {len(images)} images!")
                    for i, img_url in enumerate(images):
                        st.image(img_url, caption=f"Image {i+1}", use_column_width=True)
                else:
                    st.warning("No images found for the given topic.")
        else:
            st.warning("Please provide both an API key and a topic.")

# Run the app
if __name__ == "__main__":
    main()