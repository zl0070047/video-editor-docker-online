from cairosvg import svg2png
from pathlib import Path
import os

# 确保输出目录存在
docs_dir = Path('docs/images')
docs_dir.mkdir(parents=True, exist_ok=True)

# 转换设置
conversion_settings = {
    'upload.svg': (600, 200),     # 上传区域
    'preview.svg': (800, 400),    # 视频预览
    'controls.svg': (800, 200),   # 控制面板
    'progress.svg': (600, 100),   # 进度条
}

# 转换所有SVG文件
for svg_file, (width, height) in conversion_settings.items():
    svg_path = docs_dir / svg_file
    png_path = docs_dir / svg_file.replace('.svg', '.png')
    
    if svg_path.exists():
        print(f"Converting {svg_file} to PNG...")
        with open(svg_path, 'rb') as svg_file:
            svg_content = svg_file.read()
            
        # 转换为PNG
        svg2png(
            bytestring=svg_content,
            write_to=str(png_path),
            output_width=width,
            output_height=height
        )
        print(f"Created {png_path}")
    else:
        print(f"Warning: {svg_file} not found")

print("Conversion complete!") 