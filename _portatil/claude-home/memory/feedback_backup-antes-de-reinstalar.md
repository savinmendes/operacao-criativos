---
name: feedback-backup-antes-de-reinstalar
description: "Antes de desinstalar/reinstalar qualquer programa, copiar as configurações do usuário (ex.: %LOCALAPPDATA%\\LogiOptionsPlus) para poder restaurar"
metadata:
  node_type: memory
  type: feedback
  originSessionId: b1265e31-6073-4e56-bb4d-84393cd16696
  modified: 2026-10-16T11:33:37.133Z
---

Antes de desinstalar ou reinstalar qualquer programa, faça backup das configurações do usuário: pastas em %LOCALAPPDATA% e %APPDATA%, arquivos .db/.json de settings. Faça o backup mesmo que o pedido seja só "desinstalar e instalar de novo".

**Why:** em 16/10/2026 reinstalei o Logi Options+ (o MX Master travava a rolagem). O desinstalador apagou `%LOCALAPPDATA%\LogiOptionsPlus\settings.db`. A pessoa pediu as configurações de antes e não havia cópia local.

**How to apply:** copie a pasta de settings para o scratchpad (ou `Downloads\_backup-<programa>-<data>`) antes do uninstall. Depois de reinstalar, ofereça a restauração. No Logi Options+, há também o backup na nuvem: Configurações → Backups, com a conta Logitech logada.
