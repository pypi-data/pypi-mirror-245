# python-gcp-logger
This repo provides a python logger wrapper for structured logs on gcp.

## Installation
```
pip install python-custom-logger
or
poetry add python-custom-logger
```

## Usage

```
from custom_logger.logger import CustomStructuredLogger

log_to_cloud: bool = True if <any condition to check if in cloud service env> else False
log_to_console: bool = not log_to_cloud
logger: CustomStructuredLogger = CustomStructuredLogger(
    project_id=<GCP_PROJECT_ID>,
    name="MyLogger",
    log_to_console=log_to_console,
    log_to_cloud=log_to_cloud,
)

logger.info(message="helloworld")
logger.info(message={"hello": "world"})
logger.error(message="helloworld")
logger.error(message={"hello": "world"})
logger.warning(message="helloworld")
logger.warning(message={"hello": "world"})

# Using additional attributes:
logger.info(message={"hello": "world"}, attributes {"foo": "bar"})
```


## TODOs
- add tests
- replace google logger with python logger using structured std out log