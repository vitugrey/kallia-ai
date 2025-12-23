<div align="center">
  <h1>👾 KaLLia 2.0 AI Bot 👾</h1>
  <p><i>Assistente virtual narcisista com conversação por voz, multi-agentes e personalidade única inspirada em Neuro-sama</i></p>
  
  ![Python](https://img.shields.io/badge/python-3.13-blue)
  ![UV](https://img.shields.io/badge/package%20manager-UV-orange)
  ![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)
</div>

---

## 🎯 Sobre o Projeto

**KaLLia 2.0** é uma assistente virtual experimental que combina reconhecimento de fala, processamento de linguagem natural via multi-agentes e síntese de voz para criar uma experiência interativa única. Desenvolvida com personalidade sarcástica e narcisista, ela utiliza um time de agentes especializados para busca na web e execução local.

### Arquitetura Multi-Agente

O projeto usa o framework **Agno** com uma estrutura de **Team** composta por:
- **KaLLia Team Leader**: Coordena as respostas e mantém a personalidade
- **KaLLia_SEARCH**: Busca informações na web via Tavily
- **KaLLia_LOCAL_EXECUTOR**: Executa comandos e automações locais

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
- **Configurável**: Vozes customizáveis via `config_bot.json`

### 🧠 Large Language Model (LLM)
- **Framework**: Agno (multi-agente)
- **Modelos**: Suporte para Gemini (Google) e Groq
- **Memória**: Persistência via SQLite com session_id
- **Team**: Sistema de colaboração entre agentes especializados
- **Tools**: Tavily Web Search integrado

### 🔧 Configuração Externa
Todas as configurações centralizadas em `config_bot.json`:
- Parâmetros de STT (modelo Whisper, taxa de amostragem)
- Configurações de TTS (voz, diretório)
- Instruções e personalidade dos agentes
- Modelos de LLM e configurações de team

---

## 🚀 Instalação e Execução

### Pré-requisitos
- **Python**: 3.13+
- **UV**: Gerenciador de pacotes moderno
- **PyAudio**: Requer dependências do sistema (ver abaixo)
- **Tesseract OCR**: Deve-se instalar o Tesseract OCR
- 

### Windows
```powershell
# Clone o repositório
git clone https://github.com/vitugrey/kallia-ai
cd kallia-ai

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

# Seguir mesmos passos do Windows
```

---

## 📁 Estrutura do Projeto

```
kallia-ai/
├── src/
│   ├── assistentbot.py    # Orquestrador principal
│   ├── stt.py              # Speech-to-Text (Whisper + AssemblyAI)
│   ├── tts.py              # Text-to-Speech (Edge-TTS)
│   ├── llm.py              # Multi-agente (Agno)
│   └── time_exec.py        # Decorador para métricas
├── data/
│   └──agents.db           # Banco SQLite (memória dos agentes)
 temporários
├── config_bot.json         # Configuração centralizada
├── pyproject.toml          # Dependências (UV)
└── README.md
```

---

## ⚙️ Configuração

### config_bot.json
```json
{
  "stt": {
    "record_key": "CAPS_LOCK",
    "whisper_model_size": "small",
    "whisper_device": "cpu"
  },
  "tts": {
    "voice": "pt-BR-FranciscaNeural"
  },
  "llm": {
    "team": {
      "name": "KaLLia Team",
      "model_teams": "qwen/qwen3-32b",
      "instruction_team": "Sua personalidade aqui...",
      "agents": [...]
    }
  }
}
```

### Variáveis de Ambiente (.env)
```env
GOOGLE_API_KEY=sua_chave_google
GROQ_API_KEY=sua_chave_groq
TAVILY_API_KEY=sua_chave_tavily
ASSEMBLYAI_API_KEY=sua_chave_assemblyai  # Opcional
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
| **LLM Framework** | [Agno](https://docs.agno.com) | Multi-agente + memória |
| **LLM Models** | Google Gemini, Groq | Geração de texto |
| **TTS** | [Edge-TTS](https://github.com/rany2/edge-tts) | Síntese de voz |
| **Tools** | [Tavily](https://tavily.com) | Web search |
| **Audio** | PyAudio, pygame | Captura e reprodução |

---

## 🤝 Contribuições

Este é um projeto pessoal/experimental. Sugestões e feedback são bem-vindos via Issues.

---

## 📄 Licença

Este projeto é de uso pessoal. Sinta-se livre para usar como inspiração, mas respeite as licenças das bibliotecas utilizadas.

---

<div align="center">
  <p><i>Desenvolvido por Vitor Grey e KaLLia 1.0</i></p>
  <p>KaLLia 2.0: "Óbvio que sou perfeita. Fui criada por mim mesma." 💅</p>
</div>



DEPLOY
DEPLOY
DEPLOY
DEPLOY
DEPLOY

adicionar o ollama para ficar 100% local