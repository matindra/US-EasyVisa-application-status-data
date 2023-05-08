from visa.constant import *
from visa.logger import logging
from visa.pipeline.pipeline import Pipeline




def main():
    try:
        pipeline = Pipeline()
        pipeline.run_pipeline()

    except Exception as e:
        logging.error(f"{e}")
        print(e)



if __name__=="__main__":
    main()