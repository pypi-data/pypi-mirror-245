import os
import unittest

from looqbox import ObjectMapper
from looqbox.objects.response_parameters.condition.temporal_relation import TemporalRelation
from looqbox.utils.utils import title_with_date, load_json_from_path


class TestTitleWithDateFunction(unittest.TestCase):

    def setUp(self):
        self.current_dir = os.path.dirname(__file__)
        self.month_temporal_relation = ObjectMapper.map(
            load_json_from_path(os.path.join(os.path.dirname(__file__), "..", "..", "objects", "response_parameters", "tests",
                                             "resources", "month_temporal_relation.json")),
            TemporalRelation
        )

    def test_simple_date(self):
        result = title_with_date("Período", ["2022-01-01", "2022-01-01"], "pt-br")
        self.assertEqual(result, "Período dia 01/01/2022 (sab sem: 52/2022)")

    def test_date_interval(self):
        result = title_with_date("Período", ["2022-01-01", "2022-01-02"], "pt-br")
        self.assertEqual(result, "Período de 01/01/2022 a 02/01/2022")

    def test_simple_datetime(self):
        result = title_with_date("Período", ["2022-01-01 12:00:00", "2022-01-01 12:00:00"], "pt-br")
        self.assertEqual(result, "Período dia 01/01/2022 12:00:00 (sab sem: 52/2022)")

    def test_datetime_interval(self):
        result = title_with_date("Período", ["2022-01-01 12:00:00", "2022-01-02 13:00:00"], "pt-br")
        self.assertEqual(result, "Período de 01/01/2022 12:00:00 a 02/01/2022 13:00:00")
        
    def test_open_date_interval(self):
        result = title_with_date("Período", ["2022-01-01", None], "pt-br")
        self.assertEqual(result, "Período a partir de 01/01/2022")
        
    def test_open_datetime_interval(self):
        result = title_with_date("Período", ["2022-01-01 12:00:00", None], "pt-br")
        self.assertEqual(result, "Período a partir de 01/01/2022 12:00:00")
        
    def test_end_open_date_interval(self):
        result = title_with_date("Período", [None, "2022-01-01"], "pt-br")
        self.assertEqual(result, "Período até 01/01/2022")
        
    def test_end_open_datetime_interval(self):
        result = title_with_date("Período", [None, "2022-01-01 12:00:00"], "pt-br")
        self.assertEqual(result, "Período até 01/01/2022 12:00:00")

    def test_title_generator_for_temporal_relation(self):
        self.assertEqual(
            "Venda de 01/11/2023 00:00:00 a 30/11/2023 00:00:00",
            title_with_date("Venda", self.month_temporal_relation, "pt-br")
        )

if __name__ == '__main__':
    unittest.main()
