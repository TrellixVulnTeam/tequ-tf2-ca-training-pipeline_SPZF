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


@echo off
python -m object_detection.model_main_tf2 --pipeline_config_path=%DATA_PATH%\pipeline.config --model_dir=%OUTPUT_PATH%  --checkpoint_dir=%OUTPUT_PATH% --alsologtostderr
