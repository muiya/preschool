"""
跟嫉妒說再見 · 情境03 — 培養有規律的生活習慣
產生每句一個 mp3 (結尾含靜音) + lines.json
用法: python generate_audio.py
"""

import asyncio
import json
import os
import edge_tts

ZH_LINES = [
    "有了第二個孩子之後、一定會比較忙碌、",
    "如果大的孩子在老二出生以前、",
    "就能定時吃飯、能定時睡覺、",
    "能簡單處理自己的大小便、",
    "做父母的就可以在這些固定時間來照顧他、",
    "讓大孩子不會感覺自己被冷落而嫉妒。"
]

EN_LINES = [
    "After a second child arrives, life gets busier.",
    "If, before the second child is born,",
    "the elder child can eat on schedule and sleep on schedule,",
    "and handle simple toileting on their own,",
    "parents can care for them at these fixed times,",
    "so the elder child does not feel neglected or jealous."
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
    print("情境03 (培養有規律的生活習慣) 開始產生...")
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
