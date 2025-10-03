from __future__ import annotations

import re
from datetime import timedelta
from typing import Iterable

from django.conf import settings

from matches.models import Match
from notifications.models import Notification
from reports.models import Report


STOPWORDS = {"the", "a", "an", "and", "or", "with", "of", "in", "on", "for", "to"}


def tokenize(text: str) -> set[str]:
    tokens = set(re.findall(r"[a-z0-9]+", (text or "").lower()))
    return {t for t in tokens if t not in STOPWORDS and len(t) > 1}


def compute_overlap(a: Iterable[str], b: Iterable[str]) -> float:
    set_a = set(a)
    set_b = set(b)
    if not set_a or not set_b:
        return 0.0
    inter = set_a & set_b
    union = set_a | set_b
    return len(inter) / len(union)


def notify_users_for_match(match: Match) -> None:
    Notification.objects.create(
        user=match.lost_report.reported_by,
        message=f"Potential match found for your lost item: {match.found_report.title}",
        related_match=match,
    )
    Notification.objects.create(
        user=match.found_report.reported_by,
        message=f"Your found item may match: {match.lost_report.title}",
        related_match=match,
    )


def run_matching_for_report(new_report: Report) -> list[Match]:
    threshold = getattr(settings, "MATCHING_CONF_THRESHOLD", 0.35)
    window_days = getattr(settings, "MATCHING_DATE_WINDOW_DAYS", 14)
    weights = getattr(settings, "MATCHING_WEIGHTS", {"category": 0.6, "keyword": 0.4, "date_boost": 0.05})

    opposite_type = Report.ReportType.FOUND if new_report.report_type == Report.ReportType.LOST else Report.ReportType.LOST
    date_min = new_report.date_lost_found - timedelta(days=window_days)
    date_max = new_report.date_lost_found + timedelta(days=window_days)

    candidates = (
        Report.objects.filter(
            report_type=opposite_type,
            category=new_report.category,
            date_lost_found__range=(date_min, date_max),
            status__in=[Report.Status.PENDING, Report.Status.UNCLAIMED],
        )
        .exclude(id=new_report.id)
    )

    tokens_new = tokenize(f"{new_report.title} {new_report.description}")
    matches: list[Match] = []

    for candidate in candidates:
        tokens_other = tokenize(f"{candidate.title} {candidate.description}")
        keyword_overlap = compute_overlap(tokens_new, tokens_other)
        category_match = 1.0 if candidate.category_id == new_report.category_id else 0.0
        date_diff = abs((candidate.date_lost_found - new_report.date_lost_found).days)
        date_boost = weights.get("date_boost", 0.05) if date_diff <= 3 else 0.0

        confidence = weights.get("category", 0.6) * category_match + weights.get("keyword", 0.4) * keyword_overlap
        confidence = min(1.0, confidence + date_boost)

        if confidence >= threshold:
            lost, found = (new_report, candidate) if new_report.report_type == Report.ReportType.LOST else (candidate, new_report)
            match = Match.objects.create(
                lost_report=lost,
                found_report=found,
                confidence_score=confidence,
            )
            notify_users_for_match(match)
            matches.append(match)

    return matches


