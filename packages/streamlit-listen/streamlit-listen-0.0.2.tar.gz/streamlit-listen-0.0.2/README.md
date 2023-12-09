# streamlit-custom-component

Streamlit component that allows you to listen continuously to the microphone

## Installation instructions

```sh
pip install streamlit-listen
```

## Usage instructions

```python
import streamlit as st

from streamlit_listen import streamlit_listen

voice = streamlit_listen()

st.audio(voice)
```