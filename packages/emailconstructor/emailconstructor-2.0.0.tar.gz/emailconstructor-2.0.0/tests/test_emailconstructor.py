from collections import OrderedDict
from typing import Sequence

import pytest

from emailconstructor import EmailConstructor


@pytest.fixture
def email_constructor():
    return EmailConstructor(
        "smtp.domain.com",
        100,
        "sender@domain.com",
        primary_recipients=["recipient1@domain.com"],
        subject="Test",
    )


def test_reset(email_constructor: EmailConstructor):
    print(email_constructor.subject)
    email_constructor.reset()

    assert email_constructor.body == ""
    assert email_constructor.primary_recipients == []
    assert email_constructor.cc_recipients == []
    assert email_constructor.subject == ""
    assert email_constructor.attachments == []
    assert email_constructor._inline_images == []


def test_add(email_constructor: EmailConstructor):
    email_constructor.add("Some text.")
    email_constructor.add(" Some more text.")

    assert email_constructor.body == "Some text. Some more text."


def test_line_break(email_constructor: EmailConstructor):
    email_constructor.add("Some text.")
    email_constructor.line_break(2)
    email_constructor.add("Some more text.")

    assert email_constructor.body == "Some text.</br></br>Some more text."


def test_strong(email_constructor: EmailConstructor):
    with email_constructor.strong():
        email_constructor.add("Some text.")

    assert email_constructor.body == "<strong>Some text.</strong>"


def test_italics(email_constructor: EmailConstructor):
    with email_constructor.italics():
        email_constructor.add("Some text.")

    assert email_constructor.body == "<i>Some text.</i>"


def test_underline(email_constructor: EmailConstructor):
    with email_constructor.underline():
        email_constructor.add("Some text.")

    assert email_constructor.body == "<u>Some text.</u>"


def test_link(email_constructor: EmailConstructor):
    with email_constructor.link(
        "https://www.google.com", {"font-family": "Arial", "font-size": "12px"}
    ):
        email_constructor.add("Google")

    assert (
        email_constructor.body
        == '<a href="https://www.google.com" style="font-family:Arial;font-size:12px">Google</a>'
    )


def test_paragraph(email_constructor: EmailConstructor):
    with email_constructor.paragraph({"font-family": "Arial", "font-size": "12px"}):
        email_constructor.add("Some text.")

    assert (
        email_constructor.body
        == '<p style="font-family:Arial;font-size:12px">Some text.</p>'
    )


def test_span(email_constructor: EmailConstructor):
    with email_constructor.span({"color": "red", "background-color": "blue"}):
        email_constructor.add("Some text.")

    assert (
        email_constructor.body
        == '<span style="color:red;background-color:blue">Some text.</span>'
    )


def div(email_constructor: EmailConstructor):
    with email_constructor.div({"color": "red", "background-color": "blue"}):
        email_constructor.add("Some text.")

    assert (
        email_constructor.body
        == '<div style="font-family:Arial;font-size:12px">Some text.</div>'
    )


def test_table(email_constructor: EmailConstructor):
    with email_constructor.table({"border": "1px solid", "padding": "5px"}):
        pass

    assert (
        email_constructor.body == '<table style="border:1px solid;padding:5px"></table>'
    )


def test_table_head(email_constructor: EmailConstructor):
    with email_constructor.table_head({"border": "1px solid", "padding": "5px"}):
        pass

    assert (
        email_constructor.body == '<thead style="border:1px solid;padding:5px"></thead>'
    )


def test_table_row(email_constructor: EmailConstructor):
    with email_constructor.table_row({"border": "1px solid", "padding": "5px"}):
        pass

    assert email_constructor.body == '<tr style="border:1px solid;padding:5px"></tr>'


def test_table_header(email_constructor: EmailConstructor):
    with email_constructor.table_header({"border": "1px solid", "padding": "5px"}):
        pass

    assert email_constructor.body == '<th style="border:1px solid;padding:5px"></th>'


def test_table_body(email_constructor: EmailConstructor):
    with email_constructor.table_body({"border": "1px solid", "padding": "5px"}):
        pass

    assert (
        email_constructor.body == '<tbody style="border:1px solid;padding:5px"></tbody>'
    )


def test_table_data(email_constructor: EmailConstructor):
    with email_constructor.table_data({"border": "1px solid", "padding": "5px"}):
        pass

    assert email_constructor.body == '<td style="border:1px solid;padding:5px"></td>'


def test_unordered_list(email_constructor: EmailConstructor):
    with email_constructor.unordered_list({"font-family": "Arial"}):
        pass

    assert email_constructor.body == '<ul style="font-family:Arial"></ul>'


def test_list_item(email_constructor: EmailConstructor):
    with email_constructor.list_item({"font-family": "Arial"}):
        pass

    assert email_constructor.body == '<li style="font-family:Arial"></li>'


def test_build_table_builds_table_with_headers_and_two_dimensional_data(
    email_constructor: EmailConstructor,
):
    headers = ["Column1", "Column2", "Column3"]
    data = [["Value1", "Value2", "Value3"], ["Value4", "Value5", "Value6"]]

    email_constructor.build_table(data, headers)

    assert (
        email_constructor.body
        == "<table><thead><tr><th>Column1</th><th>Column2</th><th>Column3</th>"
        "</tr></thead><tbody><tr><td>Value1</td><td>Value2</td><td>Value3</td>"
        "</tr><tr><td>Value4</td><td>Value5</td><td>Value6</td></tr></tbody></table>"
    )


