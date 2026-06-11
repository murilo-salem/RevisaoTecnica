#!/usr/bin/env python3
"""
Agente de Web Scraping de Patentes
===================================

Recebe uma string de busca, realiza scraping de patentes no Google Patents,
e utiliza Ollama gemma3:27b para avaliar e analisar os resultados.

Uso:
    python main.py --query "biodiesel production from waste oil"
    python main.py --query "solar cell efficiency" --max-results 15
    python main.py -q "machine learning drug discovery" -n 5 --model gemma3:27b
    python main.py -q "carbon dioxide thermal energy storage" --upgrade-benchmark --corpus-run-state output/smoke_whitespace_20260409/run_state_latest.json
"""

import argparse
import logging
import os
import sys

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import config
from logging_utils import configure_structured_logging, log_event
from pipeline.features import PipelineFeatures

logger = logging.getLogger("patent-agent")


def main():
    """Entry point principal."""
    parser = argparse.ArgumentParser(
        description="🔬 Agente de Web Scraping de Patentes — Busca e avalia patentes usando IA",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python main.py --query "biodiesel production from waste oil"
  python main.py -q "solar cell perovskite" --max-results 15
  python main.py -q "CRISPR gene therapy" -n 5 --model gemma3:27b
  python main.py -q "lithium battery recycling" --output-dir ./resultados
  python main.py -q "carbon dioxide thermal energy storage" --upgrade-benchmark --corpus-run-state output/smoke_whitespace_20260409/run_state_latest.json
        """,
    )

    parser.add_argument(
        "-q", "--query",
        type=str,
        required=True,
        help="String de busca para pesquisar patentes",
    )
    parser.add_argument(
        "-n", "--max-results",
        type=int,
        default=config.MAX_RESULTS,
        help=f"Número máximo de patentes a buscar (padrão: {config.MAX_RESULTS})",
    )
    parser.add_argument(
        "-m", "--model",
        type=str,
        default=config.OLLAMA_MODEL,
        help=f"Modelo Ollama para avaliação (padrão: {config.OLLAMA_MODEL})",
    )
    parser.add_argument(
        "-o", "--output-dir",
        type=str,
        default=config.OUTPUT_DIR,
        help=f"Diretório de saída dos relatórios (padrão: {config.OUTPUT_DIR})",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Ativa logs detalhados (modo debug)",
    )
    parser.add_argument(
        "--include-threshold",
        type=float,
        default=config.SCREEN_INCLUDE_THRESHOLD,
        help=f"Score mínimo para inclusão automática (padrão: {config.SCREEN_INCLUDE_THRESHOLD})",
    )
    parser.add_argument(
        "--review-threshold",
        type=float,
        default=config.SCREEN_REVIEW_THRESHOLD,
        help=f"Score mínimo para fila de revisão manual (padrão: {config.SCREEN_REVIEW_THRESHOLD})",
    )
    parser.add_argument(
        "--disable-evidence",
        action="store_true",
        help="Desliga a exigência de evidências textuais no LLM",
    )
    parser.add_argument(
        "--disable-clusters",
        action="store_true",
        help="Desliga a síntese temática por cluster",
    )
    parser.add_argument(
        "--disable-structural-roles",
        action="store_true",
        help="Desliga a extração de papéis técnicos estruturados",
    )
    parser.add_argument(
        "--disable-rerank",
        action="store_true",
        help="Desliga o segundo passe de triagem para casos limítrofes",
    )
    parser.add_argument(
        "--disable-prisma",
        action="store_true",
        help="Desliga os artefatos PRISMA-like",
    )
    parser.add_argument(
        "--disable-snapshot",
        action="store_true",
        help="Desliga o snapshot versionado da execução",
    )
    parser.add_argument(
        "--disable-comparative-analysis",
        action="store_true",
        help="Desliga a etapa de análise comparativa",
    )
    parser.add_argument(
        "--disable-whitespace-analysis",
        action="store_true",
        help="Desliga a etapa estruturada de whitespace",
    )
    parser.add_argument(
        "--disable-manual-review",
        action="store_true",
        help="Desliga a fila de revisão manual",
    )
    parser.add_argument(
        "--ablation",
        action="store_true",
        help="Executa o benchmark de ablation com variantes pré-definidas",
    )
    parser.add_argument(
        "--benchmark-file",
        type=str,
        default=os.path.join("benchmarks", "ablation_benchmark.json"),
        help="Arquivo JSON com casos fixos para o benchmark de ablation",
    )
    parser.add_argument(
        "--upgrade-benchmark",
        action="store_true",
        help="Compara o pipeline atual contra uma baseline sem as melhorias técnicas do dia",
    )
    parser.add_argument(
        "--corpus-run-state",
        type=str,
        default="",
        help="Run state JSON usado como corpus congelado para o benchmark de melhorias",
    )
    parser.add_argument(
        "--model-comparison-summary",
        type=str,
        default="",
        help="Resumo JSON opcional de comparação entre modelos para embutir recomendação no relatório",
    )

    args = parser.parse_args()

    configure_structured_logging(logging.DEBUG if args.verbose else logging.INFO)

    config.SCREEN_INCLUDE_THRESHOLD = args.include_threshold
    config.SCREEN_REVIEW_THRESHOLD = args.review_threshold
    features = PipelineFeatures(
        require_evidence=not args.disable_evidence,
        enable_thematic_clusters=not args.disable_clusters,
        enable_structural_roles=not args.disable_structural_roles,
        enable_screening_rerank=not args.disable_rerank,
        enable_prisma=not args.disable_prisma,
        enable_snapshot=not args.disable_snapshot,
        enable_comparative_analysis=not args.disable_comparative_analysis,
        enable_whitespace_analysis=not args.disable_whitespace_analysis,
        enable_manual_review_queue=not args.disable_manual_review,
    )

    from pipeline.orchestrator import print_banner, run_agent
    from pipeline.ablation import run_ablation_suite
    from pipeline.upgrade_benchmark import run_today_upgrade_benchmark

    print_banner()
    log_event(
        logger,
        logging.INFO,
        "cli_invocation",
        query=args.query,
        max_results=args.max_results,
        model=args.model,
        output_dir=args.output_dir,
        ablation=args.ablation,
        upgrade_benchmark=args.upgrade_benchmark,
        feature_flags=features.to_dict(),
    )
    if args.upgrade_benchmark:
        summary = run_today_upgrade_benchmark(
            query=args.query,
            max_results=args.max_results,
            model=args.model,
            output_dir=args.output_dir,
            corpus_run_state=args.corpus_run_state,
            model_comparison_summary=args.model_comparison_summary,
        )
        log_event(
            logger,
            logging.INFO,
            "upgrade_benchmark_completed",
            summary_paths=summary.get("summary_paths", {}),
            suite_root=summary.get("suite_root", ""),
        )
    elif args.ablation:
        summary = run_ablation_suite(
            query=args.query,
            max_results=args.max_results,
            model=args.model,
            output_dir=args.output_dir,
            benchmark_file=args.benchmark_file,
        )
        log_event(
            logger,
            logging.INFO,
            "ablation_completed",
            summary_paths=summary.get("summary_paths", {}),
            suite_root=summary.get("suite_root", ""),
        )
    else:
        run_agent(
            query=args.query,
            max_results=args.max_results,
            model=args.model,
            output_dir=args.output_dir,
            features=features,
        )


if __name__ == "__main__":
    main()
