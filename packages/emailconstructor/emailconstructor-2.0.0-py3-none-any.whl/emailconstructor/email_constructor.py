import os
import smtplib
from collections import OrderedDict
from email import encoders
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Any, Callable, Sequence


class EmailConstructor:
    """Class for dynamically building and sending emails with HTML content,
    inline images, and attachments."""

    def __init__(
        self,
        smtp_server_url: str,
        smtp_server_port: int,
        sender_address: str,
        primary_recipients: list[str] = [],
        cc_recipients: list[str] = [],
        subject: str | None = None,
        attachments: list[str] = [],
    ):
        """Initializes the `EmailConstructor`.

        Args:
            smtp_server_url: The URL of the SMTP email server (i.e. smtp.gmail.com).
            smtp_server_port: The SMTP port number to use.
            sender_address: The email address of the sender.
            primary_recipients: A list of primary recipient email addresses. Defaults to [].
            cc_recipients: A list of CC recipient email addresses. Defaults to [].
            subject: The email message subject. Defaults to None.
            attachments: A list of file paths for email attachments. Defaults to [].
        """

        self.body = ""
        self.primary_recipients = primary_recipients
        self.cc_recipients = cc_recipients
        self.subject = subject
        self.attachments = attachments

        self._smtp_server_url = smtp_server_url
        self._smtp_server_port = smtp_server_port
        self._sender_address = sender_address
        self._inline_images: list[str] = []

    def reset(self):
        """Resets the email body, all recipients, inline images, and attachments."""

        self.body = ""
        self.primary_recipients = []
        self.cc_recipients = []
        self.subject = ""
        self.attachments = []

        self._inline_images = []

    def add(self, content: str):
        """Adds some string content to the email message.

        Args:
            content: Content to be added.
        """

        self.body += content

    def line_break(self, count=1):
        """Adds the specified number of line break tags to the email body.

        Args:
            count: The number of line break tags to add. Defaults to 1.

        Raises:
            ValueError: If the provided `count` argument is less than 1.
        """

        if count < 1:
            raise ValueError("The `count` argument must be 1 or greater.")

        self.body += "".join("</br>" for i in range(0, count))

    def strong(self):
        """Returns a context manager class that opens and closes a `<strong>` tag within the email body.

        Returns:
            A context manager class for the tag.
        """

        return _StrongTag(self)

    def italics(self):
        """Returns a context manager class that opens and closes a `<i>` tag within the email body.

        Returns:
            A context manager class for the tag.
        """

        return _ItalicsTag(self)

    def underline(self):
        """Returns a context manager class that opens and closes a `<u>` tag within the email body.

        Returns:
            A context manager class for the tag.
        """

        return _UnderlineTag(self)

    def link(self, href: str, style: dict[str, Any] = {}):
        """Returns a context manager class that opens and closes a `<strong>` tag within the email body.

        Returns:
            A context manager class for the tag.
        """

        return _LinkTag(self, href, style)

    def paragraph(self, style: dict[str, Any] = {}):
        """Returns a context manager class that opens and closes a `<p>` tag within the email body.

        Args:
            style: A dict containing CSS style properties and values. Defaults to {}.

        Returns:
            A context manager class for the tag.
        """

        return _ParagraphTag(self, style)

    def span(self, style: dict[str, Any] = {}):
        """Returns a context manager class that opens and closes a `<span>` tag within the email body.

        Args:
            style: A dict containing CSS style properties and values. Defaults to {}.

        Returns:
            A context manager class for the tag.
        """

        return _SpanTag(self, style)

    def div(self, style: dict[str, Any] = {}):
        """Returns a context manager class that opens and closes a `<div>` tag within the email body.

        Args:
            style: A dict containing CSS style properties and values. Defaults to {}.

        Returns:
            A context manager class for the tag.
        """

        return _DivTag(self, style)

    def table(self, style: dict[str, Any] = {}):
        """Returns a context manager class that opens and closes a `<table>` tag within the email body.

        Args:
            style: A dict containing CSS style properties and values. Defaults to {}.

        Returns:
            A context manager class for the tag.
        """

        return _Table(self, style)

    def table_head(self, style: dict[str, Any] = {}):
        """Returns a context manager class that opens and closes a `<thead>` tag within the email body.

        Args:
            style: A dict containing CSS style properties and values. Defaults to {}.

        Returns:
            A context manager class for the tag.
        """

        return _TableHead(self, style)

    def table_row(self, style: dict[str, Any] = {}):
        """Returns a context manager class that opens and closes a `<tr>` tag within the email body.

        Args:
            style: A dict containing CSS style properties and values. Defaults to {}.

        Returns:
            A context manager class for the tag.
        """

        return _TableRow(self, style)

    def table_header(self, style: dict[str, Any] = {}):
        """Returns a context manager class that opens and closes a `<th>` tag within the email body.

        Args:
            style: A dict containing CSS style properties and values. Defaults to {}.

        Returns:
            A context manager class for the tag.
        """

        return _TableHeader(self, style)

    def table_body(self, style: dict[str, Any] = {}):
        """Returns a context manager class that opens and closes a `<tbody>` tag within the email body.

        Args:
            style: A dict containing CSS style properties and values. Defaults to {}.

        Returns:
            A context manager class for the tag.
        """

        return _TableBody(self, style)

    def table_data(self, style: dict[str, Any] = {}):
        """Returns a context manager class that opens and closes a `<td>` tag within the email body.

        Args:
            style: A dict containing CSS style properties and values. Defaults to {}.

        Returns:
            A context manager class for the tag.
        """

        return _TableData(self, style)

    def unordered_list(self, style: dict[str, Any] = {}):
        """Returns a context manager class that opens and closes a `<ul>` tag within the email body.

        Args:
            style: A dict containing CSS style properties and values. Defaults to {}.

        Returns:
            A context manager class for the tag.
        """

        return _UnorderedList(self, style)

    def list_item(self, style: dict[str, Any] = {}):
        """Returns a context manager class that opens and closes a `<li>` tag within the email body.

        Args:
            style: A dict containing CSS style properties and values. Defaults to {}.

        Returns:
            A context manager class for the tag.
        """

        return _ListItem(self, style)

    def build_table[
        T
    ](
        self,
        data: Sequence[Sequence[T]] | Sequence[OrderedDict[Any, T]],
        headers: Sequence[Any] | None = None,
        table_style: dict[str, Any] = {},
        header_style: dict[str, Any] = {},
        body_style: dict[str, Any] = {},
        get_row_style: Callable[[Sequence[T]], dict[str, Any]] | None = None,
        get_cell_style: Callable[[T], dict[str, Any]] | None = None,
    ):
        """Builds a table from the provided data within the email body.

        Args:
            data: The data to use to build the rows within the table. This can either be a two dimensional data structure (i.e. a list of lists) or a sequence of dicts.
            headers: A sequence of values to use for the table's column headers. If `headers` is not provided and the `data` is in a sequence of ordered dicts format, the dict key values will be used as column headers. Passing an empty sequence value such as `[]` will suppress this behavior. Defaults to None.
            table_style: A dict containing CSS style properties and values to apply to the table. Defaults to {}.
            header_style: A dict containing CSS style properties and values to apply to the table header. Defaults to {}.
            body_style: A dict containing CSS style properties and values to apply to the table body. Defaults to {}.
            get_row_style: An optional function that accepts a row of data type `Sequence[_T]` and returns a dict of CSS style properties and values to apply to the row. Can be used to conditionally style entire rows by value. Defaults to None.
            get_cell_style: An optional function that accepts a cell of data type `_T` and returns a dict of CSS style properties and values to apply to the cell. Can be used to conditionally style cells by value. Defaults to None.
        """

        dict_data = tuple(row for row in data if isinstance(row, dict))
        sequence_data = tuple(row for row in data if isinstance(row, Sequence))

        if headers is None and dict_data and isinstance(dict_data[0], OrderedDict):
            headers = tuple(key for key in dict_data[0].keys())

        if dict_data:
            sequence_data = tuple(tuple(row.values()) for row in dict_data)

        with self.table(table_style):
            if headers:
                with self.table_head(header_style):
                    with self.table_row():
                        for header in headers:
                            with self.table_header():
                                self.add(str(header))
            if data:
                with self.table_body(body_style):
                    for row in sequence_data:
                        if get_row_style:
                            row_style = get_row_style(row)
                        else:
                            row_style = {}

                        with self.table_row(row_style):
                            for cell in row:
                                if get_cell_style:
                                    cell_style = get_cell_style(cell)
                                else:
                                    cell_style = {}

                                with self.table_data(cell_style):
                                    self.add(str(cell))

    def build_list[
        T
    ](
        self,
        data: Sequence[T],
        list_style: dict[str, Any] = {},
        get_list_item_style: Callable[[T], dict[str, Any]] | None = None,
    ):
        """Constructs a simple unordered (bulleted) list from a sequence of data.

        Args:
            data: The sequence of data to build the list from.
            list_style: A dict containing CSS style properties and values to apply to the list. Defaults to {}.
            get_list_item_style: An optional function that accepts an item in the list of type `T` and returns a dict of CSS style properties and values to apply to the list item. Can be used to conditionally style list items by value. Defaults to None.
        """

        if not data:
            return

        with self.unordered_list(list_style):
            for list_item in data:
                if get_list_item_style:
                    list_item_style = get_list_item_style(list_item)
                else:
                    list_item_style = {}

                with self.list_item(list_item_style):
                    self.add(str(list_item))

    def add_inline_image(
        self,
        image_path: str,
        style: dict[str, Any] = {},
    ):
        """Inserts an inline image into the email body.

        Args:
            image_path: The file path to the image.
            style: A dict containing CSS style properties and values to apply to the image. Defaults to {}.
        """

        attributes = {"src": f"cid:{image_path}"}

        self._inline_images.append(image_path)
        _ImageTag(self, style, attributes).add()

    def send(self, sender_login_password: str):
        """Logs into the sender's email address using the provided password and sends the current email body content.

        Args:
            sender_login_password: The password for the sender's email account. For security, the password is not stored after use.

        Raises:
            RuntimeError: If no primary recipience email addresses are set.
        """
        if not self.primary_recipients:
            raise RuntimeError(
                "At least one primary recipient email address is required to send the email."
            )

        email = MIMEMultipart()
        email["From"] = self._sender_address
        email["To"] = ";".join(self.primary_recipients)
        email["Cc"] = ";".join(self.cc_recipients)
        email["Subject"] = self.subject

        email.attach(MIMEText(self.body, "html"))

        for inline_image in self._inline_images:
            with open(inline_image, "rb") as image_file:
                mime_image = MIMEImage(image_file.read())

            mime_image.add_header("Content-ID", f"<{inline_image}>")
            email.attach(mime_image)

        for attachment in self.attachments:
            mime_attachment = MIMEBase("application", "octet-stream")

            with open(attachment, "rb") as attachment_file:
                mime_attachment.set_payload(attachment_file.read())

            mime_attachment.add_header(
                "Content-Disposition",
                f'attachment; filename="{os.path.basename(attachment)}"',
            )
            encoders.encode_base64(mime_attachment)
            email.attach(mime_attachment)

        with smtplib.SMTP(self._smtp_server_url, self._smtp_server_port) as server:
            server.ehlo()
            server.starttls()
            server.login(self._sender_address, sender_login_password)
            server.sendmail(
                self._sender_address,
                self.primary_recipients + self.cc_recipients,
                email.as_string(),
            )


