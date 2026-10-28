#!/usr/bin/env python3
"""Deterministic checks for the journey-audit skill family.

Commands:
  check    journey.json            structural logic checks (the part visible from data)
  load     journey.json            cognitive load model: index, KLM time, fatigue, exit risk
  vision   journey.json            draft owner-vision coverage table
  curve    journey.json -o x.svg   emotion and load curve
  findings <work>                  validate cjm/edge/load findings.json against the contract
  merge    <work>                  cluster findings and compute starting scores for the verdict
  render   <work>                  expand report_md / verdict files into markdown files

Options: --lang en|ru (output language), --json, --persona-tech, --persona-patience, --family.
Weights of the load model are documented in skills/journey-load/references/cognitive-load.md;
change both places together. Python 3.8+, standard library only.
"""
import argparse
import html
import json
import math
import os
import re
import sys

# ---------------------------------------------------------------- vocabulary

SEVERITIES = ("critical", "high", "medium", "low")
EVIDENCE = ("provided", "absent", "synthetic", "interpretation", "hypothesis", "unknown")
CONFIDENCE = ("high", "med", "low")
FAMILIES = ("cjm", "edge", "load")
PREFIX = {"cjm": "CJM-", "edge": "EDGE-", "load": "LOAD-"}
REQUIRED = ("id", "family", "check", "severity", "steps", "title", "evidence_class", "confidence")

# Accept Russian legacy values in input so hand-written files in either language work.
SEV_ALIASES = {"К": "critical", "В": "high", "С": "medium", "Н": "low"}
EVIDENCE_ALIASES = {
    "предоставлено": "provided", "нет во входе": "absent", "синтетическое поведение": "synthetic",
    "интерпретация": "interpretation", "гипотеза": "hypothesis", "неизвестно": "unknown",
}

