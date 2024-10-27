import streamlit as st
import openai
from PIL import Image
import json
import time

def main():
    st.title("냉장고 비우기 (Empty the Refrigerator)")
    st.write("Provide a list of your leftover items, and we'll suggest recipes!")

    # User input method selection
    input_method = st.radio("How would you like to input your items?", ("Type a list", "Upload an image"))

    if input_method == "Type a list":
        typed_items = st.text_area("Enter your leftover items (separated by commas):")
        if st.button("Submit"):
            items_list = [item.strip() for item in typed_items.split(',') if item.strip()]
            if items_list:
                process_items(items_list)
            else:
                st.error("Please enter at least one item.")
    else:
        uploaded_image = st.file_uploader("Upload an image of your items", type=["jpg", "jpeg", "png"])
        if uploaded_image is not None:
            image = Image.open(uploaded_image)
            st.image(image, caption="Uploaded Image", use_column_width=True)
            if st.button("Process Image"):
                items_list = recognize_items_from_image(image)
                if items_list:
                    st.write("Detected items: " + ', '.join(items_list))
                    process_items(items_list)
                else:
                    st.error("No items recognized in the image. Please try again.")

def recognize_items_from_image(image):
    """
    Recognize items from the uploaded image.
    Implement image recognition here using an appropriate library or API.
    """
    # Placeholder function for image recognition
    st.info("Processing image for item recognition...")
    time.sleep(2)  # Simulate processing time

    # TODO: Implement image recognition
    # For demonstration, return a simulated list of items
    recognized_items = ["tomato", "cheese", "lettuce"]
    return recognized_items

def process_items(items_list):
    """
    Process the list of items and prompt user for preferences.
    """
    st.write("You have the following items: " + ', '.join(items_list))

    # Get user preferences
    st.subheader("Preferences")
    theme = st.selectbox("Select a theme", ["No preference", "Quick meals", "Healthy eating", "Comfort food"])
    occasion = st.selectbox("Select an occasion", ["No preference", "Dinner party", "Family lunch", "Snack"])
    cuisine = st.selectbox("Select a cuisine", ["No preference", "Italian", "Korean", "Mexican", "American"])

    if st.button("Get Recipe Suggestions"):
        with st.spinner("Generating recipe suggestions..."):
            suggestions = get_recipe_suggestions(items_list, theme, occasion, cuisine)
            if suggestions:
                selected_recipe = st.selectbox("Select a recipe to view", suggestions)
                if st.button("Get Recipe Details"):
                    with st.spinner("Generating recipe details..."):
                        recipe_details = get_recipe_details(selected_recipe, items_list)
                        display_recipe(recipe_details)
            else:
                st.error("No recipes found with the given items and preferences.")

def get_recipe_suggestions(items_list, theme, occasion, cuisine):
    """
    Use OpenAI GPT API to generate recipe suggestions based on items and preferences.
    """
    openai.api_key = st.secrets["openai_api_key"]

    prompt = f"""
You are a cooking assistant. Based on the following ingredients: {', '.join(items_list)}, suggest 5 recipes that match the following preferences:

Theme: {theme}
Occasion: {occasion}
Cuisine: {cuisine}

Provide only the names of the dishes as a numbered list.
"""
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150,
            temperature=0.7,
            n=1,
            stop=None
        )
        suggestions_text = response.choices[0].text.strip()
        suggestions = suggestions_text.split('\n')
        suggestions = [s.strip('0123456789. ') for s in suggestions if s.strip()]
        return suggestions
    except Exception as e:
        st.error(f"Failed to get recipe suggestions: {str(e)}")
        return None

def get_recipe_details(selected_recipe, items_list):
    """
    Use OpenAI GPT API to generate detailed recipe instructions.
    """
    openai.api_key = st.secrets["openai_api_key"]

    prompt = f"""
Provide a detailed recipe for "{selected_recipe}" including:

- Ingredients list (highlight the following ingredients if they are used: {', '.join(items_list)}).
- Cooking instructions broken down into clear, manageable steps.
- Estimated cooking time.
- Difficulty level.

Format the response as JSON with the following structure:
{{
    "ingredients": ["ingredient1", "ingredient2", ...],
    "instructions": ["Step 1", "Step 2", ...],
    "estimated_cooking_time": "X minutes",
    "difficulty_level": "Easy/Medium/Hard"
}}
"""
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=700,
            temperature=0.7,
            n=1,
            stop=None
        )
        recipe_text = response.choices[0].text.strip()
        # Try to parse the JSON
        recipe_details = json.loads(recipe_text)
        return recipe_details
    except Exception as e:
        st.error(f"Failed to get recipe details: {str(e)}")
        return None

def display_recipe(recipe_details):
    """
    Display the recipe details in the app, including progress indicators for each step.
    """
    if recipe_details is None:
        st.error("No recipe details to display.")
        return
    st.subheader("Ingredients")
    for ingredient in recipe_details.get("ingredients", []):
        st.write(f"- {ingredient}")

    st.subheader("Instructions")
    steps = recipe_details.get("instructions", [])
    for i, step in enumerate(steps):
        st.checkbox(f"Step {i+1}: {step}", key=f"step_{i}")

    st.write(f"**Estimated Cooking Time:** {recipe_details.get('estimated_cooking_time', 'N/A')}")
    st.write(f"**Difficulty Level:** {recipe_details.get('difficulty_level', 'N/A')}")

if __name__ == "__main__":
    main()
