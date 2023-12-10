import streamlit.components.v1 as components
import os

import warnings


_RELEASE = True


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

def st_customer_journey(content: list, space_main_nodes: int = 200, space_between_child_nodes: int = 50, key: str = "first_cj", defaultValue=None,
                        custom_font_awesome_url: str = "https://kit.fontawesome.com/c7cbba6207.js", tooltipStyle=None, height=300, max_width=1750,
                        first_child_extra_space: int = 65, mainLabelOffset=40, custom_css="", mainNodeHoverStyle=None, mainNodeClickedStyle=None,
                        mainNodeDefaultStyle=None, childNodeDefaultStyle=None, childNodeHoverStyle=None, childNodeClickedStyle=None,
                        mainNodeLineStyle=None, childNodeLineStyle=None) -> int:
    """
    Create a custom Streamlit component for visualizing a customer journey or similar flow.
    There are main nodes and child nodes. The main nodes are the main steps in the journey and the child nodes are the sub-steps. Each main node
    can have multiple child nodes. The component is interactive and the user can click on the nodes to select them. The component returns the ID, Return Value as well as Node Settings.

    The input is a list of Node objects. Each Node object has the following attributes:
    Attributes:
        id (int): Unique identifier for the node.
        name (str): Name of the node.
        label (str, optional): Label for the node, displayed on or near the node (e.g. 'R&D').
        color (str, optional): Fill color of the node, specified in CSS color formats.
        return_value (any, optional): Value returned when the node is interacted with.
        disabled (bool, optional): Flag indicating if the node is interactive. If True, the node cannot be clicked.
        icon (str, optional): FontAwesome icon class for display on the node. For example, 'fa fa-home' will display a home icon.
        icon_style (str, optional): CSS styling for the icon.
        expand_direction (str, optional): Direction ('up' or 'down') for child nodes expansion.
        children (list of Node, optional): Child nodes of this node - Each children can have the same attributes as the parent node.
        size (int, optional): Size of the node, determining its diameter if circular.
        label_position (str, optional): Position of the label relative to the node ('bottom', 'top',).
        label_style (str, optional): CSS styling for the label text.
        node_style (str, optional): Additional CSS styling for the node.
        tooltip (str, optional): Tooltip text displayed on hover over the node. - HTML can be used.
  

    Args:
    content (list): A list of Node objects representing the nodes in the journey.
    space_main_nodes (int): Horizontal space between main nodes.
    space_between_child_nodes (int): Vertical space between child nodes.
    key (str): A unique key for the component instance.
    defaultValue: Default value to be used in the component - will be returned if nothing was clicked yet.
    custom_font_awesome_url (str): URL for  FontAwesome icons.
    tooltipStyle: CSS properties for styling the tooltip.
    height (int): Height of the component.
    max_width (int): Maximum width of the component.
    first_child_extra_space (int): Additional vertical space for the first child node.
    mainLabelOffset (int): Offset for the main label.
    custom_css (str): Custom CSS string for additional styling.
    mainNodeHoverStyle, mainNodeClickedStyle, mainNodeDefaultStyle,
    childNodeDefaultStyle, childNodeHoverStyle, childNodeClickedStyle,
    mainNodeLineStyle, childNodeLineStyle: CSS properties for various node states.

    Returns:
    int: The selected node's ID or other return value based on user interaction.
    """

    if any([mainNodeHoverStyle, mainNodeClickedStyle, mainNodeDefaultStyle, childNodeDefaultStyle, 
            childNodeHoverStyle, childNodeClickedStyle, mainNodeLineStyle, childNodeLineStyle]):
        warnings.warn("The styling features (like hover and click styles for nodes) are not yet implemented.", UserWarning)
    
    component_value = _component_func(content=content, space_main_nodes=space_main_nodes, space_between_child_nodes=space_between_child_nodes,
                                      key=key, default=defaultValue, custom_font_awesome_url=custom_font_awesome_url, tooltipStyle=tooltipStyle, 
                                      height_user=height, max_width=max_width, first_child_extra_space=first_child_extra_space,
                                      mainLabelOffset=mainLabelOffset, custom_css=custom_css, mainNodeClickedStyle=mainNodeClickedStyle,
                                      mainNodeHoverStyle=mainNodeHoverStyle, mainNodeDefaultStyle=mainNodeDefaultStyle, 
                                      childNodeDefaultStyle=childNodeDefaultStyle, childNodeHoverStyle=childNodeHoverStyle,
                                      childNodeClickedStyle=childNodeClickedStyle, mainNodeLineStyle=mainNodeLineStyle, 
                                      childNodeLineStyle=childNodeLineStyle)
                                      
    return component_value