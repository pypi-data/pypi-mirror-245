# ops-py-message-handler

---

## Description
Post a message to a url (webhook).


---

## Installation
`pip install ops-py-message-handler`

---

## Usage

### Slack
Note: In the example code below a Slack Automation Workflow has already been built. The message part of the Slack Workflow has been defined to receive a `Title` and a `Text` variable.
Export your slack webhook:   
`export WEBHOOK="12345blablabla...."`

Example code:   
```
import os
from message_handler import message_handler as mh

WEBHOOK = os.getenv("WEBHOOK")
heading = "This is the heading"
message = "This is the message"

handler = mh.MessageHandler(WEBHOOK)
handler.build_payload(Title=heading, Text=message)
handler.post_payload()
response_code = handler.get_response_code()
print(response_code)
```

### MS Teams
Export your MS Teams webhook:   
`export WEBHOOK="12345blablabla...."`

Example code:
```
import os
from message_handler import message_handler as mh

WEBHOOK = os.getenv("WEBHOOK")
payload = {
  "@type": "MessageCard",
  "@context": "http://schema.org/extensions",
  "themeColor": "0076D7",
  "summary": "-",
  "sections": [
    {
      "activityTitle": "Super Secret Key Vault",
      "activitySubtitle": "",
      "activityImage": "",
      "facts": [],
      "markdown": True
    },
    {
      "startGroup": True,
      "text": """<table bordercolor='black' border='2'>
    <thead>
    <tr style='background-color : Teal; color: White'>
        <th>Secret Name</th>
        <th>Last Updated</th>
        <th>Expiration</th>
        <th>Comment</th>
    </tr>
    </thead>
    <tbody>
    <tr>
        <td>SuperSecret</td>
        <td>2023-10-31</td>
        <td>2024-06-25</td>
        <td>Will expire in 201 days. Updated 37 days ago.</td>
    </tr>
    </tbody>
</table>"""
    }
  ]
}

handler = mh.MessageHandler(WEBHOOK)
handler.set_payload(payload)
handler.post_payload()
response_code = handler.get_response_code()
print(response_code)
```
