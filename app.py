from flask import Flask, render_template, request
from PIL import Image
import numpy as np

app = Flask(__name__)

def rgb_to_hex(rgb_tuple):
    return "#%02x%02x%02x" % (rgb_tuple[0], rgb_tuple[1], rgb_tuple[2])

def extract_top_colors(image_file, num_colors=10):
    """Return a list of top colors with rgb, hex, count, and percent using NumPy."""
    with Image.open(image_file) as image:
        image = image.convert("RGB")
        image.thumbnail((400, 400))

        # Convert to NumPy array (H, W, 3) and flatten to (N, 3)
        pixel_array = np.asarray(image, dtype=np.uint8)
        pixels = pixel_array.reshape(-1, 3)

        # Light quantization to reduce noise and group similar colors (32 levels/channel)
        # This keeps the output stable and avoids millions of unique colors for photos
        quantized_pixels = (pixels >> 3) << 3

        # Count unique colors
        unique_colors, counts = np.unique(quantized_pixels, axis=0, return_counts=True)

        # Sort by count descending
        order = np.argsort(-counts)
        unique_colors = unique_colors[order]
        counts = counts[order]

        total_pixels = int(pixels.shape[0]) or 1

        results = []
        top_k = min(num_colors, unique_colors.shape[0])
        for i in range(top_k):
            r, g, b = (int(unique_colors[i, 0]), int(unique_colors[i, 1]), int(unique_colors[i, 2]))
            count = int(counts[i])
            rgb = (r, g, b)
            results.append(
                {
                    "rgb": rgb,
                    "hex": rgb_to_hex(rgb),
                    "count": count,
                    "percent": round((count / total_pixels) * 100, 2),
                }
            )

        return results


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        uploaded = request.files.get("file")
        num_colors_str = request.form.get("num_colors", "10").strip()
        try:
            num_colors = max(3, min(20, int(num_colors_str)))
        except ValueError:
            num_colors = 10

        if not uploaded or uploaded.filename == "":
            return render_template("index.html", error="Please choose an image file.")

        try:
                colors = extract_top_colors(uploaded, num_colors=num_colors)
        except Exception:
            return render_template(
                "index.html",
                error="Failed to process image. Please upload a valid image.",
            )

        return render_template("result.html", colors=colors, num_colors=num_colors)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)

