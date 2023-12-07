from dataclasses import dataclass
from typing import cast

from textual import events, on
from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.css.query import NoMatches
from textual.message import Message
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Button, Input, TextArea


class PastableInput(Input):
    def _on_paste(self, event: events.Paste) -> None:
        if event.text:
            self.insert_text_at_cursor(event.text)
            if len(event.text.splitlines()) > 1:
                input = cast(FlexibleInput, self.parent.parent)  # type: ignore
                input.text = self.value
                input.toggle_multiline()
        event.stop()
        event.prevent_default()


class FlexibleInput(Widget):
    is_multiline = reactive(False)
    text = reactive("")

    @dataclass
    class Submitted(Message):
        input: "FlexibleInput"
        value: str

        @property
        def control(self) -> "FlexibleInput":
            return self.input

    def __init__(self, text, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.text = text

    def on_mount(self) -> None:
        input = self.query_one("#promptInput", PastableInput)
        textarea = self.query_one("#promptArea", TextArea)
        textarea.show_line_numbers = False
        input.focus()

    def clear(self) -> None:
        self.text = ""
        self.query_one("#promptInput", PastableInput).value = ""
        self.query_one("#promptArea", TextArea).text = ""

    def focus(self) -> "FlexibleInput":
        if self.is_multiline:
            self.query_one("#promptArea", TextArea).focus()
        else:
            self.query_one("#promptInput", PastableInput).focus()
        return self

    def toggle_multiline(self):
        self.is_multiline = not self.is_multiline
        input = self.query_one("#promptInput", PastableInput)
        textarea = self.query_one("#promptArea", TextArea)
        if self.is_multiline:
            textarea.text = self.text
            self.add_class("multiline")
            self.remove_class("singleline")
            line_count = textarea.document.line_count
            textarea.cursor_location = (
                line_count - 1,
                len(textarea.document.get_line(line_count - 1)),
            )
        else:
            input.value = self.text
            self.add_class("singleline")
            self.remove_class("multiline")
        self.focus()

    def watch_text(self):
        try:
            if len(self.text.splitlines()) > 1:
                self.query_one("#toggle-multiline", Button).disabled = True
            else:
                self.query_one("#toggle-multiline", Button).disabled = False
        except NoMatches:
            pass

    @on(PastableInput.Submitted, "#promptInput")
    def on_input_submitted(self, event: PastableInput.Submitted):
        self.post_message(self.Submitted(self, event.input.value))
        event.stop()
        event.prevent_default()

    @on(Button.Pressed, "#toggle-multiline")
    def on_toggle_multiline_pressed(self):
        self.toggle_multiline()

    @on(PastableInput.Changed, "#promptInput")
    def on_input_changed(self, event: PastableInput.Changed):
        self.text = event.input.value

    @on(TextArea.Changed, "#promptArea")
    def on_area_changed(self, event: TextArea.Changed):
        lines = [
            event.text_area.document.get_line(line)
            for line in range(event.text_area.document.line_count)
        ]

        self.text = "\n".join(lines)

    @on(Button.Pressed, "#post")
    async def on_post(self):
        self.post_message(self.Submitted(self, self.text))

    def compose(self) -> ComposeResult:
        with Horizontal():
            yield PastableInput(
                id="promptInput",
                placeholder="Message Ollama…",
            )
            yield TextArea(id="promptArea")
            with Horizontal(id="button-container"):
                yield Button("post", id="post", variant="primary")
                yield Button("↕", id="toggle-multiline", variant="success")
