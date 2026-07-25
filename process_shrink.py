import re

with open('C:/Users/Aubie Bryne/.gemini/antigravity-ide/brain/82383ea0-3f4a-4007-827e-aadea5f84584/scratch/ascii.txt', 'r', encoding='utf-8') as f:
    new_art = f.read()

with open('update_profile.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace ART
content = re.sub(r'ART = r"""\n(.*?)\n"""', 'ART = r"""\n' + new_art.replace('\\', '\\\\') + '\n"""', content, flags=re.DOTALL)

# SVG Dimensions
content = content.replace('width="1000" height="680" viewBox="0 0 1000 680"', 'width="900" height="500" viewBox="0 0 900 500"')
content = content.replace('width="999" height="679"', 'width="899" height="499"')

# Layout
content = content.replace('x="650" y="{130 + i * 21}"', 'x="420" y="{45 + i * 21}"')
content = content.replace('y="{30 + i * 5.8}" fill="{p["art"]}" font-size="5px"', 'y="{45 + i * 3.6}" fill="{p["art"]}" font-size="3px"')

# Color mapping: pure greyscale (remove the \x01 stuff)
old_replace = 'line_html = html.escape(line).replace("\\x01", \'<tspan fill="#ff0000">@</tspan>\').replace("\\x02", \'<tspan fill="#ff0000">%</tspan>\').replace("\\x03", \'<tspan fill="#ff0000">#</tspan>\').replace("\\x04", \'<tspan fill="#ff0000">*</tspan>\')'
content = content.replace(old_replace, 'line_html = html.escape(line)')

# Text changes
content = content.replace('kv("Security.Focus", "Pen Testing, Vulnerability Research")', 'kv("Security.Focus", "Pen Testing, Vulnerability Research, OSINT")')
content = content.replace('kv("Security.Record", "Hack4Gov 2025 Finals")', 'kv("Awards", "Hack4Gov 2025 Finals, Programmer of the Year")')

with open('update_profile.py', 'w', encoding='utf-8') as f:
    f.write(content)
