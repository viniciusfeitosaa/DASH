# 📊 STDASH - Dashboard Streamlit

Dashboard interativo e leve criado com Streamlit para visualização e análise de planilhas.

## 🚀 Funcionalidades

- **Carregamento via URL**: Suporte para planilhas hospedadas na web (Excel, CSV ou Google Sheets)
- **Visualizações Interativas**: Gráficos de barras, linhas, histogramas, scatter plots e box plots
- **Análise Estatística**: Métricas descritivas e distribuições
- **Exportação de Dados**: Download dos dados processados em CSV ou Excel
- **Interface Intuitiva**: Interface limpa e fácil de usar
- **Cache Inteligente**: Dados em cache por 5 minutos para melhor performance

## 📋 Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

## 🔧 Instalação Local

1. Clone ou baixe este repositório

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute o dashboard:
```bash
streamlit run app.py
```

4. Acesse no navegador: `http://localhost:8501`

## ☁️ Deploy no Render

### Opção 1: Usando render.yaml (Recomendado)

1. Faça push do código para um repositório Git (GitHub, GitLab, etc.)

2. No Render:
   - Acesse [dashboard.render.com](https://dashboard.render.com)
   - Clique em "New +" → "Blueprint"
   - Conecte seu repositório
   - Render detectará automaticamente o arquivo `render.yaml`
   - Clique em "Apply"

### Opção 2: Configuração Manual

1. No Render, crie um novo **Web Service**

2. Configure:
   - **Name**: stdash-dashboard (ou seu nome preferido)
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`

3. Salve e aguarde o deploy (pode levar alguns minutos)

### Configurações Importantes no Render

- **Port**: Render define automaticamente a porta através da variável `$PORT`
- **Plan**: Plano gratuito disponível (limitações: pode "hibernar" após inatividade)
- **Region**: Escolha a região mais próxima de você

### Configurar URL da Planilha no Render

Para que o dashboard carregue automaticamente os dados na inicialização:

1. No dashboard do Render, vá para o seu serviço
2. Clique em **"Environment"** (Ambiente)
3. Adicione uma nova variável de ambiente:
   - **Key**: `DATA_URL`
   - **Value**: A URL completa da sua planilha
     - Exemplo: `https://docs.google.com/spreadsheets/d/SHEET_ID/export?format=xlsx&gid=0`
     - Ou: `https://exemplo.com/dados.xlsx`
4. Clique em **"Save Changes"**
5. O serviço será reiniciado automaticamente

**Dica**: Para Google Sheets, certifique-se de que a planilha está pública ou acessível via link.

## 📁 Estrutura de Arquivos

```
STDASH/
│
├── app.py              # Aplicação principal do Streamlit
├── requirements.txt    # Dependências do projeto
├── render.yaml         # Configuração para deploy no Render
├── logo.png            # Logo do dashboard
├── README.md           # Este arquivo
└── .gitignore          # Arquivos a serem ignorados pelo Git
```

## 💡 Como Usar

1. **Carregar Dados**:
   - **Opção 1 (Local)**: Cole a URL da planilha na barra lateral e clique em "Carregar Dados"
   - **Opção 2 (Produção)**: Configure a variável de ambiente `DATA_URL` no Render (dados carregam automaticamente)

2. **Formatos Suportados**:
   - **CSV via URL**: `https://exemplo.com/dados.csv`
   - **Excel via URL**: `https://exemplo.com/dados.xlsx`
   - **Google Sheets**: Cole o link de compartilhamento público
     - Exemplo: `https://docs.google.com/spreadsheets/d/SHEET_ID/edit`
     - Certifique-se de que a planilha está configurada como "Público" ou "Qualquer pessoa com o link"

3. **Explorar Dados**:
   - **Visão Geral**: Visualize as primeiras linhas e estatísticas básicas
   - **Gráficos**: Crie visualizações interativas com diferentes tipos de gráficos
   - **Análise Estatística**: Explore métricas detalhadas das colunas numéricas
   - **Exportar**: Baixe os dados processados

## 🔒 Segurança

- O dashboard é público se você usar o plano gratuito do Render
- Para dados sensíveis, considere:
  - Usar autenticação (Streamlit Authenticator)
  - Usar planos pagos do Render com autenticação
  - Deploy em servidor privado

## 🐛 Solução de Problemas

### Erro ao carregar dados da URL
- **URL inacessível**: Verifique se a URL está correta e acessível publicamente
- **Google Sheets**: Certifique-se de que a planilha está configurada como "Público" ou "Qualquer pessoa com o link"
- **CORS**: Alguns servidores podem bloquear requisições. Considere usar Google Sheets ou hospedar em um servidor que permita CORS
- **Formato**: Verifique se o formato do arquivo é suportado (.csv, .xlsx, .xls)

### Google Sheets não carrega
- Certifique-se de que o link de compartilhamento está correto
- A planilha deve estar configurada como "Público" (Anyone with the link)
- Você pode usar o link de exportação direto:
  - `https://docs.google.com/spreadsheets/d/SHEET_ID/export?format=xlsx&gid=0`

### Dashboard não inicia no Render
- Verifique os logs no dashboard do Render
- Confirme que o `startCommand` está correto
- Verifique se todas as dependências estão no `requirements.txt`
- Verifique se a variável de ambiente `DATA_URL` está configurada corretamente (se estiver usando)

### Porta não disponível
- No Render, sempre use `$PORT` no comando de start
- Não especifique uma porta fixa

### Dados não atualizam
- O cache é atualizado a cada 5 minutos. Use o botão "🔄 Carregar Dados" para forçar atualização
- Para atualizar manualmente o cache, adicione `?clear_cache=true` na URL

## 📝 Licença

Este projeto é de código aberto e está disponível para uso livre.

## 🤝 Contribuições

Sinta-se à vontade para melhorar este dashboard! Sugestões de funcionalidades:
- Filtros avançados
- Múltiplas planilhas
- Gráficos personalizados
- Análises preditivas

---

Desenvolvido com ❤️ usando Streamlit
