from src.ApsSensorFault.configuration.mongo_db_connection import MongoDBClient
from src.ApsSensorFault.pipeline.training_pipeline import TrainingPipeline
from src.ApsSensorFault.logging import log


if __name__ == '__main__':
    try:
        log.info(f">>>>>>>>>>>>>>>>> Training Pipeline started")
        trainig_pipeline = TrainingPipeline()
        trainig_pipeline.run_pipeline()
        log.info(f">>>>>>>>>>>>>>>>>> Training Pipeline compleated successfully\n\n X========================X\n\n")
    except Exception as e:
        log.exception(e)
        log.info(f">>>>>>>>>>>>>>>>>> Training Pipeline Failed\n\n X========================X\n\n")
        raise e 
