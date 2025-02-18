import streamlit as st
import openai
from typing import Optional, Tuple

# Load API key from Streamlit secrets
try:
    openai_api_key = st.secrets["openai"]["api_key"]
except KeyError:
    openai_api_key = None


class CodeConverter:
    def __init__(self, api_key: str):
        self.client = openai.Client(api_key=api_key)

    def convert_r_to_python(self, r_code: str) -> Tuple[Optional[str], Optional[str]]:
        try:
            prompt = f"""Convert the following R code to equivalent Python code. 
            Include necessary import statements (like pandas, numpy, matplotlib) and explain any key differences.
            
            R code:
            {r_code}
            
            Provide only the Python equivalent code with appropriate library usage. No explanations needed.
            """

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert in both R and Python, specializing in converting R code to Python with appropriate library usage.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.1,
            )

            return response.choices[0].message.content, None

        except Exception as e:
            return None, str(e)


# Streamlit UI
st.set_page_config(page_title="R to Python Converter", layout="wide")

# Title and description
st.title("R to Python Code Converter")
st.markdown("""
This tool converts R code to Python code using OpenAI's GPT model.
Enter your R code to get started.
""")

# Create two columns
left_col, right_col = st.columns(2)

with left_col:
    st.header("R Code")
    r_code = st.text_area(
        "Enter R code here", height=300, key="r_input", help="Paste your R code here"
    )

with right_col:
    st.header("Python Code")
    python_output = st.empty()

# Convert button
if st.button("Convert", key="convert"):
    if not openai_api_key:
        st.error("OpenAI API key is missing. Please add it to your Streamlit secrets.")
    elif not r_code.strip():
        st.warning("Please enter some R code.")
    else:
        with st.spinner("Converting..."):
            converter = CodeConverter(openai_api_key)
            python_code, error = converter.convert_r_to_python(r_code)

            if error:
                st.error(f"Error: {error}")
            else:
                with right_col:
                    st.code(python_code, language="python")

                    # Copy button
                    if st.button("Copy Python Code", key="copy"):
                        st.session_state["copy_code"] = python_code
                        st.success("Code copied! You can manually copy from below:")
                        st.text_area("", value=python_code, height=150, key="copy_area")


# # Example R code in sidebar
# st.sidebar.header("Example R Code")
# example_r_code = """# Read and process data
# data <- read.csv("data.csv")
# head(data)

# # Data manipulation
# filtered_data <- data[data$age > 25, ]
# mean_age <- mean(data$age, na.rm=TRUE)

# # Create visualization
# library(ggplot2)
# ggplot(data, aes(x=age, y=salary)) +
#   geom_point() +
#   geom_smooth(method="lm") +
#   labs(title="Age vs Salary")
"""

# if st.sidebar.button("Try Example"):
#     st.session_state.r_input = example_r_code

# # Add helpful information
# st.sidebar.markdown("""
# ### Common R to Python Equivalents:
# - `read.csv()` → `pd.read_csv()`
# - `head()` → `df.head()`
# - `library(ggplot2)` → `import seaborn as sns`
# - `%>%` → `.pipe()`
# """)
