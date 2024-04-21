from uagents import Model

class Image(Model):
    path: str

class Message(Model):
    message: str

class APIResponse(Model):
    description: str
    is_dangerous: bool
    risk_level: str