LANG = "en"
DASH = "\u2014"
T = {
    "sev": {"en": {"critical": "critical", "high": "high", "medium": "medium", "low": "low"},
            "ru": {"critical": "К", "high": "В", "medium": "С", "low": "Н"}},
    "levels": {"en": ["overload", "high", "moderate", "low"], "ru": ["перегрузка", "высокая", "умеренная", "низкая"]},
    "no_steps": {"en": "{p}: no steps array", "ru": "{p}: нет массива steps"},
    "L01": {"en": "No trigger: what starts the journey is not stated", "ru": "Не указан триггер пути"},
    "L02": {"en": "No success criterion stated from the user's side", "ru": "Не указан критерий успеха от лица пользователя"},
    "L03": {"en": "No persona", "ru": "Не указана персона"},
    "L03m": {"en": "Several personas in one map: split into separate maps", "ru": "Несколько персон в одной карте: разделите на карты"},
    "L00": {"en": "Duplicate step ids: {x}", "ru": "Повторяющиеся id шагов: {x}"},
    "L04": {"en": "Looks like several actions in one step: «{x}»", "ru": "Похоже на несколько действий в одном шаге: «{x}»"},
    "L05u": {"en": "Recovery from failure is unknown: «{x}»", "ru": "Выход из сбоя неизвестен: «{x}»"},
    "L05": {"en": "Failure without a way out: «{x}»", "ru": "Сбой без выхода: «{x}»"},
    "L05z": {"en": "No failures and no branches in the journey: happy-path monotony",
             "ru": "В пути нет ни одного сбоя и ни одной ветки: счастливая монотонность"},
    "L06": {"en": "No visible response to the user's action", "ru": "Нет видимого отклика на действие"},
    "L08": {"en": "Emotion without a stated reason", "ru": "Эмоция без причины"},
    "L09": {"en": "Emotion jumps {a:+} → {b:+} without a failure or moment of truth",
            "ru": "Скачок эмоции {a:+} → {b:+} без сбоя или момента истины"},
    "L09f": {"en": "The emotion curve never goes below zero", "ru": "Кривая эмоций ни разу не опускается ниже нуля"},
    "L10": {"en": "Moment of truth without evidence: a hypothesis", "ru": "Момент истины без доказательства: это гипотеза"},
    "L11": {"en": "Assumed steps: {a} of {b} ({c:.0%})", "ru": "Шагов-догадок: {a} из {b} ({c:.0%})"},
    "L12": {"en": "Main scenario ends with negative emotion while success is claimed",
            "ru": "Основной сценарий заканчивается отрицательной эмоцией при заявленном успехе"},
    "L13": {"en": "External system step without a described failure", "ru": "Шаг внешней системы без описанного сбоя"},
    "L14u": {"en": "Wait duration unknown: the user does not know how long to wait",
             "ru": "Длительность ожидания неизвестна: пользователь не знает, сколько ждать"},
    "L14s": {"en": "Wait of {x:g} s without a status indicator", "ru": "Ожидание {x:g} с без индикатора состояния"},
    "L14c": {"en": "Wait of {x:g} s without cancel or leave-and-return", "ru": "Ожидание {x:g} с без отмены или ухода с возвратом"},
    "L19": {"en": "Internal terms in what the user sees: {x}", "ru": "Внутренние термины в том, что видит пользователь: {x}"},
    "L20": {"en": "Steps in the main path: {x} (guide: 6–20)", "ru": "Шагов в основном пути: {x} (ориентир 6–20)"},
    "V_violated": {"en": "{id}: violated — {e}", "ru": "{id}: нарушено — {e}"},
    "V_missing": {"en": "{id}: not covered by any step — {e}", "ru": "{id}: не закрыто ни одним шагом — {e}"},
    "V_badref": {"en": "{id}: references non-existent steps {x}", "ru": "{id}: ссылки на несуществующие шаги {x}"},
    "V_note": {"en": "Status below is derived from step references only, not from content. Review every item by hand.",
               "ru": "Статус ниже выведен только из ссылок на шаги, а не из содержания. Пересмотрите каждый пункт вручную."},
    "V_derived": {"en": "Vision is partly or fully reconstructed from documents, not received from the owner.",
                  "ru": "Видение частично или полностью восстановлено из документов, а не получено от владельца."},
    "V_head": {"en": "| Item | Expectation | Status | Steps | Origin |", "ru": "| Пункт | Ожидание | Статус | Шаги | Происхождение |"},
    "V_status": {"en": {"covered": "covered", "at-risk": "covered, at risk", "violated": "violated", "not-mentioned": "not mentioned"},
                 "ru": {"covered": "закрыт", "at-risk": "закрыт с риском", "violated": "нарушен", "not-mentioned": "не упомянут"}},
    "F_head": {"en": "| ID | Severity | Step | Finding |", "ru": "| ID | Тяжесть | Шаг | Находка |"},
    "F_count": {"en": "Findings: ", "ru": "Находок: "},
    "load_head1": {"en": "Persona: tech={t}, patience={p} · total KLM {k} s", "ru": "Персона: tech={t}, patience={p} · KLM всего {k} с"},
    "load_peak": {"en": "Peak: {id} — {i} ({l})", "ru": "Пик: {id} — {i} ({l})"},
    "load_head": {"en": "| Step | Stage | Index | Level | Fatigue F | KLM, s | Main drivers | Exit risk |",
                  "ru": "| Шаг | Этап | Индекс | Уровень | Усталость F | KLM, с | Главные вклады | Риск ухода |"},
    "system": {"en": " (system)", "ru": " (система)"},
    "drivers": {"en": {"decisions": "decisions", "fields": "fields", "terms": "new terms", "memory": "memory",
                       "context": "context switches", "wait": "wait", "uncertainty": "uncertainty"},
                "ru": {"decisions": "решения", "fields": "поля", "terms": "термины", "memory": "память",
                       "context": "контекст", "wait": "ожидание", "uncertainty": "неясность"}},
    "risk_index": {"en": "index ≥ {x}", "ru": "индекс ≥ {x}"},
    "risk_fatigue": {"en": "fatigue ≥ {x} with emotion ≤ −1", "ru": "усталость ≥ {x} при эмоции ≤ −1"},
    "risk_wait": {"en": "wait ≥ 10 s without status", "ru": "ожидание ≥ 10 с без статуса"},
    "risk_unknown": {"en": "wait not estimated", "ru": "ожидание не оценено"},
    "curve_title": {"en": "emotion and load (model)", "ru": "эмоция и нагрузка (модель)"},
    "curve_load": {"en": "load", "ru": "нагрузка"},
    "curve_exit": {"en": "exit?", "ru": "уход?"},
    "curve_note": {"en": "Model: load index 0–100 with open weights, not a measurement. System steps count wait only.",
                   "ru": "Модель: индекс 0–100 по открытым весам, не измерение. Системные шаги — только ожидание."},
    "curve_branches": {"en": " Branches ({n}) are not drawn.", "ru": " Ветки ({n}) на кривой не показаны."},
    "contract_ok": {"en": "Contract OK.", "ru": "Контракт соблюдён."},
    "contract_err": {"en": "Contract errors: {n}", "ru": "Ошибок контракта: {n}"},
}


def t(key, **kw):
    v = T[key][LANG]
    return v.format(**kw) if kw and isinstance(v, str) else v


# ---------------------------------------------------------------- helpers

