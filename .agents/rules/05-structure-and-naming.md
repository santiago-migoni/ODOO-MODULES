---
trigger:
globs: "modules/**/*"
description: Module structure and naming conventions (dipl_ prefix)
---

# structure-and-naming

Module structure & naming are mandatory:

- Module technical name must follow: `dipl_<module_name>`.
- Versioning conventions follow the repository/scaffold rules.
- XML IDs must be namespaced (include the module technical prefix) and must be stable.
- Security files belong under `security/` (`ir.model.access.csv` and rules XML when applicable).
- `company_id` and multi-company considerations must be considered from the start when the model is multi-company.
