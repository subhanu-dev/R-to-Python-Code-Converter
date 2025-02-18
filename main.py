import streamlit as st
import openai
from typing import Optional


class CodeConverter:
    def __init__(self, api_key: str):
        openai.api_key = api_key

    def convert_r_to_python(self, r_code: str) -> tuple[str, Optional[str]]:
        try:
            prompt = f"""Convert the following R code to equivalent Python code. 
            Include necessary import statements (like pandas, numpy, matplotlib) and explain any key differences.
            
            R code:
            {r_code}
            
            Provide only the Python equivalent code with appropriate library usage. No explanations needed.
            """

            response = openai.ChatCompletion.create(
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
Enter your OpenAI API key and R code to get started.
""")

# API Key input
api_key = st.text_input("Enter your OpenAI API key", type="password")

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
    if not api_key:
        st.error("Please enter your OpenAI API key")
    elif not r_code:
        st.warning("Please enter some R code")
    else:
        with st.spinner("Converting..."):
            converter = CodeConverter(api_key)
            python_code, error = converter.convert_r_to_python(r_code)

            if error:
                st.error(f"Error: {error}")
            else:
                with right_col:
                    st.code(python_code, language="python")

                    # Add copy button
                    if st.button("Copy Python Code"):
                        st.write("Code copied to clipboard!")
                        st.text_area("", value=python_code, height=0, key="copy_area")
                        st.code(python_code, language="python")

# Example R code in sidebar
st.sidebar.header("Example R Code")
example_r_code = """# Read and process data
data <- read.csv("data.csv")
head(data)

# Data manipulation
filtered_data <- data[data$age > 25, ]
mean_age <- mean(data$age, na.rm=TRUE)

# Create visualization
library(ggplot2)
ggplot(data, aes(x=age, y=salary)) + 
  geom_point() +
  geom_smooth(method="lm") +
  labs(title="Age vs Salary")
"""

if st.sidebar.button("Try Example"):
    st.session_state.r_input = example_r_code

# Add helpful information
st.sidebar.markdown("""
### Common R to Python Equivalents:
- `read.csv()` → `pd.read_csv()`
- `head()` → `df.head()`
- `library(ggplot2)` → `import seaborn as sns`
- `%>%` → `.pipe()`
""")


# Requirements and setup instructions
st.sidebar.markdown("""
### Setup Instructions:
1. Get an OpenAI API key from [OpenAI](https://platform.openai.com)
2. Install requirements:
```bash
pip install streamlit openai
                    """)
