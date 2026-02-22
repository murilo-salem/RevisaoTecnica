#!/usr/bin/env python3
"""
Agente de Web Scraping de Patentes
===================================

Recebe uma string de busca, realiza scraping de patentes no Google Patents,
e utiliza Ollama gemma3:4b para avaliar e analisar os resultados.

Uso:
    python main.py --query "biodiesel production from waste oil"
    python main.py --query "solar cell efficiency" --max-results 15
    python main.py -q "machine learning drug discovery" -n 5 --model gemma3:4b
"""

import argparse
import logging
import os
import sys
import time

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import config

# Configura logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("patent-agent")


def print_banner():
    """Imprime banner do agente."""
    banner = """
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   🔬  AGENTE DE WEB SCRAPING DE PATENTES  🔬                    ║
║                                                                  ║
║   Busca, extrai e avalia patentes usando IA (Ollama)             ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
"""
    print(banner)


def print_progress(step: str, current: int = 0, total: int = 0):
    """Imprime progresso formatado."""
    if total > 0:
        bar_len = 30
        filled = int(bar_len * current / total)
        bar = "█" * filled + "░" * (bar_len - filled)
        pct = current / total * 100
        print(f"\r  [{bar}] {pct:.0f}% — {step}", end="", flush=True)
        if current == total:
            print()  # Nova linha ao completar
    else:
        print(f"  ⏳ {step}...")


def run_agent(query: str, max_results: int, model: str, output_dir: str):
    """Executa o fluxo completo do agente."""
    from scraper.google_patents import GooglePatentsScraper
    from scraper.patentscope import PatentscopeScraper
    from evaluator.llm_evaluator import OllamaEvaluator
    from report.generator import ReportGenerator

    start_time = time.time()

    # --- Etapa 1: Verificação do Ollama ---
    print("\n" + "=" * 60)
    print("  📡 ETAPA 1: Verificando conexão com Ollama")
    print("=" * 60)

    evaluator = OllamaEvaluator(model=model)

    if not evaluator.check_connection():
        print(f"\n  ⚠️  Modelo '{model}' não disponível no Ollama.")
        print(f"  Execute: ollama pull {model}")
        print(f"  Continuando sem avaliação por LLM...\n")
        use_llm = False
    else:
        print(f"  ✅ Ollama conectado — modelo: {model}")
        use_llm = True

    # --- Etapa 2: Scraping ---
    print("\n" + "=" * 60)
    print("  🔍 ETAPA 2: Buscando patentes")
    print("=" * 60)
    print(f"  Query: \"{query}\"")
    print(f"  Máximo de resultados: {max_results}")
    print()

    scrapers = [
        GooglePatentsScraper(),
        PatentscopeScraper(),
    ]

    patents = []
    for scraper in scrapers:
        source_name = scraper.__class__.__name__.replace("Scraper", "")
        print_progress(f"Iniciando scraping no {source_name}")
        try:
            results = scraper.search(query, max_results=max_results)
            patents.extend(results)
            print(f"    → {len(results)} patentes encontradas no {source_name}")
        except Exception as e:
            logger.error(f"Erro no scraper {source_name}: {e}")

    if not patents:
        print("\n  ❌ Nenhuma patente encontrada para a busca.")
        print("  Tente termos diferentes ou mais genéricos.")
        return

    print(f"\n  ✅ {len(patents)} patente(s) encontrada(s)!\n")

    # Lista patentes encontradas
    for i, patent in enumerate(patents, 1):
        print(f"  {i}. [{patent.patent_id}] {patent.title[:80]}")
        if patent.assignee:
            print(f"     Titular: {patent.assignee}")
        print()

    # --- Etapa 3: Avaliação com LLM ---
    evaluations = []
    if use_llm:
        print("=" * 60)
        print("  🤖 ETAPA 3: Avaliando patentes com IA")
        print("=" * 60)
        print(f"  Modelo: {model}")
        print()

        for i, patent in enumerate(patents, 1):
            print_progress(
                f"Avaliando: {patent.patent_id} — {patent.title[:40]}...",
                i, len(patents)
            )
            evaluation = evaluator.evaluate_patent(patent, query)
            evaluations.append(evaluation)

            if evaluation.relevance_score > 0:
                print(
                    f"    → Score: {evaluation.relevance_score:.1f}/10 | "
                    f"Inovação: {evaluation.innovation_level}"
                )

        print(f"\n  ✅ Avaliação concluída para {len(evaluations)} patente(s)!")
    else:
        print("\n  ⏭️  Etapa de avaliação pulada (Ollama não disponível)")
        from models.patent import PatentEvaluation
        evaluations = [
            PatentEvaluation(patent_id=p.patent_id) for p in patents
        ]

    # --- Etapa 4: Análise Comparativa ---
    comparative_analysis = ""
    if use_llm and len(patents) > 1:
        print("\n" + "=" * 60)
        print("  📊 ETAPA 4: Gerando análise comparativa")
        print("=" * 60)

        print_progress("Gerando análise comparativa com IA")
        comparative_analysis = evaluator.generate_comparative_analysis(
            patents, evaluations, query
        )
        print("  ✅ Análise comparativa gerada!")

    # --- Etapa 5: Geração de Relatório ---
    print("\n" + "=" * 60)
    print("  📝 ETAPA 5: Gerando relatórios")
    print("=" * 60)

    reporter = ReportGenerator(output_dir=output_dir)
    md_path, json_path = reporter.generate_report(
        query, patents, evaluations, comparative_analysis
    )

    elapsed = time.time() - start_time

    print(f"\n  ✅ Relatórios gerados com sucesso!")
    print(f"  📄 Markdown: {os.path.abspath(md_path)}")
    print(f"  📋 JSON:     {os.path.abspath(json_path)}")

    # --- Resumo Final ---
    print("\n" + "=" * 60)
    print("  📋 RESUMO FINAL")
    print("=" * 60)
    print(f"  🔍 Query: \"{query}\"")
    print(f"  📊 Patentes encontradas: {len(patents)}")
    if use_llm:
        avg_score = (
            sum(e.relevance_score for e in evaluations) / len(evaluations)
            if evaluations else 0
        )
        print(f"  ⭐ Score médio de relevância: {avg_score:.1f}/10")

        top_patents = sorted(
            zip(patents, evaluations),
            key=lambda x: x[1].relevance_score,
            reverse=True,
        )[:3]

        if top_patents:
            print(f"\n  🏆 Top 3 Patentes mais relevantes:")
            for i, (p, e) in enumerate(top_patents, 1):
                print(
                    f"     {i}. [{e.relevance_score:.1f}] {p.title[:60]}"
                )

    print(f"\n  ⏱️  Tempo total: {elapsed:.1f}s")
    print(f"  ✅ Concluído!\n")


def main():
    """Entry point principal."""
    parser = argparse.ArgumentParser(
        description="🔬 Agente de Web Scraping de Patentes — Busca e avalia patentes usando IA",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python main.py --query "biodiesel production from waste oil"
  python main.py -q "solar cell perovskite" --max-results 15
  python main.py -q "CRISPR gene therapy" -n 5 --model gemma3:4b
  python main.py -q "lithium battery recycling" --output-dir ./resultados
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

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    print_banner()
    run_agent(
        query=args.query,
        max_results=args.max_results,
        model=args.model,
        output_dir=args.output_dir,
    )


if __name__ == "__main__":
    main()
