echo Run protoc...
cd models
cd research
%PROTOC_PATH%protoc.exe object_detection\protos\*.proto --python_out=.
cd.. 
cd..
