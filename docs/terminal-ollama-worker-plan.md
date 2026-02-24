# Terminal-Ollama Worker Implementation Plan

## Overview

This document outlines the implementation plan for a `terminal-ollama` worker type that integrates with Mahavishnu's worker pool system. The worker will enable task execution through Ollama's local HTTP API, providing a zero-cost, privacy-preserving AI worker option.

## Goals

1. Create a self-contained Ollama worker implementation in the Bodai project
2. Design for easy integration into Mahavishnu's worker pool system
3. Support all standard Ollama models via HTTP API
4. Maintain isolation from core Mahavishnu codebase during development

## Architecture

### Component Overview

```
+---------------------------+
|    Mahavishnu Pool        |
|    (pool_spawn)           |
+-------------+-------------+
              |
              | worker_type="terminal-ollama"
              v
+---------------------------+
|    OllamaWorker           |
|    (bodai.workers)        |
+-------------+-------------+
              |
              | HTTP POST
              v
+---------------------------+
|    Ollama HTTP API        |
|    localhost:11434        |
+---------------------------+
              |
              v
+---------------------------+
|    Local Models           |
|    (qwen2.5, llama3, etc) |
+---------------------------+
```

### Key Components

1. **OllamaWorker** - Main worker class implementing BaseWorker interface
2. **OllamaClient** - Async HTTP client for Ollama API communication
3. **OllamaConfig** - Configuration dataclass for worker settings
4. **Worker Registry Entry** - Configuration for Mahavishnu's WORKER_REGISTRY

## Implementation Details

### 1. Module Structure

```
bodai/
  workers/
    __init__.py
    ollama/
      __init__.py
      worker.py        # OllamaWorker class
      client.py        # OllamaClient HTTP wrapper
      config.py        # Configuration models
      models.py        # API request/response models
```

### 2. Configuration Model

```python
# bodai/workers/ollama/config.py

from dataclasses import dataclass, field
from enum import Enum


class OllamaModel(str, Enum):
    """Common Ollama models for code tasks."""
    QWEN_CODER_7B = "qwen2.5-coder:7b"
    QWEN_CODER_14B = "qwen2.5-coder:14b"
    LLAMA3_8B = "llama3:8b"
    LLAMA3_70B = "llama3:70b"
    CODESTRAL = "codestral:22b"
    DEEPSEEK_CODER = "deepseek-coder:6.7b"


@dataclass
class OllamaWorkerConfig:
    """Configuration for Ollama worker.

    Attributes:
        base_url: Ollama API endpoint
        model: Model identifier to use
        timeout: Request timeout in seconds
        temperature: Sampling temperature (0.0-2.0)
        num_ctx: Context window size
        num_predict: Maximum tokens to generate
        top_p: Nucleus sampling parameter
        top_k: Top-k sampling parameter
        stream: Whether to stream responses
        keep_alive: How long to keep model loaded (e.g., "5m", "1h")
    """
    base_url: str = "http://localhost:11434"
    model: str = "qwen2.5-coder:7b"
    timeout: int = 300
    temperature: float = 0.7
    num_ctx: int = 4096
    num_predict: int = 2048
    top_p: float = 0.9
    top_k: int = 40
    stream: bool = False
    keep_alive: str = "5m"

    # Worker identification
    worker_type: str = "terminal-ollama"
    name: str = "Ollama AI"
```

### 3. API Models

```python
# bodai/workers/ollama/models.py

from pydantic import BaseModel, Field
from typing import Any


class OllamaGenerateRequest(BaseModel):
    """Request model for Ollama generate API."""
    model: str
    prompt: str
    stream: bool = False
    options: dict[str, Any] = Field(default_factory=dict)
    keep_alive: str = "5m"


class OllamaChatRequest(BaseModel):
    """Request model for Ollama chat API."""
    model: str
    messages: list[dict[str, str]]
    stream: bool = False
    options: dict[str, Any] = Field(default_factory=dict)
    keep_alive: str = "5m"


class OllamaResponse(BaseModel):
    """Response model from Ollama API."""
    model: str
    created_at: str
    response: str
    done: bool
    context: list[int] | None = None
    total_duration: int | None = None
    load_duration: int | None = None
    prompt_eval_count: int | None = None
    eval_count: int | None = None
    eval_duration: int | None = None


class OllamaModelInfo(BaseModel):
    """Model information from Ollama API."""
    name: str
    modified_at: str
    size: int
    digest: str
    details: dict[str, Any] | None = None
```

