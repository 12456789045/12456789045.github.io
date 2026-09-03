from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Optional
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="HK Translator API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DICT_FILE = Path("dictionary.json")

DEFAULT_DICT = {
    "en": {
        "es": {
            "hello": {"translation": "hola", "meaning": "saludo de bienvenida"},
            "world": {"translation": "mundo", "meaning": "el planeta o la humanidad"},
            "thank": {"translation": "gracias", "meaning": "expresión de agradecimiento"},
            "friend": {"translation": "amigo", "meaning": "persona cercana"},
            "home": {"translation": "hogar", "meaning": "lugar donde uno vive"},
            "water": {"translation": "agua", "meaning": "líquido esencial"},
            "food": {"translation": "comida", "meaning": "alimento para comer"},
            "love": {"translation": "amor", "meaning": "sentimiento de afecto"},
            "time": {"translation": "tiempo", "meaning": "duración o momento"},
            "day": {"translation": "día", "meaning": "período de luz"},
        },
        "fr": {
            "hello": {"translation": "bonjour", "meaning": "salutation de bienvenue"},
            "world": {"translation": "monde", "meaning": "la planète ou l’humanité"},
            "thank": {"translation": "merci", "meaning": "expression de gratitude"},
            "friend": {"translation": "ami", "meaning": "personne proche"},
            "home": {"translation": "maison", "meaning": "lieu où l’on vit"},
            "water": {"translation": "eau", "meaning": "liquide essentiel"},
            "food": {"translation": "nourriture", "meaning": "aliment à manger"},
            "love": {"translation": "amour", "meaning": "sentiment d’affection"},
            "time": {"translation": "temps", "meaning": "durée ou moment"},
            "day": {"translation": "jour", "meaning": "période de lumière"},
        },
        "hi": {
            "hello": {"translation": "नमस्ते", "meaning": "स्वागत का शब्द"},
            "world": {"translation": "दुनिया", "meaning": "पृथ्वी या मानव-समुदाय"},
            "thank": {"translation": "धन्यवाद", "meaning": "कृतज्ञता व्यक्त करने वाला शब्द"},
            "friend": {"translation": "दोस्त", "meaning": "करीबी व्यक्ति"},
            "home": {"translation": "घर", "meaning": "वह स्थान जहाँ आप रहते हैं"},
            "water": {"translation": "पानी", "meaning": "जीवन का आवश्यक तरल"},
            "food": {"translation": "खाना", "meaning": "खाने की चीज़"},
            "love": {"translation": "प्यार", "meaning": "स्नेह का भाव"},
            "time": {"translation": "समय", "meaning": "क्षण या अवधि"},
            "day": {"translation": "दिन", "meaning": "प्रकाश का समय"},
        },
        "mr": {
            "hello": {"translation": "नमस्कार", "meaning": "आभार किंवा स्वागताचा शब्द"},
            "world": {"translation": "जग", "meaning": "पृथ्वी किंवा मानव समुदाय"},
            "thank": {"translation": "धन्यवाद", "meaning": "कृतज्ञता दर्शविणारा शब्द"},
            "friend": {"translation": "मित्र", "meaning": "जवळचा व्यक्ती"},
            "home": {"translation": "घर", "meaning": "जिथे आपण राहत असतो"},
            "water": {"translation": "पाणी", "meaning": "जीवनाचे आवश्यक द्रव"},
            "food": {"translation": "अन्न", "meaning": "खाण्याचे पदार्थ"},
            "love": {"translation": "प्रेम", "meaning": "आकर्षण आणि स्नेह"},
            "time": {"translation": "वेळ", "meaning": "क्षण किंवा कालावधी"},
            "day": {"translation": "दिवस", "meaning": "प्रकाशाचा काळ"},
        },
        "de": {
            "hello": {"translation": "hallo", "meaning": "Begrüßungswort"},
            "world": {"translation": "Welt", "meaning": "die Erde oder die Menschheit"},
            "thank": {"translation": "danke", "meaning": "Ausdruck der Dankbarkeit"},
            "friend": {"translation": "Freund", "meaning": "naher Mensch"},
            "home": {"translation": "Haus", "meaning": "Ort, an dem man lebt"},
            "water": {"translation": "Wasser", "meaning": "essentielle Flüssigkeit"},
            "food": {"translation": "Essen", "meaning": "Nahrung zum Essen"},
            "love": {"translation": "Liebe", "meaning": "Gefühl der Zuneigung"},
            "time": {"translation": "Zeit", "meaning": "Dauer oder Moment"},
            "day": {"translation": "Tag", "meaning": "Zeitraum mit Licht"},
        },
    },
    "es": {
        "en": {
            "hola": {"translation": "hello", "meaning": "a greeting of welcome"},
            "mundo": {"translation": "world", "meaning": "the planet or humanity"},
            "gracias": {"translation": "thanks", "meaning": "expression of gratitude"},
            "amigo": {"translation": "friend", "meaning": "a close person"},
            "hogar": {"translation": "home", "meaning": "the place where one lives"},
            "agua": {"translation": "water", "meaning": "essential liquid"},
            "comida": {"translation": "food", "meaning": "something to eat"},
            "amor": {"translation": "love", "meaning": "feeling of affection"},
            "tiempo": {"translation": "time", "meaning": "duration or moment"},
            "día": {"translation": "day", "meaning": "period of light"},
        },
        "fr": {
            "hola": {"translation": "salut", "meaning": "salutation"},
            "mundo": {"translation": "monde", "meaning": "le monde"},
            "gracias": {"translation": "merci", "meaning": "remerciement"},
        },
    },
    "fr": {
        "en": {
            "bonjour": {"translation": "hello", "meaning": "greeting"},
            "monde": {"translation": "world", "meaning": "the world"},
            "merci": {"translation": "thanks", "meaning": "expression of gratitude"},
            "ami": {"translation": "friend", "meaning": "close person"},
            "maison": {"translation": "home", "meaning": "place where one lives"},
        },
        "es": {
            "bonjour": {"translation": "hola", "meaning": "saludo"},
            "merci": {"translation": "gracias", "meaning": "agradecimiento"},
        },
    },
    "hi": {
        "en": {
            "नमस्ते": {"translation": "hello", "meaning": "a greeting"},
            "दुनिया": {"translation": "world", "meaning": "the world"},
            "धन्यवाद": {"translation": "thanks", "meaning": "expression of gratitude"},
            "दोस्त": {"translation": "friend", "meaning": "a close companion"},
            "घर": {"translation": "home", "meaning": "place where one lives"},
            "पानी": {"translation": "water", "meaning": "essential liquid"},
            "खाना": {"translation": "food", "meaning": "something to eat"},
            "प्यार": {"translation": "love", "meaning": "affection"},
        },
    },
    "mr": {
        "en": {
            "नमस्कार": {"translation": "hello", "meaning": "a greeting"},
            "जग": {"translation": "world", "meaning": "the world"},
            "धन्यवाद": {"translation": "thanks", "meaning": "expression of gratitude"},
            "मित्र": {"translation": "friend", "meaning": "a close companion"},
            "घर": {"translation": "home", "meaning": "place where one lives"},
        },
    },
}