class _BaseTag:
    def __init__(
        self,
        email_constructor: EmailConstructor,
        tag_name: str,
        attributes: dict[str, str],
    ):
        self._email_constructor = email_constructor
        self._tag_name = tag_name
        self._attributes_string = " ".join(
            f'{key}="{value}"' for key, value in attributes.items()
        )

        if self._attributes_string:
            self._attributes_string = " " + self._attributes_string

    def __enter__(self):
        self._email_constructor.add(f"<{self._tag_name}{self._attributes_string}>")

    def __exit__(self, *args):
        self._email_constructor.add(f"</{self._tag_name}>")


class _StyledTag(_BaseTag):
    def __init__(
        self,
        email_constructor: EmailConstructor,
        tag_name: str,
        style: dict[str, Any],
        attributes: dict[str, str],
    ):
        if style:
            attributes["style"] = ";".join(
                (f"{key}:{value}" for key, value in style.items())
            )

        super().__init__(email_constructor, tag_name, attributes)


class _StrongTag(_BaseTag):
    def __init__(self, email_constructor: EmailConstructor):
        super().__init__(email_constructor, "strong", {})


class _ItalicsTag(_BaseTag):
    def __init__(self, email_constructor: EmailConstructor):
        super().__init__(email_constructor, "i", {})