EXTERNAL_HINTS = re.compile(
    r"payment|gateway|sms|otp|ocr|recogni|llm|model|bank|third[- ]party|external|api|provider|email|mail|"
    r"оплат|платёж|платеж|смс|госуслуг|распозна|модел|банк|шлюз|внешн|провайдер|почт|письм",
    re.I,
)
MULTI_ACTION = re.compile(r"\s(and then|then|after that|и затем|затем|потом|после чего)\s|;|\s→\s", re.I)
INTERNAL_TERMS = re.compile(
    r"\b[A-Z][A-Z0-9_]{3,}\b|\b[a-z]+[A-Z][a-zA-Z]*\b|\b[A-Z][a-z]+[A-Z][a-zA-Z]*\b|\bDTO\b|\bAPI\b|\bJSON\b"
)
COMMON_TERMS = {"PDF", "JPEG", "JPG", "PNG", "HEIC", "SMS", "QR", "URL", "WIFI", "OK", "PIN", "IBAN", "CVV", "CVC"}

KLM_BASE = {"P": 1.1, "B": 0.1, "H": 0.4, "M": 1.35}
K_BY_TECH = {"high": 0.2, "mid": 0.28, "low": 0.5}
TECH_MULT = {"low": 1.25, "mid": 1.0, "high": 0.85}


def load_journey(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data.get("steps"), list) or not data["steps"]:
        sys.exit(t("no_steps", p=path))
    return data


def all_steps(data):
    for s in data["steps"]:
        yield None, s
    for b in data.get("branches") or []:
        for s in b.get("steps") or []:
            yield b.get("id"), s


def qid(branch, s):
    """Full step id: b1.s1 inside branches (prefix added only if missing)."""
    sid = str(s.get("id", "?"))
    if branch and not sid.startswith(f"{branch}."):
        return f"{branch}.{sid}"
    return sid


def is_unknown(v):
    return v is None or (isinstance(v, str) and v.strip().lower() in ("unknown", "неизвестно", "?"))


def num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return 0.0


def norm_sev(v):
    return SEV_ALIASES.get(v, v)


def finding(fid, sev, step, text):
    return {"id": fid, "severity": sev, "step": step, "text": text}


# ---------------------------------------------------------------- check

def cmd_check(data):
    out = []
    steps = data["steps"]
    persona = data.get("persona") or {}
    custom_terms = [x for x in data.get("internal_terms", []) if x]
    allowed = COMMON_TERMS | {x.upper() for x in data.get("allowed_terms", [])}

    if not str(data.get("trigger", "")).strip():
        out.append(finding("L01", "medium", None, t("L01")))
    if not str(data.get("success", "")).strip():
        out.append(finding("L02", "high", None, t("L02")))
    if isinstance(persona, list):
        if len(persona) > 1:
            out.append(finding("L03", "medium", None, t("L03m")))
    elif not persona or not (persona.get("name") or persona.get("goal")):
        out.append(finding("L03", "medium", None, t("L03")))

    ids = [qid(b, s) for b, s in all_steps(data)]
    dup = sorted({i for i in ids if ids.count(i) > 1})
    if dup:
        out.append(finding("L00", "low", None, t("L00", x=", ".join(dup))))

    assumed, prev_feel, has_failure = 0, None, False
    for branch, s in all_steps(data):
        tag = qid(branch, s)
        actor = s.get("actor", "user")
        action = str(s.get("action", ""))
        resp = str(s.get("response", "")).strip()
        load = s.get("load") or {}
        if s.get("assumption"):
            assumed += 1
        if s.get("failure"):
            has_failure = True

        if actor == "user" and MULTI_ACTION.search(action):
            out.append(finding("L04", "medium", tag, t("L04", x=action[:80])))
        if s.get("failure"):
            rec = s.get("recovery", "")
            if "recovery" in s and is_unknown(rec):
                out.append(finding("L05", "medium", tag, t("L05u", x=str(s["failure"])[:80])))
            elif not str(rec).strip():
                sev = norm_sev(s.get("failure_severity") or ("critical" if s.get("moment_of_truth") else "high"))
                out.append(finding("L05", sev, tag, t("L05", x=str(s["failure"])[:80])))
        if actor == "user" and not resp:
            out.append(finding("L06", "high", tag, t("L06")))
        if s.get("feeling") is not None and not str(s.get("feeling_reason", "")).strip():
            out.append(finding("L08", "medium", tag, t("L08")))

        feel = s.get("feeling")
        if branch is None and feel is not None:
            if prev_feel is not None and abs(feel - prev_feel) > 2 and not (s.get("failure") or s.get("moment_of_truth")):
                out.append(finding("L09", "medium", tag, t("L09", a=prev_feel, b=feel)))
            prev_feel = feel

        if s.get("moment_of_truth") and not str(s.get("evidence", "")).strip():
            out.append(finding("L10", "high", tag, t("L10")))

        external = actor == "external" or (actor == "system" and EXTERNAL_HINTS.search(action + " " + resp))
        if external and not s.get("failure"):
            out.append(finding("L13", "high", tag, t("L13")))

        if "wait_s" in load and is_unknown(load.get("wait_s")):
            out.append(finding("L14", "medium", tag, t("L14u")))
        wait = num(load.get("wait_s"))
        if wait >= 1 and s.get("status_feedback") is False:
            out.append(finding("L14", "high", tag, t("L14s", x=wait)))
        if wait >= 10 and not s.get("recovery") and not re.search(r"cancel|отмен", resp + action, re.I):
            out.append(finding("L14", "high", tag, t("L14c", x=wait)))

        visible = resp + " " + str(s.get("failure", ""))
        terms = {x for x in INTERNAL_TERMS.findall(visible) if x.upper() not in allowed}
        terms |= {x for x in custom_terms if x.lower() in visible.lower()}
        if terms:
            out.append(finding("L19", "medium", tag, t("L19", x=", ".join(sorted(terms)[:6]))))

    total = len(ids)
    if total:
        share = assumed / total
        out.append(finding("L11", "medium" if share > 0.7 else "low", None, t("L11", a=assumed, b=total, c=share)))
    last = steps[-1]
    if data.get("success") and last.get("feeling") is not None and last["feeling"] < 0 \
            and data.get("scenario", "main") in ("main", "основной"):
        out.append(finding("L12", "high", last.get("id"), t("L12")))
    if not has_failure and not data.get("branches"):
        out.append(finding("L05", "critical", None, t("L05z")))
    feels = [s.get("feeling") for s in steps if s.get("feeling") is not None]
    if len(feels) >= 4 and min(feels) >= 0:
        out.append(finding("L09", "medium", None, t("L09f")))
    if not 6 <= len(steps) <= 20:
        out.append(finding("L20", "low", None, t("L20", x=len(steps))))
    if data.get("owner_vision"):
        out.extend(vision_findings(data))
    return out


