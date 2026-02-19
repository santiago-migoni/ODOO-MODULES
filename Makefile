.PHONY: help init scaffold branch commit push pr lint format

# ── Colors ───────────────────────────────────────────────────
BLUE   := \033[0;34m
GREEN  := \033[0;32m
YELLOW := \033[0;33m
RED    := \033[0;31m
NC     := \033[0m

# ============================================================
#  AYUDA
# ============================================================
help: ## Muestra esta ayuda
	@echo "$(BLUE)╔══════════════════════════════════════════════════╗$(NC)"
	@echo "$(BLUE)║      Odoo Modules — Desarrollo (Terminal 2)      ║$(NC)"
	@echo "$(BLUE)╚══════════════════════════════════════════════════╝$(NC)"
	@echo ""
	@echo "$(YELLOW)── 🛠️  HERRAMIENTAS DE DESARROLLO ──────────────────$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""

# ============================================================
#  🚀 NUEVO CÓDIGO
# ============================================================

init: ## Instala hooks de git y dependencias de desarrollo
	@echo "$(BLUE)Instalando pre-commit hooks...$(NC)"
	@pre-commit install
	@echo "$(GREEN)✓ Entorno listo para desarrollar$(NC)"

scaffold: ## Crea un nuevo módulo base interactivo
	@read -p "Nombre técnico del módulo (ej: dipl_ventas_extra): " NAME; \
	if [ -z "$$NAME" ]; then echo "$(RED)Error: nombre requerido$(NC)"; exit 1; fi; \
	if [ -d "$$NAME" ]; then echo "$(RED)Error: el directorio $$NAME ya existe$(NC)"; exit 1; fi; \
	echo "$(BLUE)Creando estructura para $$NAME...$(NC)"; \
	mkdir -p $$NAME/models $$NAME/views $$NAME/security $$NAME/data $$NAME/static/description; \
	touch $$NAME/__init__.py; \
	touch $$NAME/models/__init__.py; \
	printf "from . import models\n" > $$NAME/__init__.py; \
	printf "{ \n\
    'name': '$$NAME', \n\
    'version': '1.0', \n\
    'category': 'Custom', \n\
    'author': 'Dipleg', \n\
    'depends': ['base'], \n\
    'data': [ \n\
        'security/ir.model.access.csv', \n\
        'views/views.xml', \n\
    ], \n\
    'installable': True, \n\
    'application': False, \n\
    'license': 'LGPL-3', \n\
}" > $$NAME/__manifest__.py; \
	printf "id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink\n" > $$NAME/security/ir.model.access.csv; \
	printf "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<odoo>\n    <data>\n        <!-- Add your views here -->\n    </data>\n</odoo>\n" > $$NAME/views/views.xml; \
	echo "$(GREEN)✓ Módulo $$NAME creado exitosamente$(NC)"

# ============================================================
#  🌿 GIT FLOW (Simplificado)
# ============================================================

branch: ## Crea una nueva rama feature desde development
	@read -p "Nombre de la feature (ej: nvo-reporte): " FEAT; \
	if [ -z "$$FEAT" ]; then echo "$(RED)Error: nombre requerido$(NC)"; exit 1; fi; \
	echo "$(BLUE)Sincronizando development...$(NC)"; \
	git checkout development && git pull origin development; \
	echo "$(BLUE)Creando rama feature/$$FEAT...$(NC)"; \
	git checkout -b feature/$$FEAT; \
	echo "$(GREEN)✓ Estás en feature/$$FEAT$(NC)"

commit: ## Commit interactivo (Add + Commit)
	@status=$$(git status --porcelain); \
	if [ -z "$$status" ]; then \
		echo "$(YELLOW)No hay cambios para commitear.$(NC)"; \
		exit 0; \
	fi; \
	git add .; \
	read -p "Tipo (feat, fix, docs, style, refactor, test, chore): " TYPE; \
	read -p "Ámbito (opcional, ej: ventas): " SCOPE; \
	read -p "Descripción (imperativo, minúsculas): " DESC; \
	if [ -n "$$SCOPE" ]; then \
		MSG="$$TYPE($$SCOPE): $$DESC"; \
	else \
		MSG="$$TYPE: $$DESC"; \
	fi; \
	echo "$(BLUE)Commiteando: $$MSG$(NC)"; \
	git commit -m "$$MSG"; \
	echo "$(GREEN)✓ Commit realizado$(NC)"

push: ## Push de la rama actual a origin
	@BRANCH=$$(git rev-parse --abbrev-ref HEAD); \
	echo "$(BLUE)Subiendo $$BRANCH a origin...$(NC)"; \
	git push -u origin $$BRANCH; \
	echo "$(GREEN)✓ Cambios subidos$(NC)"

pr: ## Abre la URL para crear PR en GitHub (si gh instalado)
	@if command -v gh > /dev/null 2>&1; then \
		gh pr create --web; \
	else \
		echo "$(YELLOW)GitHub CLI (gh) no instalado. Abre GitHub manualmente.$(NC)"; \
	fi

promote-dev: ## Promueve feature actual → development (Merge + Push + Delete feature)
	@CURRENT=$$(git rev-parse --abbrev-ref HEAD); \
	if [[ ! $$CURRENT =~ ^feature/ ]]; then \
		echo "$(RED)❌ Solo desde una rama feature/ (estás en $$CURRENT)$(NC)"; exit 1; \
	fi; \
	if [ -n "$$(git status --porcelain)" ]; then \
		echo "$(RED)❌ Hay cambios sin commitear$(NC)"; exit 1; \
	fi; \
	echo "$(BLUE)Mergeando $$CURRENT → development...$(NC)"; \
	git push origin $$CURRENT && \
	git checkout development && \
	git pull origin development && \
	git merge $$CURRENT --no-edit && \
	git push origin development && \
	git branch -d $$CURRENT && \
	echo "$(GREEN)✓ $$CURRENT mergeado a development$(NC)"

promote-stag: ## Promueve development → staging
	@echo "$(BLUE)Promocionando development → staging...$(NC)"
	@git checkout staging && \
	git pull origin staging && \
	git merge development --no-edit && \
	git push origin staging
	@echo "$(GREEN)✓ Código en staging. Ve a ODOO y ejecuta: make deploy-stag$(NC)"

promote-prod: ## Promueve staging → main
	@echo "$(YELLOW)⚠ Promocionando staging → main (PRODUCCIÓN)...$(NC)"
	@git checkout main && \
	git pull origin main && \
	git merge staging --no-edit && \
	git push origin main
	@echo "$(GREEN)✓ Código en main. Ve a ODOO y ejecuta: make deploy-prod$(NC)"

# ============================================================
#  🧹 CALIDAD DE CÓDIGO
# ============================================================

lint: ## Ejecuta flake8 en el directorio actual
	@echo "$(BLUE)Analizando código Python...$(NC)"
	@flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	@flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
	@echo "$(GREEN)✓ Linting finalizado$(NC)"

format: ## Formatea código con black (si instalado)
	@if command -v black > /dev/null 2>&1; then \
		echo "$(BLUE)Formateando código...$(NC)"; \
		black .; \
		echo "$(GREEN)✓ Formato aplicado$(NC)"; \
	else \
		echo "$(YELLOW)Black no instalado. pip install black$(NC)"; \
	fi