### 4. Ollama Client

```python
# bodai/workers/ollama/client.py

import asyncio
import logging
from typing import Any

import httpx

from .config import OllamaWorkerConfig
from .models import OllamaChatRequest, OllamaGenerateRequest, OllamaModelInfo, OllamaResponse

logger = logging.getLogger(__name__)


class OllamaClient:
    """Async HTTP client for Ollama API.

    Provides methods for generate, chat, and model management operations.
    Handles connection pooling, timeouts, and error recovery.

    Args:
        config: Worker configuration with API settings
    """

    def __init__(self, config: OllamaWorkerConfig) -> None:
        self.config = config
        self._client: httpx.AsyncClient | None = None

    async def __aenter__(self) -> "OllamaClient":
        """Initialize HTTP client on context entry."""
        self._client = httpx.AsyncClient(
            base_url=self.config.base_url,
            timeout=httpx.Timeout(self.config.timeout),
        )
        return self

    async def __aexit__(self, *args: Any) -> None:
        """Close HTTP client on context exit."""
        if self._client:
            await self._client.aclose()
            self._client = None

    @property
    def client(self) -> httpx.AsyncClient:
        """Get the HTTP client, raising if not initialized."""
        if self._client is None:
            raise RuntimeError("OllamaClient not initialized - use async context manager")
        return self._client

    async def is_available(self) -> bool:
        """Check if Ollama server is running and accessible.

        Returns:
            True if Ollama API responds to health check
        """
        try:
            response = await self.client.get("/", timeout=5.0)
            return response.status_code == 200 or "Ollama is running" in response.text
        except Exception as e:
            logger.debug(f"Ollama availability check failed: {e}")
            return False

    async def list_models(self) -> list[OllamaModelInfo]:
        """List available models from Ollama server.

        Returns:
            List of model information objects
        """
        response = await self.client.get("/api/tags")
        response.raise_for_status()
        data = response.json()

        return [OllamaModelInfo(**model) for model in data.get("models", [])]

    async def generate(
        self,
        prompt: str,
        model: str | None = None,
        **options: Any,
    ) -> OllamaResponse:
        """Generate completion for a prompt.

        Args:
            prompt: Input prompt text
            model: Override model (uses config default if not specified)
            **options: Additional generation options

        Returns:
            OllamaResponse with generated text and metadata
        """
        request = OllamaGenerateRequest(
            model=model or self.config.model,
            prompt=prompt,
            stream=False,
            options={
                "temperature": self.config.temperature,
                "num_ctx": self.config.num_ctx,
                "num_predict": self.config.num_predict,
                "top_p": self.config.top_p,
                "top_k": self.config.top_k,
                **options,
            },
            keep_alive=self.config.keep_alive,
        )

        response = await self.client.post(
            "/api/generate",
            json=request.model_dump(),
        )
        response.raise_for_status()

        return OllamaResponse(**response.json())

    async def chat(
        self,
        messages: list[dict[str, str]],
        model: str | None = None,
        **options: Any,
    ) -> OllamaResponse:
        """Generate chat completion.

        Args:
            messages: List of message dicts with 'role' and 'content'
            model: Override model (uses config default if not specified)
            **options: Additional generation options

        Returns:
            OllamaResponse with generated text and metadata
        """
        request = OllamaChatRequest(
            model=model or self.config.model,
            messages=messages,
            stream=False,
            options={
                "temperature": self.config.temperature,
                "num_ctx": self.config.num_ctx,
                "num_predict": self.config.num_predict,
                "top_p": self.config.top_p,
                "top_k": self.config.top_k,
                **options,
            },
            keep_alive=self.config.keep_alive,
        )

        response = await self.client.post(
            "/api/chat",
            json=request.model_dump(),
        )
        response.raise_for_status()
        data = response.json()

        # Chat response has different structure
        return OllamaResponse(
            model=data.get("model", ""),
            created_at=data.get("created_at", ""),
            response=data.get("message", {}).get("content", ""),
            done=True,
            total_duration=data.get("total_duration"),
            eval_count=data.get("eval_count"),
            eval_duration=data.get("eval_duration"),
        )

    async def pull_model(self, model_name: str) -> bool:
        """Pull a model from Ollama registry.

        Args:
            model_name: Name of model to pull (e.g., "llama3:8b")

        Returns:
            True if pull succeeded
        """
        response = await self.client.post(
            "/api/pull",
            json={"name": model_name, "stream": False},
            timeout=600.0,  # Long timeout for model downloads
        )
        response.raise_for_status()
        return response.json().get("status") == "success"
```

