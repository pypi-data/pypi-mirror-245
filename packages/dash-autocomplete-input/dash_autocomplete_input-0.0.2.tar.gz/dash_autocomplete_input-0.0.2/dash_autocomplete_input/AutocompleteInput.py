# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class AutocompleteInput(Component):
    """An AutocompleteInput component.


Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- autoFocus (boolean; optional):
    autofocus.

- className (string; optional):
    Class name for the component.

- component (string; default "input"):
    Component to use, either 'textarea' or 'input'.

- disabled (boolean; optional):
    Disables widget, i.e. during form submission.

- matchAny (boolean; optional):
    If True, will match options in the middle of the word as well.

- maxOptions (number; optional):
    Defines how many options can be listed simultaneously. Show all
    matched options if maxOptions equals 0.

- minChars (number; optional):
    Only show autocompletion option list after this many characters
    have been typed after the trigger character.

- n_submit (number; default 0):
    Number of times the `Enter` key was pressed while the input had
    focus.

- offsetX (number; optional):
    Popup horizontal offset.

- offsetY (number; optional):
    Popup vertical offset.

- options (list | dict; optional):
    List of available options for autocomplete.

- passThroughEnter (boolean; optional):
    If True, then an enter / return keypress is passed on (after being
    used to autocomplete).

- passThroughTab (boolean; optional):
    If True, then an Tab keypress is passed on (after being used to
    autocomplete) to the next form input.

- placeholder (string; optional):
    Placeholder string.

- quoteWhitespaces (boolean; default False):
    Whether the options containing whitespaces should be quoted.

- regex (string; optional):
    This regular expression checks if text after trigger can be
    autocompleted or not.

- spaceRemovers (string; optional):
    Remove spacer if user inputs one of these characters.

- spacer (string; optional):
    Character which is inserted along with the selected option.

- style (dict; optional):
    The input's inline styles.

- trigger (string | list of strings; optional):
    Character or string, which triggers showing autocompletion option
    list.

- value (string; default ""):
    The value displayed in the input."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_autocomplete_input'
    _type = 'AutocompleteInput'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, value=Component.UNDEFINED, placeholder=Component.UNDEFINED, quoteWhitespaces=Component.UNDEFINED, style=Component.UNDEFINED, n_submit=Component.UNDEFINED, component=Component.UNDEFINED, trigger=Component.UNDEFINED, options=Component.UNDEFINED, className=Component.UNDEFINED, disabled=Component.UNDEFINED, maxOptions=Component.UNDEFINED, matchAny=Component.UNDEFINED, offsetX=Component.UNDEFINED, offsetY=Component.UNDEFINED, regex=Component.UNDEFINED, spaceRemovers=Component.UNDEFINED, spacer=Component.UNDEFINED, minChars=Component.UNDEFINED, passThroughEnter=Component.UNDEFINED, passThroughTab=Component.UNDEFINED, autoFocus=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'autoFocus', 'className', 'component', 'disabled', 'matchAny', 'maxOptions', 'minChars', 'n_submit', 'offsetX', 'offsetY', 'options', 'passThroughEnter', 'passThroughTab', 'placeholder', 'quoteWhitespaces', 'regex', 'spaceRemovers', 'spacer', 'style', 'trigger', 'value']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'autoFocus', 'className', 'component', 'disabled', 'matchAny', 'maxOptions', 'minChars', 'n_submit', 'offsetX', 'offsetY', 'options', 'passThroughEnter', 'passThroughTab', 'placeholder', 'quoteWhitespaces', 'regex', 'spaceRemovers', 'spacer', 'style', 'trigger', 'value']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(AutocompleteInput, self).__init__(**args)
