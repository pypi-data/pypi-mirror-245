# Introduction

`emailconstructor` is a simple tool for dynamically constructing and sending HTML-based emails. Some of it's high level features include:
- Composing email content using text and styled HTML elements.
- Adding email file attachments.
- Adding styled inline images.
- Creating HTML tables or lists from data sets with optional conditional styling applied per row or per data item.

`emailconstructor` was originally written for the specific use case of quickly building and sending conditional alert emails containing large amounts of tabular data, however it is suitable to be used in a wide variety of other applications.

# Installation

```
pip install emailconstructor
```

# Usage

All functionality is contained within the `EmailConstructor` class.

```py
from emailconstructor import EmailConstructor

email = EmailConstructor(
    smtp_server_url="smtpserver.domain.com",
    smtp_server_port=100,
    sender_address="senderemail@domain.com"
)
```

The subject, primary recipients, and CC recipients can all be set during initialization, or can be set/modified after.

```py
email.subject = "Your subject"
email.primary_recipients.extend(["recipient1@domain.com", "recipient2@domain.com"])
email.cc_recipients.append("recipient3@domain.com")
```

Content can be added to the email using the `add` method while HTML elements are opened and closed using context manager classes.

```py
email.add("This is some basic text followed by line breaks.")
email.line_break(count=3)

with email.span({"color": "red"}):
    email.add("This text is inside the span tag and will appear red.")

with email.div({"font-size": "30px"}):
    email.add("This text will appear in a large font ")
    with email.span({"background-color": "yellow"}):
        email.add("and this text will be highlighted.")
```

Tables and bullet lists can be easily created from data sets.

```py
list_data = ["bullet 1", "bullet 2", "bullet 3"]

# Builds a simple <ul> bulleted list from the data
email.build_list(list_data)

table_data = [
    OrderedDict({"column1": 1, "column2": 2}),
    OrderedDict({"column1": 3, "column2": 4}),
    OrderedDict({"column1": 5, "column2": 6}),
]
get_cell_style = lambda cell: {"color": "blue"} if cell % 2 == 0 else {}

# Builds a table with bolded headers and with even numbered cells colored blue
email.build_table(
    table_data, header_style={"font-weight": "bold"}, get_cell_style=get_cell_style
)
```

Inline images and file attachments can be added by path.

```py
email.add_inline_image("my_image.jpg", {"width": "100%"})
email.attachments.append("my_attachment.pdf")
```

Once finished, emails can be sent with the `send` method. A call to `reset` will clear out the email body, recipients, and subject so a new email can be built and sent.

```py
email.send("emailpassword")
email.reset()
```

