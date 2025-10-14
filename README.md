# Projeto TCC - Sistema de Massoterapia

## Pré-requisitos

- Python 3.13+ instalado
- Node.js e npm instalados
- PowerShell com política de execução configurada

## Configuração Inicial

### 1. Configurar Política de Execução do PowerShell
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 2. Criar e Configurar Ambiente Virtual Python
```powershell
cd C:\tcc\Projeto
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r Back_end\requirements.txt
```

### 3. Instalar Dependências do Front-end
```powershell
cd C:\tcc\Projeto\Front_end
npm install
```

## Como Iniciar o Projeto

### Opção 1: Script Automatizado
```powershell
cd C:\tcc\Projeto
.\start.ps1
```

### Opção 2: Comandos Manuais (Como Especificado)

#### Front-end:
```powershell
cd C:\tcc\Projeto\Front_end
npm run dev
```

#### Back-end:
```powershell
cd C:\tcc\Projeto
& .\.venv\Scripts\Activate.ps1
python -m Back_end.app
```

## Estrutura do Projeto

```
C:\tcc\Projeto\
├── Front_end/          # Aplicação React + Vite
├── Back_end/           # API Flask
├── .venv/             # Ambiente virtual Python
├── start.ps1          # Script de inicialização
└── README.md          # Este arquivo
```

## URLs de Acesso

- **Front-end**: http://localhost:5173
- **Back-end**: http://localhost:5000

## Notas Importantes

- O Front-end roda na porta 5173 (Vite padrão)
- O Back-end roda na porta 5000 (Flask padrão)
- Certifique-se de que ambas as portas estejam livres antes de iniciar