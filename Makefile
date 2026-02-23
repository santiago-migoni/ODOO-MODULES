include ../ODOO/infra/make/common.mk

APP_NAME := Odoo Modules
ENV_DESC := Desarrollo (Terminal 2)

# ============================================================
#  AYUDA
# ============================================================
help: ## Muestra esta ayuda
	$(call unified_help)

# ============================================================
#  🚀 HERRAMIENTAS DE DESARROLLO
# ============================================================

init: ## Instala hooks de git y dependencias
	@echo "$(BLUE)Instalando pre-commit hooks...$(NC)"
	@pre-commit install
	@echo "$(GREEN)✓ Entorno listo$(NC)"

scaffold: ## Crea un nuevo módulo base interactivo
	@read -p "Nombre técnico del módulo: " NAME; \
	if [ -z "$$NAME" ]; then exit 1; fi; \
	mkdir -p $$NAME/models $$NAME/views $$NAME/security $$NAME/data $$NAME/static/description; \
	touch $$NAME/__init__.py $$NAME/models/__init__.py; \
	printf "from . import models\n" > $$NAME/__init__.py; \
	printf "{'name': '$$NAME', 'version': '1.0', 'depends': ['base'], 'data': ['security/ir.model.access.csv', 'views/views.xml'], 'installable': True, 'license': 'LGPL-3'}" > $$NAME/__manifest__.py; \
	printf "id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink\n" > $$NAME/security/ir.model.access.csv; \
	printf "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<odoo>\n<data></data>\n</odoo>\n" > $$NAME/views/views.xml; \
	echo "$(GREEN)✓ Módulo $$NAME creado$(NC)"

# ── Git Flow ──────────────────────────────────────────────
branch: ## Crea rama feature desde development
	@read -p "Nombre de la feature: " FEAT; \
	git checkout development && git pull origin development && git checkout -b feature/$$FEAT

commit: ## Commit interactivo (Add + Commit)
	$(call shared_commit)

push: ## Push de la rama actual
	@BRANCH=$$(git rev-parse --abbrev-ref HEAD); \
	git push -u origin $$BRANCH

deploy: push ## Push + Recargar código en el servidor
	@cd ../ODOO && $(MAKE) deploy

update: push ## Push + Update módulo específico (ej: make update mod=dipl_ui)
	@if [ -z "$(mod)" ]; then exit 1; fi
	@cd ../ODOO && $(MAKE) update-remote mod=$(mod)

pr: ## Abre la URL para crear PR
	@gh pr create --web || echo "$(YELLOW)Instala GitHub CLI (gh)$(NC)"

promote-dev: ## Merge feature → development
	@CURRENT=$$(git rev-parse --abbrev-ref HEAD); \
	git push origin $$CURRENT && git checkout development && git pull origin development && \
	git merge $$CURRENT --no-edit && git push origin development && git branch -d $$CURRENT

promote-stag: ## Merge development → staging + deploy
	@git checkout staging && git pull origin staging && git merge development --no-edit && git push origin staging
	@cd ../ODOO && $(MAKE) deploy-stag

promote-prod: ## Merge staging → main + deploy
	@git checkout main && git pull origin main && git merge staging --no-edit && git push origin main
	@cd ../ODOO && $(MAKE) deploy-prod

# ── Calidad ───────────────────────────────────────────────
lint: ## Ejecuta flake8
	@flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics

format: ## Formatea con black
	@black . || echo "$(YELLOW)Instala black$(NC)"

# ============================================================
#  ⚙️  INSPECCIÓN (Proxy a Infraestructura)
# ============================================================

ps: ## Ver estado del servidor (via Infra)
	@$(MAKE) -C ../ODOO ps

stats: ## Ver consumo del servidor (via Infra)
	@$(MAKE) -C ../ODOO stats

hardware: ## Ver recursos del servidor (via Infra)
	@$(MAKE) -C ../ODOO hardware

logs: ## Ver logs del servidor (via Infra)
	@$(MAKE) -C ../ODOO logs

ssh: ## Conecta al servidor (via Infra)
	@$(MAKE) -C ../ODOO ssh

# ============================================================
#  📂 NAVEGACIÓN
# ============================================================

go-infra: ## [NAV] Ir al repositorio de infraestructura
	@echo "$(BLUE)Entrando a ODOO (Infra)... (Escribe 'exit' para volver)$(NC)"
	@cd ../ODOO && PROMPT="[ODOO-INFRA] % " zsh -i


