"""Tests for the Phase 3 checkers (scripture, translation, press, course). Run:  python -m unittest discover -s tests -v

Fixtures are synthetic. Verse text in the verification test is a tiny temp file, not a stored translation.
"""
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.dont_write_bytecode = True
REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "execution"))

import course_check  # noqa: E402
import press_check  # noqa: E402
import scripture_check  # noqa: E402
import translation_check  # noqa: E402

JOHN = "For God so loved the world, that he gave his only begotten Son"


def scripture(hook="Do you know the verse everyone quotes?", quote=JOHN, translation="KJV", extra=""):
    body = (f"{hook}\nHere is what it says: \"{quote}\".\n"
            "Take a quiet minute today and ask what that love asks of you.\n"
            "Who needs to hear it from you this week? " + extra)
    return (f"Reference: John 3:16\nTranslation: {translation}\nQuote: \"{quote}\"\nPlatform: Reels\n"
            f"Script:\n{body}\nCaption: A verse to sit with.\nHashtags: #faith #scripture\n"
            "\n## Sources / Assumptions\n- KJV text copied from the approved source.\n")


class ScriptureTests(unittest.TestCase):
    def pad(self):
        return " ".join(["Pause and breathe before you read it again slowly."] * 3)

    def test_good_script_passes_with_unverified_warning(self):
        r = scripture_check.check(scripture(extra=self.pad()))
        self.assertTrue(r["pass"], r["fails"])
        self.assertTrue(any("UNVERIFIED" in w for w in r["warns"]))

    def test_quote_not_in_script_fails(self):
        text = scripture(extra=self.pad()).replace(f'Here is what it says: "{JOHN}".', "Here is what it says.")
        r = scripture_check.check(text)
        self.assertFalse(r["pass"])
        self.assertTrue(any("does not appear in the Script" in f for f in r["fails"]))

    def test_unlisted_translation_fails(self):
        r = scripture_check.check(scripture(translation="NIV", extra=self.pad()))
        self.assertFalse(r["pass"])
        self.assertTrue(any("not listed" in f for f in r["fails"]))

    def test_outcome_promise_outside_quotes_fails_but_verse_wording_is_ignored(self):
        r = scripture_check.check(scripture(extra=self.pad() + " God will make you rich if you trust him."))
        self.assertFalse(r["pass"])
        self.assertTrue(any("outcome promise" in f for f in r["fails"]))

    def test_too_short_and_long_hook_fail(self):
        r = scripture_check.check(scripture(hook=" ".join(["word"] * 20)))
        self.assertTrue(any("hook is" in f for f in r["fails"]))
        r2 = scripture_check.check(scripture())          # no padding: well under 15 seconds? check length rule fires or passes
        self.assertEqual(r2["seconds"], round(r2["words"] / 2.5))

    def test_local_verse_text_verifies_and_catches_altered_quote(self):
        tmp = Path(tempfile.mkdtemp())
        try:
            (tmp / "config/scripture").mkdir(parents=True)
            shutil.copy(REPO / "config/scripture.md", tmp / "config/scripture.md")
            (tmp / "config/scripture/KJV.txt").write_text(
                f"John 3:16\t{JOHN}, that whosoever believeth in him should not perish.\n")
            ok = scripture_check.check(scripture(extra=self.pad()), tmp)
            self.assertTrue(ok["pass"], ok["fails"])
            self.assertFalse(any("UNVERIFIED" in w for w in ok["warns"]))
            bad = scripture_check.check(scripture(quote=JOHN.replace("loved", "liked"), extra=self.pad()), tmp)
            self.assertFalse(bad["pass"])
            self.assertTrue(any("not a contiguous part" in f for f in bad["fails"]))
        finally:
            shutil.rmtree(tmp)


EN = ("Hi Dana,\n\nThank you for the time today. We will send a written proposal by October 9 for your accountant. "
      "Our AI Audit is $1,500 and takes 7 business days. Book 20 minutes at https://cal.example.com/x or call 856-254-6000.\n\n"
      "Chief of Staff\nOffice of Joaquin Garcia, CEO\n\n"
      "The AI Agency Blueprint | 80 River St., Hoboken, NJ 07030 | 856-254-6000 | www.theaiagencyblueprint.com\n")
