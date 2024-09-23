import base64
from pathlib import Path
from typing import Union

from loguru import logger
from natsort import natsorted

# 音频文件扩展名集合
AUDIO_EXTENSIONS = {
    ".mp3",
    ".wav",
    ".flac",
    ".ogg",
    ".m4a",
    ".wma",
    ".aac",
    ".aiff",
    ".aif",
    ".aifc",
}

# 视频文件扩展名集合
VIDEO_EXTENSIONS = {
    ".mp4",
    ".avi",
}


def audio_to_bytes(file_path):
    """将音频文件转换为字节"""
    if not file_path or not Path(file_path).exists():
        return None
    with open(file_path, "rb") as wav_file:
        wav = wav_file.read()
    return wav


def read_ref_text(ref_text):
    """读取参考文本"""
    path = Path(ref_text)
    if path.exists() and path.is_file():
        with path.open("r", encoding="utf-8") as file:
            return file.read()
    return ref_text


def list_files(
    path: Union[Path, str],
    extensions: set[str] = None,
    recursive: bool = False,
    sort: bool = True,
) -> list[Path]:
    """列出目录中的文件。

    参数:
        path (Path): 目录路径。
        extensions (set, optional): 要筛选的文件扩展名。默认为None。
        recursive (bool, optional): 是否递归搜索。默认为False。
        sort (bool, optional): 是否对文件进行排序。默认为True。

    返回:
        list: 文件列表。
    """

    if isinstance(path, str):
        path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"目录 {path} 不存在。")

    files = [file for ext in extensions for file in path.rglob(f"*{ext}")]

    if sort:
        files = natsorted(files)

    return files


def load_filelist(path: Path | str) -> list[tuple[Path, str, str, str]]:
    """
    加载Bert-VITS2风格的文件列表。
    """

    files = set()
    results = []
    count_duplicated, count_not_found = 0, 0

    LANGUAGE_TO_LANGUAGES = {
        "zh": ["zh", "en"],
        "jp": ["jp", "en"],
        "en": ["en"],
    }

    with open(path, "r", encoding="utf-8") as f:
        for line in f.readlines():
            splits = line.strip().split("|", maxsplit=3)
            if len(splits) != 4:
                logger.warning(f"无效行: {line}")
                continue

            filename, speaker, language, text = splits
            file = Path(filename)
            language = language.strip().lower()

            if language == "ja":
                language = "jp"

            assert language in ["zh", "jp", "en"], f"无效语言 {language}"
            languages = LANGUAGE_TO_LANGUAGES[language]

            if file in files:
                logger.warning(f"重复文件: {file}")
                count_duplicated += 1
                continue

            if not file.exists():
                logger.warning(f"文件未找到: {file}")
                count_not_found += 1
                continue

            results.append((file, speaker, languages, text))

    if count_duplicated > 0:
        logger.warning(f"重复文件总数: {count_duplicated}")

    if count_not_found > 0:
        logger.warning(f"未找到文件总数: {count_not_found}")

    return results
