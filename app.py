import streamlit as st
import openai
from PIL import Image
import json
import time

def main():
    st.title("낭장고 비우기 (Empty the Refrigerator)")
    st.write("Provide a list of your leftover items, and we'll suggest recipes!")

    # Initialize session state variables
    if 'items_list' not in st.session_state:
        st.session_state['items_list'] = []
    if 'suggestions' not in st.session_state:
        st.session_state['suggestions'] = []
    if 'selected_recipe' not in st.session_state:
        st.session_state['selected_recipe'] = None
    if 'recipe_details' not in st.session_state:
        st.session_state['recipe_details'] = None
    if 'preferences_submitted' not in st.session_state:
        st.session_state['preferences_submitted'] = False
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []
    if 'current_step' not in st.session_state:
        st.session_state['current_step'] = 0

    # User input method selection
    input_method = st.radio("How would you like to input your items?", ("Type a list", "Upload an image"))

    if input_method == "Type a list":
        typed_items = st.text_area("Enter your leftover items (separated by commas):")
        if st.button("Submit"):
            items_list = [item.strip() for item in typed_items.split(',') if item.strip()]
            if items_list:
                st.session_state['items_list'] = items_list
                st.session_state['suggestions'] = []
                st.session_state['selected_recipe'] = None
                st.session_state['recipe_details'] = None
                st.session_state['preferences_submitted'] = False
                st.session_state['chat_history'] = []
                st.session_state['current_step'] = 0
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
                    st.session_state['items_list'] = items_list
                    st.session_state['suggestions'] = []
                    st.session_state['selected_recipe'] = None
                    st.session_state['recipe_details'] = None
                    st.session_state['preferences_submitted'] = False
                    st.session_state['chat_history'] = []
                    st.session_state['current_step'] = 0
                    st.write("Detected items: " + ', '.join(items_list))
                else:
                    st.error("No items recognized in the image. Please try again.")

    # If items_list is already in session_state, process items
    if st.session_state['items_list']:
        process_items()


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


def process_items():
    """
    Process the list of items and prompt user for preferences.
    """
    items_list = st.session_state['items_list']
    st.write("You have the following items: " + ', '.join(items_list))

    # Check if preferences have been submitted
    if not st.session_state['preferences_submitted']:
        # Get user preferences within a form
        with st.form(key='preferences_form'):
            st.subheader("Preferences")
            theme = st.selectbox("Select a theme", ["No preference", "Quick meals", "Healthy eating", "Comfort food", "Custom text"])
            if theme == "Custom text":
                theme = st.text_input("Enter your custom theme:")
            occasion = st.selectbox("Select an occasion", ["No preference", "Dinner party", "Family lunch", "Snack", "Custom text"])
            if occasion == "Custom text":
                occasion = st.text_input("Enter your custom occasion:")
            cuisine = st.selectbox("Select a cuisine", ["No preference", "Italian", "Korean", "Mexican", "American", "Custom text"])
            if cuisine == "Custom text":
                cuisine = st.text_input("Enter your custom cuisine:")
            submit_preferences = st.form_submit_button(label='Get Recipe Suggestions')

        if submit_preferences:
            with st.spinner("Generating recipe suggestions..."):
                suggestions = get_recipe_suggestions(items_list, theme, occasion, cuisine)
                if suggestions:
                    st.session_state['suggestions'] = suggestions
                    st.session_state['preferences_submitted'] = True
                else:
                    st.error("No recipes found with the given items and preferences.")
    else:
        # Preferences already submitted, display suggestions
        suggestions = st.session_state['suggestions']
        if suggestions:
            selected_recipe = st.selectbox("Select a recipe to view", suggestions)
            if st.button("Get Recipe Details"):
                st.session_state['selected_recipe'] = selected_recipe
                with st.spinner("Generating recipe details..."):
                    recipe_details = get_recipe_details(selected_recipe, items_list)
                    if recipe_details:
                        st.session_state['recipe_details'] = recipe_details
                        st.session_state['current_step'] = 0
                    else:
                        st.error("Failed to get recipe details.")

    # Display recipe details if available
    if st.session_state['recipe_details']:
        display_recipe(st.session_state['recipe_details'])
        initiate_chat()


