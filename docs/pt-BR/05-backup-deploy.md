# Backup, restauração e deploy — roteiro operacional

## Backup MySQL (Windows PowerShell)
```powershell
& "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqldump.exe" -u omnilog_app -p --single-transaction --routines --triggers omnilog_hub > .\backup_omnilog.sql
```
Digite a senha no prompt; não a coloque no comando nem compartilhe o arquivo com credenciais.

## Restauração em schema de teste
```powershell
& "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u omnilog_app -p -e "CREATE DATABASE omnilog_hub_restore CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;"
& "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u omnilog_app -p omnilog_hub_restore < .\backup_omnilog.sql
```
Validar contagens e integridade referencial antes de qualquer troca de ambiente. Definir RPO/RTO com o responsável; testar restauração periodicamente.

## Deploy de homologação
Executar os serviços em ambiente isolado, configurar variáveis por secret manager, restringir firewall, habilitar HTTPS e logs sem dados sensíveis. O deploy remoto não foi executado por este pacote.