# ---------------------------------------------------------------- vision

def vision_table(data):
    ids = {qid(b, s) for b, s in all_steps(data)}
    rows = []
    for v in data.get("owner_vision") or []:
        linked = [x for x in v.get("steps", []) if x in ids]
        status = v.get("status") or ("covered" if linked else "not-mentioned")
        rows.append({"id": v.get("id"), "expect": v.get("expect"), "status": status,
                     "steps": linked, "origin": v.get("origin", "owner")})
    return rows


def vision_findings(data):
    out = []
    ids = {qid(b, s) for b, s in all_steps(data)}
    for v in data.get("owner_vision") or []:
        linked = [x for x in v.get("steps", []) if x in ids]
        missing = [x for x in v.get("steps", []) if x not in ids]
        status = v.get("status")
        if status == "violated":
            out.append(finding("L17", "critical", ",".join(linked) or None, t("V_violated", id=v.get("id"), e=v.get("expect"))))
        elif not linked or status == "not-mentioned":
            out.append(finding("L17", "high", None, t("V_missing", id=v.get("id"), e=v.get("expect"))))
        if missing:
            out.append(finding("L17", "low", None, t("V_badref", id=v.get("id"), x=missing)))
    return out


def print_vision(data):
    rows = vision_table(data)
    if any(r["origin"] != "owner" for r in rows):
        print(t("V_derived"))
    print(t("V_note"))
    print(t("V_head") + "\n|---|---|---|---|---|")
    labels = t("V_status")
    for r in rows:
        print(f"| {r['id']} | {r['expect']} | {labels.get(r['status'], r['status'])} | "
              f"{', '.join(r['steps']) or '—'} | {r['origin']} |")
    print_findings(vision_findings(data))


def print_findings(items):
    items.sort(key=lambda f: (SEVERITIES.index(f["severity"]) if f["severity"] in SEVERITIES else 9, f["id"], str(f["step"])))
    labels = t("sev")
    counts = {k: sum(1 for f in items if f["severity"] == k) for k in SEVERITIES}
    print(t("F_count") + " · ".join(f"{labels[k]} {v}" for k, v in counts.items()))
    print(t("F_head") + "\n|---|---|---|---|")
    for f in items:
        print(f"| {f['id']} | {labels.get(f['severity'], f['severity'])} | {f['step'] or '—'} | {f['text']} |")


# ---------------------------------------------------------------- load

