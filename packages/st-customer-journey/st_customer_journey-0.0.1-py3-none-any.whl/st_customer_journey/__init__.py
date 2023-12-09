import streamlit.components.v1 as components
import os

import logging


_RELEASE = False


if not _RELEASE:
    _component_func = components.declare_component(
        # We give the component a simple, descriptive name ("my_component"
        # does not fit this bill, so please choose something better for your
        # own component :)
        "st_customer_journey",
        # Pass `url` here to tell Streamlit that the component will be served
        # by the local dev server that you run via `npm run start`.
        # (This is useful while your component is in development.)
        url="http://localhost:3000",
    )
else:
    # When we're distributing a production version of the component, we'll
    # replace the `url` param with `path`, and point it to to the component's
    # build directory:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("st_customer_journey", path=build_dir)

def st_customer_journey(content:list, space_main_nodes:int = 200, space_between_child_nodes:int = 50, key:str = "first_cj", defaultValue = None,
                        custom_font_awesome_url:str = "https://kit.fontawesome.com/d115db5fb4.js", tooltipStyle = {}, height = 300, max_width = 1750,
                        first_child_extra_space:int = 65, mainLabelOffset = 40, custom_css="") -> int:

       
    component_value = _component_func(content=content, space_main_nodes = space_main_nodes, space_between_child_nodes = space_between_child_nodes,
                                      key = key ,default=defaultValue, custom_font_awesome_url = custom_font_awesome_url, tooltipStyle = tooltipStyle, height_user = height,
                                      max_width = max_width, first_child_extra_space = first_child_extra_space, mainLabelOffset = mainLabelOffset,custom_css=custom_css)
                                      
    return component_value