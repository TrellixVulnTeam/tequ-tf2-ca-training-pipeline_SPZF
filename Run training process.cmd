echo Set paths...


SET CLOUD_ANNOTATIONS_MOUNT=%cd%\content\ca_source_data
SET ANNOTATIONS_JSON_PATH=%cd%\content\ca_source_data\_annotations.json
SET CHECKPOINT_PATH=%cd%\content\checkpoint
SET OUTPUT_PATH=%cd%\content\output
SET EXPORTED_PATH=%cd%\content\exported
SET DATA_PATH=%cd%\content\data
SET LABEL_MAP_PATH=%cd%\content\data\label_map.pbtxt
SET TRAIN_RECORD_PATH=%cd%\content\data\train.record
SET VAL_RECORD_PATH=%cd%\content\data\val.record
SET CONFIG_PATH=%cd%\models\research\object_detection\configs\tf2\
SET YYYYMMDD=%DATE:~9,4%-%DATE:~6,2%-%DATE:~3,2%
SET /a _rand=(%RANDOM%*500/32768)+1
SET MODEL_PATH=%cd%\content\trained_models\%YYYYMMDD%\
SET PROTOC_PATH=%cd%\protoc\bin\


RMDIR %cd%\content\exported /S /Q 
RMDIR %cd%\content\output /S /Q
RMDIR %cd%\content\data /S /Q
RMDIR %cd%\content\checkpoint /S /Q

echo Run protoc...
cd models
cd research
%PROTOC_PATH%protoc.exe object_detection\protos\*.proto --python_out=.
echo Run model_builder_tf2_test.py
python object_detection/builders/model_builder_tf2_test.py
cd..
cd..

echo Prepare training...
python prepare_model_training.py %CLOUD_ANNOTATIONS_MOUNT% %ANNOTATIONS_JSON_PATH% %CHECKPOINT_PATH% %OUTPUT_PATH% %EXPORTED_PATH% %DATA_PATH% %LABEL_MAP_PATH% %TRAIN_RECORD_PATH% %VAL_RECORD_PATH% %CONFIG_PATH%
cd models\research

@echo off
SET /p TRAIN_STEPS="Set number of training steps: "

python -m object_detection.model_main_tf2 --pipeline_config_path=%DATA_PATH%\pipeline.config --model_dir=%OUTPUT_PATH% --num_train_steps=%TRAIN_STEPS% --num_eval_steps=100 --alsologtostderr

REM python -m object_detection.model_main_tf2 --pipeline_config_path=%DATA_PATH%\pipeline.config --model_dir=%OUTPUT_PATH% --checkpoint_dir=%CHECKPOINT_PATH% --num_train_steps=%TRAIN_STEPS% --sample_1_of_n_eval_examples=1 --run_once=True  --alsologtostderr

cd..
cd..

python export_inference_graph.py %OUTPUT_PATH%

SET /p TRAINED_CHECKPOINT_PREFIX=<temp.txt
SET /p BATCH_SIZE=<batch_size.txt
SET /p BASE_MODEL=<base_model.txt
SET /p TRAIN_FILES_PERCENT=<train_files_percent.txt
SET /p MODEL_TYPE=<model_type.txt



cd models\research

python -m object_detection.exporter_main_v2 --input_type image_tensor  --pipeline_config_path=%DATA_PATH%\pipeline.config --trained_checkpoint_dir=%OUTPUT_PATH% --output_directory=%MODEL_PATH%%BASE_MODEL%_%TRAIN_STEPS%_%BATCH_SIZE%

cd..
cd..
python create_labels.py %MODEL_PATH%%BASE_MODEL%_%TRAIN_STEPS%_%BATCH_SIZE%\saved_model %MODEL_TYPE% %BATCH_SIZE% %TRAIN_FILES_PERCENT% %TRAIN_STEPS%