ES = ("Hola Dana,\n\nGracias por su tiempo de hoy. Le enviaremos una propuesta por escrito antes del 9 de octubre para que la revise con su contador. "
      "Nuestra auditoría de IA cuesta $1,500 y toma 7 días hábiles. Reserve 20 minutos en https://cal.example.com/x o llame al 856-254-6000.\n\n"
      "Chief of Staff\nOffice of Joaquin Garcia, CEO\n\n"
      "The AI Agency Blueprint | 80 River St., Hoboken, NJ 07030 | 856-254-6000 | www.theaiagencyblueprint.com\n")


class TranslationTests(unittest.TestCase):
    def test_faithful_translation_passes(self):
        r = translation_check.check(EN, ES)
        self.assertTrue(r["pass"], r["fails"])

    def test_changed_price_fails(self):
        r = translation_check.check(EN, ES.replace("$1,500", "$1.500"))
        self.assertFalse(r["pass"])
        self.assertTrue(any("money" in f for f in r["fails"]))

    def test_dropped_number_and_link_fail(self):
        r = translation_check.check(EN, ES.replace("7 días", "siete días").replace("https://cal.example.com/x", "mi enlace"))
        joined = " ".join(r["fails"])
        self.assertIn("number '7'", joined)
        self.assertIn("url", joined)

    def test_altered_footer_fails(self):
        r = translation_check.check(EN, ES.replace("80 River St., Hoboken", "80 Calle del Río, Hoboken"))
        self.assertTrue(any("footer" in f for f in r["fails"]))

    def test_untranslated_text_fails(self):
        r = translation_check.check(EN, EN)
        self.assertFalse(r["pass"])

    def test_added_claim_number_fails(self):
        r = translation_check.check(EN, ES.replace("Gracias por", "Reducimos 50% el trabajo. Gracias por"))
        self.assertFalse(r["pass"])

    def test_json_structure_must_match(self):
        src = json.dumps({"subject": "Next steps", "emails": ["Thank you for the time today and the chance to talk about your office and your team."]})
        tr_ok = json.dumps({"subject": "Próximos pasos", "emails": ["Gracias por su tiempo de hoy y por la oportunidad de hablar de su oficina y de su equipo."]})
        tr_bad = json.dumps({"asunto": "Próximos pasos", "emails": ["Gracias por su tiempo de hoy y por la oportunidad de hablar de su oficina y de su equipo."]})
        self.assertTrue(translation_check.check(src, tr_ok)["pass"], translation_check.check(src, tr_ok)["fails"])
        self.assertFalse(translation_check.check(src, tr_bad)["pass"])

    def test_unsupported_language_is_blocked(self):
        r = translation_check.check(EN, ES, lang="pt")
        self.assertFalse(r["pass"])


