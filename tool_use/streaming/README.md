# Tool Use with Streaming · LAB CRÍTICO para producción

Estos 2 notebooks son los más importantes para nuestro stack en H3L Consulting. Combinan **tool use** + **streaming** = arquitectura production-grade para agentes IA que dan feedback en tiempo real al usuario.

## Files

| Notebook | Para qué |
|----------|----------|
| `003_tool_streaming.ipynb` | Lab base · construir `chat_stream()` paso a paso |
| `003_tool_streaming_completed.ipynb` | Solución completa · con tool `save_article` + `run_conversation` streaming |

## Por qué este lab es crítico (no negociable para producción)

Sin streaming en tool use, el usuario ve un spinner de 10-30 segundos mientras Claude:
1. Decide qué tools usar
2. Construye los parámetros JSON
3. Ejecuta las tools
4. Genera la respuesta final

Con streaming en tool use, el usuario ve **en tiempo real**:
- "Claude está pensando..."
- "Llamando a `query_supercias` con RUC `1790016919001`..."
- "Resultado: [streamed]"
- Texto final apareciendo token por token

UX comparable a Claude.ai, Perplexity, ChatGPT con tools. Sin esto, las apps de H3L sienten "viejas".

## Eventos de streaming (tipos críticos para quiz + producción)

```python
with client.messages.stream(model=..., tools=tools, messages=messages) as stream:
    for event in stream:
        # event.type es uno de:
        #   message_start          ← inicio de respuesta
        #   content_block_start    ← Claude empieza un bloque (text o tool_use)
        #   content_block_delta    ← incremento dentro del bloque
        #       - text_delta       (texto regular)
        #       - input_json_delta (parámetros de tool armándose token por token)
        #   content_block_stop     ← bloque completo
        #   message_delta          ← actualización de message metadata (stop_reason)
        #   message_stop           ← respuesta completa
        
        if event.type == "content_block_start":
            if event.content_block.type == "tool_use":
                print(f"\n→ Calling tool: {event.content_block.name}")
        elif event.type == "content_block_delta":
            if event.delta.type == "text_delta":
                print(event.delta.text, end="", flush=True)
            elif event.delta.type == "input_json_delta":
                # parámetros de tool armándose · útil para debugging
                print(event.delta.partial_json, end="", flush=True)
```

## Patrón production-ready

```python
def chat_stream(messages, tools, system=None):
    """Stream de la respuesta de Claude con tool use."""
    kwargs = {"model": MODEL, "max_tokens": 2048, "tools": tools, "messages": messages}
    if system:
        kwargs["system"] = system
    
    with client.messages.stream(**kwargs) as stream:
        for event in stream:
            yield event   # generador · el caller decide qué hacer con cada evento
        
        final_message = stream.get_final_message()
        return final_message

def run_conversation_streamed(messages, tools):
    """Agentic loop con streaming · cada turn emite eventos."""
    while True:
        final = None
        for event in chat_stream(messages, tools):
            # Aquí el caller puede emitir SSE / WebSocket al frontend
            handle_event_for_user(event)
            if event.type == "message_stop":
                final = event.message
        
        add_assistant_message(messages, final.content)
        
        if final.stop_reason == "end_turn":
            return final
        
        if final.stop_reason == "tool_use":
            tool_results = run_tools(final.content)
            add_user_message(messages, tool_results)
```

## Aplicación en H3L Consulting (impacto real)

### 1. `profundiza.h3l.ai` · ya tiene streaming de texto · falta tool streaming
**Estado actual:** stream de texto OK · tool calls invisibles (spinner)
**Mejora:** mostrar "Consultando base Supercias..." cuando el agente llame `query_supercias`
**Impacto UX:** usuario confía más al ver el progreso

### 2. `diagnostico.h3l.ai` · sin streaming aún
**Implementar:** chat_stream completo desde día 1
**Impacto:** time-to-first-feedback de 15s → 500ms

### 3. `sri.h3l.ai` · agente con múltiples tools (consultar RUC, calcular IVA, etc.)
**Mejora:** stream visible de cada paso del cálculo tributario
**Impacto:** el usuario aprende qué hace el agente · se vuelve enseñable

### 4. `publico.h3l.ai` (Policía UNOE) · diagnóstico institucional
**Mejora:** streaming de cada departamento auditado
**Impacto:** percepción de profundidad analítica (vs caja negra)

### 5. Imagemia chat de soporte a radiólogos
**Mejora:** stream de "consultando guideline ACR..." cuando llame tool específica
**Impacto:** trust crítica en contexto médico

## Conceptos críticos para quiz final

| Concepto | Detalle |
|----------|---------|
| `content_block_start` | Inicio de un bloque · type puede ser `text` o `tool_use` |
| `input_json_delta` | Parámetros de tool llegando token por token como JSON parcial |
| `partial_json` | Campo del delta con fragmento de JSON · concatenas para reconstruir |
| `message_stop` | Respuesta completa · es donde lees `final.stop_reason` |
| `stream.get_final_message()` | Después del stream, devuelve el objeto Message completo |
| **Backpressure** | Si tu UI no procesa eventos rápido, el stream se acumula · diseñar consumer eficiente |

## Run

```bash
export ANTHROPIC_API_KEY="your-api-key"
uv pip install anthropic python-dotenv jupyter
jupyter notebook 003_tool_streaming_completed.ipynb
```
