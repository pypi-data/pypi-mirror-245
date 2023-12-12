from pathlib import Path
from typing import Optional

import streamlit as st
import streamlit.components.v1 as components

# Tell streamlit that there is a component called streamlit_query_input,
# and that the code to display that component is in the "frontend" folder
frontend_dir = (Path(__file__).parent / "frontend").absolute()
_component_func = components.declare_component(
	"query_input", path=str(frontend_dir)
)

# Create the python function that will be called
def query_input(value, height=38, cols=120, max_height=200, submit_label='▶️', reset_label='🔄', on_change=None,
    key: Optional[str] = None,
):
    """
    Multi-line text inputbox: 
        Enter to submit, shift+enter to add new line
    Arguments:
        value: default text when the component rendered
        height: the initial component height in px
        cols: the width of the input area in char
        max_height: max height of the component it can expend to.
        submit_label: submit button label, emoji preferred
        reset_label: reset button label, emoji referred
        on_change: [not available] a callback function called on resetting, submitting, or new line added
    """
    component_value = _component_func(
        value=value, height=height, cols=cols, max_height=max_height, submit_label=submit_label, reset_label=reset_label, 
        on_change=on_change,
        key=key,
    )

    return component_value

def fn(jobj):
    print("callback function et called:", jobj)

def main():

    st.set_page_config(page_title="test", layout="wide")

    st.write("Multiline text input")
    valiue = query_input("Enter your question here...", height=38, cols=60, submit_label='🎈', reset_label='✨')
    st.write(valiue)

if __name__ == "__main__":
    main()
