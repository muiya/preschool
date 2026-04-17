"""
如何幫助孩子克服害羞 · 情境01 — 幫助孩子拓展人際關係
產生每句一個 mp3 (結尾含靜音) + lines.json
用法: python generate_audio.py
"""

import asyncio
import json
import os
import edge_tts

ZH_LINES = [
    "害羞的孩子往往對加入團體遊戲、",
    "學校中的人際關係缺乏信心、",
    "這時候家長應留意並引導孩子接觸周遭的人、",
    "鼓勵孩子開拓新的人際交往、",
    "這時候家長以溫和的態度讓他習慣陌生人、",
    "父母可在孩子幼小時即帶他到便利商店、",
    "展覽館等人群聚集處、",
    "並嘗試讓孩子有單獨與親人相處的機會。"
]

EN_LINES = [
    "Shy children often feel unsure about joining group play,",
    "and lack confidence in school relationships.",
    "At this point, parents should notice and guide them to connect with those around them,",
    "encouraging them to build new relationships.",
    "Parents should, with a gentle approach, help them grow used to strangers.",
    "From a young age, parents can take them to convenience stores,",
    "exhibition halls, and other places where people gather,",
    "and try giving the child chances to spend time alone with relatives."
]

ZH_VOICE = "zh-TW-HsiaoChenNeural"
EN_VOICE = "en-US-AriaNeural"
ZH_RATE = "-10%"
EN_RATE = "-5%"

TARGET_TAIL_SILENCE_MS = 150
SILENCE_THRESHOLD_DB = -45


async def synth_one(text, voice, rate, out_file):
    tts = edge_tts.Communicate(text, voice, rate=rate)
    await tts.save(out_file)


async def generate_lang(lines, voice, rate, prefix, label):
    from pydub import AudioSegment
    from pydub.silence import detect_leading_silence

    print(f"\n  [{label}] 產生 {len(lines)} 個句子檔案...")

    for i, line in enumerate(lines):
        idx = f"{i+1:02d}"
        tmp_file = f".tmp_{prefix}_{idx}.mp3"
        final_file = f"line_{idx}_{prefix}.mp3"

        await synth_one(line.strip(), voice, rate, tmp_file)

        try:
            audio = AudioSegment.from_mp3(tmp_file)
            original_len = len(audio)

            leading_silence = detect_leading_silence(audio, silence_threshold=SILENCE_THRESHOLD_DB)
            leading_silence = max(0, leading_silence - 50)
            if leading_silence > 0:
                audio = audio[leading_silence:]

            reversed_audio = audio.reverse()
            trailing_silence = detect_leading_silence(reversed_audio, silence_threshold=SILENCE_THRESHOLD_DB)
            if trailing_silence > 0:
                audio = audio[:-trailing_silence]

            if i < len(lines) - 1:
                audio = audio + AudioSegment.silent(
                    duration=TARGET_TAIL_SILENCE_MS,
                    frame_rate=audio.frame_rate
                )

            audio.export(final_file, format="mp3", bitrate="48k")
            print(f"    [{idx}] {line[:15]}... ({original_len}ms -> {len(audio)}ms)")
        except Exception as e:
            print(f"    WARN pydub 失敗,使用原檔: {e}")
            os.replace(tmp_file, final_file)
        else:
            try:
                os.remove(tmp_file)
            except OSError:
                pass

    print(f"  [{label}] OK")


async def main():
    print("=" * 50)
    print("情境01 (幫助孩子拓展人際關係) 開始產生...")
    print("=" * 50)
    await generate_lang(ZH_LINES, ZH_VOICE, ZH_RATE, "zh", "中文")
    await generate_lang(EN_LINES, EN_VOICE, EN_RATE, "en", "英文")

    lines_data = []
    for i in range(len(ZH_LINES)):
        lines_data.append({
            "index": i,
            "zh": ZH_LINES[i],
            "en": EN_LINES[i] if i < len(EN_LINES) else ""
        })
    with open("lines.json", "w", encoding="utf-8") as f:
        json.dump(lines_data, f, ensure_ascii=False, indent=2)

    print("\n全部完成!")


if __name__ == "__main__":
    asyncio.run(main())
