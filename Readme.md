# Piper clipboard voice

Simple clipboard monitor application.

When it detects a text in the clipboard it will create and play a piper voice.

## How to use

You need set the setup the path to the Piper executable to use this.
You can use the environment variable `PIPER_BIN` for that.
Or directly change the default value inside `clipboard_piper.py`

Execute it from the 'clipboard_piper_ui'.

```bash
python clipboard_piper_ui.py
```

Select the voice from the dropbox. Models configured at speakers.json.
You can choose to copy from the clipboard or write the text on the box and click
the 'play voice' button.

## Setup voices

You can setup available voices inside the `speakers.json` file.
`name` is the displayed name inside the dropbox
`model` is the local path to the voice model.
Local to the piper bin path setup above.

### UI shortcuts

- `win+z` | Play voice button shortcut
- `win+c` | Toggle auto-play from clipboard
- `ctrl+alt+a` | Stop playing voice
