import unittest

from hypersubjectivity import (
    SubjectClaim,
    ObjectPresentationRef,
    Perspective,
    LinkClaim,
    Frame,
)


class SubjectivityFrameTests(unittest.TestCase):
    def frame(self, *, second_subject="s", mechanism="bridge-claim", continuity=None):
        return Frame(
            subjects=(SubjectClaim("s", subjectifiable=True, consciousness_claim="conscious-claim"),
                      SubjectClaim("other", subjectifiable=True, consciousness_claim=None)),
            objects=(ObjectPresentationRef("ob", "o", "base-reality"),
                     ObjectPresentationRef("oa", "o", "areality")),
            perspectives=(Perspective("pb", "s", "ob", "view-a"),
                          Perspective("pa", second_subject, "oa", "view-b")),
            links=(LinkClaim("link", "s", "pb", "pa", mechanism, continuity),),
        )

    def test_cross_reality_link_is_typed_but_not_ontological_proof(self):
        result = self.frame().link("link")
        self.assertEqual(result.typed_status, "PASS")
        self.assertEqual(result.consciousness_status, "UNKNOWN")
        self.assertEqual(result.object_continuity_status, "UNKNOWN")

    def test_subjectifiability_does_not_create_a_perspective(self):
        frame = Frame(
            subjects=(SubjectClaim("s", subjectifiable=True, consciousness_claim=None),),
            objects=(ObjectPresentationRef("ob", "o", "base-reality"),),
            perspectives=(),
            links=(LinkClaim("link", "s", "missing", "missing", "bridge", None),),
        )
        self.assertEqual(frame.link("link").typed_status, "FAIL")

    def test_different_subjects_do_not_form_one_subject_link(self):
        self.assertEqual(self.frame(second_subject="other").link("link").typed_status, "FAIL")

    def test_missing_mechanism_does_not_count_as_link(self):
        self.assertEqual(self.frame(mechanism="").link("link").typed_status, "FAIL")

    def test_declared_object_transport_is_still_only_a_claim(self):
        result = self.frame(continuity="object-transport-claim").link("link")
        self.assertEqual(result.typed_status, "PASS")
        self.assertEqual(result.object_continuity_status, "UNKNOWN")


if __name__ == "__main__":
    unittest.main()
