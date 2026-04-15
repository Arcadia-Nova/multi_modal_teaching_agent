"""
多模态解析器测试脚本

请确保环境变量或配置文件中已正确设置模型路径和参数。
请将下方的测试文件路径替换为你本地实际存在的文件。
"""
import os
import sys
from pprint import pprint

# --- ⚠️ 请修改这里的路径为你本地的测试文件 ---
TEST_PDF_PATH = "../uploads/e6e32c41-d0de-4246-a5cd-e22afed227a7/refs/0abe582297fb45e2a483e7cb60e6ad57.docx1"  # 替换为你的测试PDF路径
TEST_IMAGE_PATH = "../uploads/e6e32c41-d0de-4246-a5cd-e22afed227a7/refs/069ef803f602469ba0158913f054f113.jpg"  # 替换为你的测试图片路径
TEST_VIDEO_PATH = "test_files/sample.mp4"  # 替换为你的测试视频路径

# 确保能导入 app 包（假设你的项目根目录下有 app 文件夹）
# 如果报错 ModuleNotFoundError，请根据你的实际目录结构调整 sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_text_parser():
    print("\n" + "=" * 60)
    print("📄 测试文档解析器 (text_parser.py)")
    print("=" * 60)

    from app.core.multimodal.text_parser import parse_document

    # 检查文件是否存在
    if not os.path.exists(TEST_PDF_PATH):
        print(f"[跳过] 测试文件不存在: {TEST_PDF_PATH}")
        return

    try:
        result = parse_document(TEST_PDF_PATH)
        print("✅ 文档解析成功！返回结果结构：")
        pprint(result, depth=2, width=100)
    except Exception as e:
        print(f"❌ 文档解析失败: {e}")


def test_image_parser():
    print("\n" + "=" * 60)
    print("🖼️ 测试图像解析器 (image_parser.py)")
    print("=" * 60)

    from app.core.multimodal.image_parser import parse_image

    if not os.path.exists(TEST_IMAGE_PATH):
        print(f"[跳过] 测试文件不存在: {TEST_IMAGE_PATH}")
        return

    try:
        result = parse_image(TEST_IMAGE_PATH)
        print("✅ 图像解析成功！返回结果：")
        pprint(result, width=100)
    except Exception as e:
        print(f"❌ 图像解析失败: {e}")


def test_video_parser():
    print("\n" + "=" * 60)
    print("🎬 测试视频解析器 (video_parser.py)")
    print("=" * 60)

    # 简单检查配置
    try:
        from app.config import settings
        print(f"⚙️  配置加载正常: 抽帧间隔 {settings.VIDEO_FRAME_INTERVAL_SEC}秒, 最大帧数 {settings.MAX_VIDEO_FRAMES}")
    except Exception as e:
        print(f"⚙️  配置加载异常 (可能使用默认值): {e}")

    from app.core.multimodal.video_parser import VideoParser

    if not os.path.exists(TEST_VIDEO_PATH):
        print(f"[跳过] 测试文件不存在: {TEST_VIDEO_PATH}")
        return

    parser = VideoParser()

    try:
        print(f"🎬 正在提取帧并解析视频 (这可能需要几秒钟)...")
        result = parser.parse_video(TEST_VIDEO_PATH)

        print(f"✅ 视频解析完成！共提取 {result['frame_count']} 帧")
        print("📝 前几条描述：")
        for desc in result['descriptions'][:3]:  # 只打印前3条
            print(f"   {desc}")
        if len(result['descriptions']) > 3:
            print("   ...")

    except Exception as e:
        print(f"❌ 视频解析失败: {e}")


if __name__ == "__main__":
    print(f"🚀 开始运行多模态解析器测试")
    print(f"   当前工作目录: {os.getcwd()}")

    # 检查是否有文件路径
    if not any([os.path.exists(p) for p in [TEST_PDF_PATH, TEST_IMAGE_PATH, TEST_VIDEO_PATH]]):
        print("\n⚠️  警告：未找到任何测试文件。请检查文件路径是否正确。")
        print(f"   PDF路径存在: {os.path.exists(TEST_PDF_PATH)}")
        print(f"   图片路径存在: {os.path.exists(TEST_IMAGE_PATH)}")
        print(f"   视频路径存在: {os.path.exists(TEST_VIDEO_PATH)}")
        sys.exit(1)

    # 运行测试
    test_text_parser()
    test_image_parser()
    test_video_parser()

    print("\n" + "=" * 60)
    print("🧪 测试结束")
