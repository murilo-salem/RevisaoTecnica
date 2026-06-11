#!/usr/bin/env bash
set -euo pipefail

API_URL="http://localhost:8000/health"
HEALTH_RETRIES=30
HEALTH_INTERVAL=5  # segundos entre tentativas

# --------------------------------------------------------------------------- #
# Helpers                                                                       #
# --------------------------------------------------------------------------- #

log() { echo "[$(date '+%H:%M:%S')] $*"; }

die() { echo "[ERRO] $*" >&2; exit 1; }

health_check() {
    local i
    for i in $(seq 1 "$HEALTH_RETRIES"); do
        local response
        response=$(curl -sf "$API_URL" 2>/dev/null) && {
            local status ollama
            status=$(echo "$response" | grep -o '"status":"[^"]*"' | cut -d'"' -f4)
            ollama=$(echo "$response" | grep -o '"ollama":[a-z]*' | cut -d':' -f2)
            log "API UP — status=$status ollama=$ollama"
            return 0
        }
        log "Aguardando API... ($i/$HEALTH_RETRIES)"
        sleep "$HEALTH_INTERVAL"
    done
    return 1
}

# --------------------------------------------------------------------------- #
# Etapas                                                                        #
# --------------------------------------------------------------------------- #

step_build() {
    log "=== BUILD ==="
    docker compose build
    log "Build concluído."
}

step_up() {
    log "=== UP ==="
    docker compose up -d
    log "Serviços iniciados. Aguardando API ficar disponível..."
    health_check || die "API não respondeu após $((HEALTH_RETRIES * HEALTH_INTERVAL))s. Verifique: docker compose logs app"
}

step_status() {
    log "=== STATUS ==="
    docker compose ps
    echo ""
    log "Resposta do /health:"
    curl -sf "$API_URL" | python3 -m json.tool || log "API não acessível."
}

step_down() {
    log "=== DOWN ==="
    docker compose down
    log "Serviços parados e containers removidos."
}

step_clean() {
    log "=== CLEAN ==="
    docker compose down --rmi local --volumes --remove-orphans
    log "Imagens locais, volumes anônimos e orphans removidos."
}

# --------------------------------------------------------------------------- #
# Execução                                                                      #
# --------------------------------------------------------------------------- #

usage() {
    echo "Uso: $0 [build|up|status|down|clean|all]"
    echo ""
    echo "  build   — constrói as imagens Docker"
    echo "  up      — sobe os containers e verifica saúde da API"
    echo "  status  — exibe containers ativos e resposta do /health"
    echo "  down    — para e remove os containers"
    echo "  clean   — down + remove imagens locais e volumes anônimos"
    echo "  all     — build → up → status → down → clean"
    exit 1
}

CMD="${1:-all}"

case "$CMD" in
    build)  step_build ;;
    up)     step_up ;;
    status) step_status ;;
    down)   step_down ;;
    clean)  step_clean ;;
    all)
        step_build
        step_up
        step_status
        step_down
        step_clean
        log "=== CONCLUÍDO ==="
        ;;
    *) usage ;;
esac