### 5. Ollama Worker

```python
# bodai/workers/ollama/worker.py

import asyncio
import logging
import time
from typing import Any

from bodai.workers.ollama.client import OllamaClient
from bodai.workers.ollama.config import OllamaWorkerConfig

logger = logging.getLogger(__name__)


# Import status enum or define locally
class WorkerStatus:
    """Worker status values."""
    PENDING = "pending"
    STARTING = "starting"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"
    CANCELLED = "cancelled"


@dataclass
class WorkerResult:
    """Result from worker execution."""
    worker_id: str
    status: WorkerStatus
    output: str | None = None
    error: str | None = None
    exit_code: int | None = None
    duration_seconds: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


class OllamaWorker:
    """Worker that executes tasks via Ollama HTTP API.

    This worker type provides AI task execution through local Ollama models,
    offering zero-cost, privacy-preserving AI capabilities without external
    API dependencies.

    Features:
    - HTTP API communication (no CLI required)
    - Support for all Ollama models
    - Configurable generation parameters
    - Connection health monitoring
    - Session-Buddy integration for result storage

    Args:
        config: Worker configuration with model and API settings
        worker_id: Unique identifier for this worker instance
        session_buddy_client: Optional Session-Buddy client for result storage
    """

    def __init__(
        self,
        config: OllamaWorkerConfig | None = None,
        worker_id: str | None = None,
        session_buddy_client: Any = None,
    ) -> None:
        self.config = config or OllamaWorkerConfig()
        self.worker_id = worker_id or f"ollama-{int(time.time())}"
        self.worker_type = self.config.worker_type
        self.session_buddy_client = session_buddy_client
        self._status = WorkerStatus.PENDING
        self._client: OllamaClient | None = None
        self._start_time: float | None = None

    async def start(self) -> str:
        """Initialize the Ollama worker.

        Verifies Ollama server availability and model presence.

        Returns:
            Worker ID string

        Raises:
            RuntimeError: If Ollama server is not available
            ValueError: If configured model is not available
        """
        self._status = WorkerStatus.STARTING
        self._start_time = time.time()

        # Initialize client
        self._client = OllamaClient(self.config)
        await self._client.__aenter__()

        # Verify Ollama is running
        if not await self._client.is_available():
            await self._client.__aexit__(None, None, None)
            self._status = WorkerStatus.FAILED
            raise RuntimeError(
                f"Ollama server not available at {self.config.base_url}. "
                "Start with: ollama serve"
            )

        # Verify model exists
        models = await self._client.list_models()
        model_names = [m.name for m in models]

        if self.config.model not in model_names:
            logger.warning(
                f"Model {self.config.model} not found. "
                f"Available: {', '.join(model_names[:5])}..."
            )
            # Attempt to pull model
            try:
                logger.info(f"Attempting to pull model {self.config.model}...")
                await self._client.pull_model(self.config.model)
            except Exception as e:
                await self._client.__aexit__(None, None, None)
                self._status = WorkerStatus.FAILED
                raise ValueError(
                    f"Model {self.config.model} not available and pull failed: {e}"
                ) from e

        self._status = WorkerStatus.RUNNING
        logger.info(f"Started Ollama worker: {self.worker_id} (model: {self.config.model})")
        return self.worker_id

    async def execute(self, task: dict[str, Any]) -> WorkerResult:
        """Execute a task using Ollama.

        Args:
            task: Task specification with keys:
                - prompt: Task prompt to send to AI (required)
                - timeout: Execution timeout in seconds (default: config.timeout)
                - model: Override model for this task
                - system: Optional system prompt
                - temperature: Override temperature for this task
                - raw: If True, use generate API; otherwise chat API

        Returns:
            WorkerResult with execution results
        """
        if self._status != WorkerStatus.RUNNING:
            await self.start()

        prompt = task.get("prompt", "")
        if not prompt:
            return WorkerResult(
                worker_id=self.worker_id,
                status=WorkerStatus.FAILED,
                error="No prompt provided in task",
            )

        timeout = task.get("timeout", self.config.timeout)
        model = task.get("model", self.config.model)
        system = task.get("system")
        temperature = task.get("temperature", self.config.temperature)
        use_raw = task.get("raw", False)

        start_time = time.time()

        try:
            # Build request based on API type
            if use_raw:
                # Use generate API for raw completion
                response = await asyncio.wait_for(
                    self._client.generate(
                        prompt=prompt,
                        model=model,
                        temperature=temperature,
                    ),
                    timeout=timeout,
                )
                output = response.response
            else:
                # Use chat API with system prompt support
                messages = []
                if system:
                    messages.append({"role": "system", "content": system})
                messages.append({"role": "user", "content": prompt})

                response = await asyncio.wait_for(
                    self._client.chat(
                        messages=messages,
                        model=model,
                        temperature=temperature,
                    ),
                    timeout=timeout,
                )
                output = response.response

            duration = time.time() - start_time

            result = WorkerResult(
                worker_id=self.worker_id,
                status=WorkerStatus.COMPLETED,
                output=output,
                exit_code=0,
                duration_seconds=duration,
                metadata={
                    "model": model,
                    "tokens_generated": response.eval_count,
                    "total_duration_ms": response.total_duration,
                    "temperature": temperature,
                    "api_type": "generate" if use_raw else "chat",
                },
            )

            # Store in Session-Buddy if available
            if self.session_buddy_client:
                await self._store_result_in_session_buddy(result, task)

            return result

        except asyncio.TimeoutError:
            duration = time.time() - start_time
            logger.warning(f"Ollama task timed out after {duration}s")
            return WorkerResult(
                worker_id=self.worker_id,
                status=WorkerStatus.TIMEOUT,
                error=f"Task timed out after {timeout}s",
                duration_seconds=duration,
                metadata={"timeout": timeout},
            )

        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"Ollama task failed: {e}")
            return WorkerResult(
                worker_id=self.worker_id,
                status=WorkerStatus.FAILED,
                error=str(e),
                duration_seconds=duration,
            )

    async def stop(self) -> None:
        """Stop the worker by closing HTTP client."""
        if self._client:
            try:
                await self._client.__aexit__(None, None, None)
                logger.info(f"Stopped Ollama worker: {self.worker_id}")
            except Exception as e:
                logger.error(f"Error stopping Ollama worker: {e}")
            finally:
                self._client = None
                self._status = WorkerStatus.COMPLETED

    async def status(self) -> WorkerStatus:
        """Get current worker status.

        Returns:
            Current WorkerStatus value
        """
        if self._client and self._status == WorkerStatus.RUNNING:
            # Verify connection is still alive
            if not await self._client.is_available():
                self._status = WorkerStatus.FAILED
        return self._status

    async def get_progress(self) -> dict[str, Any]:
        """Get worker progress information.

        Returns:
            Dictionary with progress details
        """
        duration = time.time() - self._start_time if self._start_time else 0

        progress = {
            "status": self._status,
            "worker_id": self.worker_id,
            "worker_type": self.worker_type,
            "model": self.config.model,
            "duration_seconds": duration,
            "base_url": self.config.base_url,
        }

        # Add model availability if client is active
        if self._client:
            try:
                available = await self._client.is_available()
                progress["ollama_available"] = available
            except Exception:
                progress["ollama_available"] = False

        return progress

    async def health_check(self) -> dict[str, Any]:
        """Check worker health and availability.

        Returns:
            Dictionary with health status
        """
        try:
            current_status = await self.status()
            ollama_available = False
            model_available = False

            if self._client:
                ollama_available = await self._client.is_available()
                if ollama_available:
                    models = await self._client.list_models()
                    model_available = any(
                        m.name == self.config.model for m in models
                    )

            return {
                "healthy": current_status == WorkerStatus.RUNNING and ollama_available,
                "status": current_status,
                "worker_type": self.worker_type,
                "details": {
                    "ollama_server": ollama_available,
                    "model_available": model_available,
                    "model": self.config.model,
                    "base_url": self.config.base_url,
                },
            }
        except Exception as e:
            return {
                "healthy": False,
                "status": WorkerStatus.FAILED,
                "worker_type": self.worker_type,
                "details": {"error": str(e)},
            }

    async def _store_result_in_session_buddy(
        self,
        result: WorkerResult,
        task: dict[str, Any],
    ) -> None:
        """Store execution result in Session-Buddy.

        Args:
            result: Worker execution result
            task: Original task specification
        """
        if not self.session_buddy_client:
            return

        try:
            await self.session_buddy_client.call_tool(
                "store_memory",
                arguments={
                    "content": result.output or "",
                    "metadata": {
                        "type": "ollama_execution",
                        "worker_id": result.worker_id,
                        "worker_type": self.worker_type,
                        "model": self.config.model,
                        "task_prompt": task.get("prompt", "")[:500],
                        "status": result.status,
                        "duration_seconds": result.duration_seconds,
                        "tokens_generated": result.metadata.get("tokens_generated"),
                    },
                },
            )
            logger.debug(f"Stored result in Session-Buddy: {self.worker_id}")
        except Exception as e:
            logger.warning(f"Failed to store result in Session-Buddy: {e}")
```

