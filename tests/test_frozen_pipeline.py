import json
import os
import tempfile
import unittest

from pipeline.ablation import run_ablation_suite
from pipeline.features import PipelineFeatures
from pipeline.frozen_benchmark import build_frozen_components, build_frozen_scrapers_from_run_state
from pipeline.orchestrator import run_agent
from pipeline.upgrade_benchmark import run_today_upgrade_benchmark


class FrozenPipelineTests(unittest.TestCase):
    def test_run_agent_with_frozen_components(self):
        fixture_path = os.path.join("benchmarks", "frozen_pipeline_fixture.json")
        scrapers, evaluator_factory = build_frozen_components(fixture_path)

        with tempfile.TemporaryDirectory() as tmpdir:
            state = run_agent(
                query="carbon dioxide thermal energy storage",
                max_results=5,
                model="frozen-model",
                output_dir=tmpdir,
                features=PipelineFeatures(),
                scrapers=scrapers,
                evaluator_factory=evaluator_factory,
            )

            self.assertEqual(state.status, "completed")
            self.assertTrue(state.llm_available)
            self.assertEqual(len(state.patents), 2)
            self.assertEqual(state.coverage_metrics["included"], 2)
            self.assertEqual(state.coverage_metrics["manual_review_required"], 0)
            self.assertTrue(state.comparative_analysis.startswith("## Panorama Geral"))
            self.assertEqual(state.whitespace_analysis.get("status"), "ok")
            self.assertIn("screening", state.llm_telemetry["operations"])
            self.assertTrue(os.path.exists(state.output_paths["markdown"]))
            self.assertTrue(os.path.exists(state.output_paths["json"]))
            self.assertTrue(os.path.exists(state.output_paths["whitespace_json"]))

            with open(state.output_paths["json"], "r", encoding="utf-8") as f:
                payload = json.load(f)
            self.assertEqual(payload["metadata"]["total_patents"], 2)
            self.assertEqual(payload["metadata"]["run_state"]["status"], "completed")
            self.assertEqual(payload["whitespace_analysis"]["status"], "ok")

    def test_run_ablation_suite_with_frozen_fixture(self):
        benchmark_file = os.path.join("benchmarks", "frozen_ablation_benchmark.json")
        with tempfile.TemporaryDirectory() as tmpdir:
            summary = run_ablation_suite(
                query="carbon dioxide thermal energy storage",
                max_results=5,
                model="frozen-model",
                output_dir=tmpdir,
                benchmark_file=benchmark_file,
            )

            self.assertTrue(summary["results"])
            self.assertTrue(os.path.exists(summary["suite_root"]))

    def test_build_frozen_scrapers_from_run_state(self):
        fixture_path = os.path.join("benchmarks", "frozen_pipeline_fixture.json")
        with open(fixture_path, "r", encoding="utf-8") as f:
            fixture = json.load(f)

        patents = []
        for source_name, items in fixture.get("sources", {}).items():
            for item in items:
                payload = dict(item)
                payload.setdefault("source", source_name)
                patents.append(payload)

        with tempfile.TemporaryDirectory() as tmpdir:
            run_state_path = os.path.join(tmpdir, "run_state_fixture.json")
            with open(run_state_path, "w", encoding="utf-8") as f:
                json.dump({"patents": patents}, f, ensure_ascii=False, indent=2)

            scrapers = build_frozen_scrapers_from_run_state(run_state_path)
            total_patents = sum(len(scraper.search("query", max_results=10)) for scraper in scrapers)

            self.assertTrue(scrapers)
            self.assertEqual(total_patents, len(patents))

    def test_run_today_upgrade_benchmark_with_frozen_components(self):
        fixture_path = os.path.join("benchmarks", "frozen_pipeline_fixture.json")
        scrapers, evaluator_factory = build_frozen_components(fixture_path)

        with tempfile.TemporaryDirectory() as tmpdir:
            summary = run_today_upgrade_benchmark(
                query="carbon dioxide thermal energy storage",
                max_results=5,
                model="frozen-model",
                output_dir=tmpdir,
                scrapers=scrapers,
                evaluator_factory=evaluator_factory,
            )

            self.assertTrue(os.path.exists(summary["summary_paths"]["json"]))
            self.assertTrue(os.path.exists(summary["summary_paths"]["markdown"]))
            result_map = {
                item["variant"]["name"]: item["summary"]
                for item in summary["results"]
            }
            self.assertEqual(result_map["pre_today_baseline"]["structural_summary"]["fill_ratio"], 0.0)
            self.assertEqual(result_map["today_updates"]["whitespace_status"], "ok")
            self.assertGreaterEqual(summary["delta"]["whitespace_candidates_delta"], 0)


if __name__ == "__main__":
    unittest.main()
