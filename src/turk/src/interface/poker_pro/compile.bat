@ECHO OFF

IF NOT EXIST build mkdir build

javac -cp thirdparty\meerkat-api.jar;thirdparty\smtp.jar;thirdparty\activation.jar;thirdparty\mailapi.jar -d build -sourcepath src src\ca\ualberta\cs\poker\free\client\*.java

javac  -cp thirdparty\meerkat-api.jar;thirdparty\smtp.jar;thirdparty\activation.jar;thirdparty\mailapi.jar -d build -sourcepath src src\ca\ualberta\cs\poker\free\alien\*.java

javac -cp thirdparty\meerkat-api.jar;thirdparty\smtp.jar;thirdparty\activation.jar;thirdparty\mailapi.jar -d build -sourcepath src src\ca\ualberta\cs\poker\free\server\*.java

javac -cp thirdparty\meerkat-api.jar;thirdparty\smtp.jar;thirdparty\activation.jar;thirdparty\mailapi.jar -d build -sourcepath src src\ca\ualberta\cs\poker\free\dynamics\*.java

javac  -cp thirdparty\meerkat-api.jar;thirdparty\smtp.jar;thirdparty\activation.jar;thirdparty\mailapi.jar -d build -sourcepath src src\ca\ualberta\cs\poker\free\academy25\*.java

javac  -cp thirdparty\meerkat-api.jar;thirdparty\smtp.jar;thirdparty\activation.jar;thirdparty\mailapi.jar -d build -sourcepath src src\ca\ualberta\cs\poker\free\tournament\*.java

javac  -cp thirdparty\meerkat-api.jar;thirdparty\smtp.jar;thirdparty\activation.jar;thirdparty\mailapi.jar -d build -sourcepath src src\*.java

jar cf aaaibot.jar -C build ca -C build StreamConnect.class -C build TCPPlugin.class
