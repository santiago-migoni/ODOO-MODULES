include ../ODOO/infra/make/common.mk

APP_NAME := Odoo Modules
ENV_DESC := Desarrollo (Terminal 2)

# ============================================================
#  AYUDA
# ============================================================
help: ## Muestra esta ayuda
	$(call unified_help)

# ============================================================
#  🛠️ DESARROLLO
# ============================================================

init: ## [DEV] Instala hooks de git y dependencias
	@echo "$(BLUE)Instalando pre-commit hooks...$(NC)"
	@pre-commit install
	@echo "$(GREEN)✓ Entorno listo$(NC)"

scaffold: ## [DEV] Crea un nuevo módulo base interactivo
	@read -p "Nombre técnico del módulo: " NAME; \
	if [ -z "$$NAME" ]; then exit 1; fi; \
	mkdir -p $$NAME/models $$NAME/views $$NAME/security $$NAME/data $$NAME/static/description; \
	touch $$NAME/__init__.py $$NAME/models/__init__.py; \
	printf "from . import models\n" > $$NAME/__init__.py; \
	printf "{'name': '$$NAME', 'version': '1.0', 'depends': ['base'], 'data': ['security/ir.model.access.csv', 'views/views.xml'], 'installable': True, 'license': 'LGPL-3'}" > $$NAME/__manifest__.py; \
	printf "id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink\n" > $$NAME/security/ir.model.access.csv; \
	printf "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<odoo>\n<data></data>\n</odoo>\n" > $$NAME/views/views.xml; \
	echo "$(GREEN)✓ Módulo $$NAME creado$(NC)"

branch: ## [DEV] Crea rama feature desde development
	@read -p "Nombre de la feature: " FEAT; \
	git checkout development && git pull origin development && git checkout -b feature/$$FEAT

commit: ## [DEV] Commit interactivo (Add + Commit)
	$(call shared_commit)

# ============================================================
#  🚀 DESPLIEGUE
# ============================================================

push: ## [DEPLOY] Push de la rama actual
	@BRANCH=$$(git rev-parse --abbrev-ref HEAD); \
	git push -u origin $$BRANCH

deploy: ## [DEPLOY] [MAC] Push (Dual) + Recargar código en el servidor
	$(call dual_push)
	@echo "$(BLUE)Actualizando servidor remoto...$(NC)"
	@BRANCH=$$(git rev-parse --abbrev-ref HEAD); \
	$(REMOTE_SSH) "cd $(REMOTE_DIR) && make deploy-dev TARGET_BRANCH=$$BRANCH"

update: ## [DEPLOY] [MAC] Push + Update módulo específico (ej: make update mod=dipl_ui)
	@if [ -z "$(mod)" ]; then exit 1; fi
	$(call dual_push)
	@echo "$(BLUE)Actualizando módulo $(mod) en el servidor...$(NC)"
	@BRANCH=$$(git rev-parse --abbrev-ref HEAD); \
	$(REMOTE_SSH) "cd $(REMOTE_DIR) && make update-dev TARGET_BRANCH=$$BRANCH mod=$(mod)"

pr: ## [DEPLOY] Abre la URL para crear PR
	@gh pr create --web || echo "$(YELLOW)Instala GitHub CLI (gh)$(NC)"

promote-dev: ## [DEPLOY] [MAC] Merge feature → development
	@if [ "$(IS_MAC)" != "1" ]; then echo "$(RED)Error: Este comando se dispara desde la Mac.$(NC)"; exit 1; fi
	@CURRENT=$$(git rev-parse --abbrev-ref HEAD); \
	git push origin $$CURRENT && git checkout development && git pull origin development && \
	git merge $$CURRENT --no-edit && git push origin development && git branch -d $$CURRENT

promote-stag: ## [DEPLOY] [MAC] Merge development → staging + deploy
	@if [ "$(IS_MAC)" != "1" ]; then echo "$(RED)Error: Este comando se dispara desde la Mac.$(NC)"; exit 1; fi
	@git checkout staging && git pull origin staging && git merge development --no-edit && git push origin staging
	$(call proxy_cmd,deploy-stag)

promote-prod: ## [DEPLOY] [MAC] Merge staging → main + deploy
	@if [ "$(IS_MAC)" != "1" ]; then echo "$(RED)Error: Este comando se dispara desde la Mac.$(NC)"; exit 1; fi
	@git checkout main && git pull origin main && git merge staging --no-edit && git push origin main
	$(call proxy_cmd,deploy-prod)

# ============================================================
#  📊 MONITORIZACIÓN
# ============================================================

ps: ## [MONITOR] Ver estado del servidor (via Infra)
	$(call proxy_cmd,ps)

stats: ## [MONITOR] Ver consumo del servidor (via Infra)
	$(call proxy_cmd,stats)

hardware: ## [MONITOR] Ver recursos del servidor (via Infra)
	$(call proxy_cmd,hardware)

logs: ## [MONITOR] Ver logs del servidor (via Infra)
	$(call proxy_cmd,logs)

ssh: ## [MONITOR] Conecta al servidor (via Infra)
	$(call proxy_cmd,ssh)

# ============================================================
#  📂 NAVEGACIÓN
# ============================================================

go-infra: ## [NAV] Ir al repositorio de infraestructura
	@echo "$(BLUE)Entrando a ODOO (Infra)... (Escribe 'exit' para volver)$(NC)"
	@cd ../ODOO && PROMPT="[ODOO-INFRA] % " zsh -i

# ============================================================
#  ⚙️  CALIDAD
# ============================================================

lint: ## [MAINT] Ejecuta flake8
	@flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics

format: ## [MAINT] Formatea con black
	@black . || echo "$(YELLOW)Instala black$(NC)"


