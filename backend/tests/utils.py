from playwright.sync_api import Page
from playwright.sync_api import expect

import re


def fill_rich_text_widget(page: Page, text: str, editor_id: str = "form-widgets-text") -> None:
    """Fill a TinyMCE rich text iframe and sync its content back to the submitted textarea."""
    page.wait_for_function(
        """(editorId) => {
            const tinymce = window.tinymce || window.tinyMCE;
            const editor = tinymce?.get(editorId);
            return Boolean(editor && editor.initialized !== false);
        }""",
        arg=editor_id,
    )

    rich_text_area = page.locator(
        f'iframe[id="{editor_id}_ifr"]'
    ).content_frame.get_by_label("Rich Text Area")

    expect(rich_text_area).to_be_visible()
    rich_text_area.fill(text)
    expect(rich_text_area).to_contain_text(text)
    page.evaluate(
        """(editorId) => {
            const tinymce = window.tinymce || window.tinyMCE;
            const editor = tinymce?.get(editorId);
            if (!editor) {
                throw new Error(`TinyMCE editor not found: ${editorId}`);
            }
            editor.save();
            editor.fire("change");
            editor.fire("blur");
        }""",
        editor_id,
    )
    expect(page.locator(f'textarea[id="{editor_id}"]')).to_have_value(
        re.compile(re.escape(text))
    )
