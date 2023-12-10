from pathlib import Path
from typing import Optional

import streamlit as st
import streamlit.components.v1 as components

# Tell streamlit that there is a component called streamlit_multiline_input,
# and that the code to display that component is in the "frontend" folder
frontend_dir = (Path(__file__).parent / "frontend").absolute()
_component_func = components.declare_component(
	"query_input", path=str(frontend_dir)
)

# Create the python function that will be called
def query_input(value, height=20, cols=120, max_height=200,
    key: Optional[str] = None,
):
    """
    Add a descriptive docstring
    """
    component_value = _component_func(value=value, height=height, cols=cols, max_height=max_height,
        key=key,
    )

    return component_value

def main():

    st.set_page_config(page_title="test", layout="wide")

    st.write("Multiline text input")
    valiue = query_input("my default valueX", height=20, cols=60)
    st.write(valiue)

if __name__ == "__main__":
    main()
