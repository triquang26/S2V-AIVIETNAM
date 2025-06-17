# S2V - Slides to Video
## AI-Powered PDF to Vietnamese Video Converter

🎯 **Chuyển đổi tự động file PDF presentation thành video có giọng nói tiếng Việt bằng AI**

---

## 🌟 Tính năng chính

- 📄 **Chuyển đổi PDF thành video**: Tự động chuyển đổi slides PDF thành video có âm thanh
- 🤖 **AI-Powered**: Sử dụng GPT-4, Claude, và Gemini để tạo nội dung giảng dạy chất lượng cao
- 🇻🇳 **Giọng nói tiếng Việt**: Tự động dịch và tạo giọng nói tiếng Việt tự nhiên
- ⚡ **Batch Processing**: Xử lý nhiều slides cùng lúc để tăng tốc độ
- 🎥 **Chất lượng HD**: Xuất video với độ phân giải tối thiểu 1920x1080
- 🔄 **Flexible Workflow**: Hỗ trợ nhiều chế độ xử lý khác nhau

---

## 🚀 Cách sử dụng

### 1. Giao diện tương tác (Khuyến nghị cho người mới)

```bash
python user_interface.py
```

Giao diện thân thiện với menu tiếng Việt, hướng dẫn từng bước:
- 🎯 Chọn chức năng cần thực hiện
- ⚙️ Cấu hình tham số dễ dàng
- 📁 Quản lý đường dẫn file
- 🔍 Kiểm tra cấu hình hiện tại
- 📖 Hướng dẫn chi tiết

### 2. Command Line Interface (Cho người dùng nâng cao)

```bash
# Cách sử dụng cơ bản
python cli.py input.pdf

# Tùy chỉnh thư mục đầu ra
python cli.py input.pdf -o /path/to/output

# Điều chỉnh batch size
python cli.py input.pdf --pdf-batch 3 --tts-batch 5

# Chế độ nhanh (test)
python cli.py input.pdf --quick

# Chế độ production (tối ưu)
python cli.py input.pdf --production

# Chế độ an toàn (bảo thủ)
python cli.py input.pdf --safe

# Hiển thị thông tin chi tiết
python cli.py input.pdf -v
```

### 3. Sử dụng trực tiếp từ code

```python
from main import GPTProcessor
from config import Config

# Khởi tạo cấu hình
config = Config()
config.default_pdf_path = "presentation.pdf"
config.default_output_folder = "./output"

# Khởi tạo processor
processor = GPTProcessor(*config.get_api_keys())

# Chạy workflow
video_path, audio_files, durations = processor.test_workflow_with_batch_splitting(
    config.default_pdf_path,
    config.default_output_folder,
    pdf_batch_size=5,
    tts_batch_size=5
)
```

---

## ⚙️ Cấu hình tham số

### 📊 PDF Batch Size (Khuyến nghị: 3-7)
- **Mô tả**: Số slide được xử lý cùng lúc với GPT-4
- **Nhỏ hơn**: Chậm hơn nhưng ít lỗi, tiết kiệm API quota
- **Lớn hơn**: Nhanh hơn nhưng có thể bị giới hạn API

### 🎤 TTS Batch Size (Khuyến nghị: 1-5)
- **Mô tả**: Số slide được chuyển thành giọng nói cùng lúc
- **= 1**: Từng slide riêng lẻ (chất lượng đồng đều)
- **> 1**: Batch processing (tự nhiên hơn, cần batch splitting)

### 🔪 Batch Splitting
- **Bật**: Tự động chia audio batch thành từng slide riêng lẻ
- **Tắt**: Giữ nguyên audio batch (không khuyến nghị khi TTS batch > 1)

---

## 💡 Khuyến nghị cấu hình

| Tình huống | PDF Batch | TTS Batch | Batch Splitting | Mô tả |
|------------|-----------|-----------|-----------------|-------|
| **Lần đầu sử dụng** | 3 | 1 | Tắt | An toàn, dễ debug |
| **Chất lượng cao** | 5 | 3 | Bật | Cân bằng chất lượng/tốc độ |
| **Xử lý nhanh** | 7 | 5 | Bật | Tối ưu cho nhiều slide |
| **Tiết kiệm API** | 3 | 1 | Tắt | Ít request API nhất |

---

## 📋 Yêu cầu hệ thống

### Phần mềm cần thiết:
- Python 3.8+
- FFmpeg (cho xử lý video/audio)

### API Keys cần thiết:
- OpenAI API Key (GPT-4 + TTS)
- Anthropic API Key (Claude)
- Google Gemini API Key

### Cài đặt dependencies:
```bash
pip install -r requirements.txt
```

---

## 📁 Cấu trúc dự án

```
S2V-AIVIETNAM/
├── main.py              # Core processing logic
├── user_interface.py    # Interactive UI (Vietnamese)
├── cli.py              # Command line interface
├── config.py           # Configuration management
├── requirements.txt    # Python dependencies
├── README.md          # Documentation
└── config.json        # User configuration (auto-generated)
```

---

## 🔧 Cài đặt

### 1. Clone repository
```bash
git clone <repository-url>
cd S2V-AIVIETNAM
```

### 2. Cài đặt Python dependencies
```bash
pip install -r requirements.txt
```

### 3. Cài đặt FFmpeg
**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
- Tải từ https://ffmpeg.org/download.html
- Thêm vào PATH

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

### 4. Cấu hình API Keys
Chỉnh sửa file `config.py` hoặc sử dụng giao diện để nhập API keys.

---

## 🎯 Workflow xử lý

1. **📄 PDF Processing**: Chuyển đổi PDF thành hình ảnh HD
2. **🤖 Content Analysis**: GPT-4 phân tích và tạo nội dung giảng dạy
3. **✨ Content Enhancement**: Claude cải thiện và làm mượt nội dung
4. **🌐 Translation**: Gemini dịch sang tiếng Việt
5. **🎤 Text-to-Speech**: Tạo giọng nói tiếng Việt tự nhiên
6. **🔪 Audio Processing**: Chia tách audio (nếu batch splitting)
7. **🎥 Video Creation**: Ghép hình ảnh và âm thanh thành video

---

## 🚨 Xử lý lỗi thường gặp

### ❌ "PDF file does not exist"
- Kiểm tra đường dẫn file PDF
- Đảm bảo file có phần mở rộng .pdf

### ❌ "API key not found"
- Cấu hình API keys trong `config.py`
- Kiểm tra API keys còn hạn sử dụng

### ❌ "FFmpeg not found"
- Cài đặt FFmpeg và thêm vào PATH
- Khởi động lại terminal sau khi cài đặt

### ❌ "Memory error"
- Giảm batch size
- Đóng các ứng dụng khác
- Kiểm tra dung lượng RAM

### ❌ "Network error"
- Kiểm tra kết nối internet
- Kiểm tra firewall/proxy settings

---