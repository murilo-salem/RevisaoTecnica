import json
import io
import logging
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import requests

from analysis_utils import COMPARATIVE_ANALYSIS_FALLBACK
from models.patent import Patent, PatentEvaluation
from evaluator.llm_evaluator import OllamaEvaluator
from logging_utils import StructuredLogFormatter, log_event
from pipeline.features import PipelineFeatures
from pipeline.memory import MemorySidecar
from pipeline.orchestrator import _dedupe_patents, _prisma_stage_artifact
from pipeline.router import ThemeRouter
from pipeline.state import RunState
from report.generator import ReportGenerator
from scraper.google_patents import GooglePatentsScraper
from scraper.patentscope import PatentscopeScraper


FIXTURES_DIR = Path(__file__).parent / "fixtures"


class FakeResponse:
    def __init__(self, text: str = "", status_code: int = 200, json_data=None, url: str = "http://example.com"):
        self.text = text
        self.status_code = status_code
        self._json_data = json_data
        self.url = url

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.exceptions.HTTPError(f"HTTP {self.status_code}")

    def json(self):
        if self._json_data is not None:
            return self._json_data
        raise ValueError("Sem payload JSON")


class ArchitectureContractTests(unittest.TestCase):
    def test_structured_log_formatter_emits_json_payload(self):
        stream = io.StringIO()
        handler = logging.StreamHandler(stream)
        handler.setFormatter(StructuredLogFormatter())
        test_logger = logging.getLogger("tests.structured")
        test_logger.handlers = [handler]
        test_logger.setLevel(logging.INFO)
        test_logger.propagate = False

        log_event(
            test_logger,
            logging.INFO,
            "sample_event",
            query="thermal storage",
            max_results=5,
        )

        payload = json.loads(stream.getvalue().strip())
        self.assertEqual(payload["event"], "sample_event")
        self.assertEqual(payload["query"], "thermal storage")
        self.assertEqual(payload["max_results"], 5)
        self.assertEqual(payload["level"], "INFO")

    def test_pipeline_features_contract(self):
        features = PipelineFeatures()
        payload = features.to_dict()
        self.assertTrue(payload["require_evidence"])
        self.assertIn("enable_prisma", payload)
        self.assertIn("enable_manual_review_queue", payload)
        self.assertIn("enable_structural_roles", payload)
        self.assertIn("enable_screening_rerank", payload)
        self.assertIn("enable_whitespace_analysis", payload)

    def test_memory_sidecar_slots_and_journal(self):
        memory = MemorySidecar(run_id="run-1", max_items_per_slot=2)
        memory.append("setup", "boot", "Inicialização")
        memory.set_slot("router", {"patent_id": "A"})
        memory.set_slot("router", {"patent_id": "B"})
        memory.set_slot("router", {"patent_id": "C"})

        payload = memory.to_dict()
        self.assertEqual(len(payload["journal"]), 1)
        self.assertEqual(len(payload["slots"]["router"]), 2)
        self.assertEqual(payload["slots"]["router"][-1]["patent_id"], "C")

    def test_theme_router_routes_by_signal(self):
        router = ThemeRouter()
        patent = Patent(
            title="CO2 cycle configuration with ejector",
            abstract="A transcritical CO2 cycle with ejector and economizer.",
            patent_id="P1",
        )
        evaluation = PatentEvaluation(
            patent_id="P1",
            screening_decision="include",
            screening_score=8.5,
            confidence=0.9,
            evidence_snippets=["transcritical CO2 cycle with ejector"],
        )
        route = router.route(patent, evaluation)
        self.assertIn(route.route, {"deep_extraction", "thematic_synthesis"})
        self.assertTrue(route.reason)

    def test_theme_router_routes_llm_errors_to_manual_review(self):
        router = ThemeRouter()
        patent = Patent(title="Patent with backend issue", patent_id="P-ERR")
        evaluation = PatentEvaluation(
            patent_id="P-ERR",
            screening_decision="review",
            llm_error="timeout",
        )
        route = router.route(patent, evaluation)
        self.assertEqual(route.route, ThemeRouter.ROUTE_MANUAL_REVIEW)

    def test_run_state_serializes_memory_and_context(self):
        state = RunState(
            query="thermal storage",
            max_results=5,
            model="gemma3:4b",
            output_dir="output",
            writing_context={"top_patents": []},
            memory_sidecar={"run_id": "run-1"},
            memory_journal=[{"stage": "setup"}],
        )
        payload = state.to_dict()
        self.assertIn("writing_context", payload)
        self.assertIn("memory_sidecar", payload)
        self.assertIn("memory_journal", payload)
        self.assertIn("whitespace_analysis", payload)

    def test_draft_gate_blocks_empty_reports(self):
        generator = ReportGenerator(output_dir="output")
        draft_status = generator._draft_status([], [], "")
        self.assertEqual(draft_status["status"], "blocked")
        self.assertTrue(draft_status["warnings"])

    def test_draft_gate_allows_substantive_reports(self):
        generator = ReportGenerator(output_dir="output")
        evaluation = PatentEvaluation(
            patent_id="P2",
            screening_decision="include",
            summary="Resumo técnico útil",
            evidence_snippets=["trecho"],
        )
        draft_status = generator._draft_status(
            [Patent(title="Example", patent_id="P2")],
            [evaluation],
            "",
        )
        self.assertEqual(draft_status["status"], "ready")

    def test_draft_gate_blocks_fallback_only_comparative_analysis(self):
        generator = ReportGenerator(output_dir="output")
        draft_status = generator._draft_status([], [], COMPARATIVE_ANALYSIS_FALLBACK)
        self.assertEqual(draft_status["status"], "blocked")
        self.assertTrue(draft_status["warnings"])

    def test_llm_cache_loads_from_disk(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            cache_path = os.path.join(tmpdir, "gemma3_4b.json")
            with open(cache_path, "w", encoding="utf-8") as f:
                json.dump({"abc": "cached-response"}, f)

            evaluator = OllamaEvaluator(model="gemma3:4b", cache_dir=tmpdir)
            stats = evaluator.cache_stats()
            self.assertEqual(stats["entries"], 1)
            self.assertEqual(stats["hits"], 0)
            self.assertEqual(stats["misses"], 0)

    def test_check_connection_requires_exact_model_match(self):
        tags_response = Mock()
        tags_response.raise_for_status.return_value = None
        tags_response.json.return_value = {"models": [{"name": "gemma3:4b"}]}

        with patch("evaluator.llm_evaluator.requests.get", return_value=tags_response):
            evaluator = OllamaEvaluator(model="gemma3:27b", cache_dir="output")
            with patch.object(evaluator, "_probe_model_generation", return_value=True):
                self.assertFalse(evaluator.check_connection())

    def test_check_connection_accepts_compatible_model_alias(self):
        tags_response = Mock()
        tags_response.raise_for_status.return_value = None
        tags_response.json.return_value = {"models": [{"name": "gemma3:27b-it-qat"}]}

        with patch("evaluator.llm_evaluator.requests.get", return_value=tags_response):
            evaluator = OllamaEvaluator(model="gemma3:27b", cache_dir="output")
            with patch.object(evaluator, "_probe_model_generation", return_value=True):
                self.assertTrue(evaluator.check_connection())
        self.assertEqual(evaluator.model, "gemma3:27b-it-qat")
        self.assertTrue(evaluator.cache_path.endswith("gemma3_27b-it-qat.json"))

    def test_screen_patent_llm_failure_becomes_review(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            evaluator = OllamaEvaluator(model="gemma3:4b", cache_dir=tmpdir)
            patent = Patent(
                record_id="rec_1",
                patent_id="P1",
                title="Fallback patent",
                abstract="Useful fallback evidence.",
            )

            with patch(
                "evaluator.llm_evaluator.requests.post",
                side_effect=requests.exceptions.ConnectionError("offline"),
            ):
                evaluation = evaluator.screen_patent(patent, "thermal storage")

            self.assertEqual(evaluation.record_id, "rec_1")
            self.assertEqual(evaluation.screening_decision, "review")
            self.assertTrue(evaluation.manual_review_required)
            self.assertTrue(evaluation.llm_error)
            self.assertTrue(evaluation.evidence_snippets)

    def test_screen_patent_extracts_structural_roles(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            evaluator = OllamaEvaluator(model="gemma3:4b", cache_dir=tmpdir)
            patent = Patent(
                record_id="rec_roles",
                patent_id="P-ROLES",
                title="Supercritical CO2 thermal storage architecture",
                abstract="A dedicated thermal storage system using supercritical CO2.",
            )

            with patch.object(
                evaluator,
                "_call_ollama",
                return_value=json.dumps({
                    "screening_score": 8.4,
                    "decision": "include",
                    "screening_reason": "Arquitetura dedicada.",
                    "technical_domain": "CO2 Storage",
                    "thematic_cluster": "CO2 Cycle Configurations",
                    "co2_role": "stored_thermodynamic_medium",
                    "storage_role": "explicit_thermal_storage",
                    "system_boundary": "dedicated_storage_system",
                    "cycle_type": "supercritical_or_transcritical_co2",
                    "heat_source_sink": "general_thermal_management",
                    "claim_focus": "system_architecture",
                    "evidence_snippets": ["supercritical CO2", "thermal storage system"],
                    "confidence": 0.88,
                }),
            ):
                evaluation = evaluator.screen_patent(
                    patent,
                    "carbon dioxide thermal energy storage",
                )

            self.assertEqual(evaluation.co2_role, "stored_thermodynamic_medium")
            self.assertEqual(evaluation.storage_role, "explicit_thermal_storage")
            self.assertEqual(evaluation.system_boundary, "dedicated_storage_system")
            self.assertEqual(evaluation.cycle_type, "supercritical_or_transcritical_co2")
            self.assertEqual(evaluation.claim_focus, "system_architecture")

    def test_screen_patent_applies_rerank_for_review_zone(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            evaluator = OllamaEvaluator(model="gemma3:4b", cache_dir=tmpdir)
            patent = Patent(
                record_id="rec_rerank",
                patent_id="P-RERANK",
                title="Carbon dioxide thermal transfer loop with storage bypass",
                abstract="A carbon dioxide loop with ambiguous thermal storage behavior.",
            )

            with patch.object(
                evaluator,
                "_call_ollama",
                side_effect=[
                    json.dumps({
                        "screening_score": 6.2,
                        "decision": "review",
                        "screening_reason": "Caso limítrofe.",
                        "technical_domain": "Thermal Systems",
                        "co2_role": "working_fluid",
                        "storage_role": "implicit_or_support_storage",
                        "system_boundary": "cycle_or_transfer_subsystem",
                        "cycle_type": "power_or_work_cycle",
                        "heat_source_sink": "general_thermal_management",
                        "claim_focus": "cycle_integration",
                        "evidence_snippets": ["thermal transfer loop"],
                        "confidence": 0.61,
                    }),
                    json.dumps({
                        "screening_score": 5.4,
                        "decision": "review",
                        "screening_reason": "Rerank confirmou fronteira técnica.",
                        "technical_domain": "Thermal Systems",
                        "co2_role": "working_fluid",
                        "storage_role": "implicit_or_support_storage",
                        "system_boundary": "cycle_or_transfer_subsystem",
                        "cycle_type": "power_or_work_cycle",
                        "heat_source_sink": "general_thermal_management",
                        "claim_focus": "cycle_integration",
                        "exclusion_category": "boundary_case",
                        "evidence_snippets": ["thermal transfer loop"],
                        "confidence": 0.78,
                    }),
                ],
            ):
                evaluation = evaluator.screen_patent(
                    patent,
                    "carbon dioxide thermal energy storage",
                )

            self.assertTrue(evaluation.rerank_applied)
            self.assertEqual(evaluation.rerank_reason, "reranked:decision_confirmed")
            self.assertEqual(evaluation.screening_decision, "review")
            self.assertEqual(evaluation.exclusion_category, "boundary_case")

    def test_screening_guardrails_exclude_generic_overlap_without_distinctive_match(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            evaluator = OllamaEvaluator(model="gemma3:4b", cache_dir=tmpdir)
            patent = Patent(
                record_id="rec_generic",
                patent_id="P-GEN",
                title="Calcination system with thermal energy storage system",
                abstract="A thermal energy storage system for high temperature industrial heat.",
            )

            with patch.object(
                evaluator,
                "_call_ollama",
                return_value=json.dumps({
                    "screening_score": 9.0,
                    "decision": "include",
                    "screening_reason": "Compartilha o domínio geral de armazenamento térmico.",
                    "technical_domain": "Armazenamento de Energia Térmica",
                    "thematic_cluster": "Thermal Transfer Mechanisms",
                    "evidence_snippets": ["thermal energy storage system"],
                    "confidence": 0.95,
                }),
            ):
                evaluation = evaluator.screen_patent(
                    patent,
                    "carbon dioxide thermal energy storage",
                )

            self.assertEqual(evaluation.screening_decision, "exclude")
            self.assertLessEqual(evaluation.screening_score, 3.5)
            self.assertIn("Guardrail de alinhamento", evaluation.screening_reason)

    def test_evaluator_degrades_globally_after_repeated_failures(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            evaluator = OllamaEvaluator(model="gemma3:4b", cache_dir=tmpdir)
            with patch(
                "evaluator.llm_evaluator.requests.post",
                side_effect=requests.exceptions.ConnectionError("offline"),
            ):
                for _ in range(3):
                    evaluator._call_ollama("prompt", operation="screening")

            self.assertTrue(evaluator.is_degraded())
            telemetry = evaluator.telemetry_stats()
            self.assertEqual(telemetry["total_failures"], 3)
            self.assertTrue(telemetry["degraded"])

    def test_text_call_retries_without_invalid_format_and_counts_single_miss(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            evaluator = OllamaEvaluator(model="gemma3:4b", cache_dir=tmpdir)

            http_error = requests.exceptions.HTTPError("500 Server Error")
            http_error.response = Mock(status_code=500)
            first_response = Mock()
            first_response.raise_for_status.side_effect = http_error

            second_response = Mock()
            second_response.raise_for_status.return_value = None
            second_response.json.return_value = {"response": "comparativo ok"}

            with patch(
                "evaluator.llm_evaluator.requests.post",
                side_effect=[first_response, second_response],
            ) as mock_post:
                response = evaluator._call_ollama(
                    "prompt comparativo",
                    response_format="text",
                    num_predict=2048,
                )

            self.assertEqual(response, "comparativo ok")
            self.assertEqual(mock_post.call_count, 2)
            first_payload = mock_post.call_args_list[0].kwargs["json"]
            second_payload = mock_post.call_args_list[1].kwargs["json"]
            self.assertNotIn("format", first_payload)
            self.assertNotIn("format", second_payload)
            self.assertEqual(first_payload["options"]["num_predict"], 2048)
            self.assertEqual(second_payload["options"]["num_predict"], 1024)

            stats = evaluator.cache_stats()
            self.assertEqual(stats["misses"], 1)
            self.assertEqual(stats["entries"], 1)

            with patch("evaluator.llm_evaluator.requests.post") as mock_post:
                cached = evaluator._call_ollama(
                    "prompt comparativo",
                    response_format="text",
                    num_predict=2048,
                )

            self.assertEqual(cached, "comparativo ok")
            self.assertEqual(mock_post.call_count, 0)
            self.assertEqual(evaluator.cache_stats()["hits"], 1)

    def test_relevance_guardrails_open_more_scale_among_included_items(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            evaluator = OllamaEvaluator(model="gemma3:4b", cache_dir=tmpdir)
            focused_patent = Patent(
                patent_id="P-FOCUS",
                title="Supercritical carbon dioxide energy storage system",
                abstract="A thermal energy storage system using supercritical carbon dioxide with heat exchangers.",
            )
            broader_patent = Patent(
                patent_id="P-BROAD",
                title="Method for thermal energy transmission using water and carbon dioxide",
                abstract="A system that transfers thermal energy using water and carbon dioxide and stores excess heat underground.",
            )
            screening = PatentEvaluation(
                screening_decision="include",
                screening_score=9.2,
                confidence=0.95,
            )
            focused_eval = PatentEvaluation(relevance_score=9.5, confidence=0.95)
            broader_eval = PatentEvaluation(relevance_score=9.5, confidence=0.95)

            evaluator._apply_relevance_guardrails(
                focused_eval,
                screening,
                focused_patent,
                "carbon dioxide thermal energy storage",
            )
            evaluator._apply_relevance_guardrails(
                broader_eval,
                screening,
                broader_patent,
                "carbon dioxide thermal energy storage",
            )

            self.assertGreater(focused_eval.relevance_score, broader_eval.relevance_score)

    def test_comparative_analysis_appends_id_support_map(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            evaluator = OllamaEvaluator(model="gemma3:4b", cache_dir=tmpdir)
            patents = [
                Patent(
                    patent_id="P1",
                    title="Supercritical carbon dioxide energy storage system",
                    abstract="Uses carbon dioxide for thermal energy storage.",
                ),
                Patent(
                    patent_id="P2",
                    title="Method for thermal energy transmission using water and carbon dioxide",
                    abstract="Transfers and stores thermal energy with carbon dioxide.",
                ),
            ]
            evaluations = [
                PatentEvaluation(
                    patent_id="P1",
                    screening_decision="include",
                    relevance_score=9.4,
                    thematic_cluster="CO2 Cycle Configurations",
                    technical_domain="Thermodynamics",
                    summary="Resumo 1",
                    evidence_snippets=["evidence 1"],
                ),
                PatentEvaluation(
                    patent_id="P2",
                    screening_decision="include",
                    relevance_score=8.8,
                    thematic_cluster="Thermal Transfer Mechanisms",
                    technical_domain="Thermal Systems",
                    summary="Resumo 2",
                    evidence_snippets=["evidence 2"],
                ),
            ]

            with patch.object(
                evaluator,
                "_call_ollama",
                return_value="## Panorama Geral\n\nTexto sem citações explícitas.",
            ):
                analysis = evaluator.generate_comparative_analysis(
                    patents,
                    evaluations,
                    "carbon dioxide thermal energy storage",
                )

            self.assertIn("### 6. Mapa de Evidências por ID", analysis)
            self.assertIn("### 5. Ranking Final", analysis)
            self.assertIn("[IDs: P1", analysis)
            self.assertIn("[IDs: P2", analysis)

    def test_comparative_analysis_rewrites_duplicate_ranking_with_deterministic_order(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            evaluator = OllamaEvaluator(model="gemma3:4b", cache_dir=tmpdir)
            patents = [
                Patent(
                    record_id="rec_1",
                    patent_id="P1",
                    title="Supercritical carbon dioxide energy storage system",
                    abstract="Uses supercritical carbon dioxide with heat exchangers and a thermal storage tank.",
                ),
                Patent(
                    record_id="rec_2",
                    patent_id="P2",
                    title="Method for thermal energy transmission using water and carbon dioxide",
                    abstract="Transfers heat with carbon dioxide and stores excess energy underground.",
                ),
            ]
            evaluations = [
                PatentEvaluation(
                    record_id="rec_1",
                    patent_id="P1",
                    screening_decision="include",
                    relevance_score=9.6,
                    summary="Resumo 1",
                    evidence_snippets=["supercritical carbon dioxide energy storage"],
                ),
                PatentEvaluation(
                    record_id="rec_2",
                    patent_id="P2",
                    screening_decision="include",
                    relevance_score=8.1,
                    summary="Resumo 2",
                    evidence_snippets=["underground thermal energy storage system"],
                ),
            ]

            with patch.object(
                evaluator,
                "_call_ollama",
                return_value=(
                    "## Panorama Geral\n\n"
                    "Texto do modelo.\n\n"
                    "### 5. Ranking Final\n\n"
                    "1. **P1** [IDs: P1]\n"
                    "2. **P1** [IDs: P1]\n"
                ),
            ):
                analysis = evaluator.generate_comparative_analysis(
                    patents,
                    evaluations,
                    "carbon dioxide thermal energy storage",
                )

            ranking_section = analysis.split("### 5. Ranking Final", 1)[1].split(
                "### 6. Mapa de Evidências por ID",
                1,
            )[0]
            self.assertIn("1. **P1**", ranking_section)
            self.assertIn("2. **P2**", ranking_section)
            self.assertNotIn("2. **P1**", ranking_section)

    def test_comparative_analysis_scopes_underground_claim_to_supported_subset(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            evaluator = OllamaEvaluator(model="gemma3:4b", cache_dir=tmpdir)
            patents = [
                Patent(
                    record_id="rec_core",
                    patent_id="P-CORE",
                    title="Supercritical carbon dioxide energy storage system",
                    abstract="Stores supercritical carbon dioxide in a thermal storage tank with heat exchangers.",
                ),
                Patent(
                    record_id="rec_ug",
                    patent_id="P-UG",
                    title="Method for thermal energy transmission using water and carbon dioxide",
                    abstract="An underground thermal energy storage system stores excess energy while carbon dioxide works as the fluid.",
                ),
            ]
            evaluations = [
                PatentEvaluation(
                    record_id="rec_core",
                    patent_id="P-CORE",
                    screening_decision="include",
                    relevance_score=9.4,
                    summary="Resumo core",
                    evidence_snippets=["supercritical carbon dioxide energy storage"],
                ),
                PatentEvaluation(
                    record_id="rec_ug",
                    patent_id="P-UG",
                    screening_decision="include",
                    relevance_score=8.0,
                    summary="Resumo underground",
                    evidence_snippets=["underground thermal energy storage system"],
                ),
            ]

            with patch.object(
                evaluator,
                "_call_ollama",
                return_value=(
                    "## Panorama Geral\n\n"
                    "As duas patentes usam armazenamento subterrâneo como traço comum [IDs: P-CORE, P-UG]."
                ),
            ):
                analysis = evaluator.generate_comparative_analysis(
                    patents,
                    evaluations,
                    "carbon dioxide thermal energy storage",
                )

            panorama_section = analysis.split("### 1. Panorama Geral", 1)[1].split(
                "### 6. Mapa de Evidências por ID",
                1,
            )[0]
            self.assertIn("aparece apenas em P-UG", panorama_section)
            self.assertNotIn("aparece apenas em P-CORE, P-UG", panorama_section)

    def test_comparative_analysis_uses_review_pairs_for_whitespace(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            evaluator = OllamaEvaluator(model="gemma3:4b", cache_dir=tmpdir)
            patents = [
                Patent(
                    record_id="rec_core",
                    patent_id="P-CORE",
                    title="Supercritical carbon dioxide thermal energy storage vessel",
                    abstract="Stores supercritical carbon dioxide in a thermal energy storage vessel.",
                ),
                Patent(
                    record_id="rec_review",
                    patent_id="P-REV",
                    title="Carbon dioxide thermal transfer loop with storage bypass",
                    abstract="Carbon dioxide thermal transfer loop with ambiguous storage role.",
                ),
            ]
            evaluations = [
                PatentEvaluation(
                    record_id="rec_core",
                    patent_id="P-CORE",
                    screening_decision="include",
                    relevance_score=9.2,
                    screening_reason="Core architecture.",
                    summary="Resumo core",
                    evidence_snippets=["Stores supercritical carbon dioxide."],
                ),
                PatentEvaluation(
                    record_id="rec_review",
                    patent_id="P-REV",
                    screening_decision="review",
                    relevance_score=6.4,
                    screening_score=6.8,
                    screening_reason="Boundary case with partial storage signal.",
                    summary="Resumo review",
                    evidence_snippets=["thermal transfer loop with storage bypass"],
                ),
            ]

            with patch.object(
                evaluator,
                "_call_ollama",
                return_value="## Tendências Identificadas\n\n- Tendência de integração ciclo-armazenamento [IDs: P-CORE, P-REV]",
            ):
                analysis = evaluator.generate_comparative_analysis(
                    patents,
                    evaluations,
                    "carbon dioxide thermal energy storage",
                )

            self.assertIn("### 3. Whitespaces e Oportunidades", analysis)
            self.assertIn("P-REV", analysis)
            self.assertNotEqual(analysis, COMPARATIVE_ANALYSIS_FALLBACK)
            self.assertLess(
                analysis.index("### 3. Whitespaces e Oportunidades"),
                analysis.index("### 4. Recomendações"),
            )

    def test_comparative_analysis_includes_adjacent_exclude_for_whitespace_boundary(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            evaluator = OllamaEvaluator(model="gemma3:4b", cache_dir=tmpdir)
            patents = [
                Patent(
                    record_id="rec_core",
                    patent_id="P-CORE",
                    title="Supercritical carbon dioxide thermal energy storage system",
                    abstract="Stores supercritical carbon dioxide in a thermal energy storage vessel.",
                ),
                Patent(
                    record_id="rec_adj",
                    patent_id="P-ADJ",
                    title="Underground supercritical carbon dioxide transfer system",
                    abstract="Uses supercritical carbon dioxide in underground thermal transfer with boundary storage behavior.",
                ),
            ]
            evaluations = [
                PatentEvaluation(
                    record_id="rec_core",
                    patent_id="P-CORE",
                    screening_decision="include",
                    relevance_score=9.1,
                    screening_reason="Core architecture.",
                    summary="Resumo core",
                    evidence_snippets=["Stores supercritical carbon dioxide."],
                ),
                PatentEvaluation(
                    record_id="rec_adj",
                    patent_id="P-ADJ",
                    screening_decision="exclude",
                    screening_score=6.1,
                    relevance_score=3.5,
                    screening_reason="Adjacente; usa CO2 em transferencia subterranea.",
                    summary="Resumo adjacente",
                    evidence_snippets=["underground thermal transfer with supercritical carbon dioxide"],
                ),
            ]

            with patch.object(
                evaluator,
                "_call_ollama",
                return_value="## Tendências Identificadas\n\n- Tendência de integração supercrítica [IDs: P-CORE, P-ADJ]",
            ):
                analysis = evaluator.generate_comparative_analysis(
                    patents,
                    evaluations,
                    "carbon dioxide thermal energy storage",
                )

            self.assertIn("### 3. Whitespaces e Oportunidades", analysis)
            self.assertIn("P-ADJ", analysis)
            self.assertIn("adjacencia", analysis.lower())

    def test_prisma_artifact_requires_substantive_comparative_analysis(self):
        state = RunState(
            query="thermal storage",
            max_results=5,
            model="gemma3:4b",
            output_dir="output",
            comparative_analysis=COMPARATIVE_ANALYSIS_FALLBACK,
        )
        artifact = _prisma_stage_artifact(state, {"full_extractions": 2})
        self.assertFalse(
            artifact["flow"]["synthesis"]["comparative_analysis_generated"]
        )

        state.comparative_analysis = "## Panorama Geral\n\nTexto comparativo."
        artifact = _prisma_stage_artifact(state, {"full_extractions": 2})
        self.assertTrue(
            artifact["flow"]["synthesis"]["comparative_analysis_generated"]
        )

    def test_dedupe_assigns_record_ids_and_uses_content_identity(self):
        patents, stats = _dedupe_patents([
            Patent(
                source="Google Patents",
                abstract="Heat exchanger with packed bed storage.",
            ),
            Patent(
                source="Patentscope",
                abstract="Heat exchanger with packed bed storage.",
            ),
        ])

        self.assertEqual(len(patents), 1)
        self.assertTrue(patents[0].record_id.startswith("rec_"))
        self.assertEqual(stats["records_with_content_identity"], 1)

    def test_dedupe_merges_family_variants_conservatively(self):
        patents, stats = _dedupe_patents([
            Patent(
                patent_id="US1234567A",
                title="Thermal storage assembly for industrial energy shifting",
                assignee="Example Energy Inc.",
                inventors=["Jane Doe"],
                publication_date="2024-01-11",
            ),
            Patent(
                patent_id="WO2024000001",
                title="Thermal storage assembly for industrial energy shifting",
                assignee="Example Energy Inc.",
                inventors=["Jane Doe"],
                publication_date="2024-04-09",
            ),
        ])

        self.assertEqual(len(patents), 1)
        self.assertTrue(patents[0].family_id.startswith("family:"))
        self.assertEqual(stats["family_duplicates_removed"], 1)

    def test_report_maps_evaluations_by_record_id(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            generator = ReportGenerator(output_dir=tmpdir)
            patents = [
                Patent(record_id="rec_a", patent_id="", title="Patent A", url="http://example.com/a"),
                Patent(record_id="rec_b", patent_id="", title="Patent B", url="http://example.com/b"),
            ]
            evaluations = [
                PatentEvaluation(record_id="rec_a", patent_id="", summary="Resumo A", screening_decision="include"),
                PatentEvaluation(record_id="rec_b", patent_id="", summary="Resumo B", screening_decision="include"),
            ]

            _, json_path = generator.generate_report(
                "thermal storage",
                patents,
                evaluations,
                run_metadata={},
            )

            with open(json_path, "r", encoding="utf-8") as f:
                payload = json.load(f)

            self.assertEqual(payload["results"][0]["evaluation"]["record_id"], "rec_a")
            self.assertEqual(payload["results"][1]["evaluation"]["record_id"], "rec_b")

    def test_report_renders_structured_manual_review_queue(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            generator = ReportGenerator(output_dir=tmpdir)
            patent = Patent(record_id="rec_q1", patent_id="P-Q1", title="Queue patent", url="http://example.com/q1")
            evaluation = PatentEvaluation(record_id="rec_q1", patent_id="P-Q1", screening_decision="review")
            md_path, _ = generator.generate_report(
                "thermal storage",
                [patent],
                [evaluation],
                run_metadata={
                    "manual_review_queue": [
                        {
                            "record_id": "rec_q1",
                            "patent_id": "P-Q1",
                            "route": "manual_review",
                            "reason": "Falha do LLM",
                            "llm_error": "timeout",
                        }
                    ]
                },
            )

            with open(md_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertIn("rec_q1", content)
            self.assertIn("erro_llm=timeout", content)

    def test_google_patents_detail_parser_with_fixture(self):
        html = (FIXTURES_DIR / "google_patent_detail.html").read_text(encoding="utf-8")
        scraper = GooglePatentsScraper()
        with patch.object(scraper, "_make_request", return_value=FakeResponse(text=html)):
            patent = scraper.get_patent_details("https://patents.google.com/patent/US1234567A/en")

        self.assertEqual(patent.patent_id, "US1234567A")
        self.assertIn("Thermal storage", patent.title)
        self.assertEqual(patent.assignee, "Example Energy Inc.")
        self.assertIn("Jane Doe", patent.inventors)
        self.assertEqual(patent.publication_date, "2024-01-11")

    def test_patentscope_detail_parser_with_fixture(self):
        html = (FIXTURES_DIR / "patentscope_detail.html").read_text(encoding="utf-8")
        scraper = PatentscopeScraper()
        with patch.object(scraper, "_make_request", return_value=FakeResponse(text=html)):
            patent = scraper.get_patent_details(
                "https://patentscope.wipo.int/search/en/detail.jsf?docId=WO2024000001"
            )

        self.assertEqual(patent.patent_id, "WO2024000001")
        self.assertIn("Supercritical CO2", patent.title)
        self.assertIn("Alice Smith", patent.inventors)
        self.assertEqual(patent.assignee, "Future Storage LLC")
        self.assertEqual(patent.filing_date, "2023-03-21")

    def test_google_patents_detects_block_signal(self):
        scraper = GooglePatentsScraper()
        fake_response = FakeResponse(
            text="<html>verify you are human</html>",
            url="https://html.duckduckgo.com/html/",
        )
        with patch.object(scraper.session, "get", return_value=fake_response):
            scraper._make_request("https://html.duckduckgo.com/html/")

        diagnostics = scraper.get_diagnostics()
        self.assertTrue(any(item["kind"] == "blocked_or_captcha" for item in diagnostics))

    def test_block_signal_ignores_meta_robots_noise(self):
        scraper = GooglePatentsScraper()
        html = "<html><head><meta name='robots' content='index,follow'></head><body>Patent page</body></html>"
        self.assertFalse(scraper._contains_block_signal(html))

    def test_report_contains_stage_metrics_and_cache_stats(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            generator = ReportGenerator(output_dir=tmpdir)
            patent = Patent(
                record_id="rec_p3",
                title="Thermal storage patent",
                patent_id="P3",
                abstract="A thermal storage system.",
                url="http://example.com",
            )
            evaluation = PatentEvaluation(
                record_id="rec_p3",
                patent_id="P3",
                screening_decision="include",
                screening_score=8.0,
                relevance_score=8.5,
                summary="Resumo útil",
                evidence_snippets=["A thermal storage system."],
            )
            run_metadata = {
                "model": "gemma3:4b",
                "status": "completed",
                "total_duration_seconds": 12.5,
                "llm_available": True,
                "feature_flags": {"require_evidence": True},
                "config_snapshot": {"pipeline_version": "1.1", "thresholds": {"include": 7, "review": 4.5}},
                "snapshot_hash": "abc123",
                "writing_context": {"top_patents": [], "thematic_clusters": {"total_clusters": 0}, "route_summary": {}, "slot_policy": {"slots": ["writer"]}},
                "stage_metrics": [
                    {"stage": "search", "status": "ok", "duration_seconds": 1.2, "items_processed": 10, "detail": "busca"},
                ],
                "llm_cache_stats": {"hits": 3, "misses": 1, "entries": 1},
                "llm_telemetry": {"degraded": False, "total_failures": 0, "consecutive_failures": 0, "recent_errors": [], "operations": {"screening": {"calls": 1, "successes": 1, "failures": 0, "retries": 0, "cache_hits": 0, "degraded_skips": 0, "prompt_chars": 10, "response_chars": 20, "total_duration_seconds": 0.1, "average_duration_seconds": 0.1, "max_duration_seconds": 0.1}}},
                "scraper_diagnostics": {"GooglePatents": [{"kind": "blocked_or_captcha", "detail": "signal"}]},
                "protocol": {"version": "1.0", "sources": ["Google Patents"], "stages": ["search"], "thresholds": {"include_score": 7, "review_score": 4.5}},
                "coverage_metrics": {"raw_scraped": 1, "unique_patents": 1, "duplicates_removed": 0, "screened": 1, "included": 1, "review": 0, "excluded": 0, "full_extractions": 1, "missing_abstract": 0, "missing_id": 0, "records_with_content_identity": 0, "records_with_fallback_identity": 0, "family_duplicates_removed": 0, "llm_screening_failures": 0, "llm_total_failures": 0},
                "prisma_flow": {"flow": {"identification": {"raw_records": 1, "unique_records": 1, "duplicates_removed": 0}, "screening": {"screened": 1, "included": 1, "review": 0, "excluded": 0}, "eligibility": {"full_extractions": 1, "manual_review_required": 0, "manual_review_deferred": 0}, "coverage": {"missing_abstract": 0, "missing_id": 0}, "synthesis": {"analyzed_records": 1}}},
                "thematic_clusters": {"clusters": [{"cluster": "Thermal", "count": 1, "average_score": 8.5, "average_confidence": 0.8, "evidence_count": 1, "patent_ids": ["P3"]}], "total_clusters": 1},
                "whitespace_analysis": {"status": "ok", "corpus_summary": {"selected_patents": 1, "core": 1, "frontier": 0, "adjacent": 0}, "whitespace_candidates": [{"opportunity": "control_and_operability_claims", "rationale": "rationale", "core_ids": ["P3"], "frontier_ids": [], "adjacent_ids": []}]},
            }

            md_path, json_path = generator.generate_report(
                "thermal storage",
                [patent],
                [evaluation],
                comparative_analysis="Comparative analysis text",
                run_metadata=run_metadata,
            )

            with open(md_path, "r", encoding="utf-8") as f:
                md_content = f.read()
            with open(json_path, "r", encoding="utf-8") as f:
                json_content = json.load(f)

            self.assertIn("## ⏱️ Métricas por Etapa", md_content)
            self.assertIn("Cache LLM", md_content)
            self.assertIn("## 🧭 Matriz de Whitespaces", md_content)
            self.assertEqual(json_content["metadata"]["draft_status"]["status"], "ready")
            self.assertEqual(json_content["metadata"]["llm_cache_stats"]["hits"], 3)
            self.assertEqual(json_content["metadata"]["stage_metrics"][0]["stage"], "search")
            self.assertEqual(json_content["whitespace_analysis"]["status"], "ok")

    def test_report_contains_structured_observability_metrics(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            generator = ReportGenerator(output_dir=tmpdir)
            patent = Patent(record_id="rec_obs", patent_id="P-OBS", title="Observed patent", url="http://example.com/obs")
            evaluation = PatentEvaluation(
                record_id="rec_obs",
                patent_id="P-OBS",
                screening_decision="include",
                analysis_route="deep_extraction",
                summary="Resumo observável",
            )
            md_path, json_path = generator.generate_report(
                "thermal storage",
                [patent],
                [evaluation],
                run_metadata={
                    "observability_metrics": {
                        "routes": {
                            "deep_extraction": {
                                "count": 1,
                                "include": 1,
                                "review": 0,
                                "exclude": 0,
                                "llm_errors": 0,
                            }
                        },
                        "sources": {
                            "GooglePatents": {
                                "raw_results": 3,
                                "duration_seconds": 1.23,
                                "diagnostic_counts": {"discovery_empty": 1},
                            }
                        },
                        "failures": {
                            "run_errors": 1,
                            "records_with_llm_error": 0,
                            "llm_total_failures": 2,
                            "llm_by_operation": {
                                "screening": {"failures": 1, "retries": 2, "degraded_skips": 0}
                            },
                            "scraper_diagnostics_by_kind": {"discovery_empty": 1},
                        },
                    }
                },
            )

            with open(md_path, "r", encoding="utf-8") as f:
                md_content = f.read()
            with open(json_path, "r", encoding="utf-8") as f:
                json_content = json.load(f)

            self.assertIn("## 🔎 Observabilidade Estruturada", md_content)
            self.assertIn("deep_extraction", md_content)
            self.assertIn("GooglePatents", md_content)
            self.assertEqual(
                json_content["metadata"]["observability_metrics"]["failures"]["llm_total_failures"],
                2,
            )


if __name__ == "__main__":
    unittest.main()
