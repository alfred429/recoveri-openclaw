#!/usr/bin/env python3
"""Localise markdown documents using Gemma 3 4B via Ollama.
Skill 133: recoveri-localisation-gemma
"""
import json, os, subprocess, sys, argparse
from datetime import datetime, timezone

OLLAMA_MODEL = os.environ.get("LOCALISE_MODEL", "gemma3:4b")
SOURCE_DIR = os.environ.get("LOCALISE_SOURCE", "/root/shared-repository/data/localisation/source/")
OUTPUT_DIR = os.environ.get("LOCALISE_OUTPUT", "/root/shared-repository/data/localisation/")

LANGUAGES = {
    "en-US": "American English (use US spelling: color, organize, catalog. Use $ for currency.)",
    "fr": "French (formal commercial tone, use EUR for currency, comply with French consumer law terminology)",
    "de": "German (formal Sie form, use EUR for currency, comply with German consumer law terminology)",
    "es": "Spanish (Spain, formal usted form, use EUR for currency, comply with Spanish consumer law terminology)",
    "nl": "Dutch (formal u form, use EUR for currency, comply with Dutch consumer law terminology)",
    "it": "Italian (formal Lei form, use EUR for currency, comply with Italian consumer law terminology)",
}

DOCS = [
    "SPRINT9_ETSY_SHOP_POLICIES_v1.md",
    "SPRINT9_ETSY_FAQ_TEMPLATE_v1.md",
    "SPRINT9_ETSY_POST_PURCHASE_AUTOMATION_v1.md",
    "SPRINT9_ETSY_BRANDING_BRIEF_v1.md",
]


def translate_with_gemma(source_text, target_lang, lang_instructions):
    """Translate source text using Gemma 3 4B via Ollama."""
    prompt = (
        "You are a professional translator specialising in e-commerce and digital product documentation.\n\n"
        f"Translate the following document from English to {target_lang}.\n\n"
        "INSTRUCTIONS:\n"
        f"- {lang_instructions}\n"
        "- Maintain all markdown formatting (headings, lists, tables, bold, italic)\n"
        "- Translate naturally for the target market — not literal word-for-word\n"
        "- Preserve any technical terms commonly used in English in that market\n"
        "- Keep brand names unchanged (RecoveriStudio, Recoveri)\n"
        "- Adapt currency symbols to the target market\n"
        "- Ensure legal/policy language is appropriate for the target country\n\n"
        "DOCUMENT TO TRANSLATE:\n\n"
        f"{source_text}\n\n"
        "TRANSLATED DOCUMENT:"
    )

    result = subprocess.run(
        ["ollama", "run", OLLAMA_MODEL, prompt],
        capture_output=True, text=True, timeout=300
    )
    return result.stdout.strip()


def main():
    parser = argparse.ArgumentParser(description="Localise documents with Gemma 3 4B")
    parser.add_argument("--doc", help="Specific document to translate (filename or path)")
    parser.add_argument("--lang", help="Specific language code, or 'all'", default="all")
    args = parser.parse_args()

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    log_entries = []
    now = datetime.now(timezone.utc)

    docs_to_process = DOCS
    if args.doc:
        docs_to_process = [os.path.basename(args.doc)]

    langs_to_process = LANGUAGES
    if args.lang and args.lang != "all":
        if args.lang in LANGUAGES:
            langs_to_process = {args.lang: LANGUAGES[args.lang]}
        else:
            print(f"Unknown language: {args.lang}")
            sys.exit(1)

    for doc_name in docs_to_process:
        source_path = os.path.join(SOURCE_DIR, doc_name)
        if not os.path.exists(source_path):
            # Try direct path
            if args.doc and os.path.exists(args.doc):
                source_path = args.doc
            else:
                print(f"SKIP: {doc_name} not found at {source_path}")
                continue

        with open(source_path) as f:
            source_text = f.read()

        source_words = len(source_text.split())
        print(f"\n=== Translating: {doc_name} ({source_words} words) ===")

        for lang_code, lang_instructions in langs_to_process.items():
            print(f"  -> {lang_code}...", end=" ", flush=True)

            try:
                translated = translate_with_gemma(source_text, lang_code, lang_instructions)

                base_name = doc_name.replace(".md", "")
                output_name = f"{base_name}_{lang_code}.md"
                output_path = os.path.join(OUTPUT_DIR, output_name)

                with open(output_path, "w") as f:
                    f.write(translated)

                translated_words = len(translated.split())
                ratio = translated_words / source_words if source_words > 0 else 0
                status = "OK" if 0.5 < ratio < 2.0 else "WARN_RATIO"
                print(f"{status} ({translated_words} words, {ratio:.0%})")

                log_entries.append({
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "source_doc": doc_name,
                    "target_lang": lang_code,
                    "source_words": source_words,
                    "translated_words": translated_words,
                    "ratio": round(ratio, 2),
                    "model": OLLAMA_MODEL,
                    "output_path": output_path,
                    "status": status,
                })

            except Exception as e:
                print(f"FAIL ({e})")
                log_entries.append({
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "source_doc": doc_name,
                    "target_lang": lang_code,
                    "model": OLLAMA_MODEL,
                    "status": "FAIL",
                    "error": str(e),
                })

    # Write log
    log_path = os.path.join(OUTPUT_DIR, "localisation-log.jsonl")
    with open(log_path, "a") as f:
        for entry in log_entries:
            f.write(json.dumps(entry) + "\n")

    ok = sum(1 for e in log_entries if e["status"] in ("OK", "WARN_RATIO"))
    total = len(log_entries)
    print(f"\n=== COMPLETE ===")
    print(f"Translations: {ok}/{total}")
    print(f"Log: {log_path}")


if __name__ == "__main__":
    main()