def test_build_table_builds_table_with_no_headers_and_sequence_of_dicts_data(
    email_constructor: EmailConstructor,
):
    data = [
        OrderedDict({"Column1": "Value1", "Column2": "Value2", "Column3": "Value3"}),
        OrderedDict({"Column1": "Value4", "Column2": "Value5", "Column3": "Value6"}),
    ]

    email_constructor.build_table(data)

    assert (
        email_constructor.body
        == "<table><thead><tr><th>Column1</th><th>Column2</th><th>Column3</th>"
        "</tr></thead><tbody><tr><td>Value1</td><td>Value2</td><td>Value3</td>"
        "</tr><tr><td>Value4</td><td>Value5</td><td>Value6</td></tr></tbody></table>"
    )


def test_build_table_builds_table_with_styling(email_constructor: EmailConstructor):
    headers = ["Column1", "Column2", "Column3"]
    data = [["Value1", "Value2", "Value3"], ["Value4", "Value5", "Value6"]]
    table_style = {"border": "1px solid"}
    header_style = {"color": "blue"}
    body_style = {"color": "grey"}

    email_constructor.build_table(
        data,
        headers,
        table_style=table_style,
        header_style=header_style,
        body_style=body_style,
    )

    assert (
        email_constructor.body
        == '<table style="border:1px solid"><thead style="color:blue"><tr><th>Column1</th>'
        '<th>Column2</th><th>Column3</th></tr></thead><tbody style="color:grey"><tr>'
        "<td>Value1</td><td>Value2</td><td>Value3</td></tr><tr><td>Value4</td><td>Value5</td>"
        "<td>Value6</td></tr></tbody></table>"
    )


def test_build_table_builds_table_with_conditional_row_styling(
    email_constructor: EmailConstructor,
):
    headers = ["Column1", "Column2", "Column3"]
    data = [["Value1", "Value2", "Value3"], ["Value4", "Value5", "Value6"]]
    get_row_style = lambda row: {"color": "red"} if row[0] == "Value4" else {}

    email_constructor.build_table(data, headers, get_row_style=get_row_style)

    assert (
        email_constructor.body
        == "<table><thead><tr><th>Column1</th><th>Column2</th><th>Column3</th></tr></thead>"
        '<tbody><tr><td>Value1</td><td>Value2</td><td>Value3</td></tr><tr style="color:red">'
        "<td>Value4</td><td>Value5</td><td>Value6</td></tr></tbody></table>"
    )


def test_build_table_builds_table_with_conditional_cell_styling(
    email_constructor: EmailConstructor,
):
    headers = ["Column1", "Column2", "Column3"]
    data = [[1, 2, 3], [4, 5, 6]]
    get_cell_style = lambda cell: {"color": "red"} if cell % 2 == 0 else {}

    email_constructor.build_table(data, headers, get_cell_style=get_cell_style)

    assert (
        email_constructor.body
        == "<table><thead><tr><th>Column1</th><th>Column2</th><th>Column3</th></tr></thead>"
        '<tbody><tr><td>1</td><td style="color:red">2</td><td>3</td></tr><tr>'
        '<td style="color:red">4</td><td>5</td><td style="color:red">6</td></tr></tbody></table>'
    )


def test_build_list_builds_list(email_constructor: EmailConstructor):
    data = ["Bullet1", "Bullet2", "Bullet3"]

    email_constructor.build_list(data)

    assert (
        email_constructor.body
        == "<ul><li>Bullet1</li><li>Bullet2</li><li>Bullet3</li></ul>"
    )


def test_build_list_builds_list_with_styling(email_constructor: EmailConstructor):
    data = ["Bullet1", "Bullet2", "Bullet3"]

    email_constructor.build_list(data, {"color": "blue", "font-size": "16px"})

    assert (
        email_constructor.body
        == '<ul style="color:blue;font-size:16px"><li>Bullet1</li><li>Bullet2</li>'
        "<li>Bullet3</li></ul>"
    )


def test_add_inline_image(email_constructor: EmailConstructor):
    email_constructor.add_inline_image(
        "folder/my_image.jpg", {"height": 100, "width": 200}
    )

    assert (
        email_constructor.body
        == '<img src="cid:folder/my_image.jpg" style="height:100;width:200">'
    )


def test_send_simple_email(mocker, email_constructor: EmailConstructor):
    SMTPMock = mocker.patch("smtplib.SMTP")

    email_constructor.add("This is some text.")
    email_constructor.send("password")

    assert (
        mocker.call().__enter__().login("sender@domain.com", "password")
        in SMTPMock.mock_calls
    )
    assert (
        mocker.call()
        .__enter__()
        .sendmail(
            "sender@domain.com",
            ["recipient1@domain.com"],
            _SubstringMatcher(("This is some text.")),
        )
        in SMTPMock.mock_calls
    )


def test_send_email_with_attachment_and_inline_image(
    mocker, email_constructor: EmailConstructor
):
    SMTPMock = mocker.patch("smtplib.SMTP")

    email_constructor.add("This is some text.")
    email_constructor.add_inline_image("tests/data/inline_image.jpg")
    email_constructor.attachments.append("tests/data/attachment.txt")

    email_constructor.send("password")

    assert (
        mocker.call().__enter__().login("sender@domain.com", "password")
        in SMTPMock.mock_calls
    )
    assert (
        mocker.call()
        .__enter__()
        .sendmail(
            "sender@domain.com",
            ["recipient1@domain.com"],
            _SubstringMatcher(
                (
                    "This is some text.",
                    "tests/data/inline_image.jpg",
                    "attachment.txt",
                )
            ),
        )
        in SMTPMock.mock_calls
    )


class _SubstringMatcher:
    def __init__(self, substrings: Sequence[str]):
        self._substrings = substrings

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, str):
            return False

        for substring in self._substrings:
            if substring not in __value:
                return False

        return True
