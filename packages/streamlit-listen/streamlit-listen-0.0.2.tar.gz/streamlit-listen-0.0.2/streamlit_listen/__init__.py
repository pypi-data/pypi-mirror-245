import os
import streamlit as st
import streamlit.components.v1 as components

_RELEASE = True

if not _RELEASE:
    _component_func = components.declare_component("streamlit_listen", url="http://localhost:3001")
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("streamlit_listen", path=build_dir)

def streamlit_listen(name,
                     start_prompt="Start listening",
                     stop_prompt="Stop listening",
                     time_slice=3,
                     key=None):
    """Create a new instance of "my_component".

    Parameters
    ----------
    name: str
    start_prompt="Start listening" :str
    stop_prompt="Stop listening" :str
    time_slice=3 :number - time in seconds
    key: str or None - optional key that uniquely identifies this component

    Returns
    -------
    recording :str base64

    """
    # "default" is a special argument that specifies the initial return
    # value of the component before the user has interacted with it.
    component_value = _component_func(name=name,
                                      start_prompt=start_prompt,
                                      stop_prompt=stop_prompt,
                                      time_slice=time_slice,
                                      key=key,
                                      default=0)
    return component_value

def main():
    if 'chunks' not in st.session_state:
        st.session_state.chunks = []

    st.subheader(f":green[Running test from {__name__} file]")

    chunk = streamlit_listen("My listener")
    if chunk:
        st.session_state.chunks.append(chunk)

    st.write(f"No of chunks: {len(st.session_state.chunks)}")

    lenghts = [len(c['audio_base64']) for c in st.session_state.chunks]
    st.write(lenghts)

if __name__ == "__main__":
    main()