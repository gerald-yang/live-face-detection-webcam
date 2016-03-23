all:

install:
	echo "Install python-env and live face detection service"
	mkdir -p ${DESTDIR}/bin
	cp -a start-livefd.sh ${DESTDIR}/bin/start-livefd
	cp -a face_detection_webcam.py ${DESTDIR}/bin/
	cp -a haarcascade_frontalface_default.xml ${DESTDIR}/bin/
	cp -ra templates ${DESTDIR}/bin/
	chmod +x ${DESTDIR}/bin/start-livefd

clean:
	echo "Clean built files"
