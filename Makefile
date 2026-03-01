# Detección dinámica de common.mk (Soporta Mac: ../ODOO y Servidor: ../../)
COMMON_MK := $(wildcard ../ODOO/infra/make/common.mk ../../infra/make/common.mk)
ifeq ($(strip $(COMMON_MK)),)
$(error Error: No se encontro common.mk. Verifica la ruta interactiva.)
endif
include $(COMMON_MK)


APP_NAME := Odoo Modules
ENV_DESC := Desarrollo de Odoo
REPO_NAME := MODULES

# ============================================================
#  AYUDA
# ============================================================
help: ## Muestra esta ayuda
	$(call unified_help)

# ============================================================
#  🛠️ DESARROLLO
# ============================================================

mod-init: ## [DEV] Instala hooks de git locales
	@echo "$(BLUE)Instalando pre-commit hooks para Módulos...$(NC)"
	@pre-commit install
	@echo "$(GREEN)✓ Entorno de Módulos listo$(NC)"

mod-scaffold: ## [DEV] Crea un nuevo módulo base interactivo
	@echo "$(BLUE)--- Generador de Módulos Dipleg ---$(NC)"
	@read -p "Nombre técnico (ej: dipl_sale_extra): " NAME; \
	if [ -z "$$NAME" ]; then echo "$(RED)Error: El nombre es obligatorio$(NC)"; exit 1; fi; \
	read -p "Categoría (default: Technical): " CAT; \
	if [ -z "$$CAT" ]; then CAT="Technical"; fi; \
	mkdir -p $$NAME/models $$NAME/views $$NAME/security $$NAME/data $$NAME/static/description; \
	touch $$NAME/__init__.py $$NAME/models/__init__.py; \
	printf "from . import models\n" > $$NAME/__init__.py; \
	printf "{\n    'name': '$$NAME',\n    'version': '1.0',\n    'category': '$$CAT',\n    'summary': 'Módulo personalizado para $$CAT',\n    'author': 'Dipleg',\n    'depends': ['base'],\n    'data': [\n        'security/ir.model.access.csv',\n        'views/views.xml',\n    ],\n    'installable': True,\n    'license': 'LGPL-3',\n}" > $$NAME/__manifest__.py; \
	printf "id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink\n" > $$NAME/security/ir.model.access.csv; \
	printf "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<odoo>\n    <data>\n\n    </data>\n</odoo>\n" > $$NAME/views/views.xml; \
	echo "$(GREEN)✓ Módulo $$NAME creado exitosamente con categoría: $$CAT$(NC)"

mod-branch: ## [DEV] Crea rama feature desde development
	@read -p "Nombre de la feature: " FEAT; \
	git checkout development && git pull origin development && git checkout -b feature/$$FEAT

commit: ## [DEV] Commit interactivo (Add + Commit)
	$(call shared_commit)

# ============================================================
#  🚀 DESPLIEGUE
# ============================================================

push: ## [DEPLOY] Push de la rama actual (Módulos)
	$(call shared_push)

pull: ## [DEPLOY] Pull de la rama actual (Módulos)
	@BRANCH=$$(git rev-parse --abbrev-ref HEAD); \
	git pull origin $$BRANCH

# deploy manejado por common.mk

mod-promote-dev: ## [DEPLOY] [MAC] Merge feature → development
	@if [ "$(IS_MAC)" != "1" ]; then echo "$(RED)Error: Este comando se dispara desde la Mac.$(NC)"; exit 1; fi
	@CURRENT=$$(git rev-parse --abbrev-ref HEAD); \
	git push origin $$CURRENT && git checkout development && git pull origin development && \
	git merge $$CURRENT --no-edit && git push origin development && git branch -d $$CURRENT

mod-promote-stag: ## [DEPLOY] [MAC] Merge development → staging + deploy
	@if [ "$(IS_MAC)" != "1" ]; then echo "$(RED)Error: Este comando se dispara desde la Mac.$(NC)"; exit 1; fi
	@git checkout staging && git pull origin staging && git merge development --no-edit && git push origin staging
	$(call proxy_cmd,odoo-update-stag)

mod-promote-main: ## [DEPLOY] [MAC] Merge staging → main + deploy
	@if [ "$(IS_MAC)" != "1" ]; then echo "$(RED)Error: Este comando se dispara desde la Mac.$(NC)"; exit 1; fi
	@git checkout main && git pull origin main && git merge staging --no-edit && git push origin main
	$(call proxy_cmd,odoo-update-prod)

# Comandos ya manejados por common.mk (ps, stats, logs-%)

# Parametrizado
logs: ## [MONITOR] Uso: make logs-[all|dev|stag|prod|nginx|dozzle]
	@echo "$(RED)Error: Debes especificar un servicio (ej: make logs-dev)$(NC)" && exit 1

logs-%: ## [MONITOR] Ver logs delegados
	$(call proxy_cmd,logs-$*)

# Comandos de navegación centralizados en common.mk

# ============================================================
#  ⚙️  CALIDAD LOCAL
# ============================================================

lint: ## [MAINT] Ejecuta flake8
	@flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics

mod-format: ## [MAINT] Formatea con black
	@black . || echo "$(YELLOW)Instala black$(NC)"

lint: mod-format ## Compatibility alias
