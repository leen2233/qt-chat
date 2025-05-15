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


reply_to_label_style = """
    QPushButton {
        font-size: 10px;
        color: white;
        background-color: #4c4c4b;
        margin: 10px;
        margin-bottom: 0px;
        border-left: 3px solid #686867;
        border-radius: 5px;
    }
    QPushButton:hover {
        background-color: #3E3E42;
    }
"""


replying_to_label_style = """
    color: white;
    font-size: 12px;
    border-left: 3px solid grey;
    background-color: #4c4c4b;
    border-radius: 5px;
"""
