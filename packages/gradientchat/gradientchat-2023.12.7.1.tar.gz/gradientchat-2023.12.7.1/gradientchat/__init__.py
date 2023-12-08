__version__ = "2023.12.07.01"

class Bot:
	cli = __import__("socketio").Client()
	isConn = False
	cmds = {}
	@cli.on("auth")
	def authHandle(aObj):
		print(aObj)
	del authHandle
	def __init__(self, usern, pref=None):
		if type(usern) != type(""):
			raise TypeError("Bot name must be a string")
		if type(pref) != type(""): pref = f"{usern[0].lower()}!"
	def cmd(self, arg=None):
		if isConn:
			raise TypeError("Cannot add commands when bot is connected")
		def decor(func):
			def wrapper(*args, **kwargs):
				result = func(*args, **kwargs)
				return result
			return wrapper
		if callable(arg):
			func = arg
			arg = func.name
			cmds.append({"name": arg, "func": func})
			return decor(func)
		cmds.append({"name": arg, "func": func})
		return decor
	def connect(self, servUrl=None):
		if isConn:
			raise Exception("Already connected")
		isConn = True
		try:
			cli.connect("https://gradientchat.glitch.me" if type(servUrl) != type("") else servUrl)
		except BaseException as err:
			raise err from None