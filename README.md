# colour-palette-generator

Simple Flask web app to upload an image and view its top colour palette using an adaptive quantization approach.

## Quickstart

1. Create a virtual environment
   - Windows PowerShell:
     ```powershell
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```
2. Install dependencies
   ```powershell
   pip install -r requirements.txt
   ```
3. Run the app
   ```powershell
   python app.py
   ```
4. Open `http://127.0.0.1:5000` in your browser.

## Notes

- Implementation inspired by the tutorial “Image Colour Palette Generator - Flask” on GeeksforGeeks: `https://www.geeksforgeeks.org/image-colour-palette-generator-flask/`.
- Uses Pillow to quantize images to an adaptive palette and count top colours.