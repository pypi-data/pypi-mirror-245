from __future__ import annotations
from loguru import logger
from agricore_sp_models.simulation_models import LogLevel, LogMessage
from time import time
from urllib.parse import urljoin
import requests

class ORMLogHandler:
    def __init__(self, base_path: str = "https://abm.agricore.idener.es/"):
        self.base_path = base_path
        
    def write(self, message):
        try:
            if "simulationRunId" in message.record["extra"] and "logSource" in message.record["extra"]:
                log = LogMessage(
                    description="" if message.record["exception"] is None else str(message.record["exception"]),
                    logLevel=int(message.record["level"].no),
                    simulationRunId=0 if "simulationRunId" not in message.record["extra"] else message.record["extra"]["simulationRunId"],
                    source="" if "logSource" not in message.record["extra"] else message.record["extra"]["logSource"],
                    timestamp=float(time() * 1000),
                    title=message.record["message"],
                )
                url = urljoin(self.base_path, f"/simulationRun/{log.simulationRunId}/logMessage/add")
                x = requests.post(url, log.dict(exclude={"id"}))
        except Exception as e:
            print("Unable to generate Log Message in ORM for message. " + str(e) )
        print (log.dict())

def configure_orm_logger(url: str, simulationRunId: int, logSource:str) -> None:
    logger.configure(handlers=[{"sink": ORMLogHandler(url), "enqueue": True}])
    bind_logger_parameters(simulationRunId, logSource)
    
def bind_logger_parameters(simulationRunId: int, logSource: str):
    logger.bind(simulationRunId = simulationRunId)
    logger.bind(logSource = logSource)
    