## Mahavishnu Integration

### Registry Entry

Add to Mahavishnu's `WORKER_REGISTRY` in `mahavishnu/workers/registry.py`:

```python
"terminal-ollama": WorkerConfig(
    name="Ollama AI",
    worker_type="terminal-ollama",
    command="",  # HTTP API, no command
    category=WorkerCategory.AI_ASSISTANT,
    description="Local AI via Ollama HTTP API (zero cost, complete privacy)",
    completion_markers=["done"],  # API returns done: true
    stream_format="json",
    requires_tool="ollama",  # Checks for 'ollama' binary
    default_timeout=300,
),
```

### Pool Spawn Integration

```python
# Example usage with Mahavishnu pool_spawn
from mahavishnu import pool_spawn, pool_execute

# Spawn pool with Ollama workers
pool = await pool_spawn(
    pool_type="mahavishnu",
    name="ollama-workers",
    min_workers=1,
    max_workers=4,
    worker_type="terminal-ollama",
    worker_config={
        "model": "qwen2.5-coder:7b",
        "temperature": 0.7,
        "base_url": "http://localhost:11434",
    }
)

# Execute task
result = await pool_execute(
    pool_id=pool["pool_id"],
    prompt="Refactor this function to use async/await: def fetch_data(url): ...",
    timeout=120,
)

print(f"Result: {result['output']}")
```

