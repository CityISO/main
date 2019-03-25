"""
Import main module
"""
from main import get_emotions_from_image

if __name__ == "__main__":
    for i in range(7):
        print(f" -- File {i}")
        get_emotions_from_image(f"tests/{i}.jpg")
