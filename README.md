<div align="center">
  <h1>👾 KaLLia 2.0 AI Bot 👾</h1>
  <p><i>Um assistente virtual de conversação por voz com personalidade única</i></p>
  
  ![Python](https://img.shields.io/badge/python-3.13-blue)
  ![UV](https://img.shields.io/badge/package%20manager-UV-orange)
  ![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)
</div>

---

## 🎯 Sobre o Projeto

**KaLLia 2.0** é uma assistente virtual experimental que combina reconhecimento de fala, processamento de linguagem natural e síntese de voz para criar uma experiência interativa única. Desenvolvida para que o dev não fique sozinho codando, ela utiliza um agente com tools de busca na web e execução local para otimizar o tempo.

---

## ✨ Funcionalidades

### 🎤 Speech-to-Text (STT)
- **Local**: Whisper (Faster-Whisper) - modelos `tiny`, `small`, `turbo`
- **Cloud**: AssemblyAI (mais rápido, requer API key)
- **Gravação**: Push-to-talk via tecla configurável (padrão: CAPS_LOCK)
- **Processamento**: Áudio processado em memória (sem arquivos temporários)

### 🔊 Text-to-Speech (TTS)
- **Engine**: Edge-TTS (voz pt-BR-FranciscaNeural)
- **Streaming**: Reprodução direta da memória via pygame

### 🧠 Large Language Model (LLM)
- **Framework**: Agno (agentes inteligentes com memória persistente)
- **Modelos**: Suporte para Gemini (Google), Groq e Ollama
- **Memória**: Persistência via SQLite (sessions, memories, knowledge)
- **Histórico**: Último **5** runs de histórico de conversação
- **Tools**: Tavily Web Search integrado

### 🔍 RAG (Retrieval-Augmented Generation)
- **Vector DB**: LanceDB com embeddings locais (Ollama nomic-embed-text)
- **Knowledge Base**: Sistema de knowledge persistente para documentos
- **Local**: Embeddings 100% locais via Ollama

### 🔧 Configuração Externa
Todas as configurações centralizadas em `config_bot.json`:
- Parâmetros de STT (modelo Whisper, taxa de amostragem)
- Configurações de TTS (voz, diretório)
- Instruções e personalidade dos agentes
- Modelos de LLM e configurações de team

---

### 🚀 Instalação e Execução

### Pré-requisitos
- **Python**: 3.13+
- **UV**: Gerenciador de pacotes moderno
- **PyAudio**: Requer dependências do sistema (ver abaixo)
- **Ollama**: Para embeddings locais (instalar em [ollama.com](https://ollama.com))

### Windows
```powershell
# Clone o repositório
git clone https://github.com/vitugrey/kallia-ai
cd kallia-ai

# Instale Ollama (https://ollama.com) e puxe o modelo:
ollama pull nomic-embed-text

# Instalar dependências com UV
uv sync

# Configurar variáveis de ambiente
# Crie um arquivo .env com:
# GOOGLE_API_KEY=sua_chave_aqui
# GROQ_API_KEY=sua_chave_aqui
# TAVILY_API_KEY=sua_chave_aqui
# ASSEMBLYAI_API_KEY=sua_chave_aqui (opcional)

# Executar o bot
uv run src/assistentbot.py
```

### Linux/MacOS
```bash
# Instalar PyAudio (requer portaudio)
# Ubuntu/Debian:
sudo apt-get install portaudio19-dev python3-pyaudio
# MacOS:
brew install portaudio

# Instale Ollama e puxe o modelo:
ollama pull nomic-embed-text

# Seguir mesmos passos do Windows
```

---

## 🎮 Uso

1. Execute o bot: `uv run src/assistentbot.py`
2. Pressione e segure **CAPS_LOCK** para gravar sua voz
3. Solte para processar
4. O bot responde via voz sintetizada

### Comandos Especiais
- "Abra [programa]": Abre programas configurados
- "Pesquise [termo]": Aciona busca web via agente KaLLia_SEARCH

---

## 📚 Tecnologias

| Componente | Tecnologia | Uso |
|------------|------------|-----|
| **STT** | [Faster-Whisper](https://github.com/SYSTRAN/faster-whisper) | Transcrição local |
| **STT Cloud** | [AssemblyAI](https://www.assemblyai.com) | Transcrição online rápida |
| **LLM Framework** | [Agno](https://docs.agno.com) | Agentes com memória persistente |
| **LLM Models** | Google Gemini, Groq, Ollama | Geração de texto |
| **RAG/Vector DB** | [LanceDB](https://lancedb.com) | Vector database eficiente |
| **Embeddings** | [Ollama](https://ollama.com) | Embeddings 100% locais |
| **TTS** | [Edge-TTS](https://github.com/rany2/edge-tts) | Síntese de voz |
| **Web Search** | [Tavily](https://tavily.com) | Web search API |
| **Audio** | PyAudio, pygame | Captura e reprodução |
| **UI** | Art | ASCII art display |

---

## � Roadmap & Features Planejadas

### 🎯 Alta Prioridade

- [ ] **Modo Offline Total**: Rodar 100% local sem dependências de APIs externas
- [ ] **Tool de Automação Local**: Sistema completo para abrir programas, executar comandos e automações Windows/Linux
- [ ] **Gestão de Context Window**: Sistema inteligente para gerenciar limite de tokens e sumarização de histórico
- [ ] **Multi-modal**: Suporte para visão (análise de imagens/screenshots)
- [ ] **Streaming TTS**: Síntese de voz em streaming para respostas mais rápidas e voz personalizada
- [ ] **Interface Gráfica**: Dashboard para configuração e monitoramento
- [ ] **Otimização de Memória**: Cache inteligente e gestão eficiente de recursos
- [ ] **Containerização**: Docker para deploy simplificado

---

## �💬 Comentario do Dev

<table>
  <tr>
    <td>
      <img src="data\image-de-vitor-de-oculos-com-fundo-verde.jpeg" width="100px" />
    </td>
    <td>
      Escrito por <a href="https://github.com/vitugrey">Vitor Grey.</a>
    </td>
    <td>
      <i>Devido ficar muito tempo sem interagir socialmente fiz essa aberração para me destrair enquanto fico no PC. </i>
    </td>
  </tr>
  <tr>
    <td>
      <img src="data\imagem-real-da-kallia.ico" width="100px" />
    </td>
    <td>
      Feito por <a href="#">Kallia 1.0.</a>
    </td>
    <td>
      <i>Obivio que sou perfeira! Fui feita por mim mesma.</i>
    </td>
  </tr>
</table>
