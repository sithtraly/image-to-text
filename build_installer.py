from version import __version__

with open("build.iss", "r") as f:
    content = f.read()

content = content.replace("{{VERSION}}", __version__)

with open("setup.iss", "w") as f:
  f.write(content)