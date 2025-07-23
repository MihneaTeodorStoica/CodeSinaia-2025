import os
import markdown2
import html2text

def load_notes(path):
    texts = []

    # Read .md files
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    raw = f.read()
                    html_text = markdown2.markdown(raw)
                    plain_text = html2text.HTML2Text().handle(html_text).strip()
                    texts.append(plain_text)
    return "\n".join(texts)

if __name__ == "__main__":
    notes = load_notes("D:/Git.Hub/FlorinTeo/CodeSinaia-2025.src/_Notes/0. Vineri - Setup")
    print(notes)
