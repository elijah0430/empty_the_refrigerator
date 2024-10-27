냉장고 비우기 (Empty the Refrigerator) - Cooking Assistant App
This is a Streamlit application that serves as a cooking assistant platform named "냉장고 비우기" ("Empty the Refrigerator"). The app provides cooking recommendations and step-by-step recipes based on the leftover items in your refrigerator.

Features
User Input: Input leftover items by typing a list or uploading an image.
Cooking Recommendations: Get personalized recipe suggestions based on your items and preferences.
Step-by-Step Recipes: View detailed recipes with ingredients, instructions, estimated time, and difficulty level.
User Interface: User-friendly interface with progress indicators for cooking steps.
Error Handling: Handles errors gracefully with user-friendly messages.
Installation
Clone the repository:
bash
Copy code
git clone https://github.com/yourusername/empty-the-refrigerator.git
cd empty-the-refrigerator
Create a virtual environment (optional but recommended):
bash
Copy code
python -m venv venv
source venv/bin/activate  # On Windows, use venv\Scripts\activate
Install the required packages:
bash
Copy code
pip install -r requirements.txt
Set up OpenAI API Key:
Create a secrets.toml file in the .streamlit directory (create the directory if it doesn't exist):
bash
Copy code
mkdir .streamlit
echo "[secrets]" > .streamlit/secrets.toml
Add your OpenAI API key to secrets.toml:
csharp
Copy code
[secrets]
openai_api_key = "YOUR_OPENAI_API_KEY"
Usage
Run the Streamlit app:

bash
Copy code
streamlit run app.py
The app will open in your web browser.

Notes
Image Recognition: The current implementation includes a placeholder function for image recognition. To enable this feature, you need to implement the recognize_items_from_image function using an appropriate image recognition library or API (e.g., Google Cloud Vision API, OpenCV, TensorFlow).

API Costs: Using the OpenAI API may incur costs. Please monitor your usage to avoid unexpected charges.

Multilingual Support: The app is designed with a Korean audience in mind but can be used by anyone.

Troubleshooting
OpenAI API Errors: Ensure your API key is correct and you have sufficient quota.
Dependencies: If you encounter import errors, make sure all dependencies are installed.
License
This project is licensed under the MIT License.

