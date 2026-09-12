from pathlib import Path
import re, shutil

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'dist'
RED=ROOT/'redesign'

# Copy the shared cinematic assets first so every generated route can use them.
shutil.copy2(RED/'cinematic.css',OUT/'cinematic.css')
shutil.copy2(RED/'cinematic-global.css',OUT/'cinematic-global.css')
shutil.copy2(RED/'cinematic.js',OUT/'cinematic.js')
(OUT/'images').mkdir(parents=True, exist_ok=True)
shutil.copy2(RED/'hero-art.webp',OUT/'images'/'visioncraft-hero-art.webp')

# Replace the homepage body with the approved cinematic composition. The homepage
# has its own header/footer so the legacy shell cannot change the mockup proportions.
index=OUT/'index.html'
doc=index.read_text()
home=(RED/'home.html').read_text()
doc=re.sub(r'<main id="main">.*?</main>',home,doc,flags=re.S)
doc=doc.replace('<body>','<body class="vc-home-page">',1)
index.write_text(doc)

# Add the live Address12 website anywhere the generated project content appears.
work_page=OUT/'work.html'
if work_page.exists():
    doc=work_page.read_text()
    doc=doc.replace(
        '<a class="text-link" href="work-address12.html">Explore the project</a>',
        '<a class="text-link" href="work-address12.html">Explore the project</a> <a class="text-link" href="https://address12.com/" target="_blank" rel="noopener noreferrer">Visit Address12 ↗</a>'
    )
    work_page.write_text(doc)

address_page=OUT/'work-address12.html'
if address_page.exists():
    doc=address_page.read_text()
    doc=doc.replace(
        '<p>Address12 is a local application, so its private operator environment is not linked from this portfolio. Request a demonstration to explore the relevant workflows.</p><a class="btn btn-primary" href="contact.html?project=Address12">Request an Address12 demonstration</a>',
        '<p>Address12 is VisionCraft Labs’ hospitality operating platform. Visit the public website or contact the studio to discuss a demonstration.</p><div class="hero-ctas"><a class="btn btn-primary" href="https://address12.com/" target="_blank" rel="noopener noreferrer">Visit Address12 ↗</a><a class="btn btn-ghost" href="contact.html?project=Address12">Request a demonstration</a></div>'
    )
    address_page.write_text(doc)

# Apply the cinematic design system. IMPORTANT: the homepage intentionally does NOT
# load cinematic-global.css because that stylesheet is for secondary pages and its
# broad !important rules would override the approved homepage composition.
for page in OUT.glob('*.html'):
    doc=page.read_text()
    if page.name == 'index.html':
        if 'href="cinematic.css"' not in doc:
            doc=doc.replace(
                '<link rel="stylesheet" href="experience.css">',
                '<link rel="stylesheet" href="experience.css"><link rel="stylesheet" href="cinematic.css">'
            )
        doc=doc.replace('<link rel="stylesheet" href="cinematic-global.css">','')
    else:
        if 'href="cinematic.css"' not in doc:
            doc=doc.replace(
                '<link rel="stylesheet" href="experience.css">',
                '<link rel="stylesheet" href="experience.css"><link rel="stylesheet" href="cinematic.css"><link rel="stylesheet" href="cinematic-global.css">'
            )
        elif 'href="cinematic-global.css"' not in doc:
            doc=doc.replace(
                '<link rel="stylesheet" href="cinematic.css">',
                '<link rel="stylesheet" href="cinematic.css"><link rel="stylesheet" href="cinematic-global.css">'
            )
    if 'src="cinematic.js"' not in doc:
        doc=doc.replace(
            '<script src="experience.js" defer></script>',
            '<script src="experience.js" defer></script><script src="cinematic.js" defer></script>'
        )
    if page.name == 'index.html':
        doc=doc.replace('<meta name="theme-color" content="#06080D">','<meta name="theme-color" content="#08090A">')
    else:
        doc=doc.replace('<meta name="theme-color" content="#06080D">','<meta name="theme-color" content="#F2F0EA">')
    page.write_text(doc)

print('Applied VisionCraft cinematic design system to all generated pages.')
