import os,sys
from visa.constant import *
from visa.logger import logging
from visa.exception import CustomException
from visa.entity.config_entity import *
from visa.utils.utils import read_yaml_file


class Configuration:
    def __init__(self, config_file_path:str = CONFIG_FILE_PATH,
                 current_time_stamp:str = CURRENT_TIME_STAMP) -> None:
        try:
            #Here we are reading yaml file
            self.config_info = read_yaml_file(file_path=config_file_path)
            self.training_pipeline_config = self.get_training_pipeline_config()
            self.time_stamp = current_time_stamp
        except Exception as e:
            raise CustomException(e, sys) from e


    def get_data_ingestion_config(self)->DataIngestionConfig:
        try:
            # Here we are going save our data ingestion work in artifact folder
            # we are calling our training_pipeline_config to store our get_data_ingestion_config() output under artifact folder
            artifact_dir = self.training_pipeline_config.artifact_dir
            
            # Here We are joining our complete file artifact dir, data_ingestion and time_stamp folder folder using os.join function to create path to store our output
            # Folder format will be artifact/data_ingestion/time_stamp and under this folder output (.i,e train and test data) will be stored
            data_ingestion_artifact_dir = os.path.join(artifact_dir,
                                                       DATA_INGESTION_ARTIFACT_DIR,
                                                       self.time_stamp)
            
            #Here we are reading DATA_INGESTION_CONFIG_KEY (.i,e data_ingestion_config)
            data_ingestion_info = self.config_info[DATA_INGESTION_CONFIG_KEY]


            dataset_download_url = data_ingestion_info[DATA_INGESTION_DOWNLOAD_URL_KEY]

            # Here 1st we are creating a varibale named raw_data_dir
            # 2nd, we are using os.join function to store our output DATA_INGESTION_RAW_DATA_DIR_KEY which is -> raw_data_dir defined in constant folder
            # 3rd, output will be stored in artifact/data_ingestion/time_stamp/raw_data folder

            raw_data_dir = os.path.join(data_ingestion_artifact_dir,
                                        data_ingestion_info[DATA_INGESTION_RAW_DATA_DIR_KEY])
            

            # Here 1st we are creating a varibale named ingested_data_dir
            # 2nd, we are using os.join function to store our output DATA_INGESTION_INGESTED_DIR_NAME_KEY which is -> ingested_dir defined in constant folder
            # 3rd, output will be stored in "artifact/data_ingestion/time_stamp/ingested_data" folder
            
            ingested_data_dir = os.path.join(data_ingestion_artifact_dir,
                                        data_ingestion_info[DATA_INGESTION_INGESTED_DIR_NAME_KEY])
            

            # Here 1st we are creating a varibale named ingested_train_dir
            # 2nd, we are using os.join function to store our output DATA_INGESTION_TRAIN_DIR_KEY which is -> ingested_train_dir defined in constant folder
            # 3rd, output will be stored in "artifact/data_ingestion/time_stamp/train" folder
            
            ingested_train_dir = os.path.join(ingested_data_dir,
                                        data_ingestion_info[DATA_INGESTION_TRAIN_DIR_KEY])
            
            # Here 1st we are creating a varibale named ingested_test_dir
            # 2nd, we are using os.join function to store our output DATA_INGESTION_TEST_DIR_KEY which is -> ingested_test_dir defined in constant folder
            # 3rd, output will be stored in "artifact/data_ingestion/time_stamp/test" folder
            
            ingested_test_dir = os.path.join(ingested_data_dir,
                                        data_ingestion_info[DATA_INGESTION_TEST_DIR_KEY])
            

            # Here we are calling all the varibales one by one (i.e, we are calling dataset_download_url, raw data directory, ingested train and test dir one by one)
            
            data_ingestion_config=DataIngestionConfig(dataset_download_url = dataset_download_url,
                                                      raw_data_dir = raw_data_dir, 
                                                      ingested_train_dir = ingested_train_dir, 
                                                      ingested_test_dir = ingested_test_dir)
            
            return data_ingestion_config

        except Exception as e:
            raise CustomException(e, sys) from e
        

 
 
    def get_data_validation_config(self) -> DataValidationConfig:
        try:
            # Here we are goging to store our output

            artifact_dir = self.training_pipeline_config.artifact_dir

            # Here We are joining our complete file artifact dir, data_validation and time_stamp folder
            # Here 1st we are creating a varibale named data_validation_artifact_dir
            # 2nd, we are using os.join function to create path by joining artifact_dir, data_validation and time_stamp for data validation  defined in constant folder
            # 3rd, our validation path will be artifact/data_validation/time_stamp folder

            data_validation_artifact_dir=os.path.join(
                artifact_dir,
                DATA_VALIDATION_ARTIFACT_DIR,
                self.time_stamp
            )
            # Here we are going to read our yaml file
            data_validation_config = self.config_info[DATA_VALIDATION_CONFIG_KEY]

            schema_file_path = os.path.join(ROOT_DIR,
            data_validation_config[DATA_VALIDATION_SCHEMA_DIR_KEY],
            data_validation_config[DATA_VALIDATION_SCHEMA_FILE_NAME_KEY]
            )

            data_validation_config = DataValidationConfig(schema_file_path=schema_file_path)


            return data_validation_config
        except Exception as e:
            raise CustomException(e,sys) from e
        


    def get_data_transformation_config(self) -> DataTransformationConfig:
        try:
            # Here we are going save our data transformation work in artifact folder
            # we are calling our training_pipeline_config to store our get_data_transformation_config() output under artifact folder
            artifact_dir = self.training_pipeline_config.artifact_dir 

            # Here We are joining our complete file artifact dir, data_transformation and time_stamp folder to create path to store our output
            # Folder format will be artifact/data_transformation/time_stamp and under this folder output (.i,e processed pickle file) will be stored in .pkl format

            data_transformation_artifact_dir=os.path.join(
                artifact_dir,
                DATA_TRANSFORMATION_ARTIFACT_DIR,
                self.time_stamp
            )

            #Here we are reading DATA_TRANSFORMATION_CONFIG_KEY (.i,e data_transformation_config)

            data_transformation_config_info=self.config_info[DATA_TRANSFORMATION_CONFIG_KEY]


            # Here 1st we are creating a varibale named preprocessed_object_file_path to store our preprocessed pickle file output 
            # 2nd, we are using os.join function to store our output created by varibale in line 127 above in this file (i.e, in data_transformation_artifact_dir varibale)
            # 3rd, output will be stored in "artifact/data_transformation/time_stamp/preprocessed/preprocessed.pkl"

            preprocessed_object_file_path = os.path.join(
                data_transformation_artifact_dir,
                data_transformation_config_info[DATA_TRANSFORMATION_PREPROCESSING_DIR_KEY],
                data_transformation_config_info[DATA_TRANSFORMATION_PREPROCESSED_FILE_NAME_KEY]
            )

            # 1st, here we are using os.join to join artifact dir, transformed_dir and transformed_train_dir
            # 2nd, output will be stored in "artifact/data_transformation/time_stamp/transformed_data/train"
            
            transformed_train_dir=os.path.join(
            data_transformation_artifact_dir,
            data_transformation_config_info[DATA_TRANSFORMATION_DIR_NAME_KEY],
            data_transformation_config_info[DATA_TRANSFORMATION_TRAIN_DIR_NAME_KEY]
            )

            # 1st, here we are using os.join to join artifact dir, transformed_dir and transformed_test_dir
            # 2nd, output will be stored in "artifact/data_transformation/time_stamp/transformed_data/test"


            transformed_test_dir = os.path.join(
            data_transformation_artifact_dir,
            data_transformation_config_info[DATA_TRANSFORMATION_DIR_NAME_KEY],
            data_transformation_config_info[DATA_TRANSFORMATION_TEST_DIR_NAME_KEY]
            )

            # Here we are calling all the varibales one by one (i.e, we are calling reprocessed_object, transformed train directory and transformed test dir one by one)           

            data_transformation_config=DataTransformationConfig(
                preprocessed_object_file_path=preprocessed_object_file_path,
                transformed_train_dir=transformed_train_dir,
                transformed_test_dir=transformed_test_dir
            )

            logging.info(f"Data transformation config: {data_transformation_config}")
            return data_transformation_config
        except Exception as e:
            raise CustomException(e,sys) from e
        



    def get_model_trainer_config(self) -> ModelTrainerConfig:
        try:
            artifact_dir = self.training_pipeline_config.artifact_dir

            model_trainer_artifact_dir=os.path.join(
                artifact_dir,
                MODEL_TRAINER_ARTIFACT_DIR,
                self.time_stamp
            )
            model_trainer_config_info = self.config_info[MODEL_TRAINER_CONFIG_KEY]
            trained_model_file_path = os.path.join(model_trainer_artifact_dir,
            model_trainer_config_info[MODEL_TRAINER_TRAINED_MODEL_DIR_KEY],
            model_trainer_config_info[MODEL_TRAINER_TRAINED_MODEL_FILE_NAME_KEY]
            )

            model_config_file_path = os.path.join(model_trainer_config_info[MODEL_TRAINER_MODEL_CONFIG_DIR_KEY],
            model_trainer_config_info[MODEL_TRAINER_MODEL_CONFIG_FILE_NAME_KEY]
            )


            base_accuracy = model_trainer_config_info[MODEL_TRAINER_BASE_ACCURACY_KEY]

            model_trainer_config = ModelTrainerConfig(
                trained_model_file_path=trained_model_file_path,
                base_accuracy=base_accuracy,
                model_config_file_path=model_config_file_path
            )
            logging.info(f"Model trainer config: {model_trainer_config}")
            return model_trainer_config
        except Exception as e:
            raise CustomException(e,sys) from e




    def get_model_evaluation_config(self) ->ModelEvaluationConfig:
        try:
            model_evaluation_config = self.config_info[MODEL_EVALUATION_CONFIG_KEY]
            artifact_dir = os.path.join(self.training_pipeline_config.artifact_dir,
                                        MODEL_EVALUATION_ARTIFACT_DIR, )

            model_evaluation_file_path = os.path.join(artifact_dir,
                                                    model_evaluation_config[MODEL_EVALUATION_FILE_NAME_KEY])
            response = ModelEvaluationConfig(model_evaluation_file_path=model_evaluation_file_path,
                                            time_stamp=self.time_stamp)
            
            
            logging.info(f"Model Evaluation Config: {response}.")
            return response
        except Exception as e:
            raise CustomException(e,sys) from e



    def get_training_pipeline_config(self) -> TrainingPipelineConfig:
        try:
            training_pipeline_config = self.config_info[TRAINING_PIPELINE_CONFIG_KEY]

            artifact_dir = os.path.join(ROOT_DIR,training_pipeline_config[TRAINING_PIPELINE_NAME_KEY],
                                        training_pipeline_config[TRAINING_PIPELINE_ARTIFACT_DIR_KEY])
            
            training_pipeline_config = TrainingPipelineConfig(artifact_dir=artifact_dir)
            logging.info(f"Training pipleine config: {training_pipeline_config}")

            return training_pipeline_config
        
        except Exception as e:
            raise CustomException(e, sys) from e
        