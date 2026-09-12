from pathlib import Path
import re, shutil

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'dist'
RED=ROOT/'redesign'

# Copy the shared cinematic assets first so every generated route can use them.
shutil.copy2(RED/'cinematic.css',OUT/'cinematic.css')
shutil.copy2(RED/'cinematic.js',OUT/'cinematic.js')

# Replace the homepage body with the approved cinematic composition while preserving
# generated metadata, schema, header and footer.
index=OUT/'index.html'
doc=index.read_text()
home=(RED/'home.html').read_text()
doc=re.sub(r'<main id="main">.*?</main>',home,doc,flags=re.S)
index.write_text(doc)

# Apply the same cinematic design system to EVERY generated HTML route. This keeps
# service, work, about, insights, investment and contact pages visually consistent.
for page in OUT.glob('*.html'):
    doc=page.read_text()
    if 'href="cinematic.css"' not in doc:
        doc=doc.replace(
            '<link rel="stylesheet" href="experience.css">',
            '<link rel="stylesheet" href="experience.css"><link rel="stylesheet" href="cinematic.css">'
        )
    if 'src="cinematic.js"' not in doc:
        doc=doc.replace(
            '<script src="experience.js" defer></script>',
            '<script src="experience.js" defer></script><script src="cinematic.js" defer></script>'
        )
    doc=doc.replace('<meta name="theme-color" content="#06080D">','<meta name="theme-color" content="#F2F0EA">')
    page.write_text(doc)

print('Applied VisionCraft cinematic design system to all generated pages.')