## Configuration Options

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama API endpoint |
| `OLLAMA_MODEL` | `qwen2.5-coder:7b` | Default model to use |
| `OLLAMA_TIMEOUT` | `300` | Request timeout in seconds |
| `OLLAMA_TEMPERATURE` | `0.7` | Sampling temperature |
| `OLLAMA_KEEP_ALIVE` | `5m` | Model memory retention |

### YAML Configuration

```yaml
# config/ollama-worker.yaml
worker:
  type: terminal-ollama
  model: qwen2.5-coder:7b
  base_url: http://localhost:11434
  timeout: 300
  temperature: 0.7
  num_ctx: 4096
  num_predict: 2048
  keep_alive: 5m

pool:
  name: ollama-tasks
  min_workers: 1
  max_workers: 4
  auto_scale: true
```

## API Reference

### OllamaWorker Methods

| Method | Purpose | Returns |
|--------|---------|---------|
| `start()` | Initialize worker and verify Ollama | `worker_id: str` |
| `execute(task)` | Execute AI task | `WorkerResult` |
| `stop()` | Gracefully shutdown worker | `None` |
| `status()` | Get current status | `WorkerStatus` |
| `get_progress()` | Get progress info | `dict` |
| `health_check()` | Check worker health | `dict` |

### Task Schema

```python
{
    "prompt": str,           # Required: Task prompt
    "timeout": int,          # Optional: Override timeout
    "model": str,            # Optional: Override model
    "system": str,           # Optional: System prompt
    "temperature": float,    # Optional: Override temperature
    "raw": bool,             # Optional: Use generate vs chat API
}
```

### WorkerResult Schema

```python
{
    "worker_id": str,
    "status": "completed" | "failed" | "timeout",
    "output": str | None,
    "error": str | None,
    "exit_code": int | None,
    "duration_seconds": float,
    "metadata": {
        "model": str,
        "tokens_generated": int,
        "total_duration_ms": int,
        "temperature": float,
        "api_type": "generate" | "chat",
    },
    "timestamp": str,
}
```

## Testing Strategy

### Unit Tests