def release(extra="", quote_tag="[QUOTE PENDING approval: Joaquin Garcia]", n=330):
    filler = " ".join(["The agreement covers one workflow and was signed on the stated date."] * (n // 11))
    return (f"# A New Jersey Municipality Signs an AI Customer Response Agreement\n\n"
            f"[CITY, NJ, DATE] - The AI Agency Blueprint today announced a signed agreement. {filler} {extra}\n\n"
            f"\"We built this to take repetitive work off the front desk,\" said Joaquin Garcia, CEO. {quote_tag}\n\n"
            "## About The AI Agency Blueprint\nWe install AI-powered operations systems.\n\n"
            "## Media contact\n[PENDING: name, Joaquin]\n\n## Sources / Assumptions\n- Signed agreement dated [DATE].\n")


class PressTests(unittest.TestCase):
    def test_good_release_passes(self):
        r = press_check.check(release(), ["Reyes"])
        self.assertTrue(r["pass"], r["fails"])

    def test_untagged_quote_fails(self):
        r = press_check.check(release(quote_tag=""), ["Reyes"])
        self.assertTrue(any("approval tag" in f for f in r["fails"]))

    def test_superlative_stat_and_client_name_fail(self):
        r = press_check.check(release(extra="It is the first and best system, saving 40% and $50,000 for Reyes Properties."), ["Reyes"])
        joined = " ".join(r["fails"])
        for needle in ("superlative", "percentage or dollar", "unapproved client name"):
            self.assertIn(needle, joined)

    def test_source_tag_exempts_a_documented_first_and_approval_allows_name(self):
        r = press_check.check(release(extra="It is the first agreement of its kind for the town [source: signed agreement, page 1]."), ["Reyes"])
        self.assertFalse(any("superlative" in f for f in r["fails"]), r["fails"])
        r2 = press_check.check(release(extra="Client: Reyes Properties."), ["Reyes"], ["Reyes"])
        self.assertTrue(r2["pass"], r2["fails"])

    def test_length_and_missing_sections(self):
        self.assertEqual(press_check.MIN_WORDS, 200)
        r = press_check.check("# Short\n\n[CITY, NJ, DATE] - Tiny.\n")
        joined = " ".join(r["fails"])
        self.assertIn("words", joined)
        self.assertIn("boilerplate", joined)
        self.assertIn("media contact", joined)

    def test_a_short_factual_release_under_300_words_passes(self):
        r = press_check.check(release(n=220), ["Reyes"])
        self.assertTrue(200 <= r["words"] < 300, r["words"])
        self.assertTrue(r["pass"], r["fails"])

    def test_honorific_fails_and_internal_note_warns(self):
        r = press_check.check(release(extra="Mr. Garcia leads the company."), ["Reyes"])
        self.assertTrue(any("honorific" in f for f in r["fails"]), r["fails"])
        r2 = press_check.check(release(extra="The municipality has not approved being named."), ["Reyes"])
        self.assertTrue(any("internal compliance language" in w for w in r2["warns"]), r2["warns"])
        self.assertTrue(r2["pass"], r2["fails"])           # a warning, not a failure

    def test_off_phase_service_fails(self):
        r = press_check.check(release(extra="The company also offers document intake."), ["Reyes"])
        self.assertTrue(any("off-phase" in f for f in r["fails"]))


def module(minutes=4, spoken_words=520, extra_task="", extra=""):
    spoken = " ".join(["Open the review queue and read the drafted reply before anything is sent."] * (spoken_words // 14))
    return (f"Module: 3\nTitle: Reviewing auto-drafted responses\nTarget minutes: {minutes}\n"
            f"Task: Decide whether to send, edit or escalate a drafted response.{extra_task}\nAudience: Staff\n"
            f"On-screen steps:\n1. Open the review queue.\n2. Read the draft.\nSpoken:\n{spoken} {extra}\n"
            "What to do next:\nWatch module 4.\n\n## Sources / Assumptions\n- Generic template.\n")


class CourseTests(unittest.TestCase):
    def test_good_module_passes(self):
        r = course_check.check(module(), ["Reyes"])
        self.assertTrue(r["pass"], r["fails"])

    def test_too_long_and_too_short_fail(self):
        self.assertFalse(course_check.check(module(minutes=8, spoken_words=1400))["pass"])
        self.assertFalse(course_check.check(module(minutes=3, spoken_words=150))["pass"])

    def test_target_outside_range_fails(self):
        r = course_check.check(module(minutes=12))
        self.assertTrue(any("outside 3-8" in f for f in r["fails"]))

    def test_more_than_one_task_fails(self):
        r = course_check.check(module(extra_task="; also update the dashboard"))
        self.assertTrue(any("more than one task" in f for f in r["fails"]))

    def test_naming_out_of_scope_items_in_a_does_not_do_clause_is_allowed(self):
        ok = course_check.check(module(extra="The system does not handle inspections or scheduling."), ["Reyes"])
        self.assertTrue(ok["pass"], ok["fails"])
        bad = course_check.check(module(extra="The system handles scheduling for your office."), ["Reyes"])
        self.assertTrue(any("off-phase" in f for f in bad["fails"]), bad["fails"])
        sneaky = course_check.check(module(extra="It handles inspections and it does not guess."), ["Reyes"])
        self.assertTrue(any("off-phase" in f for f in sneaky["fails"]), sneaky["fails"])

    def test_claims_offphase_and_client_name_fail(self):
        r = course_check.check(module(extra="This cuts workload 60% and handles inspection scheduling for Reyes."), ["Reyes"])
        joined = " ".join(r["fails"])
        for needle in ("percentage", "off-phase", "unapproved client name"):
            self.assertIn(needle, joined)

    def test_missing_sections_fail(self):
        r = course_check.check("Module: 1\nTitle: X\nTarget minutes: 4\nTask: Do one thing.\n")
        self.assertTrue(any("On-screen steps" in f for f in r["fails"]))


if __name__ == "__main__":
    unittest.main()
