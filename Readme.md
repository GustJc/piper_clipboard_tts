# Piper clipboard voice

Simple clipboard monitor application.

When it detects a text in the clipboard it will create and play a piper voice.

## How to use

You need to have Piper and set the location to it

Execute it from the 'clipboard_piper_ui'.

```bash
python clipboard_piper_ui.py
```

Select the voice from the dropbox. Models configured at speakers.json.
You can choose to copy from the clipboard or write the text on the box and click
the 'play voice' button.

### UI shortcuts

- `ctrl+alt+a` | Stop playing voice
- `win+z` | Play voice button shortcut
- `win+c` | Toggle auto-play from clipboard