def klm_seconds(expr, tech, mobile=False):
    if not expr:
        return 0.0
    k = K_BY_TECH.get(tech, 0.28)
    if mobile and tech != "low":
        # Typing on a phone is slower: mid uses the low value, high uses mid.
        k = K_BY_TECH["low"] if tech == "mid" else K_BY_TECH["mid"]
    total = 0.0
    for tok in str(expr).split():
        m = re.fullmatch(r"([KPBHM])(?:\*(\d+))?", tok)
        if m:
            op, n = m.group(1), int(m.group(2) or 1)
            total += (k if op == "K" else KLM_BASE[op]) * n
            continue
        m = re.fullmatch(r"W(\d+(?:\.\d+)?)", tok)
        if m:
            total += float(m.group(1))
            continue
        raise ValueError(f"unknown KLM operator: {tok}")
    return total


def step_load(s, tech, patience):
    L = s.get("load") or {}
    g = lambda k: num(L.get(k))
    decisions, options = g("decisions"), g("max_options")
    parts = {
        "decisions": 6 * decisions + (5 * math.log2(options + 1) if decisions > 0 else 0),
        "fields": 2.5 * g("fields"),
        "terms": 6 * g("new_terms"),
        "memory": 6 * min(g("memory_items"), 4) + 15 * max(g("memory_items") - 4, 0),
        "context": 7 * g("context_switches"),
        "wait": (3 if s.get("status_feedback", True) else 6) * math.log2(g("wait_s") + 1)
        * (1.5 if patience == "low" else 1.0),
        "uncertainty": 8 * g("uncertainty"),
    }
    index = min(100.0, sum(parts.values()) * TECH_MULT.get(tech, 1.0))
    return index, parts


def level(index):
    names = t("levels")
    for thr, name in zip((70, 50, 25, 0), names):
        if index >= thr:
            return name
    return names[-1]


def cmd_load(data, tech, patience):
    persona = data.get("persona") or {}
    if isinstance(persona, list):
        persona = persona[0] if persona else {}
    tech = tech or persona.get("tech", "mid")
    patience = patience or persona.get("patience", "mid")
    idx_thr = 60 if patience == "low" else 70
    f_thr = 100 if patience == "low" else 120
    rows, F = [], None
    for s in data["steps"]:
        is_user = s.get("actor", "user") == "user"
        if not is_user and not s.get("load"):
            continue
        index, parts = step_load(s, tech, patience)
        if is_user:
            F = index if F is None else 0.75 * F + index
        elif F is not None:
            # Waiting for the system tires the user; other features of a system step do not.
            F = 0.75 * F + parts["wait"] * TECH_MULT.get(tech, 1.0)
        L = s.get("load") or {}
        ch = (str(s.get("channel", "")) + " " + str(persona.get("context", ""))).lower()
        try:
            klm = klm_seconds(L.get("klm"), tech, mobile=bool(re.search(r"mobile|phone|моб|телефон", ch)))
        except ValueError as e:
            sys.exit(f"{s.get('id')}: {e}")
        wait = num(L.get("wait_s"))
        flags = []
        if is_user and index >= idx_thr:
            flags.append(t("risk_index", x=idx_thr))
        if is_user and F is not None and F >= f_thr and s.get("feeling") is not None and s["feeling"] <= -1:
            flags.append(t("risk_fatigue", x=f_thr))
        if wait >= 10 and s.get("status_feedback") is False:
            flags.append(t("risk_wait"))
        notes = [t("risk_unknown")] if "wait_s" in L and is_unknown(L.get("wait_s")) else []
        names = t("drivers")
        top = sorted(parts.items(), key=lambda kv: -kv[1])[:2]
        rows.append({
            "id": s.get("id"), "stage": s.get("stage", ""), "actor": s.get("actor", "user"),
            "index": round(index, 1), "level": level(index), "fatigue": round(F, 1) if F is not None else 0,
            "klm_s": round(klm, 2), "drivers": ", ".join(f"{names[k]} {v:.0f}" for k, v in top if v > 0),
            "parts": {k: round(v, 1) for k, v in parts.items()}, "exit_risk": flags, "notes": notes,
            "feeling": s.get("feeling"),
        })
    users = [r for r in rows if r["actor"] == "user"]
    return {"tech": tech, "patience": patience, "rows": rows,
            "total_klm_s": round(sum(r["klm_s"] for r in rows), 1),
            "peak": max(users, key=lambda r: r["index"]) if users else None}


def print_load(res):
    print(t("load_head1", t=res["tech"], p=res["patience"], k=res["total_klm_s"]))
    if res["peak"]:
        p = res["peak"]
        print(t("load_peak", id=p["id"], i=p["index"], l=p["level"]))
    print(t("load_head") + "\n|---|---|---|---|---|---|---|---|")
    for r in res["rows"]:
        lvl = r["level"] + (t("system") if r["actor"] != "user" else "")
        print(f"| {r['id']} | {r['stage']} | {r['index']} | {lvl} | {r['fatigue']} | {r['klm_s']} | "
              f"{r['drivers'] or '—'} | {'; '.join(r['exit_risk'] + r['notes']) or '—'} |")


