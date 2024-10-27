# 낭장고 비우기 (Empty the Refrigerator)

Welcome to **Empty the Refrigerator**, a simple yet powerful recipe recommendation app built using [Streamlit](https://streamlit.io/). This app helps you make the most out of your leftover items by suggesting delicious recipes that match your preferences. Whether you type in a list of ingredients or upload an image, the app will suggest recipes and guide you step-by-step through cooking.

## Features

- **Flexible Ingredient Input**: You can either type a list of leftover ingredients or upload an image of them to get started.
- **Preferences & Customization**: Choose from a variety of themes, cuisines, and occasions to customize recipe suggestions.
- **Recipe Recommendations**: Uses OpenAI's GPT model to provide tailored recipe suggestions.
- **Step-by-Step Cooking Guide**: Guides you through the selected recipe, with detailed ingredients, instructions, and interactive cooking guidance.
- **Interactive Cooking Chat**: Receive real-time help and recommendations for every cooking step via interactive chat.

## Installation

Follow these instructions to set up the app locally:

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/empty-the-refrigerator.git
   cd empty-the-refrigerator
   ```
2. Create a virtual environment and install the dependencies:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows, use `env\Scripts\activate`
   pip install -r requirements.txt
   ```
3. Add your OpenAI API key to the Streamlit secrets file:
   - Create a `.streamlit/secrets.toml` file in the root directory of the project.
   - Add the following content to the file:
     ```toml
     [openai]
     api_key = "YOUR_OPENAI_API_KEY"
     ```
4. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

## How to Use the App

1. **Input Ingredients**: Choose to either type in your leftover items or upload an image of them.
   - **Type a List**: Enter your items separated by commas and click **Submit**.
   - **Upload an Image**: Upload a picture of your ingredients, and the app will automatically recognize them (using a placeholder image recognition function).

2. **Set Preferences**: Enter your preferences for theme, occasion, and cuisine. You can even provide custom options if desired.

3. **Get Recipe Suggestions**: The app will generate 5 recipe suggestions for your ingredients, using OpenAI's GPT-4.

4. **View Recipe Details**: Select a recipe to get detailed instructions, including ingredients, cooking steps, estimated cooking time, and difficulty level.

5. **Interactive Cooking Guide**: Follow the recipe step-by-step with real-time help. Ask questions or seek clarification through the chat function as you proceed.

## Requirements
- Python 3.7+
- Dependencies are listed in `requirements.txt`.
- OpenAI API key for recipe generation.

## Technologies Used
- **Streamlit**: For the web interface.
- **OpenAI GPT API**: For generating recipe suggestions and detailed instructions.
- **Pillow (PIL)**: For image handling.

## Future Improvements
- Implement a more advanced image recognition model for identifying ingredients.
- Add multi-language support to make the app accessible to a broader audience.
- Provide nutritional information for each recipe.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing
Contributions are welcome! Feel free to open an issue or submit a pull request.

## Acknowledgements
- **OpenAI**: For providing the GPT model to power recipe suggestions.
- **Streamlit**: For making it easy to build and deploy interactive web apps.

## Contact
If you have any questions or suggestions, please feel free to contact the project maintainer at `your.email@example.com`.

Enjoy cooking with **Empty the Refrigerator**! 🍳🥗

