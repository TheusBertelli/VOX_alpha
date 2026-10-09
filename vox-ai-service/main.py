"""VOX interpretation API: deterministic MVP parser ready for an AI-provider adapter.

This starter does not call a generative model. It extracts common Portuguese date/time
expressions and classifies a few domains/priority words so the end-to-end integration
can be exercised before an AI provider and credentials are chosen.
"""

from __future__ import annotations

import os
import re
import unicodedata
from datetime import date, datetime, timedelta
from typing import Optional
from zoneinfo import ZoneInfo

from fastapi import FastAPI
from pydantic import BaseModel, Field

APP_TIMEZONE = ZoneInfo(os.getenv("VOX_TIMEZONE", "America/Sao_Paulo"))
app = FastAPI(
    title="VOX Interpretation Service",
    version="0.1.0",
    description="Interprets natural-language reminder text for the Agenda API.",
)


class InterpretRequest(BaseModel):
    text: str = Field(min_length=1, max_length=2000)


class InterpretResponse(BaseModel):
    title: str
    date: Optional[str] = None
    time: Optional[str] = None
    domain: str = "pessoal"
    priority: str = "média"


def normalize(value: str) -> str:
    decomposed = unicodedata.normalize("NFKD", value)
    return "".join(ch for ch in decomposed if not unicodedata.combining(ch)).lower()


def current_local_date() -> date:
    return datetime.now(APP_TIMEZONE).date()


def parse_date(text: str, today: Optional[date] = None) -> Optional[date]:
    normalized = normalize(text)
    base = today or current_local_date()

    if re.search(r"\bdepois de amanha\b", normalized):
        return base + timedelta(days=2)
    if re.search(r"\bamanha\b", normalized):
        return base + timedelta(days=1)
    if re.search(r"\bhoje\b", normalized):
        return base

    # Explicit Brazilian date: 12/10 or 12/10/2026.
    match = re.search(r"\b(\d{1,2})/(\d{1,2})(?:/(\d{2,4}))?\b", normalized)
    if match:
        day, month = int(match.group(1)), int(match.group(2))
        year_raw = match.group(3)
        year = int(year_raw) if year_raw else base.year
        if year_raw and len(year_raw) == 2:
            year += 2000
        try:
            parsed = date(year, month, day)
        except ValueError:
            return None
        if not year_raw and parsed < base:
            parsed = date(base.year + 1, month, day)
        return parsed

    # Day number without month: "dia 18".
    match = re.search(r"\bdia\s+(\d{1,2})\b", normalized)
    if match:
        day = int(match.group(1))
        for year, month in ((base.year, base.month), (base.year + 1 if base.month == 12 else base.year, 1 if base.month == 12 else base.month + 1)):
            try:
                parsed = date(year, month, day)
            except ValueError:
                continue
            if parsed >= base:
                return parsed
        return None

    weekdays = {
        "segunda": 0,
        "terca": 1,
        "quarta": 2,
        "quinta": 3,
        "sexta": 4,
        "sabado": 5,
        "domingo": 6,
    }
    weekday_pattern = r"\b(segunda|terca|quarta|quinta|sexta|sabado|domingo)(?:-feira)?\b"
    weekday_match = re.search(weekday_pattern, normalized)
    if weekday_match:
        target_weekday = weekdays[weekday_match.group(1)]
        delta = (target_weekday - base.weekday()) % 7
        # Treat a named weekday as the next upcoming occurrence, not earlier today.
        if delta == 0 or re.search(r"\b(proxima|proximo)\s+" + weekday_pattern, normalized):
            delta = 7
        return base + timedelta(days=delta)

    return None


def parse_time(text: str) -> Optional[str]:
    normalized = normalize(text)
    patterns = (
        r"\bas\s*(\d{1,2})(?::(\d{2})|h(\d{2})?)?\b",
        r"\b(\d{1,2}):(\d{2})\b",
        r"\b(\d{1,2})h(\d{2})?\b",
    )
    for pattern in patterns:
        match = re.search(pattern, normalized)
        if not match:
            continue
        hour = int(match.group(1))
        minute_text = match.group(2) or match.group(3) or "0"
        minute = int(minute_text)
        if 0 <= hour <= 23 and 0 <= minute <= 59:
            return f"{hour:02d}:{minute:02d}"
    return None


def parse_domain(text: str) -> str:
    normalized = normalize(text)
    if any(word in normalized for word in ("consulta", "medico", "medica", "remedio", "exame", "dentista", "saude")):
        return "saúde"
    if any(word in normalized for word in ("prova", "estudar", "faculdade", "aula", "atividade", "trabalho da faculdade", "professor")):
        return "estudos"
    if any(word in normalized for word in ("reuniao", "cliente", "chefe", "empresa", "trabalho", "relatorio", "apresentacao")):
        return "trabalho"
    return "pessoal"


def parse_priority(text: str) -> str:
    normalized = normalize(text)
    if any(word in normalized for word in ("urgente", "prioridade alta", "muito importante", "nao posso esquecer", "o mais rapido possivel")):
        return "alta"
    if any(word in normalized for word in ("sem pressa", "quando puder", "prioridade baixa", "nao e urgente")):
        return "baixa"
    return "média"


def clean_title(text: str) -> str:
    title = text.strip()
    clean_patterns = (
        r"\bdepois de amanh[ãa]\b",
        r"\bamanh[ãa]\b",
        r"\bhoje\b",
        r"\b(?:na|nesta|proxima|proximo)?\s*(?:segunda|terça|terca|quarta|quinta|sexta|sábado|sabado|domingo)(?:-feira)?\b",
        r"\b(?:dia\s+)?\d{1,2}/\d{1,2}(?:/\d{2,4})?\b",
        r"\bdia\s+\d{1,2}\b",
        r"\b(?:às|as)\s*\d{1,2}(?::\d{2}|h\d{0,2})?\b",
        r"\b\d{1,2}:\d{2}\b",
        r"\b\d{1,2}h\d{0,2}\b",
        r"\b(?:por favor|com urgência|urgente|prioridade alta|prioridade baixa)\b",
    )
    for pattern in clean_patterns:
        title = re.sub(pattern, " ", title, flags=re.IGNORECASE)

    title = re.sub(r"^\s*[:\-–]+\s*", "", title)
    title = re.sub(
        r"^\s*(?:por favor,?\s*)?(?:me\s+)?(?:lembre|lembra)(?:-me)?\s+(?:de\s+)?",
        "",
        title,
        flags=re.IGNORECASE,
    )
    title = re.sub(
        r"^\s*(?:por favor,?\s*)?(?:agendar|agende|colocar na agenda|adicionar na agenda)\s+",
        "",
        title,
        flags=re.IGNORECASE,
    )
    title = re.sub(r"^\s*(?:nao esquecer de|lembrar de|preciso|tenho que)\s+", "", title, flags=re.IGNORECASE)
    title = re.sub(r"^\s*[:\-–]+\s*", "", title)
    title = re.sub(r"\s+", " ", title).strip(" .,!;:-")
    return title or text.strip()


def interpret_text(text: str) -> InterpretResponse:
    clean_text = text.strip()
    due_date = parse_date(clean_text)
    due_time = parse_time(clean_text)
    return InterpretResponse(
        title=clean_title(clean_text),
        date=due_date.isoformat() if due_date else None,
        time=due_time,
        domain=parse_domain(clean_text),
        priority=parse_priority(clean_text),
    )


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "vox-ai-service", "mode": "rule-based-mvp"}


@app.post("/interpret", response_model=InterpretResponse)
def interpret(request: InterpretRequest) -> InterpretResponse:
    return interpret_text(request.text)