# ---------------------------------------------------------------- curve

def cmd_curve(data, out_path, tech, patience):
    res = cmd_load(data, tech, patience)
    by_id = {r["id"]: r for r in res["rows"]}
    steps = data["steps"]
    n = len(steps)
    W, H, padl, padr, top, mid_h = max(640, 70 * n + 120), 440, 70, 30, 40, 200
    xs = [padl + i * (W - padl - padr) / max(n - 1, 1) for i in range(n)]
    fy = lambda f: top + (2 - f) / 4 * mid_h
    ly0, lh = top + mid_h + 40, 110
    e = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="system-ui,sans-serif" font-size="11">',
         '<style>.ax{stroke:#999;stroke-width:1}.zero{stroke:#666;stroke-dasharray:4 3}.t{fill:#333}'
         '.feel{fill:none;stroke:#5b4bd6;stroke-width:2.5}.neg{fill:#e5484d;opacity:.15}'
         '.bar{fill:#f5a524}.over{fill:#e5484d}.flag{fill:#e5484d;font-weight:600}'
         '.bg{fill:#fff}@media (prefers-color-scheme:dark){.bg{fill:#0d1117}.t{fill:#ddd}.ax{stroke:#666}}</style>',
         f'<rect class="bg" width="{W}" height="{H}" rx="12"/>',
         f'<text class="t" x="{padl}" y="20" font-size="13" font-weight="600">'
         f'{html.escape(data.get("title", "Journey"))} — {t("curve_title")}</text>']
    for f, lab in [(2, "+2"), (1, "+1"), (0, "0"), (-1, "−1"), (-2, "−2")]:
        e.append(f'<text class="t" x="{padl - 30}" y="{fy(f) + 4:.0f}">{lab}</text>')
        e.append(f'<line class="{"zero" if f == 0 else "ax"}" x1="{padl}" x2="{W - padr}" y1="{fy(f):.0f}" '
                 f'y2="{fy(f):.0f}" opacity="{1 if f == 0 else .25}"/>')
    pts = [(xs[i], fy(s["feeling"])) for i, s in enumerate(steps) if s.get("feeling") is not None]
    if pts:
        poly = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        z = fy(0)
        e.append(f'<clipPath id="below"><rect x="0" y="{z:.1f}" width="{W}" height="{mid_h}"/></clipPath>')
        e.append(f'<polygon class="neg" clip-path="url(#below)" points="{pts[0][0]:.1f},{z:.1f} {poly} {pts[-1][0]:.1f},{z:.1f}"/>')
        e.append(f'<polyline class="feel" points="{poly}"/>')
        e.extend(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.5" fill="#5b4bd6"/>' for x, y in pts)
    e.append(f'<text class="t" x="{padl - 60}" y="{ly0 + 12}">{t("curve_load")}</text>')
    bw = min(36, (W - padl - padr) / max(n, 1) * 0.6)
    for i, s in enumerate(steps):
        r = by_id.get(s.get("id"))
        if r:
            h = r["index"] / 100 * lh
            cls = "over" if r["index"] >= 70 else "bar"
            e.append(f'<rect class="{cls}" x="{xs[i] - bw / 2:.1f}" y="{ly0 + lh - h:.1f}" width="{bw:.1f}" height="{h:.1f}" rx="2"/>')
            e.append(f'<text class="t" x="{xs[i]:.1f}" y="{ly0 + lh - h - 4:.1f}" text-anchor="middle">{r["index"]:.0f}</text>')
            if r["exit_risk"]:
                e.append(f'<text class="flag" x="{xs[i]:.1f}" y="{ly0 - 6:.1f}" text-anchor="middle">{t("curve_exit")}</text>')
        e.append(f'<text class="t" x="{xs[i]:.1f}" y="{ly0 + lh + 16:.1f}" text-anchor="middle">{html.escape(str(s.get("id", i + 1)))}</text>')
        if s.get("stage") and (i == 0 or s.get("stage") != steps[i - 1].get("stage")):
            e.append(f'<text class="t" x="{xs[i]:.1f}" y="{ly0 + lh + 29:.1f}" text-anchor="middle" opacity=".6" '
                     f'font-size="9">{html.escape(str(s["stage"])[:14])}</text>')
    nb = len(data.get("branches") or [])
    note = t("curve_note") + (t("curve_branches", n=nb) if nb else "")
    e.append(f'<text class="t" x="{padl}" y="{H - 8}" opacity=".7">{html.escape(note)}</text>')
    e.append("</svg>")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(e))
    print(f"SVG: {out_path}")


