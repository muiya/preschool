"""
單親問題面面觀 · 情境02 — 面對離婚的失落
產生每句一個 mp3 (結尾含靜音) + lines.json
用法: python generate_audio.py
"""

import asyncio
import json
import os
import edge_tts

ZH_LINES = [
    "王老五是個已離婚的男人、",
    "目前與獨生女住在一起、",
    "女兒六歲上幼兒園大班、",
    "個性乖巧很黏爸爸、",
    "但王老五卻覺得女兒很煩、",
    "讓他無法專心工作、",
    "對此王老五頗有微詞、",
    "常對女兒怒目相向、",
    "而王老五的太太是主動提出離婚、",
    "所以王老五不應該把家長離婚的問題怪罪於女兒、",
    "一般來說王老五要能面對離婚的失落感、",
    "去了解離婚的原因、",
    "勇敢面對現實。",
    "建議讓女兒了解到父母離婚的原因絕對不是因為女兒的緣故、",
    "雖然離婚了但是父母都還是很愛她的、",
    "並且鼓勵女兒說出自己內心的想法、",
    "同時接納女兒的感受、",
    "以免造成孩子的陰影。"
]

EN_LINES = [
    "Mr. Wang is a divorced man,",
    "currently living with his only daughter.",
    "She is six and in her final year of preschool,",
    "a sweet-tempered girl who clings to her father.",
    "But Mr. Wang finds her annoying,",
    "saying she keeps him from focusing on his work,",
    "and he grumbles about this,",
    "often glaring at her.",
    "But it was his wife who actively asked for the divorce,",
    "so he shouldn't blame the divorce on his daughter.",
    "Generally speaking, he must face his own sense of loss from the divorce,",
    "understand the reasons behind it,",
    "and confront reality with courage.",
    "He should help his daughter understand the divorce has nothing to do with her,",
    "that even after the divorce, both parents still love her deeply.",
    "And he should encourage her to share her inner thoughts,",
    "while fully accepting her feelings,",
    "so no shadow is cast over her childhood."
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
    print("情境02 (面對離婚的失落) 開始產生...")
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
