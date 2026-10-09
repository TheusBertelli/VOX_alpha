import unittest
from datetime import date

from main import clean_title, parse_date, parse_domain, parse_priority, parse_time


class VoxParserTests(unittest.TestCase):
    def test_tomorrow(self):
        self.assertEqual(parse_date("Me lembre de estudar amanhã", date(2026, 10, 9)), date(2026, 10, 10))

    def test_date_and_time(self):
        text = "Me lembre de entregar o trabalho dia 12/10 às 18h30"
        self.assertEqual(parse_date(text, date(2026, 10, 9)), date(2026, 10, 12))
        self.assertEqual(parse_time(text), "18:30")

    def test_domain_and_priority(self):
        text = "Urgente: lembrar da consulta médica amanhã às 9h"
        self.assertEqual(parse_domain(text), "saúde")
        self.assertEqual(parse_priority(text), "alta")
        self.assertEqual(parse_time(text), "09:00")

    def test_title_cleanup(self):
        self.assertEqual(clean_title("Me lembre de entregar o trabalho amanhã às 18h."), "entregar o trabalho")

    def test_urgent_medical_reminder_title(self):
        text = "Urgente: agendar consulta médica dia 12/10 às 09:30"
        self.assertEqual(clean_title(text), "consulta médica")
        self.assertEqual(parse_domain(text), "saúde")
        self.assertEqual(parse_priority(text), "alta")

    def test_relative_date_and_study_domain(self):
        text = "Me lembre de estudar para a prova amanhã às 19h"
        self.assertEqual(parse_date(text, date(2026, 10, 9)), date(2026, 10, 10))
        self.assertEqual(parse_time(text), "19:00")
        self.assertEqual(parse_domain(text), "estudos")
        self.assertEqual(clean_title(text), "estudar para a prova")


if __name__ == "__main__":
    unittest.main()