# ---------------------------------------------------------------- findings contract

def read_findings(work):
    out = {}
    for fam in FAMILIES:
        path = os.path.join(work, fam, "findings.json")
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                out[fam] = json.load(f)
    return out


def step_ids(work):
    path = os.path.join(work, "journey.json")
    if not os.path.exists(path):
        return None
    data = load_journey(path)
    ids = {qid(b, s) for b, s in all_steps(data)}
    br = os.path.join(work, "edge", "branches.json")
    if os.path.exists(br):
        with open(br, encoding="utf-8") as f:
            extra = json.load(f)
        for b in extra if isinstance(extra, list) else extra.get("branches", []):
            for s in b.get("steps", []):
                ids.add(qid(b.get("id"), s))
    return ids


def cmd_findings(work, only=None):
    errors, stats = [], {}
    ids = step_ids(work)
    files = read_findings(work)
    for fam in FAMILIES:
        if only and fam != only:
            continue
        if fam not in files:
            errors.append(f"{fam}: missing {fam}/findings.json")
            continue
        items = files[fam].get("findings")
        if not isinstance(items, list):
            errors.append(f"{fam}: no findings array")
            continue
        seen = set()
        stats[fam] = {k: 0 for k in SEVERITIES}
        for i, f in enumerate(items):
            where = f"{fam}[{i}] {f.get('id', '?')}"
            for k in REQUIRED:
                if k not in f or f[k] in ("", None):
                    errors.append(f"{where}: missing field {k}")
            if f.get("id") in seen:
                errors.append(f"{where}: duplicate id")
            seen.add(f.get("id"))
            if f.get("id") and not str(f["id"]).startswith(PREFIX[fam]):
                errors.append(f"{where}: id must start with {PREFIX[fam]}")
            if f.get("family") and f["family"] != fam:
                errors.append(f"{where}: family={f['family']} in the {fam} file")
            sev = norm_sev(f.get("severity"))
            if sev not in SEVERITIES:
                errors.append(f"{where}: severity not in {SEVERITIES}")
            else:
                stats[fam][sev] += 1
            ev = EVIDENCE_ALIASES.get(f.get("evidence_class"), f.get("evidence_class"))
            if ev and ev not in EVIDENCE:
                errors.append(f"{where}: evidence_class '{f.get('evidence_class')}' not in {EVIDENCE}")
            if ev == "provided" and not f.get("evidence_ref"):
                errors.append(f"{where}: evidence_class 'provided' without evidence_ref")
            if f.get("confidence") and f["confidence"] not in CONFIDENCE:
                errors.append(f"{where}: confidence not in {CONFIDENCE}")
            if fam == "edge":
                for k in ("frequency", "impact"):
                    if f.get(k) not in (1, 2, 3):
                        errors.append(f"{where}: {k} must be 1–3")
            if ids is not None and isinstance(f.get("steps"), list):
                bad = [x for x in f["steps"] if x not in ids]
                if bad:
                    errors.append(f"{where}: steps not found in journey.json / edge/branches.json: {bad}")
    labels = t("sev")
    for fam, st in stats.items():
        print(f"{fam}: " + " · ".join(f"{labels[k]} {v}" for k, v in st.items()))
    if errors:
        print(t("contract_err", n=len(errors)))
        for e in errors:
            print("  - " + e)
        sys.exit(1)
    print(t("contract_ok"))


# ---------------------------------------------------------------- merge

SEV_W = {"critical": 8, "high": 4, "medium": 2, "low": 1}
CONF_W = {"high": 1.0, "med": 0.7, "low": 0.4}
IMPACT_BY_SEV = {"critical": 3, "high": 2, "medium": 1, "low": 1}