class _UnderlineTag(_BaseTag):
    def __init__(self, email_constructor: EmailConstructor):
        super().__init__(email_constructor, "u", {})


class _LinkTag(_StyledTag):
    def __init__(
        self, email_constructor: EmailConstructor, href: str, style: dict[str, Any]
    ):
        super().__init__(email_constructor, "a", style, {"href": href})


class _ParagraphTag(_StyledTag):
    def __init__(self, email_constructor: EmailConstructor, style: dict[str, Any]):
        super().__init__(email_constructor, "p", style, {})


class _SpanTag(_StyledTag):
    def __init__(self, email_constructor: EmailConstructor, style: dict[str, Any]):
        super().__init__(email_constructor, "span", style, {})


class _DivTag(_StyledTag):
    def __init__(self, email_constructor: EmailConstructor, style: dict[str, Any]):
        super().__init__(email_constructor, "div", style, {})


class _Table(_StyledTag):
    def __init__(self, email_constructor: EmailConstructor, style: dict[str, Any]):
        super().__init__(email_constructor, "table", style, {})


class _TableHead(_StyledTag):
    def __init__(self, email_constructor: EmailConstructor, style: dict[str, Any]):
        super().__init__(email_constructor, "thead", style, {})


class _TableRow(_StyledTag):
    def __init__(self, email_constructor: EmailConstructor, style: dict[str, Any]):
        super().__init__(email_constructor, "tr", style, {})


