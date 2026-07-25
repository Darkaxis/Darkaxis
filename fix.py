import os, re
with open('C:/Users/Aubie Bryne/.gemini/antigravity-ide/brain/82383ea0-3f4a-4007-827e-aadea5f84584/scratch/ascii.txt', 'r', encoding='utf-8') as f:
    new_art = f.read()

with open('update_profile.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace ART
content = re.sub(r'ART = r\"\"\"(.*?)\"\"\"', 'ART = r"""\n' + new_art.replace('\\', '\\\\') + '\n"""', content, flags=re.DOTALL)

# Replace SVG dimensions
content = content.replace('width="1000" height="540" viewBox="0 0 1000 540"', 'width="2100" height="1720" viewBox="0 0 2100 1720"')
content = content.replace('width="999" height="539"', 'width="2099" height="1719"')
content = content.replace('x="540" y="{45 + i * 21}"', 'x="1600" y="{600 + i * 30}"')

# Also increase the right column spacing and font size maybe? Let's just keep font size 13px but scale up? 
# Wait, if we keep font size 13px, it will be tiny next to a 1700px ASCII art.
# The ASCII art is drawn at font-size="13px". So it will be 1700px tall. The right side should probably have a larger font, or just be grouped. 
# Let's increase font size of the right column by separating the text tags or we just use 13px everywhere. The ASCII art is also 13px. So they will visually match the scale of characters.
# Let's increase the spacing `30` instead of `21`.

# Replace colors for `@` and `%` too
content = content.replace(
    'replace("#", f\'<tspan fill="{p["h"]}">#</tspan>\')',
    'replace("#", f\'<tspan fill="{p["h"]}">#</tspan>\').replace("@", f\'<tspan fill="{p["k"]}">@</tspan>\').replace("%", f\'<tspan fill="{p["g"]}">%</tspan>\')'
)

with open('update_profile.py', 'w', encoding='utf-8') as f:
    f.write(content)
