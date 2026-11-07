"""Draws the LiftLog app icons (no dependencies). Run: python tools/make_icons.py

Full-bleed dark square with an orange dumbbell kept inside the middle 60%,
so it survives iOS corner rounding and Android's circular/maskable crop.
"""
import os
import struct
import zlib

BG = (0x0f, 0x10, 0x12)
FG = (0xff, 0x7a, 0x45)

# shapes in a 0..1 square: (x0, y0, x1, y1, corner radius)
SHAPES = [
    (0.27, 0.47, 0.73, 0.53, 0.01),   # handle
    (0.31, 0.33, 0.37, 0.67, 0.025),  # inner plates
    (0.63, 0.33, 0.69, 0.67, 0.025),
    (0.23, 0.39, 0.29, 0.61, 0.025),  # outer plates
    (0.71, 0.39, 0.77, 0.61, 0.025),
]


def inside(x, y):
    for x0, y0, x1, y1, r in SHAPES:
        if x0 <= x <= x1 and y0 <= y <= y1:
            cx = min(max(x, x0 + r), x1 - r)
            cy = min(max(y, y0 + r), y1 - r)
            if (x - cx) ** 2 + (y - cy) ** 2 <= r * r:
                return True
    return False


def draw(size):
    ss = 4  # 4x4 supersampling for smooth edges
    rows = []
    for py in range(size):
        row = bytearray([0])
        for px in range(size):
            hits = 0
            for sy in range(ss):
                for sx in range(ss):
                    if inside((px + (sx + .5) / ss) / size, (py + (sy + .5) / ss) / size):
                        hits += 1
            a = hits / (ss * ss)
            row += bytes(round(BG[i] + (FG[i] - BG[i]) * a) for i in range(3))
        rows.append(bytes(row))
    return b''.join(rows)


def png(size, path):
    def chunk(tag, data):
        return struct.pack('>I', len(data)) + tag + data + struct.pack('>I', zlib.crc32(tag + data) & 0xffffffff)
    raw = draw(size)
    data = b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', size, size, 8, 2, 0, 0, 0)) \
        + chunk(b'IDAT', zlib.compress(raw, 9)) + chunk(b'IEND', b'')
    with open(path, 'wb') as f:
        f.write(data)


if __name__ == '__main__':
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'icons')
    os.makedirs(out, exist_ok=True)
    for size, name in [(180, 'apple-touch-icon.png'), (192, 'icon-192.png'), (512, 'icon-512.png')]:
        png(size, os.path.join(out, name))
        print('wrote', name)