def cmd_merge(work):
    files = read_findings(work)
    main_ids = set()
    jp = os.path.join(work, "journey.json")
    if os.path.exists(jp):
        main_ids = {str(s.get("id")) for s in load_journey(jp)["steps"]}
    items = [f for fam in FAMILIES for f in (files.get(fam, {}).get("findings") or [])]
    for f in items:
        f["severity"] = norm_sev(f.get("severity"))
    parent = list(range(len(items)))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    for i, a in enumerate(items):
        for j in range(i + 1, len(items)):
            b = items[j]
            same_cause = a.get("root_cause") and a.get("root_cause") == b.get("root_cause")
            shared = set(a.get("steps") or []) & set(b.get("steps") or [])
            if same_cause and (shared or not a.get("steps") or not b.get("steps")):
                parent[find(i)] = find(j)
    groups = {}
    for i in range(len(items)):
        groups.setdefault(find(i), []).append(items[i])
    clusters = []
    for n, members in enumerate(groups.values(), 1):
        sev = min((m["severity"] for m in members), key=lambda x: SEVERITIES.index(x) if x in SEVERITIES else 9)
        conf = max((m.get("confidence", "low") for m in members), key=lambda c: CONF_W.get(c, 0))
        steps = sorted({x for m in members for x in (m.get("steps") or [])})
        fams = sorted({m.get("family") for m in members})
        on_main = not steps or any(x in main_ids for x in steps)
        freq = max([m["frequency"] for m in members if m.get("frequency") in (1, 2, 3)] or [3 if on_main else 1])
        imp = max([m["impact"] for m in members if m.get("impact") in (1, 2, 3)] or [IMPACT_BY_SEV.get(sev, 1)])
        confirm = 1 + 0.25 * (len(fams) - 1)
        score = SEV_W.get(sev, 1) * CONF_W.get(conf, 0.4) * freq * imp * confirm / 2  # effort M = 2
        if sev == "critical" and conf in ("high", "med"):
            prio = "P0"
        elif score >= 12 or (sev == "high" and steps and on_main):
            prio = "P1"
        elif score >= 3:
            prio = "P2"
        else:
            prio = "deferred"
        clusters.append({
            "cluster": f"K-{n:02d}", "priority_hint": prio, "score": round(score, 1), "severity": sev,
            "confidence": conf, "frequency": freq, "impact": imp, "families": fams, "steps": steps,
            "vision": sorted({v for m in members for v in (m.get("vision") or [])}),
            "useful_friction": any(m.get("useful_friction") for m in members),
            "root_cause": sorted({m.get("root_cause") for m in members if m.get("root_cause")}),
            "findings": [{"id": m.get("id"), "check": m.get("check"), "title": m.get("title")} for m in members],
        })
    order = {"P0": 0, "P1": 1, "P2": 2, "deferred": 3}
    clusters.sort(key=lambda c: (order[c["priority_hint"]], -c["score"]))
    print(json.dumps({"total_findings": len(items), "clusters": clusters,
                      "note": "Effort assumed M=2; priority is a hint, the verdict agent decides."},
                     ensure_ascii=False, indent=1))


# ---------------------------------------------------------------- render

def cmd_render(work):
    for fam, doc in read_findings(work).items():
        text, path = doc.get("report_md"), os.path.join(work, fam, "report.md")
        if text:
            with open(path, "w", encoding="utf-8") as f:
                f.write(text.rstrip() + "\n")
            print(f"{fam}: {path}")
    vpath = os.path.join(work, "verdict", "verdict.json")
    if os.path.exists(vpath):
        with open(vpath, encoding="utf-8") as f:
            v = json.load(f)
        for rel, text in (v.get("files") or {}).items():
            out = os.path.normpath(os.path.join(work, "verdict", rel))
            if not out.startswith(os.path.normpath(os.path.join(work, "verdict"))):
                continue  # never write outside verdict/
            os.makedirs(os.path.dirname(out), exist_ok=True)
            with open(out, "w", encoding="utf-8") as f:
                f.write(text.rstrip() + "\n")
            print(f"verdict: {out}")


# ---------------------------------------------------------------- main

def main():
    global LANG
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=["check", "load", "vision", "curve", "findings", "merge", "render"])
    ap.add_argument("target", help="journey.json; for findings, merge and render: the work folder")
    ap.add_argument("--lang", choices=["en", "ru"], default=os.environ.get("JOURNEY_AUDIT_LANG", "en"))
    ap.add_argument("--persona-tech", choices=["low", "mid", "high"])
    ap.add_argument("--persona-patience", choices=["low", "mid", "high"])
    ap.add_argument("--family", choices=list(FAMILIES), help="findings: validate one family only")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("-o", "--out", default="journey-curve.svg")
    a = ap.parse_args()
    LANG = a.lang
    if a.command == "findings":
        return cmd_findings(a.target, a.family)
    if a.command == "merge":
        return cmd_merge(a.target)
    if a.command == "render":
        return cmd_render(a.target)
    data = load_journey(a.target)
    if a.command == "check":
        res = cmd_check(data)
        print(json.dumps(res, ensure_ascii=False, indent=1)) if a.json else print_findings(res)
    elif a.command == "vision":
        if a.json:
            print(json.dumps({"table": vision_table(data), "findings": vision_findings(data)}, ensure_ascii=False, indent=1))
        else:
            print_vision(data)
    elif a.command == "load":
        res = cmd_load(data, a.persona_tech, a.persona_patience)
        print(json.dumps(res, ensure_ascii=False, indent=1)) if a.json else print_load(res)
    else:
        cmd_curve(data, a.out, a.persona_tech, a.persona_patience)


if __name__ == "__main__":
    main()
