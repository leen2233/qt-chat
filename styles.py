context_menu_style = """
    QMenu {
        background-color: #2D2D30;
        color: white;
        border: 1px solid #3E3E42;
        border-radius: 14px;
        padding: 10px;
    }
    QMenu::item {
        padding: 8px 30px 8px 8px;
        border-radius: 7px;
    }
    QPushButton {
        color: red;
        padding: 8px;
        border-radius: 7px;
        background-color: transparent;
        text-align: left;
    }
    QPushButton:hover {
        background-color: #3E3E42;
    }
    QMenu::icon {
        padding-left: 4px;  /* Space before the icon */
        width: 12px;
    }
    QMenu::icon {
        padding-left: 10px;
    }
    QMenu::item:selected {
        background-color: #3E3E42;
    }
    QMenu::separator {
        height: 1px;
        background: #3E3E42;
        margin: 4px 0px 4px 0px;
    }
"""


def build_reply_to_label_style(is_mine=False):
    if is_mine:
        background_color, hover_color, border_color = "#a46857", "#e78d74", "#c5664c"
    else:
        background_color, hover_color, border_color = "#4c4c4b", "#3E3E42", "#686867"
    return (
        "QPushButton {                            "
        "    font-size: 10px;                     "
        "    color: white;                        "
        f"   background-color: {background_color};"
        "    margin: 10px;                        "
        "    margin-bottom: 0px;                  "
        f"   border-left: 3px solid {border_color};"
        "    border-radius: 15px;                 "
        "}                                        "
        "QPushButton:hover {                      "
        f"   background-color: {hover_color};           "
        "}                                        "
    )


replying_to_label_style = """
    color: white;
    font-size: 12px;
    border-left: 3px solid grey;
    background-color: #4c4c4b;
    border-radius: 5px;
"""


class Colors:
    # Main colors
    PRIMARY = "#c96442"  # Main terracotta
    PRIMARY_DARK = "#a84f34"  # Darker terracotta
    PRIMARY_LIGHT = "#e87a55"  # Lighter terracotta

    # Secondary colors
    SECONDARY = "#42a5c9"  # Teal blue (complementary to main color)
    SECONDARY_DARK = "#346e87"  # Darker teal
    SECONDARY_LIGHT = "#5dbfe6"  # Lighter teal

    # Background colors
    BACKGROUND_DARK = "#1f1a17"  # Very dark brown/black
    BACKGROUND_MEDIUM = "#2d2622"  # Dark brown
    BACKGROUND_LIGHT = "rgb(201, 100, 66)"  # Medium-dark brown

    # Accent colors
    ACCENT_SUCCESS = "#4a9660"  # Dark green
    ACCENT_WARNING = "#c9a542"  # Dark gold
    ACCENT_ERROR = "#c94252"  # Dark red

    # Text colors
    TEXT_PRIMARY = "#f0e6e0"  # Light cream
    TEXT_SECONDARY = "#b3aaa3"  # Medium gray
    TEXT_MUTED = "#7d746d"  # Dark gray

    # UI elements
    DIVIDER = "#413b36"  # Slightly lighter than background
    CARD_BACKGROUND = "#342e29"  # Slightly lighter than main background
    TOOLTIP_BACKGROUND = "#262220"  # Dark background for tooltips

    # Message bubbles
    USER_MESSAGE_BUBBLE = "#a04d36"  # Darker version of primary
    OTHER_MESSAGE_BUBBLE = "#30302e"  # Same as BACKGROUND_MEDIUM

    # Status indicators
    OFFLINE_STATUS = "#8a8582"  # Gray
