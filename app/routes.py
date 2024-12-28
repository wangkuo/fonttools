from flask import Blueprint, render_template, request, jsonify, send_file, current_app
from fontTools.ttLib import TTFont
import os
from werkzeug.utils import secure_filename
import json
from fontTools import subset

main = Blueprint('main', __name__)

ALLOWED_EXTENSIONS = {'ttf', 'otf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/')
def index():
    # 检查字体文件夹是否存在
    fonts_dir = current_app.config['FONTS_DIR']
    if not os.path.exists(fonts_dir):
        os.makedirs(fonts_dir)
    
    # 获取字体文件列表
    fonts = [f for f in os.listdir(fonts_dir) if allowed_file(f)]
    return render_template('index.html', fonts=fonts)

@main.route('/upload', methods=['POST'])
def upload_font():
    if 'font' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['font']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(current_app.config['FONTS_DIR'], filename))
        return jsonify({'message': 'File uploaded successfully'})
    
    return jsonify({'error': 'Invalid file type'}), 400

@main.route('/metadata/<font_name>')
def get_metadata(font_name):
    font_path = os.path.join(current_app.config['FONTS_DIR'], font_name)
    try:
        font = TTFont(font_path)
        metadata = {
            'name': font_name,
            'tables': list(font.keys()),
            'glyphs_count': len(font.getGlyphOrder())
        }
        
        # 获取字体名称等信息
        if 'name' in font:
            name_records = {}
            for record in font['name'].names:
                if record.platformID == 3 and record.platEncID == 1:
                    name_records[record.nameID] = record.string.decode('utf-16-be')
            metadata['name_records'] = name_records
            
        return jsonify(metadata)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/subset', methods=['POST'])
def subset_font():
    data = request.json
    font_name = data.get('font_name')
    text = data.get('text')
    
    if not font_name or not text:
        return jsonify({'error': 'Missing parameters'}), 400
        
    try:
        font_path = os.path.join(current_app.config['FONTS_DIR'], font_name)
        new_filename = f"subset_{font_name}"
        new_path = os.path.join(current_app.config['FONTS_DIR'], new_filename)
        
        # 使用 fonttools.subset 创建子集
        options = subset.Options()
        
        # 设置选项，保持字体布局特性
        options.layout_features = ['*']  # 保留所有布局特性
        options.name_IDs = ['*']        # 保留所有名称记录
        options.name_languages = ['*']   # 保留所有语言
        options.notdef_outline = True    # 保留 .notdef 字形轮廓
        options.recalc_bounds = True     # 重新计算边界
        options.recommended_glyphs = True  # 包含推荐的字形
        
        # 准备字符集
        text_utf8 = text.encode('utf-8')
        
        # 使用 subset 模块创建子集
        subsetter = subset.Subsetter(options=options)
        font = TTFont(font_path)
        subsetter.populate(text=text_utf8)
        subsetter.subset(font)
        font.save(new_path)
        
        return jsonify({
            'message': 'Subset created successfully',
            'filename': new_filename
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500 