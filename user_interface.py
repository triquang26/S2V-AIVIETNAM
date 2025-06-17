import os
import sys
from pathlib import Path
from config import Config
from main import GPTProcessor
import time
import argparse

class S2VUserInterface:
    """User-friendly interface for S2V (Slides to Video) application"""
    
    def __init__(self):
        self.config = Config()
        self.processor = None
        
    def print_banner(self):
        """Print application banner"""
        banner = """
        ╔═══════════════════════════════════════════════════════════╗
        ║                    S2V - SLIDES TO VIDEO                  ║
        ║                   AI-Powered Presentation                 ║
        ║                    Generator (Vietnamese)                 ║
        ╚═══════════════════════════════════════════════════════════╝
        """
        print(banner)
    
    def print_menu(self):
        """Print main menu"""
        menu = """
        🎯 Chọn chức năng:
        
        1. 🚀 Chạy chuyển đổi PDF thành Video (Workflow đầy đủ)
        2. ⚙️  Cấu hình tham số
        3. 📁 Quản lý đường dẫn file
        4. 🔍 Kiểm tra cấu hình hiện tại
        5. 💾 Lưu cấu hình
        6. 📖 Hướng dẫn sử dụng
        7. ❌ Thoát
        
        """
        print(menu)
    
    def get_user_choice(self, prompt="Nhập lựa chọn của bạn: ", valid_choices=None):
        """Get user input with validation"""
        while True:
            try:
                choice = input(prompt).strip()
                if valid_choices and choice not in valid_choices:
                    print(f"❌ Lựa chọn không hợp lệ. Vui lòng chọn: {', '.join(valid_choices)}")
                    continue
                return choice
            except KeyboardInterrupt:
                print("\n👋 Tạm biệt!")
                sys.exit(0)
    
    def configure_paths(self):
        """Configure file paths"""
        print("\n📁 CẤU HÌNH ĐƯỜNG DẪN FILE")
        print("=" * 50)
        
        # PDF Path
        print(f"\n📄 Đường dẫn PDF hiện tại: {self.config.default_pdf_path or 'Chưa cấu hình'}")
        
        while True:
            pdf_path = input("📂 Nhập đường dẫn PDF mới (Enter để giữ nguyên): ").strip()
            if not pdf_path:
                break
            
            if os.path.exists(pdf_path) and pdf_path.lower().endswith('.pdf'):
                self.config.default_pdf_path = pdf_path
                print(f"✅ Đã cập nhật đường dẫn PDF: {pdf_path}")
                break
            else:
                print("❌ File PDF không tồn tại hoặc không đúng định dạng. Vui lòng thử lại.")
        
        # Output folder
        print(f"\n📁 Thư mục đầu ra hiện tại: {self.config.default_output_folder}")
        output_folder = input("📂 Nhập thư mục đầu ra mới (Enter để giữ nguyên): ").strip()
        if output_folder:
            # Create folder if it doesn't exist
            os.makedirs(output_folder, exist_ok=True)
            self.config.default_output_folder = output_folder
            print(f"✅ Đã cập nhật thư mục đầu ra: {output_folder}")
    
    def configure_processing_settings(self):
        """Configure processing parameters"""
        print("\n⚙️ CẤU HÌNH THAM SỐ XỬ LÝ")
        print("=" * 50)
        
        # PDF Batch Size
        print(f"\n📄 Kích thước batch PDF hiện tại: {self.config.pdf_batch_size}")
        print("   (Số slide được xử lý cùng lúc với GPT-4 - Khuyến nghị: 3-7)")
        try:
            pdf_batch = input("📊 Nhập kích thước batch PDF mới (Enter để giữ nguyên): ").strip()
            if pdf_batch:
                pdf_batch = int(pdf_batch)
                if 1 <= pdf_batch <= 10:
                    self.config.pdf_batch_size = pdf_batch
                    print(f"✅ Đã cập nhật PDF batch size: {pdf_batch}")
                else:
                    print("⚠️ Khuyến nghị sử dụng giá trị từ 1-10")
        except ValueError:
            print("❌ Vui lòng nhập số nguyên hợp lệ")
        
        # TTS Batch Size
        print(f"\n🎤 Kích thước batch TTS hiện tại: {self.config.tts_batch_size}")
        print("   (Số slide được chuyển thành giọng nói cùng lúc - Khuyến nghị: 1-5)")
        try:
            tts_batch = input("🔊 Nhập kích thước batch TTS mới (Enter để giữ nguyên): ").strip()
            if tts_batch:
                tts_batch = int(tts_batch)
                if 1 <= tts_batch <= 10:
                    self.config.tts_batch_size = tts_batch
                    print(f"✅ Đã cập nhật TTS batch size: {tts_batch}")
                else:
                    print("⚠️ Khuyến nghị sử dụng giá trị từ 1-10")
        except ValueError:
            print("❌ Vui lòng nhập số nguyên hợp lệ")
        
        # Batch Splitting
        print(f"\n🔪 Batch splitting hiện tại: {'Bật' if self.config.use_batch_splitting else 'Tắt'}")
        print("   (Tự động chia audio batch thành từng slide riêng lẻ)")
        batch_split = self.get_user_choice(
            "🔄 Bật batch splitting? (y/n, Enter để giữ nguyên): ",
            valid_choices=['y', 'n', 'Y', 'N', '']
        )
        if batch_split.lower() == 'y':
            self.config.use_batch_splitting = True
            print("✅ Đã bật batch splitting")
        elif batch_split.lower() == 'n':
            self.config.use_batch_splitting = False
            print("✅ Đã tắt batch splitting")
    
    def show_current_config(self):
        """Display current configuration"""
        print("\n🔍 CẤU HÌNH HIỆN TẠI")
        print("=" * 50)
        print(f"📄 Đường dẫn PDF:        {self.config.default_pdf_path or 'Chưa cấu hình'}")
        print(f"📁 Thư mục đầu ra:       {self.config.default_output_folder}")
        print(f"📊 PDF Batch Size:       {self.config.pdf_batch_size}")
        print(f"🎤 TTS Batch Size:       {self.config.tts_batch_size}")
        print(f"🔪 Batch Splitting:      {'Bật' if self.config.use_batch_splitting else 'Tắt'}")
        print(f"🎥 Video FPS:            {self.config.video_fps}")
        print(f"🔊 Audio Rate:           {self.config.audio_rate}Hz")
    
    def show_help(self):
        """Show help information"""
        help_text = """
        📖 HƯỚNG DẪN SỬ DỤNG S2V
        ═══════════════════════════════════════════════════════════
        
        🎯 TỔNG QUAN:
        S2V (Slides to Video) là công cụ AI chuyển đổi file PDF presentation 
        thành video có giọng nói tiếng Việt tự động.
        
        📋 CÁC BƯỚC SỬ DỤNG:
        1. Cấu hình đường dẫn PDF và thư mục đầu ra
        2. Điều chỉnh tham số xử lý (nếu cần)
        3. Chạy workflow chuyển đổi
        4. Nhận video kết quả
        
        ⚙️ THAM SỐ QUAN TRỌNG:
        
        📊 PDF Batch Size (3-7 khuyến nghị):
        - Số slide được xử lý cùng lúc với GPT-4
        - Nhỏ hơn: chậm hơn nhưng ít lỗi
        - Lớn hơn: nhanh hơn nhưng có thể bị giới hạn API
        
        🎤 TTS Batch Size (1-5 khuyến nghị):
        - Số slide được chuyển thành giọng nói cùng lúc
        - = 1: Từng slide riêng lẻ (chất lượng đồng đều)
        - > 1: Batch processing (tự nhiên hơn, cần batch splitting)
        
        🔪 Batch Splitting:
        - Bật: Tự động chia audio batch thành từng slide
        - Tắt: Giữ nguyên audio batch (không khuyến nghị)
        
        💡 KHUYẾN NGHỊ:
        - Lần đầu sử dụng: PDF=3, TTS=1, Splitting=Tắt
        - Muốn chất lượng cao: PDF=5, TTS=3, Splitting=Bật
        - Muốn xử lý nhanh: PDF=7, TTS=5, Splitting=Bật
        
        ⚠️ LƯU Ý:
        - Cần kết nối internet
        - File PDF phải có chất lượng tốt
        - Quá trình có thể mất 5-30 phút tùy số slide
        """
        print(help_text)
    
    def run_conversion(self):
        """Run the complete PDF to Video conversion"""
        print("\n🚀 BẮT ĐẦU CHUYỂN ĐỔI PDF THÀNH VIDEO")
        print("=" * 60)
        
        # Validate configuration
        if not self.config.default_pdf_path or not os.path.exists(self.config.default_pdf_path):
            print("❌ Chưa cấu hình đường dẫn PDF hoặc file không tồn tại!")
            print("   Vui lòng chọn chức năng '3. Quản lý đường dẫn file' trước.")
            return
        
        # Show current settings
        print("📋 Cấu hình sẽ được sử dụng:")
        print(f"   📄 PDF: {self.config.default_pdf_path}")
        print(f"   📁 Output: {self.config.default_output_folder}")
        print(f"   📊 PDF Batch: {self.config.pdf_batch_size}")
        print(f"   🎤 TTS Batch: {self.config.tts_batch_size}")
        print(f"   🔪 Batch Split: {'Bật' if self.config.use_batch_splitting else 'Tắt'}")
        
        confirm = self.get_user_choice(
            "\n✅ Xác nhận bắt đầu chuyển đổi? (y/n): ",
            valid_choices=['y', 'n', 'Y', 'N']
        )
        
        if confirm.lower() != 'y':
            print("❌ Đã hủy chuyển đổi.")
            return
        
        try:
            # Initialize processor
            self.processor = GPTProcessor(*self.config.get_api_keys())
            
            # Create output folder with timestamp
            output_folder = self.processor.create_random_output_folder(
                self.config.default_output_folder
            )
            
            print(f"\n🎬 Bắt đầu xử lý...")
            print(f"📁 Thư mục kết quả: {output_folder}")
            
            start_time = time.time()
            
            if self.config.use_batch_splitting and self.config.tts_batch_size > 1:
                # Use batch splitting workflow
                print("🔄 Sử dụng workflow: Batch TTS + Audio Splitting")
                video_path, audio_files, durations = self.processor.test_workflow_with_batch_splitting(
                    self.config.default_pdf_path,
                    output_folder,
                    self.config.pdf_batch_size,
                    self.config.tts_batch_size
                )
            else:
                # Use original workflow
                print("🔄 Sử dụng workflow: Xử lý từng slide riêng lẻ")
                
                # Process PDF
                descriptions_file, image_files = self.processor.process_pdf_to_descriptions(
                    self.config.default_pdf_path, output_folder, self.config.pdf_batch_size
                )
                
                # Process with Claude
                final_context_file = self.processor.process_with_claude(descriptions_file, output_folder)
                
                # Generate audio
                audio_files, vietnamese_descriptions, translated_file = self.processor.generate_vietnamese_audio(
                    final_context_file, output_folder, tts_batch_size=1
                )
                
                # Create video
                video_path, durations = self.processor.create_video_with_audio(
                    image_files, audio_files, output_folder
                )
            
            end_time = time.time()
            processing_time = end_time - start_time
            
            # Show results
            print("\n" + "=" * 60)
            print("🎉 CHUYỂN ĐỔI HOÀN THÀNH!")
            print("=" * 60)
            print(f"📊 Tổng thời gian xử lý: {processing_time:.2f} giây ({processing_time/60:.1f} phút)")
            print(f"🎥 Video đã tạo: {video_path}")
            print(f"📁 Thư mục kết quả: {output_folder}")
            
            if 'durations' in locals():
                print(f"⏱️  Độ dài video: {sum(durations):.2f} giây")
                print(f"📄 Số slide đã xử lý: {len(durations)}")
            
            # Ask to open folder
            open_folder = self.get_user_choice(
                "\n📂 Mở thư mục kết quả? (y/n): ",
                valid_choices=['y', 'n', 'Y', 'N']
            )
            
            if open_folder.lower() == 'y':
                try:
                    if sys.platform == "darwin":  # macOS
                        os.system(f"open '{output_folder}'")
                    elif sys.platform == "win32":  # Windows
                        os.system(f"explorer '{output_folder}'")
                    else:  # Linux
                        os.system(f"xdg-open '{output_folder}'")
                    print("✅ Đã mở thư mục kết quả")
                except:
                    print(f"📁 Bạn có thể tìm kết quả tại: {output_folder}")
        
        except Exception as e:
            print(f"\n❌ Lỗi trong quá trình xử lý: {str(e)}")
            print("💡 Vui lòng kiểm tra:")
            print("   - Kết nối internet")
            print("   - API keys")
            print("   - File PDF có thể đọc được")
            print("   - Dung lượng ổ cứng đủ")
    
    def save_config(self):
        """Save current configuration"""
        print("\n💾 LƯU CẤU HÌNH")
        print("=" * 30)
        
        config_file = input("📂 Tên file cấu hình (Enter = config.json): ").strip()
        if not config_file:
            config_file = "config.json"
        
        if not config_file.endswith('.json'):
            config_file += '.json'
        
        self.config.save_to_file(config_file)
        print(f"✅ Đã lưu cấu hình vào {config_file}")
    
    def run(self):
        """Main application loop"""
        self.print_banner()
        
        while True:
            self.print_menu()
            
            choice = self.get_user_choice("Nhập lựa chọn (1-7): ", 
                                        valid_choices=['1', '2', '3', '4', '5', '6', '7'])
            
            if choice == '1':
                self.run_conversion()
            elif choice == '2':
                self.configure_processing_settings()
            elif choice == '3':
                self.configure_paths()
            elif choice == '4':
                self.show_current_config()
            elif choice == '5':
                self.save_config()
            elif choice == '6':
                self.show_help()
            elif choice == '7':
                print("\n👋 Cảm ơn bạn đã sử dụng S2V!")
                break
            
            if choice != '7':
                input("\n⏸️  Nhấn Enter để tiếp tục...")

def main():
    """Main entry point"""
    app = S2VUserInterface()
    app.run()

if __name__ == "__main__":
    main() 