from datetime import datetime
import unittest


class AdoptionAcceptanceTests(unittest.TestCase):
    def test_current_and_historical_queries_follow_a_correction(self):
        from memory_os import MemorySystem, make_event
        from memory_os.schema import UTC

        system = MemorySystem()
        jan = datetime(2026, 1, 1, tzinfo=UTC)
        mar = datetime(2026, 3, 1, tzinfo=UTC)
        system.observe(make_event(
            jan, "s1", "user", "message", "I prefer concise summaries.",
            entity_hints=("summary_style",),
        ))
        system.observe(make_event(
            mar, "s2", "user", "correction", "I prefer detailed summaries.",
            entity_hints=("summary_style",),
        ))

        self.assertIn("concise summaries", system.ask("what summary format?", jan).render())
        self.assertIn("detailed summaries", system.ask("what summary format?", mar).render())
