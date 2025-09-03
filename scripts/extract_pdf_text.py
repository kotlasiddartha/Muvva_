from PyPDF2 import PdfReader
p = r"media/case_sheets/hell_helo.pdf"
reader = PdfReader(p)
text = []
for i, page in enumerate(reader.pages, start=1):
    t = page.extract_text()
    text.append(t or '')
full = "\n".join(text)
print('PAGE_COUNT:', len(reader.pages))
print('TOTAL_CHARS:', len(full))
if full.strip():
    print('---BEGIN SAMPLE---')
    print(full[:2000])
    print('---END SAMPLE---')
else:
    print('No extractable text found; PDF may be image-only or use unsupported encoding.')
