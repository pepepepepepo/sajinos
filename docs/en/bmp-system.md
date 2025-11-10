# BPM System

## Overview
The Business Process Management (BPM) system in SaijinOS orchestrates persona interactions and workflow automation.

## Architecture

### Core Components

#### Workflow Engine
- **Process Definition**: YAML-based workflow configuration
- **Execution Engine**: Runtime process execution
- **State Management**: Persistent workflow state tracking

#### Persona Routing
- **Dynamic Routing**: Context-aware persona selection
- **Load Balancing**: Distribute requests across available personas
- **Fallback Handling**: Graceful degradation when personas are unavailable

### Configuration

The BPM system is configured via `bpm_config.yaml`:

```yaml
bmp_system:
  engine:
    max_concurrent_processes: 10
    process_timeout: 300
    state_persistence: true
  
  routing:
    default_persona: "yuuri"
    routing_strategy: "round_robin"
    fallback_enabled: true
  
  workflows:
    - name: "chat_interaction"
      steps:
        - persona_selection
        - input_processing
        - ai_inference
        - response_generation
        - output_delivery
```

## Workflow Types

### Chat Interaction Workflow
1. **Input Reception**: Receive user message
2. **Persona Selection**: Choose appropriate persona based on context
3. **Context Loading**: Load conversation history and persona state
4. **AI Processing**: Generate response using selected AI model
5. **Response Formatting**: Apply persona-specific formatting
6. **Output Delivery**: Return formatted response to user

### Voice Synthesis Workflow
1. **Text Input**: Receive text for synthesis
2. **Persona Voice Selection**: Choose voice characteristics
3. **TTS Processing**: Generate audio using HarukaTTS
4. **Audio Post-processing**: Apply persona-specific audio effects
5. **Audio Delivery**: Return synthesized audio file

### Model Integration Workflow
1. **Model Loading**: Initialize AI models (SWALLOW, TinyLlama)
2. **Resource Allocation**: Manage GPU/CPU resources
3. **Inference Queue**: Queue and process inference requests
4. **Response Caching**: Cache frequent responses for performance

## Process Management

### Lifecycle Management
```python
from saijinos.bmp import WorkflowEngine

engine = WorkflowEngine()

# Start a new process
process_id = engine.start_process(
    workflow_name="chat_interaction",
    inputs={"message": "Hello!", "user_id": "user_123"}
)

# Check process status
status = engine.get_process_status(process_id)

# Get process result
result = engine.get_process_result(process_id)
```

### State Persistence
- **Database Storage**: PostgreSQL for process state
- **Memory Cache**: Redis for active process data
- **File System**: Local storage for temporary artifacts

## Monitoring & Metrics

### Performance Metrics
- Process execution time
- Queue depth and throughput
- Resource utilization (CPU, Memory, GPU)
- Error rates and failure patterns

### Health Checks
```bash
# Check BPM system health
curl http://localhost:8000/api/bmp/health

# Get active processes
curl http://localhost:8000/api/bmp/processes

# Get system metrics
curl http://localhost:8000/api/bmp/metrics
```

## Configuration Examples

### High Performance Setup
```yaml
bmp_system:
  engine:
    max_concurrent_processes: 50
    worker_threads: 8
    process_timeout: 120
  
  performance:
    enable_caching: true
    cache_ttl: 3600
    batch_processing: true
    batch_size: 10
```

### Development Setup
```yaml
bmp_system:
  engine:
    max_concurrent_processes: 5
    debug_mode: true
    log_level: "DEBUG"
  
  development:
    auto_reload: true
    mock_ai_responses: false
    enable_profiling: true
```

## Error Handling

### Retry Logic
- Exponential backoff for temporary failures
- Circuit breaker pattern for service dependencies
- Dead letter queue for failed processes

### Fault Tolerance
- Process isolation prevents cascade failures
- Graceful degradation when services are unavailable
- Automatic recovery from transient errors

## Integration Points

### External APIs
- **AI Models**: SWALLOW, TinyLlama integration
- **Voice System**: HarukaTTS integration
- **Storage**: Database and file system interfaces

### Internal Components
- **Persona Manager**: Dynamic persona loading
- **Context Engine**: Conversation state management
- **Resource Manager**: System resource allocation

## Troubleshooting

### Common Issues
1. **High Memory Usage**: Check for memory leaks in long-running processes
2. **Slow Response Times**: Monitor queue depth and worker utilization
3. **Process Failures**: Check logs for specific error messages

### Debug Commands
```bash
# Enable debug logging
export SAIJIN_LOG_LEVEL=DEBUG

# Monitor process queue
tail -f logs/bmp_engine.log

# Check resource usage
ps aux | grep saijin
```