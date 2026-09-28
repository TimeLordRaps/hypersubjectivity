"""Finite [FRAME] for situated perspectives and candidate cross-reality links.

Typed links do not establish consciousness, experiential truth, object identity,
or reality-kind transport. Those questions remain open even when a reference is
present in the record.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class SubjectClaim:
    identifier: str
    subjectifiable: bool
    consciousness_claim: str | None


@dataclass(frozen=True)
class ObjectPresentationRef:
    identifier: str
    object_id: str
    reality_kind: str


@dataclass(frozen=True)
class Perspective:
    identifier: str
    subject_id: str
    object_presentation: str
    experience_claim: str


@dataclass(frozen=True)
class LinkClaim:
    identifier: str
    subject_id: str
    source_perspective: str
    target_perspective: str
    mechanism_claim: str
    object_transport_claim: str | None


@dataclass(frozen=True)
class LinkResult:
    typed_status: str
    consciousness_status: str
    object_continuity_status: str
    reason: str


def _index(items, label):
    indexed = {}
    for item in items:
        if not item.identifier or item.identifier in indexed:
            raise ValueError(f"{label} identifiers must be nonempty and unique")
        indexed[item.identifier] = item
    return indexed


@dataclass(frozen=True)
class Frame:
    subjects: tuple[SubjectClaim, ...]
    objects: tuple[ObjectPresentationRef, ...]
    perspectives: tuple[Perspective, ...]
    links: tuple[LinkClaim, ...]

    def __post_init__(self):
        _index(self.subjects, "subject")
        _index(self.objects, "object presentation")
        _index(self.perspectives, "perspective")
        _index(self.links, "link")

    def link(self, identifier: str) -> LinkResult:
        claim = _index(self.links, "link")[identifier]
        subjects = _index(self.subjects, "subject")
        objects = _index(self.objects, "object presentation")
        perspectives = _index(self.perspectives, "perspective")

        def reject(reason):
            return LinkResult("FAIL", "UNKNOWN", "UNKNOWN", reason)

        subject = subjects.get(claim.subject_id)
        source = perspectives.get(claim.source_perspective)
        target = perspectives.get(claim.target_perspective)
        if subject is None or not subject.subjectifiable:
            return reject("no declared subjectifiable subject for this link")
        if source is None or target is None or source.identifier == target.identifier:
            return reject("a link needs two distinct actual perspective records")
        if source.subject_id != subject.identifier or target.subject_id != subject.identifier:
            return reject("both perspectives must belong to the linking subject")
        first = objects.get(source.object_presentation)
        second = objects.get(target.object_presentation)
        if first is None or second is None:
            return reject("a perspective references a missing object presentation")
        if not first.object_id or not second.object_id or not first.reality_kind or not second.reality_kind:
            return reject("object presentation references need object and reality-kind identifiers")
        if first.reality_kind == second.reality_kind:
            return reject("this candidate cross-reality link has only one declared reality kind")
        if not source.experience_claim or not target.experience_claim or not claim.mechanism_claim:
            return reject("experience and linking mechanism need explicit claim references")
        return LinkResult(
            "PASS", "UNKNOWN", "UNKNOWN",
            "finite link is typed; consciousness, object continuity, and mechanism soundness remain unproved",
        )
