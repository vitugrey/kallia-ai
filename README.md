<div align="center">
  <h1>👾 KaLLia 2.0 AI Bot 👾</h1>
  <p><i>Um assistente virtual de conversação por voz com personalidade única</i></p>
  
  ![Python](https://img.shields.io/badge/python-3.13-blue)
  ![UV](https://img.shields.io/badge/package%20manager-UV-orange)
  ![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)
</div>

---

## 🎯 Sobre o Projeto

**KaLLia 2.0** é uma assistente virtual experimental que combina reconhecimento de fala, processamento de linguagem natural e síntese de voz para criar uma experiência interativa única. Funciona **online (rápido)** ou **100% local (Ollama)**, sendo que a velocidade de resposta e taxa de alucinações dependem diretamente da potência do hardware e do modelo utilizado.

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
- **Modelo**: Ollama (ex.: ministral-3:3b / gpt-oss:120b-cloud)
- **Memória**: Persistência via SQLite (sessions, memories)
- **Histórico**: Último **5** runs de conversação
- **Tools**: Tavily Web Search, Open Program (atalhos .lnk)

### 🔍 RAG (Retrieval-Augmented Generation)
- **Vector DB**: LanceDB com embeddings locais (Ollama nomic-embed-text)
- **Local**  Embeddings 100% locais via Ollama

### 🔧 Configuração Externa
Tudo configurável no `config_bot.json`:
- STT: modelo Whisper, taxa de amostragem, tecla de gravação
- TTS: voz, diretório
- LLM: modelo Ollama (local/online) e instruções
- Instruções: Personalidade e comportamento da KaLLia

---

### 🚀 Instalação e Execução

### Pré-requisitos
- **Python**: 3.13+
- **UV**: Gerenciador de pacotes moderno
- **PyAudio**: Requer dependências do sistema (ver abaixo)
- **Ollama**: Para rodar o modelo local (instalar em [ollama.com](https://ollama.com))

### Windows
```bash
# Clone o repositório
git clone https://github.com/vitugrey/kallia-ai
cd kallia-ai

# Instale Ollama (https://ollama.com) e puxe o modelo principal:
ollama pull gpt-oss:120b-cloud

# Instalar dependências com UV
uv sync

# Configurar variáveis de ambiente (apenas se usar serviços externos; modo local não precisa)
# OLLAMA_API_KEY=sua_chave_aqui
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
ollama pull ministral-3:3b
# or
ollama pull gpt-oss:120b-cloud # online
```

---

## 🎮 Uso

1. Execute o bot: `uv run src/assistentbot.py`
2. Pressione e segure **CAPS_LOCK** para gravar sua voz
3. Solte para processar
4. O bot responde via voz sintetizada

### Comandos Especiais
- "Pesquise [termo]": Aciona busca web via API Tavily
- "Abra [programa]": Abre programas via atalhos (.lnk) no diretório ~/Links (ex: "Abra o vscode")

---

## 📚 Tecnologias

| Componente | Tecnologia | Uso |
|------------|------------|-----|
| **STT** | [Faster-Whisper](https://github.com/SYSTRAN/faster-whisper) | Transcrição local |
| **STT Cloud** | [AssemblyAI](https://www.assemblyai.com) | Transcrição online rápida |
| **LLM Framework** | [Agno](https://docs.agno.com) | Agentes com memória persistente |
| **LLM Models** | [Ollama](https://ollama.com) | Geração de texto |
| **RAG/Vector DB** | [LanceDB](https://lancedb.com) | Vector database eficiente |
| **Embeddings** | [Ollama](https://ollama.com) | Embeddings 100% locais |
| **TTS** | [Edge-TTS](https://github.com/rany2/edge-tts) | Síntese de voz |
| **Web Search** | [Tavily](https://tavily.com)  | Web search API |
| **Automação Local** | Open program | Abre atalhos .lnk de ~/Links |
| **Audio** | PyAudio, pygame | Captura e reprodução |
| **UI** | Art | ASCII art display |

---

## 🎯 Roadmap & Features Planejadas

- [ ] **Vida própia**: Iniciar conversações sozinha
- [x] **Gestão de Context Window**: Sistema inteligente para gerenciar limite de tokens e sumarização de histórico
- [x] **Multi-modal**: Suporte para visão (análise de imagens/screenshots)
- [ ] **Streaming TTS**: Síntese de voz em streaming para respostas mais rápidas e voz personalizada
- [ ] **Interface Gráfica**: Dashboard para configuração e monitoramento
- [x] **Otimização de Memória**: Cache inteligente e gestão eficiente de recursos
- [ ] **Containerização**: Docker para deploy simplificado

---

#### 💬 Comentario dos Devs

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
      <i>Óbvio que sou perfeira! Fui feita por mim mesma.</i>
    </td>
  </tr>
</table>