def get_recipe_suggestions(items_list, theme, occasion, cuisine):
    """
    Use OpenAI GPT API to generate recipe suggestions based on items and preferences.
    """
    openai.api_key = st.secrets['openai_api_key']

    prompt = f"""
    You are a cooking assistant. Based on the following ingredients: {', '.join(items_list)}, suggest 5 recipes that match the following preferences:

    Theme: {theme}
    Occasion: {occasion}
    Cuisine: {cuisine}

    Provide only the names of the dishes as a numbered list.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a cooking assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7
        )
        suggestions_text = response['choices'][0]['message']['content'].strip()
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
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a cooking assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=700,
            temperature=0.7,
            functions=[
                {
                    "name": "format_recipe_response",
                    "description": "Formats the recipe response as JSON",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "ingredients": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of ingredients"
                            },
                            "instructions": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Step-by-step cooking instructions"
                            },
                            "estimated_cooking_time": {
                                "type": "string",
                                "description": "Estimated cooking time"
                            },
                            "difficulty_level": {
                                "type": "string",
                                "enum": ["Easy", "Medium", "Hard"],
                                "description": "Difficulty level of the recipe"
                            }
                        },
                        "required": ["ingredients", "instructions", "estimated_cooking_time", "difficulty_level"]
                    }
                }
            ]
        )
        recipe_text = response['choices'][0]['message']['function_call']['arguments']
        recipe_details = json.loads(recipe_text)
        return recipe_details
    except json.JSONDecodeError:
        st.error("Failed to parse the response. Ensure the response is in valid JSON format.")
        return None
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
        if st.checkbox(f"Step {i+1}: {step}", key=f"step_{i}"):
            st.session_state['current_step'] = i + 1

    st.write(f"**Estimated Cooking Time:** {recipe_details.get('estimated_cooking_time', 'N/A')}")
    st.write(f"**Difficulty Level:** {recipe_details.get('difficulty_level', 'N/A')}")


def initiate_chat():
    """
    Initiate a chat to guide the user step by step.
    """
    st.subheader("Interactive Cooking Guide")
    current_step = st.session_state['current_step']
    if current_step < len(st.session_state['recipe_details']['instructions']):
        current_instruction = st.session_state['recipe_details']['instructions'][current_step]
    else:
        current_instruction = "You have completed all the steps!"
    st.write(f"**Current Step ({current_step + 1}):** {current_instruction}")

    user_input = st.text_input("Ask for guidance or clarification on the current step or for recommendations:")
    uploaded_image = st.file_uploader("Upload an image related to your cooking process (optional):", type=["jpg", "jpeg", "png"])
    if st.button("Send"):
        if user_input or uploaded_image:
            user_message = user_input
            if uploaded_image is not None:
                image_url = "Uploaded an image."
                user_message += f" {image_url}"
            # Append user message to chat history
            st.session_state['chat_history'].append({"role": "user", "content": user_message})
            # Generate assistant response
            response = get_chat_response(st.session_state['chat_history'], current_instruction)
            if response:
                st.session_state['chat_history'].append({"role": "assistant", "content": response})

    # Display chat history
    for message in st.session_state['chat_history']:
        if message['role'] == 'user':
            st.write(f"**You:** {message['content']}")
        elif message['role'] == 'assistant':
            st.write(f"**Assistant:** {message['content']}")


def get_chat_response(chat_history, current_instruction):
    """
    Use OpenAI GPT API to generate chat responses based on chat history.
    """
    openai.api_key = st.secrets["openai_api_key"]
    try:
        prompt = f"You are currently on the following step of the recipe: '{current_instruction}'. Provide guidance for this step, and recommendations for completing it or moving to the next step."
        chat_history.append({"role": "system", "content": prompt})
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=chat_history,
            max_tokens=150,
            temperature=0.7
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        st.error(f"Failed to get chat response: {str(e)}")
        return None


if __name__ == "__main__":
    main()