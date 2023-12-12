# 🌐 Voxa

Voxa is an easy-to-use Python package designed to translate text.

---

## 🛠 Installation

To get started with Voxa, simply run the following command:

```bash
pip install voxa
```

## 🚀 Usage
Using Voxa is straightforward. Below is a quick example to translate an English text into French:
```python
import voxa

translator = voxa.Translator(source='en', target='fr')
translated_text = translator.translate("Hello")

print(translated_text)
```

Happy translating! 🌍