class _TableHeader(_StyledTag):
    def __init__(self, email_constructor: EmailConstructor, style: dict[str, Any]):
        super().__init__(email_constructor, "th", style, {})


class _TableBody(_StyledTag):
    def __init__(self, email_constructor: EmailConstructor, style: dict[str, Any]):
        super().__init__(email_constructor, "tbody", style, {})


class _TableData(_StyledTag):
    def __init__(self, email_constructor: EmailConstructor, style: dict[str, Any]):
        super().__init__(email_constructor, "td", style, {})


class _UnorderedList(_StyledTag):
    def __init__(self, email_constructor: EmailConstructor, style: dict[str, Any]):
        super().__init__(email_constructor, "ul", style, {})


class _ListItem(_StyledTag):
    def __init__(self, email_constructor: EmailConstructor, style: dict[str, Any]):
        super().__init__(email_constructor, "li", style, {})


class _ImageTag(_StyledTag):
    def __init__(
        self,
        email_constructor: EmailConstructor,
        style: dict[str, Any],
        attributes: dict[str, str] = {},
    ):
        super().__init__(email_constructor, "img", style, attributes)

    def __enter__(self):
        return

    def __exit__(self, *args):
        return

    def add(self):
        self._email_constructor.add(f"<{self._tag_name}{self._attributes_string}>")
