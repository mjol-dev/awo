import psutil
from typing import Dict, Any

def get_system_metrics() -> Dict[str, Any]:
    """Collect general system metrics using psutil."""
    return {
        "cpu_percent": psutil.cpu_percent(interval=None),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_usage_percent": psutil.disk_usage('/').percent,
    }

def get_gpu_metrics() -> Dict[str, Any]:
    """Attempt to collect GPU metrics if available."""
    try:
        import pynvml
        pynvml.nvmlInit()
        handle = pynvml.nvmlDeviceGetHandleByIndex(0)
        mem_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
        util = pynvml.nvmlDeviceGetUtilizationRates(handle)
        return {
            "gpu_utilization": util.gpu,
            "gpu_memory_used_mb": mem_info.used // (1024 * 1024),
            "gpu_memory_total_mb": mem_info.total // (1024 * 1024),
        }
    except Exception:
        return {"gpu_available": False}

def collect_all_metrics() -> Dict[str, Any]:
    """Collect all available metrics."""
    return {
        **get_system_metrics(),
        **get_gpu_metrics()
    }