```python
# tests/test_ollama_worker.py

import pytest
from unittest.mock import AsyncMock, patch

from bodai.workers.ollama.worker import OllamaWorker
from bodai.workers.ollama.config import OllamaWorkerConfig


@pytest.fixture
def worker():
    """Create worker with test configuration."""
    config = OllamaWorkerConfig(
        base_url="http://localhost:11434",
        model="qwen2.5-coder:7b",
        timeout=30,
    )
    return OllamaWorker(config=config)


@pytest.mark.asyncio
async def test_worker_start(worker):
    """Test worker initialization."""
    with patch.object(worker, '_client') as mock_client:
        mock_client.is_available = AsyncMock(return_value=True)
        mock_client.list_models = AsyncMock(return_value=[
            type('Model', (), {'name': 'qwen2.5-coder:7b'})()
        ])

        worker_id = await worker.start()
        assert worker_id.startswith("ollama-")


@pytest.mark.asyncio
async def test_execute_task(worker):
    """Test task execution."""
    with patch.object(worker, '_client') as mock_client:
        mock_client.chat = AsyncMock(return_value=type(
            'Response', (), {
                'response': 'Test output',
                'eval_count': 100,
                'total_duration': 1000,
            }
        )())

        result = await worker.execute({
            "prompt": "Test prompt",
            "timeout": 30,
        })

        assert result.status == "completed"
        assert result.output == "Test output"
```

### Integration Tests

```python
# tests/integration/test_ollama_integration.py

import pytest
import httpx

from bodai.workers.ollama.worker import OllamaWorker


@pytest.fixture
def ollama_available():
    """Check if Ollama is running locally."""
    try:
        response = httpx.get("http://localhost:11434", timeout=5.0)
        return response.status_code == 200
    except Exception:
        return False


@pytest.mark.asyncio
@pytest.mark.skipif(not ollama_available(), reason="Ollama not running")
async def test_real_execution():
    """Test against real Ollama instance."""
    worker = OllamaWorker()
    await worker.start()

    result = await worker.execute({
        "prompt": "Say 'Hello, World!' and nothing else.",
        "timeout": 60,
    })

    assert result.status == "completed"
    assert "Hello" in result.output or "hello" in result.output.lower()

    await worker.stop()
```

## Implementation Phases

### Phase 1: Core Implementation (Day 1-2)

1. Create module structure in `bodai/workers/ollama/`
2. Implement `OllamaConfig` and `OllamaWorkerConfig`
3. Implement `OllamaClient` with basic HTTP operations
4. Implement `OllamaWorker` with core lifecycle methods
5. Add unit tests for all components

### Phase 2: Integration (Day 2-3)

1. Test against real Ollama instance
2. Implement Session-Buddy integration
3. Add error handling and recovery
4. Performance optimization
5. Add integration tests

### Phase 3: Documentation & Deployment (Day 3)

1. Update Bodai documentation
2. Create Mahavishnu integration guide
3. Add configuration examples
4. Create usage examples
5. Document troubleshooting steps

## Success Criteria

1. **Functional Requirements**
   - Worker can connect to Ollama HTTP API
   - Worker can execute tasks and return results
   - Worker handles timeouts gracefully
   - Worker supports multiple models

2. **Non-Functional Requirements**
   - Response time < 5s for simple tasks
   - Memory usage < 100MB per worker
   - Zero external API dependencies
   - Complete privacy (no data leaves machine)

3. **Integration Requirements**
   - Compatible with Mahavishnu pool_spawn
   - Registerable in WORKER_REGISTRY
   - Health check integration
   - Session-Buddy storage support

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Ollama server down | High | Health checks, clear error messages |
| Model not available | Medium | Auto-pull on start, fallback models |
| Memory exhaustion | Medium | Configure keep_alive, limit workers |
| Slow generation | Low | Timeout handling, progress tracking |

## Dependencies

### Runtime

- `httpx>=0.25.0` - Async HTTP client
- `pydantic>=2.0.0` - Data validation

### Development

- `pytest>=7.0.0` - Testing
- `pytest-asyncio>=0.21.0` - Async test support

### External

- Ollama server running on `localhost:11434`
- At least one model installed (e.g., `qwen2.5-coder:7b`)

## References

- [Ollama API Documentation](https://github.com/ollama/ollama/blob/main/docs/api.md)
- [Mahavishnu Pool Quickstart](/Users/les/Projects/ARCHIVED/crackerjack.bak-20260217_043710/docs/MAHAVISHNU_POOL_QUICKSTART.md)
- [Ollama Provider for Crackerjack](/Users/les/Projects/ARCHIVED/crackerjack.bak-20260217_043710/docs/features/OLLAMA_PROVIDER.md)
- [Mahavishnu Worker Registry](/Users/les/Projects/mahavishnu/mahavishnu/workers/registry.py)

## Changelog

### v0.1.0 (2026-02-24) - Initial Plan

- Created implementation plan
- Defined architecture and components
- Specified API interfaces
- Outlined testing strategy
