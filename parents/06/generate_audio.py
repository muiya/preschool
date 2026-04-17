"""
新時代的父母 · 情境06 — 要讓孩童有十足的想像空間
產生每句一個 mp3 (結尾含靜音) + lines.json
用法: python generate_audio.py
"""

import asyncio
import json
import os
import edge_tts

ZH_LINES = [
    "要讓孩童有十足的想像空間、",
    "在傳統的社會裏、",
    "父母親往往因太溺愛子女、",
    "處處為其安排、",
    "子女要順著做順著想就是好寶寶、",
    "因此傳統的家庭父母應有責任給孩子更廣的想像空間、",
    "父母親的角色隨著時代改變、",
    "已沒有一成不變的法則、",
    "對孩童除了要關心、細心、耐心的照料外、",
    "更是孩童所有知識的啓蒙老師、",
    "而事實孩童的學前教育對孩子的往後成長、",
    "影響非常的深遠、",
    "願天下所有的父母親能夠不斷鞭策自己、",
    "讓我們的下一代能有更完善的空間、",
    "使孩子們心存感激更有尊嚴、",
    "讓我們的社會更祥和更進步。"
]

EN_LINES = [
    "Give children plenty of room to imagine.",
    "In traditional societies,",
    "parents often spoil their children too much,",
    "arranging everything for them.",
    "Those who simply obey and think as told are called good children,",
    "so today's parents should give children wider space to imagine.",
    "The role of parents changes with the times;",
    "there are no fixed rules anymore.",
    "Beyond caring for children with attention, care, and patience,",
    "parents are also the very first teachers of all knowledge.",
    "A child's preschool education shapes their future growth",
    "in ways that run very deep.",
    "May all parents everywhere keep pushing themselves,",
    "so our next generation has a better space to grow.",
    "So our children feel grateful and live with dignity,",
    "and so our society becomes more peaceful and more advanced."
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
    print("情境06 (要讓孩童有十足的想像空間) 開始產生...")
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
