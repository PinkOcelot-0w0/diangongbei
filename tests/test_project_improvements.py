from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import pandas as pd
from openpyxl import Workbook

import q1_solution
import q2_solution
import q4_solution


class ProjectImprovementTests(unittest.TestCase):
    """覆盖论文第七节指出的工程改进点。"""

    def test_q1_reads_transition_probabilities_from_workbook(self) -> None:
        """REQ-001：问题一转移概率应来自附件 1，而不是源码硬编码。"""
        with tempfile.TemporaryDirectory() as temp_dir:
            workbook_path = Path(temp_dir) / "附件1：小区基础数据.xlsx"
            workbook = Workbook()
            population_sheet = workbook.active
            population_sheet.title = "人口与老人结构"
            population_sheet.append(["人口与老人结构"])
            population_sheet.append(["小区编号", "总人口", "60+老人数", "自理老人", "半失能老人", "失能老人", "人均月收入(元)"])
            for index in range(10):
                population_sheet.append([chr(ord("A") + index), 1000, 200, 140, 40, 20, 3000])

            transition_sheet = workbook.create_sheet("转移概率")
            transition_sheet.append(["转移概率", None])
            transition_sheet.append(["转移类型", "年度转移概率参考区间"])
            transition_sheet.append(["自理 → 半失能", 0.123])
            transition_sheet.append(["半失能 → 失能", 0.234])
            workbook.save(workbook_path)

            original_base_dir = q1_solution.BASE_DIR
            try:
                q1_solution.BASE_DIR = Path(temp_dir)
                _, self_to_semi, semi_to_disabled = q1_solution.load_community_data()
            finally:
                q1_solution.BASE_DIR = original_base_dir

        self.assertEqual(self_to_semi, 0.123)
        self.assertEqual(semi_to_disabled, 0.234)

    def test_distance_matrix_is_symmetric(self) -> None:
        """REQ-002：附件 4 的小区距离矩阵应为 10x10 对称矩阵。"""
        distance_matrix = q2_solution.load_distance_matrix()

        self.assertEqual(distance_matrix.shape, (10, 10))
        self.assertEqual(list(distance_matrix.index), list(distance_matrix.columns))
        pd.testing.assert_frame_equal(distance_matrix, distance_matrix.T)

    def test_q2_default_candidate_selection_uses_all_sites(self) -> None:
        """REQ-002：问题二默认不截断候选站点，完整枚举 10 个小区。"""
        distance_matrix = q2_solution.load_distance_matrix()
        communities, _, _ = q1_solution.load_community_data()

        candidate_sites = q2_solution.select_candidate_sites(distance_matrix, communities)

        self.assertEqual(len(candidate_sites), len(distance_matrix.index))
        self.assertEqual(set(candidate_sites), set(distance_matrix.index))

    def test_q2_capacity_check_marks_overloaded_stations(self) -> None:
        """REQ-002：软容量模型应额外输出容量核查和过载标记。"""
        station_rows = pd.DataFrame(
            [
                {"站点": "A", "规模": "小型", "日容量": 1000, "利用率": 1.25},
                {"站点": "B", "规模": "中型", "日容量": 2000, "利用率": 0.75},
            ]
        )

        check = q2_solution.build_capacity_check(station_rows)

        self.assertEqual(check.loc[check["站点"] == "A", "是否过载"].iloc[0], "是")
        self.assertEqual(check.loc[check["站点"] == "B", "是否过载"].iloc[0], "否")
        self.assertEqual(check.loc[check["站点"] == "A", "估计日有效服务人次"].iloc[0], 1250.0)

    def test_q4_rejects_negative_profit_even_when_profit_rate_is_under_limit(self) -> None:
        """REQ-004：第四问统一定价方案必须同时满足利润率上限和利润非负。"""
        self.assertFalse(q4_solution.is_station_financially_feasible(annual_profit=-1.0, profit_rate=0.0))
        self.assertTrue(q4_solution.is_station_financially_feasible(annual_profit=0.0, profit_rate=0.0))
        self.assertFalse(q4_solution.is_station_financially_feasible(annual_profit=100.0, profit_rate=9.0))


if __name__ == "__main__":
    unittest.main()
