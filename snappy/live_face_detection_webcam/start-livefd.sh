#! /bin/sh

export LD_LIBRARY_PATH="$SNAP_APP_PATH/usr/lib/libblas:$SNAP_APP_PATH/usr/lib/lapack:$LD_LIBRARY_PATH" 
PYTHON_EGG_CACHE=$SNAP_APP_DATA_PATH/.python-eggs $SNAP_APP_PATH/usr/bin/python $SNAP_APP_PATH/bin/face_detection_webcam.py $SNAP_APP_PATH/bin/haarcascade_frontalface_default.xml

