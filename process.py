import re

with open('update_profile.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Extract ART
art_match = re.search(r'ART = r"""\n(.*?)\n"""', content, flags=re.DOTALL)
art_lines = art_match.group(1).split('\n')

# 2. Modify eyes
for i in range(61, 67):
    line = art_lines[i]
    if len(line) > 140:
        left = line[:105]
        middle = line[105:140]
        right = line[140:]
        
        middle = middle.replace('@', '\x01')
        middle = middle.replace('%', '\x02')
        middle = middle.replace('#', '\x03')
        middle = middle.replace('*', '\x04')
        
        art_lines[i] = left + middle + right

new_art = '\n'.join(art_lines)
content = content[:art_match.start()] + 'ART = r"""\n' + new_art + '\n"""' + content[art_match.end():]

# 3. Modify SVG dimensions
content = content.replace('width="1250" height="850" viewBox="0 0 1250 850"', 'width="1000" height="680" viewBox="0 0 1000 680"')
content = content.replace('width="1249" height="849"', 'width="999" height="679"')
content = content.replace('x="760" y="{200 + i * 21}"', 'x="650" y="{130 + i * 21}"')
content = content.replace('y="{40 + i * 7}" fill="{p["art"]}" font-size="6px"', 'y="{30 + i * 5.8}" fill="{p["art"]}" font-size="5px"')

# 4. Modify the replace chain for colors
old_replace = 'line_html = html.escape(line).replace("#", f\'<tspan fill="{p["h"]}">#</tspan>\').replace("@", f\'<tspan fill="{p["k"]}">@</tspan>\').replace("%", f\'<tspan fill="{p["g"]}">%</tspan>\')'
new_replace = 'line_html = html.escape(line).replace("\\x01", \'<tspan fill="#ff0000">@</tspan>\').replace("\\x02", \'<tspan fill="#ff0000">%</tspan>\').replace("\\x03", \'<tspan fill="#ff0000">#</tspan>\').replace("\\x04", \'<tspan fill="#ff0000">*</tspan>\')'
content = content.replace(old_replace, new_replace)

with open('update_profile.py', 'w', encoding='utf-8') as f:
    f.write(content)