def save_dict() -> None:
    with open(DICT_FILE, "w", encoding="utf-8") as f:
        json.dump(DICT, f, ensure_ascii=False, indent=2)


if DICT_FILE.exists():
    with open(DICT_FILE, "r", encoding="utf-8") as f:
        DICT = json.load(f)
else:
    DICT = DEFAULT_DICT
    save_dict()


class TranslationRequest(BaseModel):
    word: Optional[str] = None
    text: Optional[str] = None
    from_lang: str = "auto"
    to_lang: str = "en"


class AddWordRequest(BaseModel):
    word: str
    translation: str
    from_lang: str
    to_lang: str


def normalize_entry(entry: Any) -> dict:
    if isinstance(entry, dict):
        return entry
    return {"translation": entry, "meaning": ""}


def translate_with_google(text: str, from_lang: str, to_lang: str) -> Optional[str]:
    try:
        encoded_text = urllib.parse.quote(text)
        url = (
            "https://translate.googleapis.com/translate_a/single"
            f"?client=gtx&sl={from_lang or 'auto'}&tl={to_lang or 'en'}&dt=t&q={encoded_text}"
        )
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode("utf-8"))
            if isinstance(data, list) and data:
                first = data[0]
                if isinstance(first, list):
                    parts = []
                    for item in first:
                        if isinstance(item, list) and item:
                            parts.append(item[0])
                    return "".join(parts) if parts else None
    except Exception:
        return None
    return None


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/languages")
def get_languages() -> dict:
    return {
        "languages": [
            {"code": "auto", "name": "Detect language"},
            {"code": "en", "name": "English"},
            {"code": "es", "name": "Spanish"},
            {"code": "fr", "name": "French"},
            {"code": "hi", "name": "Hindi"},
            {"code": "mr", "name": "Marathi"},
            {"code": "de", "name": "German"},
            {"code": "ar", "name": "Arabic"},
        ]
    }


@app.post("/translate")
def translate(req: TranslationRequest) -> dict:
    text = (req.text or req.word or "").strip()
    if not text:
        raise HTTPException(status_code=400, detail="Text is required")

    from_lang = req.from_lang or "auto"
    to_lang = req.to_lang or "en"

    if from_lang == to_lang:
        return {"translation": text, "meaning": "same language", "provider": "same"}

    lookup = DICT.get(from_lang, {}).get(to_lang, {})
    word_key = text.lower()
    if word_key in lookup:
        entry = normalize_entry(lookup[word_key])
        return {
            "translation": entry.get("translation", text),
            "meaning": entry.get("meaning", ""),
            "provider": "dictionary",
        }

    for source_lang, target_map in DICT.items():
        if from_lang == "auto" and text.lower() in target_map.get(to_lang, {}):
            entry = normalize_entry(target_map[to_lang][text.lower()])
            return {
                "translation": entry.get("translation", text),
                "meaning": entry.get("meaning", ""),
                "provider": "dictionary",
            }

    google_translation = translate_with_google(text, from_lang, to_lang)
    if google_translation:
        return {"translation": google_translation, "meaning": "", "provider": "google"}

    return {"translation": text, "meaning": "", "provider": "fallback"}


@app.post("/add")
def add_word(req: AddWordRequest) -> dict:
    DICT.setdefault(req.from_lang, {}).setdefault(req.to_lang, {})[req.word.lower()] = {
        "translation": req.translation,
        "meaning": "",
    }
    save_dict()
    return {"message": "Word added successfully"}


@app.delete("/delete")
def delete_word(req: AddWordRequest) -> dict:
    if req.from_lang in DICT and req.to_lang in DICT[req.from_lang]:
        if req.word.lower() in DICT[req.from_lang][req.to_lang]:
            del DICT[req.from_lang][req.to_lang][req.word.lower()]
            save_dict()
            return {"message": "Word deleted"}
    raise HTTPException(status_code=404, detail="Word not found")


@app.get("/dictionary")
def get_dict() -> dict:
    return DICT
